# Selenium Text Finding Utilities

Make your tests user-first by using these utilities to test against the
presented content on the page, not the implementation detail of specific
markup.

## Find Elements by Text

The most powerful utilities are `find_element_by_text(driver, text)` and
`find_elements_by_text(driver, text)`, which search the page for one or
multiple elements with content matching the given text, as efficiently as
possible. By default, the inner text must match exactly.


Call with the flag `exact=False` to find elements which simply
_contain_ the text.

For example::

```python
    # Find the logout element and click it, whatever it might be
    findtext.find_element_by_text(driver, 'Logout').click()
```

## Form Helpers

You can locate and interact with form elements based on their labels, the
way a user would find things on the page and the way your features are most
likely to be documented.

### `fill_input_by_label(driver, element, label, value, timeout=None):`

Interact with text fields on the page based on their visible label. Here is
how you might fill in a login form:

```python
    fill_input_by_label(driver, None, "Username", username)
    fill_input_by_label(driver, None, "Password", username)
```

Notice how you don't need to know anything about the markup on the page, the
ID of the input elements, or if the label text is "Username" or
"Username:".

If you only want to look at a part of the page, not the whole page, you can
pass an optional element as the second parameter. The search will be done
to descendents under that element.

### `fill_input_by_placeholder(driver, element, label, value):`

You might also know youb can locate an element based on the placeholder text
that can be read in the input. This function is called just like the previous
function.

### `read_input_by_label(driver, element, label):`

You can use the same logic to read information back out of forms, too.

```python
    assert expected == read_input_by_label(driver, None, "State")
```
