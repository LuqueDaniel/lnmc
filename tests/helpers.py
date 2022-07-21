# © 2019 Daniel Luque
# License AGPLv3 (http://www.gnu.org/licenses/agpl-3.0-standalone.html)
import shutil
import sys
from pathlib import Path

import pytest

import lnmc

sys.path.insert(0, "..")

SRC = Path("tests/src")
DST = Path("tests/dst")
YAML_TEST_FILE = "tests/test.yaml"


@pytest.fixture(scope="function")
def filesystem_actions() -> lnmc.FileSystemActions:
    return lnmc.FileSystemActions(SRC, DST, verbose=True)


@pytest.fixture(scope="module")
def files_setup(request):
    """Create src and dst test hierarchy and cleanup after test finalize."""
    dirs_to_create = 3
    files_to_create = 4

    SRC.mkdir()
    for directory in range(dirs_to_create):
        directory = SRC / f"dir {directory}"
        directory.mkdir()
        directory.joinpath("dir_copy/").mkdir()
        for file_ in range(files_to_create):
            Path(f"{directory}/file {file_}.txt").touch()

    DST.mkdir()
    request.addfinalizer(cleanup)


def cleanup():
    shutil.rmtree(SRC)
    shutil.rmtree(DST)
