# © 2019 Daniel Luque
# License AGPLv3 (http://www.gnu.org/licenses/agpl-3.0-standalone.html)
from pathlib import Path
import sys
import shutil

import pytest
from click.testing import CliRunner

import lnmc

sys.path.insert(0, "..")

YAML_TEST_FILE = "tests/test.yaml"
SRC = Path("tests/src")
DST = Path("tests/dst")


@pytest.fixture(scope="module")
def setup(request):
    """Create src and dst test hierarchy and cleanup after test finalize."""
    SRC.mkdir()
    for subdir in range(3):
        subdir = Path(f"{SRC}/subdir {subdir}")
        subdir.mkdir()
        for file_ in range(4):
            Path(f"{subdir}/file {file_}.txt").touch()
    DST.mkdir()

    request.addfinalizer(cleanup)


def cleanup():
    shutil.rmtree(SRC)
    shutil.rmtree(DST)


def test_yaml_read():
    result = lnmc.yaml_read(YAML_TEST_FILE)
    assert result is not None
    assert isinstance(result, dict)


@pytest.mark.parametrize("rewrite", [False, True, False])
def test_symlink_create(setup, rewrite):
    """Try to create symbolic links with different values ​​in the 'rewrite'
    argument."""
    src = Path(f"{SRC}/subdir 0/file 3.txt")
    dst = Path(f"{DST}/file 3.txt")
    lnmc.symlink_create(src, dst, rewrite=rewrite, verbose=True)


def test_symlink_create_check(setup):
    """Check if the symbolic link has been created."""
    dst = Path(f"{DST}/file 3.txt")
    lnmc.symlink_create(
        Path(f"{SRC}/subdir 1/file 3.txt"), dst, rewrite=False, verbose=True
    )
    assert dst.exists()
    assert dst.is_symlink()


def test_symlink_create_file_exists(setup):
    """Test symlink_create when file or directory already exists."""
    dst = DST.joinpath("file 2.txt")
    dst.touch()
    lnmc.symlink_create(
        Path(f"{SRC}/subdir 1/file 2.txt"), dst, rewrite=False, verbose=True
    )
    dst.unlink()


def test_lnmc(setup):
    """Test the full command."""
    runner = CliRunner()
    runner.invoke(
        lnmc.lnmc,
        [YAML_TEST_FILE, str(SRC), str(DST), "--rewrite", "--verbose"],
    )

    yaml_file = lnmc.yaml_read(YAML_TEST_FILE)

    for directory in yaml_file:
        for item in yaml_file[directory]:
            assert DST.joinpath(item).exists()
            assert DST.joinpath(item).is_symlink()
