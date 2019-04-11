import logging
import os

import pytest
from selenium import webdriver


logger = logging.getLogger(__name__)

BROWSERS = os.environ.get('UI_BROWSER', 'Chrome').split(',')


@pytest.fixture(scope='session')
def browser(request):
    """Adjust the selenium fixture's browser size."""
    use_saucelabs = os.environ.get('UI_USE_SAUCELABS', False)
    use_remote = os.environ.get('UI_USE_REMOTE', False)
    browser = BROWSERS[0]
    testsfailed = request.session.testsfailed

    if use_saucelabs or browser in (
        'MicrosoftEdge',
        'InternetExplorer',
    ):
        cap = {
            'browserName': browser,
        }
        user = os.environ['SAUCELABS_USERNAME']
        key = os.environ['SAUCELABS_API_KEY']
        url = _sauce_ondemand_url(user, key)
        driver = webdriver.Remote(desired_capabilities=cap,
                                    command_executor=url)

    # Use selenium remote driver to connect to containerized browsers on CI
    elif use_remote:
        caps = webdriver.DesiredCapabilities
        cap = getattr(caps, browser.upper()).copy()
        driver = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            desired_capabilities=cap,
        )

    elif browser == 'Firefox':
        opt = webdriver.FirefoxOptions()
        if os.environ.get('UITEST_SHOW', 'No').lower() != 'yes':
            opt.add_argument('--headless')
        driver = webdriver.Firefox(options=opt)
    elif browser == 'Chrome':
        opt = webdriver.ChromeOptions()
        if os.environ.get('UITEST_SHOW', 'No').lower() != 'yes':
            opt.add_argument('--headless')
        opt.add_argument('--no-sandbox')
        opt.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=opt)

    driver.set_window_size(1200, 800)

    yield driver

    driver.close()

from time import sleep
import findtext

def body(browser, text):
    browser.execute_script('document.body.innerHTML=arguments[0]', text)


def test_find_one_element(browser):
    body(browser, '<button>Click Me</button> <b>Do not Click Me!</b> <i>Do not even look at me</i>')

    assert findtext.find_element_by_text(browser, 'Click Me').tag_name == 'button'


def test_find_several_element(browser):
    body(browser, '<button>Click Me</button> <b>Do not Click Me!</b> <i>Do not even look at me</i>')

    elements = findtext.find_elements_by_text(browser, 'Click Me', exact=False)
    assert len(elements) == 2
    assert elements[0].tag_name == 'button'
    assert elements[1].tag_name == 'b'


def test_find_closest_container(browser):
    body(browser, '''
        <div>
            <span>HERE</span>
        </div>
    ''')
    assert findtext.find_element_by_text(browser, 'HERE').tag_name == 'span'


def test_find_one_element_per_text(browser):
    body(browser, '''
        <div>
            <span>HERE</span>
        </div>
    ''')
    els = findtext.find_elements_by_text(browser, 'HERE')
    assert len(els) == 1


def test_find_with_siblings(browser):
    body(browser, '''
        <div>
            HERE
            <img src="data:">
        </div>
    ''')
    els = findtext.find_elements_by_text(browser, 'HERE')
    assert len(els) == 1


def test_find_is_case_sensitive(browser):
    body(browser, '''
        <div>
            HERE
        </div>
    ''')
    els = findtext.find_elements_by_text(browser, 'HeRe')
    assert len(els) == 0


def test_skip_non_visible_elements(browser):
    body(browser, '''
        <select>
            <option value=1>ONE</option>
            <option selected value=2>TWO</option>
            <option value=3>THREE</option>
        </select>
    ''')
    els = findtext.find_elements_by_text(browser, 'TWO')
    assert len(els) == 0
