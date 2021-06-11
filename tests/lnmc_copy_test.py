import pytest

from .helpers import DST, SRC, files_setup, filesystem_actions


@pytest.mark.parametrize(
    "rewrite", [False, True, False], ids=["not exists", "overwrite", "Can't copy"]
)
def test_copy_item(files_setup, filesystem_actions, rewrite, capsys):
    """Try to copy with different values ​​in 'rewrite' argument."""
    filesystem_actions.rewrite = rewrite
    src = SRC / "dir 0/file 3.txt"
    dst = DST / "file 3.txt"
    filesystem_actions._copy_item(src, dst)

    captured = capsys.readouterr()
    if captured.out == f"Copying: {dst}\n":
        assert True
    elif captured.out.startswith(f"Overwritten: {dst}"):
        assert True
    elif captured.out.startswith(
        f"Can't copy. The file or directory: {dst} already exists."
    ):
        assert True
    else:
        assert False
