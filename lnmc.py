# © 2019 Daniel Luque
# License AGPLv3 (http://www.gnu.org/licenses/agpl-3.0-standalone.html)
"""lnmc

Allows to create symbolic links in batches from a YAML file and consolidate
them in aspecific directory.
"""

import pathlib
import shutil
from typing import Generator, NamedTuple, Union

import click as cli
import yaml


class PathPair(NamedTuple):
    src: pathlib.Path
    dst: pathlib.Path


class FileSystemActions:
    def __init__(
        self, src: str, dst: str, rewrite: bool = False, verbose: bool = False
    ) -> None:
        self.src = pathlib.Path(src)
        self.dst = pathlib.Path(dst)
        self.rewrite = rewrite
        self.verbose = verbose

    def _remove_item(self, item: pathlib.Path) -> None:
        if item.is_dir() and not item.is_symlink():
            shutil.rmtree(item)
        else:
            item.unlink()

    def _is_broken_symlink(self, path: pathlib.Path) -> bool:
        return not path.exists() and path.is_symlink()

    def _symlink_create(self, src: pathlib.Path, dst: pathlib.Path) -> None:
        """Create the symbolic link.

        Check that there aren't other files or directories with the same name in
        the destination directory. If the symbolic link already exists it will be
        ignored, unless the `rewrite` argument is True.

        Args:
            src (pathlib.Path): symbolic link source path.
            dst (pathlib.Path): symbolic link destination path.
        """
        if dst.exists():
            if dst.is_symlink():
                cli.secho(f"Symlink already exists: {dst}", fg="cyan")
            else:
                cli.secho(
                    f"File or directory: {dst} already exists.",
                    bold=True,
                    fg="red",
                )
            if not self.rewrite:
                return
            self._remove_item(dst)
        elif self._is_broken_symlink(dst):
            cli.secho(f"Symlink is broken: {dst}. Unlinking", fg="yellow")
            self._remove_item(dst)

        if self.verbose:
            cli.secho(f"Creating symlink: {dst}", fg="green", bold=True)
        dst.resolve().symlink_to(src.resolve())

    def _copy_item(self, src: pathlib.Path, dst: pathlib.Path):
        """Copy a file from a source path to a destination path.

        Args:
            src (pathlib.Path): source path.
            dst (pathlib.Path): destination path.
        """
        if dst.exists() or self._is_broken_symlink(dst):
            cli.secho(
                f"Can't copy. The file or directory: {dst} already exists.",
                bold=True,
                fg="red",
            )
            if not self.rewrite:
                return
            self._remove_item(dst)

        if self.verbose:
            cli.secho(f"Copying: {dst}", fg="green", bold=True)

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


def yaml_read(yaml_file: str) -> dict:
    """Read the YAML file and return a dictionary."""
    with open(yaml_file, "r") as stream:
        return yaml.safe_load(stream.read())


@cli.command()
@cli.argument("yaml_file", type=cli.Path(exists=True))
@cli.argument("src", type=cli.Path(exists=True))
@cli.argument("dst", type=cli.Path(exists=True))
@cli.option(
    "--copy/--no-copy",
    default=False,
    help="Copy directories and files instead of create symbolic links",
)
@cli.option(
    "--rewrite/--no-rewrite",
    default=False,
    help="Overwrite the symbolic links if exist.",
)
@cli.option("--verbose", is_flag=True, help="Enables verbose mode.")
@cli.version_option(version="1.2.0", prog_name="lnmc")
def lnmc(
    yaml_file: str, src: str, dst: str, copy: bool, rewrite: bool, verbose: bool
) -> None:
    """Allows to create symbolic links in batches from a YAML file and
    consolidate them in a specific directory.

    The files, directories and sub-directories that are going to be targeted to
    create the symbolic links are specified in a yaml file.

    Example:

        $ lnmc directories.yaml source_directory/ destination_directory/
    """
    file_actions = FileSystemActions(src, dst, rewrite, verbose)
    if verbose:
        cli.echo(f"Reading {cli.style(yaml_file, fg='green')} file.")
    directories = yaml_read(yaml_file)

    if copy:
        file_actions.copy(directories)
    else:
        file_actions.symlink(directories)
