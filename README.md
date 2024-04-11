<h1 align="center">tiny-match-snapshot</h1>

<p align="center">
    <img alt="Supported Python Versions" src="https://img.shields.io/badge/Python-3.8+-blue" />
    <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/tiny-match-snapshot" />
    <img alt="GitHub License" src="https://img.shields.io/github/license/inventare/tiny-match-snapshot" />
    <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/tiny-match-snapshot" />
    <img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/inventare/tiny-match-snapshot/tests.yml?label=tests" />
    <img src='https://coveralls.io/repos/github/inventare/tiny-match-snapshot/badge.svg?branch=main' alt='Coverage Status' />
</p>

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

Some examples of usage is disponible at `examples` folder on the root of this repository. For more complex usages, this package is used to run UI regression tests on the [inventare/django-image-uploader-widget](https://github.com/inventare/django-image-uploader-widget/tree/main/tests/tests_ui_regression) package.

### With unittest and playwright

A first way, using `unittest` and `playwright` is:

```python
import unittest
from unittest.case import TestCase
from match_snapshot import MatchSnapshot
from playwright.sync_api import sync_playwright

class MyTests(TestCase, MatchSnapshot):
    snapshot_path = "./__snapshots__"
    failed_path = "./__errors__"

    def test_selenium(self):
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto("https://playwright.dev/")

        banner = page.query_selector(".hero.hero--primary")

        self.assert_match_snapshot(banner, "test_unittest_playwright")

        browser.close()

if __name__ == '__main__':
    unittest.main()
```

### With unittest and selenium

An simple example of using `unittest` and `selenium` is:

```python
import unittest
from unittest.case import TestCase
from match_snapshot import MatchSnapshot
from selenium import webdriver
from selenium.webdriver.common.by import By

class MyTests(TestCase, MatchSnapshot):
    snapshot_path = "./__snapshots__"
    failed_path = "./__errors__"

    def test_selenium(self):
        driver = webdriver.Chrome()
        driver.get("http://www.python.org")

        banner = driver.find_element(By.CLASS_NAME, "main-header")

        self.assert_match_snapshot(banner, "test_unittest_selenium")

if __name__ == '__main__':
    unittest.main()
```

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
        self.assert_match_snapshot(element, 'test_pytest_playwright')
```

### With pytest and selenium

A, not beautifull way to use with `pytest` and `selenium` is to use:

```python
from match_snapshot import MatchSnapshot
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestsSelenium(MatchSnapshot):
    snapshot_path = "./__snapshots__"
    failed_path = "./__errors__"

    def test_selenium(self):
        driver = webdriver.Chrome()
        driver.get("http://www.python.org")

        banner = driver.find_element(By.CLASS_NAME, "main-header")

        self.assert_match_snapshot(banner, "test_pytest_selenium")
```

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
