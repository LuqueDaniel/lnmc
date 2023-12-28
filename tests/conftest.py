# © 2023 Daniel Luque
# License AGPLv3 (http://www.gnu.org/licenses/agpl-3.0-standalone.html)
import shutil
import sys
from pathlib import Path
from typing import Generator

import pytest

from lnmc import FileSystemActions, PathPair, yaml_read

sys.path.insert(0, "..")

DST = Path("tests/dst")
YAML_TEST_FILE = Path("tests/test.yaml")


@pytest.fixture()
def filesystem_actions(tmp_path: Path) -> FileSystemActions:
    """Instantiate a lnmc.FileSystemActions object and return it.

    Args:
        tmp_path: A pytest fixture to return temp test directory.

    Returns:
        FileSystemActions:
    """
    return FileSystemActions(tmp_path, DST, verbose=True)


@pytest.fixture()
def create_test_tree(tmp_path: Path) -> Generator[None, None, None]:
    """Create a test directory tree based on the content of YAML_TEST_FILE."""
    directories = yaml_read(YAML_TEST_FILE)
    for directory in directories:
        path = Path(tmp_path / directory)
        path.mkdir()
        # if directory has no files, create a subdirectory containing a file
        if not directories[directory]:
            item = Path(path / f"dir_to_copy/file {directory}.txt")
            item.parent.mkdir()
            item.touch()
            continue
        for file in directories[directory]:
            Path(path / file).touch()
    DST.mkdir(exist_ok=True)
    yield None
    shutil.rmtree(DST)


@pytest.fixture()
def create_test_file(
    tmp_path: Path, file_path: str = "dir/file.txt"
) -> Generator[PathPair, None, None]:
    """Creates a test file and returns a PathPair containing the source and
    destination path.

    Args:
        tmp_path:
        file_path (optional): Path of the file to create. Defaults to "dir/file.txt".

    Yields:
        Generator[PathPair, None, None]
    """
    src: Path = tmp_path / file_path
    src.parent.mkdir()
    src.touch()
    DST.mkdir(exist_ok=True)
    yield PathPair(src, DST / src.name)
    if DST.exists():
        shutil.rmtree(DST)
