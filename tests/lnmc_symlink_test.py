# © 2019 Daniel Luque
# License AGPLv3 (http://www.gnu.org/licenses/agpl-3.0-standalone.html)
from pathlib import Path

import pytest

from lnmc import FileSystemActions, PathPair

from .helpers import create_test_file, filesystem_actions


class TestSymlink:
    @pytest.mark.parametrize(
        "rewrite", [False, True], ids=["create symlink", "overwrite symlink"]
    )
    def test_symlink_create(
        self,
        create_test_file: PathPair,
        filesystem_actions: FileSystemActions,
        rewrite: bool,
        capsys,
    ):
        """Test to create symbolic links with different values in 'rewrite' argument."""
        if rewrite:
            Path(create_test_file.dst).symlink_to(create_test_file.src.resolve())
        filesystem_actions.rewrite = rewrite
        filesystem_actions._symlink_create(*create_test_file)

        captured = capsys.readouterr()
        if captured.out.startswith(f"Creating symbolic link {create_test_file.dst}"):
            assert True
        elif (
            captured.out.startswith(
                f"A symbolic link already exists: {create_test_file.dst}"
            )
            and rewrite
        ):
            assert True
        else:
            assert False

    def test_symlink_create_file_exists(
        self, create_test_file: PathPair, filesystem_actions: FileSystemActions, capsys
    ):
        """Test symlink_create when file or directory already exists."""
        # Create destination file
        create_test_file.dst.touch()

        filesystem_actions._symlink_create(*create_test_file)

        captured = capsys.readouterr()  # capture std/stderr
        assert captured.out.startswith(
            f"A file or directory already exists: {create_test_file.dst}"
        )

    def test_symlink_broken(
        self,
        create_test_file: PathPair,
        filesystem_actions: FileSystemActions,
        tmp_path: Path,
        capsys,
    ):
        """Test broken symlink detection"""
        # Create a broken symlink
        src = tmp_path / "dir/file_dont_exist.txt"
        create_test_file.dst.resolve().symlink_to(src.resolve())

        filesystem_actions.rewrite = True
        filesystem_actions._symlink_create(*create_test_file)

        captured = capsys.readouterr()
        assert captured.out.startswith(
            f"A broken symbolic link already exists: {create_test_file.dst}"
        )
