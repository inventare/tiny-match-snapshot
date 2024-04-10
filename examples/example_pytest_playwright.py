from playwright.sync_api import Page, expect

from match_snapshot import MatchSnapshot


class TestsPlaywright(MatchSnapshot):
    snapshot_path = "./__snapshots__"
    failed_path = "./__errors__"

    def test_playwright(self, page: Page):
        page.goto("https://playwright.dev/")

        element = page.query_selector(".hero.hero--primary")
        MatchSnapshot().assert_match_snapshot(element, "test_pytest_playwright")
