from pathlib import PurePath

import pytest

from .helpers import DST, SRC, files_setup, filesystem_actions


@pytest.mark.parametrize(
    "rewrite", [False, True, False], ids=["not exists", "overwrite", "Can't copy"]
)
def test_copy_item(files_setup, filesystem_actions, rewrite, capsys):
    """Try to copy with different values in 'rewrite' argument."""
    filesystem_actions.rewrite = rewrite
    directories = {"dir 0": ["dir_copy"]}
    filesystem_actions.copy(directories)

    dst = PurePath(DST / "dir_copy")
    captured = capsys.readouterr()
    if captured.out.startswith(f"Copying {dst}"):
        assert True
    elif captured.out.startswith(f"A file or directory already exists: {dst}"):
        assert True
    else:
        assert False
