import pytest

from match_snapshot import MatchSnapshot, WebElementNotSupportedError


def test_get_snapshot_filename():
    path = "demo-path-of-snapshots"
    id = "any-id"

    instance = MatchSnapshot()
    instance.snapshot_path = path

    file = instance.get_snapshot_filename(id)

    assert file == f"{path}/snapshot_{id}.png"


def test_get_compare_filename():
    path = "demo-path-of-snapshots"
    id = "any-id"

    instance = MatchSnapshot()
    instance.snapshot_path = path

    file = instance.get_compare_filename(id)

    assert file == f"{path}/compare_{id}.png"


def test_takes_screenshot_without_screenshot():
    class WebElement:
        pass

    instance = MatchSnapshot()
    element = WebElement()

    with pytest.raises(WebElementNotSupportedError):
        instance.takes_screenshot(element, "any-file.png")


def test_takes_screenshot_with_path():
    parse_path = "success-result"

    class WebElement:
        def screenshot(self, *, path: str):
            return path

    instance = MatchSnapshot()
    element = WebElement()

    response = instance.takes_screenshot(element, parse_path)
    assert response == parse_path


def test_takes_screenshot_with_positioned():
    parse_path = "success-result"

    class WebElement:
        def screenshot(self, image: str):
            return image

    instance = MatchSnapshot()
    element = WebElement()

    response = instance.takes_screenshot(element, parse_path)
    assert response == parse_path


def test_takes_screenshot_without_args():
    parse_path = "success-result"

    class WebElement:
        def screenshot(self):
            return parse_path

    instance = MatchSnapshot()
    element = WebElement()

    with pytest.raises(WebElementNotSupportedError):
        instance.takes_screenshot(element, parse_path)
