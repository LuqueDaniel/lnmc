# © 2019 Daniel Luque
# License AGPLv3 (http://www.gnu.org/licenses/agpl-3.0-standalone.html)
from pathlib import PurePath

import pytest

from .helpers import DST, SRC, YAML_TEST_FILE, files_setup, filesystem_actions


@pytest.mark.parametrize(
    "rewrite", [False, True], ids=["Create symlink", "Rewrite symlink"]
)
def test_symlink_create(files_setup, filesystem_actions, rewrite, capsys):
    """Try to create symbolic links with different values in 'rewrite' argument."""
    filesystem_actions.rewrite = rewrite
    directories = {"dir 0": ["file 3.txt"]}
    filesystem_actions.symlink(directories)

    dst = PurePath(DST / "file 3.txt")
    captured = capsys.readouterr()
    if captured.out == f"Creating symlink: {dst}\n":
        assert True
    elif captured.out.startswith(f"Symlink already exists: {dst}"):
        assert True
    else:
        assert False


def test_symlink_create_file_exists(files_setup, filesystem_actions, capsys):
    """Test symlink_create when file or directory already exists."""
    dst = DST / "file 2.txt"
    dst.touch()
    directories = {"dir 1": ["file 2.txt"]}
    filesystem_actions.symlink(directories)

    captured = capsys.readouterr()  # capture std/stderr
    dst.unlink()
    assert captured.out.startswith(f"File or directory: {dst} already exists.")


@pytest.mark.parametrize(
    "rewrite,file_", [(False, "file_dont_exist.txt"), (True, "file 4.txt")]
)
def test_symlink_broken(files_setup, filesystem_actions, capsys, rewrite, file_):
    """Test broken symlink detection"""
    filesystem_actions.rewrite = rewrite
    src = SRC / f"dir 1/{file_}"
    dst = DST / file_
    dst.resolve().symlink_to(src.resolve())
    directories = {"dir 1": [file_]}
    filesystem_actions.symlink(directories)

    captured = capsys.readouterr()
    assert captured.out.startswith(f"Symlink is broken: {dst}. Unlinking\n")
