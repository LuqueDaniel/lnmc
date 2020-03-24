# © 2019 Daniel Luque
# License AGPLv3 (http://www.gnu.org/licenses/agpl-3.0-standalone.html)
from pathlib import Path
import sys
import shutil

import pytest

sys.path.insert(0, "..")

SRC = Path("tests/src")
DST = Path("tests/dst")


@pytest.fixture(scope="module")
def setup(request):
    """Create src and dst test hierarchy and cleanup after test finalize."""
    SRC.mkdir()
    for subdir in range(3):
        subdir = SRC / f"subdir {subdir}"
        subdir.mkdir()
        for file_ in range(4):
            Path(f"{subdir}/file {file_}.txt").touch()

    DST.mkdir()
    request.addfinalizer(cleanup)


def cleanup():
    shutil.rmtree(SRC)
    shutil.rmtree(DST)
