from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='findtext',
    version='0.1',
    description='Text finding helpers for Selenium tests',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/peaqe/findtext',
    author='Calvin Spealman',
    author_email='cspealma@redhat.com',
    license='MIT',
    py_modules=['findtext'],
    zip_safe=True,
)
