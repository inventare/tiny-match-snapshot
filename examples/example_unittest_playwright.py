import unittest
from unittest.case import TestCase

from playwright.sync_api import sync_playwright

from match_snapshot import MatchSnapshot


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


if __name__ == "__main__":
    unittest.main()
