import os
from shutil import rmtree

import pytest

from match_snapshot import MatchSnapshot


class Element:
    def screenshot(self, path):
        pass


class TestsMatchSnapshotWithImages(MatchSnapshot):
    def test_match_snapshot_same_images(self):
        self.snapshot_path = "./tests/__snapshots__"
        id = "python_home_page"

        with open("./tests/__snapshots__/snapshot_python_home_page.png", "rb") as f1:
            with open("./tests/__snapshots__/compare_python_home_page.png", "wb") as f2:
                f2.write(f1.read())

        self.assert_match_snapshot(Element(), id)

    def test_match_snapshot_wrong_image(self):
        self.snapshot_path = "./tests/__snapshots__"
        self.failed_path = "./tests/__errors__"
        id = "python_home_wrong_box"
        if os.path.exists("./tests/__errors__"):
            rmtree("./tests/__errors__")

        with open("./tests/__snapshots__/snapshot_python_home_page.png", "rb") as f1:
            with open(
                "./tests/__snapshots__/compare_python_home_wrong_box.png", "wb"
            ) as f2:
                f2.write(f1.read())

        with pytest.raises(AssertionError):
            self.assert_match_snapshot(Element(), id)

        assert os.path.exists(f"./tests/__errors__/{id}/comparison.png")
        assert os.path.exists(f"./tests/__errors__/{id}/difference_threshold.png")
        assert os.path.exists(f"./tests/__errors__/{id}/difference.png")
        assert os.path.exists(f"./tests/__errors__/{id}/snapshot.png")
        assert os.path.isfile(f"./tests/__errors__/{id}/comparison.png")
        assert os.path.isfile(f"./tests/__errors__/{id}/difference_threshold.png")
        assert os.path.isfile(f"./tests/__errors__/{id}/difference.png")
        assert os.path.isfile(f"./tests/__errors__/{id}/snapshot.png")

        if os.path.exists("./tests/__errors__"):
            rmtree("./tests/__errors__")

    def test_match_snapshot_threshold(self):
        self.snapshot_path = "./tests/__snapshots__"
        id = "python_home_threshold"

        with open("./tests/__snapshots__/snapshot_python_home_page.png", "rb") as f1:
            with open(
                "./tests/__snapshots__/compare_python_home_threshold.png", "wb"
            ) as f2:
                f2.write(f1.read())

        self.assert_match_snapshot(Element(), id)
