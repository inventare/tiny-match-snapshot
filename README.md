# tiny-match-snapshot

---

TODO: 

---

This package provides a tiny match snaptshot utility for usages with **Playwright** or with **Selenium** to capture screenshot of some web element and store it as snapshot and in next runs of tests, compare the taken screenshot with the stored as snapshot.

## Requirements

- Python 3.8+
- Selenium or Playwright (or any other, see "Extending the behaviour" section)

## Instalation

The package can be installed with the `pip` package manager:

```sh
pip install tiny-match-snapshot
```

## Usage

TODO: write this

### With unittest and playwright

TODO: write this

### With unittest and selenium

TODO: write this

### With pytest and playwright

To use with `pytest` and `playwright` we can encapsulate our tests inside a class to inherits the `MatchSnapshot` class. To run the tests, we recommend to use the plugin [pytest test runner](https://playwright.dev/python/docs/test-runners) and run the tests using the command: `pytest --browser webkit --headed`.

```python
from playwright.sync_api import Page
from match_snapshot import MatchSnapshot

class TestsPlaywright(MatchSnapshot):
    snapshot_path = "./__snapshots__"
    failed_path = "./__errors__"

    def test_playwright(self, page: Page):
        page.goto("https://playwright.dev/")

        element = page.query_selector('.hero.hero--primary')
        MatchSnapshot().assert_match_snapshot(element, 'test_pytest_playwright')
```

### With pytest and selenium

TODO: write this

## Extending the behaviour

The basic behaviour of this library is the usage of the `.screenshot()` method of a web element. To extends the behaviour of the package to be used with other tool is basically write a wrapper class to compose with the element:

```python
class MyCustomElement:
    def __init__(self, element):
        self.element = element

    def screenshot(self, path: str):
        # TODO: TAKE the screenshot and save it to the path
        pass
```

Now, instead of use the API element to the `assert_match_snapshot()` we use the composed `MyCustomElement` class:

```python
class MyTestCase(MatchSnapshot, ...)
    def test_any_thing(self):
        element = ...

        match_element = MyCustomElement(element)
        self.assert_match_snapshot(match_element, 'my_test')
```
