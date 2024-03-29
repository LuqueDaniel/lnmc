import pytest

from lnmc import FileSystemActions, PathPair


@pytest.mark.parametrize(
    "rewrite", [False, True], ids=["create copy", "overwrite copy"]
)
def test_copy_item(
    create_test_file: PathPair,
    filesystem_actions: FileSystemActions,
    rewrite: bool,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test to copy with different values in 'rewrite' argument."""
    if rewrite:
        create_test_file.dst.touch()
    filesystem_actions.rewrite = rewrite
    filesystem_actions._copy_item(create_test_file)

    captured = capsys.readouterr()
    if captured.out.startswith(f"Copying {create_test_file.dst}"):
        assert True
    else:
        pytest.raises(AssertionError)
