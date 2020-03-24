# © 2019 Daniel Luque
# License AGPLv3 (http://www.gnu.org/licenses/agpl-3.0-standalone.html)
from pathlib import Path

import pytest
from click.testing import CliRunner

import lnmc

from .helpers import SRC, DST, setup


YAML_TEST_FILE = "tests/test.yaml"


def test_yaml_read():
    result = lnmc.yaml_read(YAML_TEST_FILE)
    assert result is not None
    assert isinstance(result, dict)


@pytest.mark.parametrize("rewrite", [False, True, False])
def test_symlink_create(setup, rewrite, capsys):
    """Try to create symbolic links with different values ​​in the 'rewrite'
    argument."""
    src = SRC / "subdir 0/file 3.txt"
    dst = DST / "file 3.txt"
    lnmc.symlink_create(src, dst, rewrite=rewrite, verbose=True)
    captured = capsys.readouterr()

    if rewrite:
        assert captured.out.startswith(f"Symbolic link exists: {dst} Unlinking")
    elif not rewrite and not dst.exists():
        assert captured.out == f"Creating symlink: {dst}\n"


def test_symlink_create_check(setup):
    """Check if the symbolic link has been created."""
    dst = DST / "file 3.txt"
    lnmc.symlink_create(SRC / "subdir 1/file 3.txt", dst, rewrite=False, verbose=True)

    assert dst.exists()
    assert dst.is_symlink()


def test_symlink_create_file_exists(setup, capsys):
    """Test symlink_create when file or directory already exists."""
    dst = DST / "file 2.txt"
    dst.touch()
    lnmc.symlink_create(SRC / "subdir 1/file 2.txt", dst, rewrite=False, verbose=True)
    captured = capsys.readouterr()  # capture std/stderr
    dst.unlink()

    assert (
        captured.out
        == f"Can't create symlink. The file or directory: {dst} already exists.\n"
    )


def test_broken_symlink(setup, capsys):
    """Test broken symlink detection"""
    src = SRC / "subdir 1/file 4.txt"  # This file don't exist
    dst = DST / "file 4.txt"
    dst.resolve().symlink_to(src.resolve())
    lnmc.symlink_create(src, dst, rewrite=False, verbose=True)
    captured = capsys.readouterr()

    assert captured.out.startswith(f"Symbolic link is broken: {dst} Unlinking\n")


def test_lnmc(setup):
    """Test the full command."""
    runner = CliRunner()
    runner.invoke(
        lnmc.lnmc, [YAML_TEST_FILE, str(SRC), str(DST), "--rewrite", "--verbose"]
    )

    yaml_file = lnmc.yaml_read(YAML_TEST_FILE)

    for directory in yaml_file:
        # When create symlink for every element inside of a directory
        if not yaml_file[directory]:
            for item in (SRC / directory).iterdir():
                assert (DST / item.name).exists() and (DST / item.name).is_symlink()
            continue
        for item in yaml_file[directory]:
            assert (DST / item).exists() and (DST / item).is_symlink()
