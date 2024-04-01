import os
from typing import Any

from PIL import Image, ImageChops


class WebElementNotSupportedError(Exception):
    def __init__(self):
        msg = "The web client is not supported by native. Implements the takes_screenshot method."
        super().__init__(msg)


class MatchSnapshot:
    snapshot_path = "./tests/__snapshots__"
    failed_path = "./tests/__errors__"
    threshold = 10

    def takes_screenshot(self, element: Any, destination_file: str):
        """
        Takes a screenshot of a web element.

        Args:
            element: the element to take screenshot.
            destination_file: the destination file path to save image.
        """
        if not hasattr(element, "screenshot"):
            raise WebElementNotSupportedError()

        try:
            return element.screenshot(path=destination_file)
        except Exception:
            pass
        try:
            return element.screenshot(destination_file)
        except Exception:
            pass

        raise WebElementNotSupportedError()

    def get_snapshot_filename(self, id: str) -> str:
        """
        Generate the snapshot file name to a unique id.

        Args:
            id: a unique id to gets the snapshot file name.
        """
        return os.path.join(self.snapshot_path, f"snapshot_{id}.png")

    def get_compare_filename(self, id: str) -> str:
        """
        Generate the comparison file name to a unique id.

        Args:
            id: a unique id to gets the comparison file name.
        """
        return os.path.join(self.snapshot_path, f"compare_{id}.png")

    def _create_snapshot_image(self, element, id: str):
        """
        Takes a screenshot of the element and stores it as snaptshot.

        Args:
            element: the element to takes the screenshot.
            id: a unique id to gets the snapshot file name.
        """
        file = self.get_snapshot_filename(id)
        self.takes_screenshot(element, file)

    def _get_snapshot_image(self, element: Any, id: str):
        """
        Gets, or create, the snapshot image from the element.

        Args:
            element: the element to create the snapshot.
            id: a unique id to gets the snapshot file name.

        Returns:
            A tuple of the Image and a boolean indicating
            if the file was created.
        """
        file = self.get_snapshot_filename(id)
        created = False

        if not os.path.exists(file):
            self._create_snapshot_image(element, id)
            created = True

        return Image.open(file).convert("RGB"), created

    def _create_compare_image(self, element, id: str):
        """
        Takes a screenshot of the element and store it as comparison.

        Args:
            element: the element to takes the screenshot.
            id: a unique id to gets the snapshot file name.
        """
        file = self.get_compare_filename(id)
        self.takes_screenshot(element, file)

    def _get_compare_image(self, element, id: str):
        """
        Create the comparison image from the element and open it.

        Args:
            element: the element to create the comparison.
            id: a unique id to gets the comparison file.
        """
        self._create_compare_image(element, id)
        file = self.get_compare_filename(id)
        return Image.open(file).convert("RGB")

    def _delete_compare_image(self, id: str):
        """
        Delete the comparison image file.

        Args:
            id: a unique id to delete the comparison file.
        """
        file = self.get_compare_filename(id)
        if not os.path.exists(file):
            return
        os.remove(file)

    def _get_failed_filename(self, id: str, image_type: str):
        """
        Generate the file name to a failed id.

        Args:
            id: a unique id to gets the file name.
            image_type: a image type to gets the file name.
        """
        return os.path.join(self.failed_path, f"{id}/{image_type}.png")

    def _save_failed_images(self, id: str, image, comparison, diff, threshold_diff):
        """
        Save snapshot, comparison, difference and thresholded difference images.

        Args:
            id: a unique id to gets the file names.
            image: the snapshot image.
            comparison: the comparison image.
            diff: the difference image.
            threshold_diff: the thresholded difference image.
        """
        if image:
            image.save(self._get_failed_filename(id, "snapshot"))
        if comparison:
            comparison.save(self._get_failed_filename(id, "comparison"))
        if diff:
            diff.save(self._get_failed_filename(id, "difference"))
        if threshold_diff:
            threshold_diff.save(self._get_failed_filename(id, "difference_threshold"))

    def _has_differences(self, id: str, image, comparison):
        """
        Compute if the two images has differences.

        Args:
            id: a unique id to gets the snapshot file names.
            image: the snapshot image.
            comparison: the comparison image.
        """
        diff = ImageChops.difference(image, comparison)

        if not diff.getbbox():
            return False

        threshold_diff = diff.point(lambda x: 0 if x < self.threshold else 255)
        pixels = threshold_diff.getcolors()

        if len(pixels) == 1:
            _, color = pixels[0]
            if color == (0, 0, 0):
                return False

        self._save_failed_images(id, image, comparison, diff, threshold_diff)
        return True

    def assert_match_snapshot(self, element: Any, id: str):
        """
        Assert if a screenshot of a element matches to the saved snapshot of it.

        Args:
            element: the element to create the comparison and snapshot image.
            id: a unique id to gets the snapshot file names.
        """
        image, created = self._get_snapshot_image(element, id)

        if created:
            return

        comparison_image = self._get_compare_image(element, id)

        has_difference = self._has_differences(id, image, comparison_image)
        self._delete_compare_image(id)

        if not has_difference:
            return

        if hasattr(self, "fail"):
            return self.fail("The UI screenshot not matches snapshot.")
        assert not has_difference, "The UI screenshot not matches snapshot."
