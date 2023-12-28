# © 2019 Daniel Luque
# License AGPLv3 (http://www.gnu.org/licenses/agpl-3.0-standalone.html)
"""lnmc

Allows to create symbolic links in batches from a YAML file and consolidate
them in a specific directory.
"""

import shutil
from pathlib import Path
from typing import Any, Dict, Generator, List, NamedTuple, Union

import click as cli
import yaml

__version__ = "1.4.0"

DirectoriesDict = Dict[str, List[str]]


class PathPair(NamedTuple):
    """Pair of source and destination paths."""

    src: Path
    dst: Path


class FileSystemActions:
    """Perform actions related to the file system such as creating symlinks or
    copy items.

    Args:
        src: source path.
        dst: destination path.
        rewrite: if True, overwrite existing files or directories.
        verbose: if True, print actions.
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
        echo(f"Removing: {item}", fg="red", display=self.verbose)
        if item.is_dir() and not item.is_symlink():
            shutil.rmtree(item)
        else:
            item.unlink()

    def _is_broken_symlink(self, path: Path) -> bool:
        return not path.exists() and path.is_symlink()

    def _check_destination_exists(self, dst: Path) -> bool:
        if self._is_broken_symlink(dst):
            echo(
                f"A broken symbolic link already exists: {cli.style(dst, fg='red')}",
                error=True,
            )
        elif dst.is_symlink():
            echo(
                f"A symbolic link already exists: {cli.style(dst, fg='yellow')}",
                error=True,
            )
        elif dst.exists():
            echo(
                f"A file or directory already exists: {cli.style(dst, fg='yellow')}",
                error=True,
            )
        else:
            return False
        return True

    def _check_source_exists(self, src: Path) -> bool:
        if not src.exists():
            echo(
                f"The source file or directory {src} does not exist. Check the Yaml "
                "file and try again.",
                fg="red",
                error=True,
            )
            return False
        return True

    def _can_create_item(self, path_pair: PathPair) -> bool:
        if not self._check_source_exists(path_pair.src):
            return False
        if self._check_destination_exists(path_pair.dst):
            if not self.rewrite:
                return False
            self._remove_item(path_pair.dst)
        return True

    def _symlink_create(self, path_pair: PathPair) -> None:
        """Create the symbolic link.

        Args:
            path_pair: src and dst path tuple.
        """
        if self._can_create_item(path_pair):
            echo(
                f"Creating symbolic link {path_pair.dst} -> {path_pair.src}", fg="green"
            )
            path_pair.dst.resolve().symlink_to(path_pair.src.resolve())

    def _copy_item(self, path_pair: PathPair) -> None:
        """Copy file or directory from a source path to a destination path.

        Args:
            path_pair: src and dst path tuple.
        """
        if self._can_create_item(path_pair):
            echo(f"Copying {path_pair.dst} from {path_pair.src}", fg="green")
            if path_pair.src.is_dir():
                shutil.copytree(*path_pair)
            elif path_pair.src.is_file():
                shutil.copy2(*path_pair)

    def _get_paths(
        self, directories: DirectoriesDict
    ) -> Generator[PathPair, None, None]:
        """Get destination and source paths from a dict.

        Returns: PathPair
        """
        for directory in directories:
            src_path = self.src / directory
            items: Union[List[str], Generator[Path, None, None]] = (
                directories[directory] or src_path.iterdir()
            )
            for item in items:
                basename = item if isinstance(item, str) else item.name
                yield PathPair(src_path / basename, self.dst / basename)

    def symlink(self, directories: DirectoriesDict) -> None:
        """Create symlinks from a dict.

        Args:
            directories: contains directories and subdirectories/files hierarchy.
        """
        for item in self._get_paths(directories):
            self._symlink_create(item)

    def copy(self, directories: DirectoriesDict) -> None:
        """Copy files and directories from a dict

        Args:
            directories: contains directories and files to copy.
        """
        for item in self._get_paths(directories):
            self._copy_item(item)


def echo(
    message: str, error: bool = False, display: bool = True, **styles: Any
) -> None:
    """Wraps click.secho function with a display check."""
    if display:
        cli.secho(message, err=error, **styles)


def yaml_read(yaml_file: Path) -> DirectoriesDict:
    """Read the YAML file and return a dictionary."""
    with yaml_file.open(encoding="utf-8") as stream:
        result = yaml.safe_load(stream.read())
        if not isinstance(result, dict):
            raise cli.UsageError(
                f"The file {yaml_file} does not match the expected format. "
                "Please check the file content and try again."
            )
        return result


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
