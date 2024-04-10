from selenium import webdriver
from selenium.webdriver.common.by import By

from match_snapshot import MatchSnapshot


class TestsSelenium(MatchSnapshot):
    snapshot_path = "./__snapshots__"
    failed_path = "./__errors__"

    def test_selenium(self):
        driver = webdriver.Chrome()
        driver.get("http://www.python.org")

        banner = driver.find_element(By.CLASS_NAME, "main-header")

        self.assert_match_snapshot(banner, "test_pytest_selenium")
