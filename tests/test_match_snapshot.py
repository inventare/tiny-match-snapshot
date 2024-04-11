from unittest.mock import MagicMock, patch

import pytest

from match_snapshot import MatchSnapshot, WebElementNotSupportedError


class CommonWebElement:
    def screenshot(self, path):
        pass


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


def test_create_snapshot_image_filename():
    id = "my-any-id-here"
    path = "./any-path-here/"

    instance = MatchSnapshot()
    instance.get_snapshot_filename = MagicMock(return_value=path)
    element = CommonWebElement()
    element.screenshot = MagicMock()

    instance._create_snapshot_image(element, id)

    instance.get_snapshot_filename.assert_called_once_with(id)
    element.screenshot.assert_called_once_with(path=path)


def test_get_snapshot_image_with_exists():
    path = "./any-path/here.png"
    instance = MatchSnapshot()
    instance.get_snapshot_filename = MagicMock(return_value=path)
    element = CommonWebElement()
    element.screenshot = MagicMock()
    id = "any-id"

    image_mock = MagicMock()
    image_mock.open = MagicMock(return_value=MagicMock())
    with patch("match_snapshot.match_snapshot.Image", image_mock):
        with patch("os.path.exists", MagicMock(return_value=True)):
            instance._get_snapshot_image(element, id)

            image_mock.open.assert_called_once_with(path)
            element.screenshot.assert_not_called()


def test_get_snapshot_image_not_exists():
    path = "./any-path/here.png"
    instance = MatchSnapshot()
    instance.get_snapshot_filename = MagicMock(return_value=path)
    element = CommonWebElement()
    element.screenshot = MagicMock()
    id = "any-id"

    image_mock = MagicMock()
    image_mock.open = MagicMock(return_value=MagicMock())
    with patch("match_snapshot.match_snapshot.Image", image_mock):
        with patch("os.path.exists", MagicMock(return_value=False)):
            instance._get_snapshot_image(element, id)

            image_mock.open.assert_called_once_with(path)
            element.screenshot.assert_called_once_with(path=path)


def test_create_compare_image():
    path = "./any-path/here.png"
    instance = MatchSnapshot()
    instance.get_compare_filename = MagicMock(return_value=path)
    element = CommonWebElement()
    element.screenshot = MagicMock()
    id = "any-id"

    instance._create_compare_image(element, id)
    element.screenshot.assert_called_once_with(path=path)


def test_get_compare_image():
    path = "./any-path/here.png"
    instance = MatchSnapshot()
    instance.get_compare_filename = MagicMock(return_value=path)
    element = CommonWebElement()
    element.screenshot = MagicMock()
    id = "any-id"

    image_mock = MagicMock()
    image_mock.open = MagicMock(return_value=MagicMock())
    with patch("match_snapshot.match_snapshot.Image", image_mock):
        instance._get_compare_image(element, id)

        image_mock.open.assert_called_once_with(path)
        element.screenshot.assert_called_once_with(path=path)


def test_delete_compare_image_exists_image():
    path = "./any-path/here.png"
    instance = MatchSnapshot()
    instance.get_compare_filename = MagicMock(return_value=path)

    with patch("os.path.exists", MagicMock(return_value=True)):
        with patch("os.remove") as remove_mock:
            instance._delete_compare_image(id)

            remove_mock.assert_called_once_with(path)


def test_delete_compare_image_not_exists_image():
    path = "./any-path/here.png"
    instance = MatchSnapshot()
    instance.get_compare_filename = MagicMock(return_value=path)

    with patch("os.path.exists", MagicMock(return_value=False)):
        with patch("os.remove") as remove_mock:
            instance._delete_compare_image(id)

            remove_mock.assert_not_called()


def test_get_failed_filename():
    path = "demo-path-of-errors"
    id = "any-id"
    image_type = "my-faillled-type"

    instance = MatchSnapshot()
    instance.failed_path = path

    file = instance._get_failed_filename(id, image_type)

    assert file == f"{path}/{id}/{image_type}.png"


def test_grant_error_path_exists_not_exists():
    path = "./demo-path/of-errors/here"
    id = "any-id"

    instance = MatchSnapshot()
    instance.failed_path = path
    with patch("os.path.exists", MagicMock(return_value=False)):
        with patch("os.makedirs") as mkdirs:
            instance._grant_error_path_exists(id)

            mkdirs.assert_called_once_with(f"{path}/{id}")


def test_grant_error_path_exists_with_existing_path():
    path = "./demo-path/of-errors/here"
    id = "any-id"

    instance = MatchSnapshot()
    instance.failed_path = path
    with patch("os.path.exists", MagicMock(return_value=True)):
        with patch("os.makedirs") as mkdirs:
            instance._grant_error_path_exists(id)

            mkdirs.assert_not_called()


def test_save_failed_with_image():
    path = "./any-error/path"
    id = "any-id"

    instance = MatchSnapshot()
    instance.failed_path = path
    instance._grant_error_path_exists = MagicMock()

    image = MagicMock()
    image.save = MagicMock()

    instance._save_failed_images(id, image, None, None, None)

    instance._grant_error_path_exists.assert_called_once_with(id)
    image.save.assert_called_once_with(f"{path}/{id}/snapshot.png")


def test_save_failed_with_comparison():
    path = "./any-error/path"
    id = "any-id"

    instance = MatchSnapshot()
    instance.failed_path = path
    instance._grant_error_path_exists = MagicMock()

    image = MagicMock()
    image.save = MagicMock()
    comparison = MagicMock()
    comparison.save = MagicMock()

    instance._save_failed_images(id, image, comparison, None, None)

    instance._grant_error_path_exists.assert_called_once_with(id)
    image.save.assert_called_once_with(f"{path}/{id}/snapshot.png")
    comparison.save.assert_called_once_with(f"{path}/{id}/comparison.png")


def test_save_failed_with_diff():
    path = "./any-error/path"
    id = "any-id"

    instance = MatchSnapshot()
    instance.failed_path = path
    instance._grant_error_path_exists = MagicMock()

    image = MagicMock()
    image.save = MagicMock()
    comparison = MagicMock()
    comparison.save = MagicMock()
    diff = MagicMock()
    diff.save = MagicMock()

    instance._save_failed_images(id, image, comparison, diff, None)

    instance._grant_error_path_exists.assert_called_once_with(id)
    image.save.assert_called_once_with(f"{path}/{id}/snapshot.png")
    comparison.save.assert_called_once_with(f"{path}/{id}/comparison.png")
    diff.save.assert_called_once_with(f"{path}/{id}/difference.png")


def test_save_failed_with_threshold_diff():
    path = "./any-error/path"
    id = "any-id"

    instance = MatchSnapshot()
    instance.failed_path = path
    instance._grant_error_path_exists = MagicMock()

    image = MagicMock()
    image.save = MagicMock()
    comparison = MagicMock()
    comparison.save = MagicMock()
    diff = MagicMock()
    diff.save = MagicMock()
    threshold_diff = MagicMock()
    threshold_diff.save = MagicMock()

    instance._save_failed_images(id, image, comparison, diff, threshold_diff)

    instance._grant_error_path_exists.assert_called_once_with(id)
    image.save.assert_called_once_with(f"{path}/{id}/snapshot.png")
    comparison.save.assert_called_once_with(f"{path}/{id}/comparison.png")
    diff.save.assert_called_once_with(f"{path}/{id}/difference.png")
    threshold_diff.save.assert_called_once_with(f"{path}/{id}/difference_threshold.png")
