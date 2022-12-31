# © 2019 Daniel Luque
# License AGPLv3 (http://www.gnu.org/licenses/agpl-3.0-standalone.html)
"""lnmc

Allows to create symbolic links in batches from a YAML file and consolidate
them in aspecific directory.
"""

import shutil
from pathlib import Path
from typing import Any, Generator, NamedTuple, Union

import click as cli
import yaml

__version__ = "1.3.0"


class PathPair(NamedTuple):
    """Pair of source and destination paths."""

    src: Path
    dst: Path


class FileSystemActions:
    """Perform actions related to the file system such as creating symlinks or copy.

    Args:
        src (Path): source path.
        dst (Path): destination path.
        rewrite (bool): if True, overwrite existing files or directories.
        verbose (bool): if True, print actions.
    """

    def __init__(
        self,
        src: Path,
        dst: Path,
        rewrite: bool = False,
        verbose: bool = False,
    ) -> None:
        self.src = src
        self.dst = dst
        self.rewrite = rewrite
        self.verbose = verbose

    def _remove_item(self, item: Path) -> None:
        if item.is_dir() and not item.is_symlink():
            shutil.rmtree(item)
        else:
            item.unlink()

    def _is_broken_symlink(self, path: Path) -> bool:
        return not path.exists() and path.is_symlink()

    def _symlink_create(self, src: Path, dst: Path) -> None:
        """Create the symbolic link.

        Check that there aren't other files or directories with the same name in
        the destination directory. If the symbolic link already exists it will be
        ignored, unless the `rewrite` argument is True.

        Args:
            src (Path): symbolic link source path.
            dst (Path): symbolic link destination path.
        """
        if dst.exists():
            if dst.is_symlink():
                echo(f"Symlink already exists: {dst}", fg="cyan")
            else:
                echo(
                    f"File or directory: {dst} already exists.",
                    bold=True,
                    fg="red",
                )
            if not self.rewrite:
                return
            self._remove_item(dst)
        elif self._is_broken_symlink(dst):
            echo(f"Symlink is broken: {dst}. Unlinking", fg="yellow")
            self._remove_item(dst)

        echo(f"Creating symlink: {dst}", fg="green", display=self.verbose)
        dst.resolve().symlink_to(src.resolve())

    def _copy_item(self, src: Path, dst: Path):
        """Copy a file from a source path to a destination path.

        Args:
            src (Path): source path.
            dst (Path): destination path.
        """
        if dst.exists() or self._is_broken_symlink(dst):
            echo(
                f"Can't copy. The file or directory: {dst} already exists.",
                bold=True,
                fg="red",
            )
            if not self.rewrite:
                return
            self._remove_item(dst)

        if self.verbose:
            echo(f"Copying: {dst}", fg="green")

        if src.is_dir():
            shutil.copytree(src, dst)
        elif src.is_file():
            shutil.copy2(src, dst)

    def _get_paths(self, directories: dict) -> Generator[PathPair, None, None]:
        """Get destination and source paths from a dict.

        Returns: PathPair
        """
        for directory in directories:
            src_path = self.src / directory
            items: Union[list, Generator] = directories[directory] or src_path.iterdir()
            for item in items:
                basename = item if isinstance(item, str) else item.name
                yield PathPair(src_path / basename, self.dst / basename)

    def symlink(self, directories: dict) -> None:
        """Create symlinks from a dict.

        Args:
            directories (dict): contains directories and subdirectories/files hierarchy.
        """
        for item in self._get_paths(directories):
            self._symlink_create(item.src, item.dst)

    def copy(self, directories: dict) -> None:
        """Copy files and directories from a dict

        Args:
            directories (dict): contains directories and files to copy.
        """
        for item in self._get_paths(directories):
            self._copy_item(item.src, item.dst)


def echo(message: str, display: bool = True, **styles: Any):
    """Wraps click.secho function with a display check."""
    if display:
        cli.secho(message, **styles)


def yaml_read(yaml_file: Path) -> dict:
    """Read the YAML file and return a dictionary."""
    with open(yaml_file, "r", encoding="utf-8") as stream:
        return yaml.safe_load(stream.read())


@cli.command()
@cli.argument("yaml_file", type=cli.Path(exists=True, dir_okay=False, path_type=Path))
@cli.argument("src", type=cli.Path(exists=True, file_okay=False, path_type=Path))
@cli.argument(
    "dst",
    type=cli.Path(exists=True, file_okay=False, writable=True, path_type=Path),
)
@cli.option(
    "--copy",
    is_flag=True,
    help="Copy directories and files instead of create symbolic links",
)
@cli.option(
    "--rewrite",
    is_flag=True,
    help="Overwrite the symbolic links if exist",
)
@cli.option("-v", "--verbose", is_flag=True, help="Enables verbose mode")
@cli.version_option(__version__, prog_name="lnmc")
def lnmc(
    yaml_file: Path,
    src: Path,
    dst: Path,
    copy: bool,
    rewrite: bool,
    verbose: bool,
) -> None:
    """Create symbolic links in batches from a YAML file and consolidate them
    in a specific directory.

    YAML_FILE is a YAML file that contain the directories, subdirectories and files
    to be symbolically linked.

    SRC source path of the element specified in YAML_FILE.

    DST destination path where the symbolic links will be created.

    Example:

        $ lnmc directories.yaml source_directory/ destination_directory/
    """
    file_actions = FileSystemActions(src, dst, rewrite, verbose)
    echo(f"Reading {cli.style(yaml_file, fg='green')} file.", display=verbose)
    directories = yaml_read(yaml_file)

    if copy:
        file_actions.copy(directories)
    else:
        file_actions.symlink(directories)
