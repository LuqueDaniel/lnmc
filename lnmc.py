"""lnmc - Allows to create symbolic link in batches from a YAML file."""

import pathlib

import click as cli
import yaml


def yaml_read(yaml_file: str) -> dict:
    """Read the YAML file and return a dictionary."""
    with open(yaml_file, "r") as stream:
        return yaml.safe_load(stream.read())


def symlink_create(src: pathlib.Path, dst: pathlib.Path, rewrite: bool,
                   verbose: bool) -> None:
    """Create the symbolic link.

    Check that there aren't other files or directories with the same name in
    the destination directory. If the symbolic link already exists it will be
    ignored, unless the `rewrite` argument is True.

    Args:
        src (pathlib.Path): symbolic link origin path.
        dst (pathlib.Path): destination directory where the symbolic link will
                            be created.
        rewrite (bool): overwrite symbolic links if exist.
        verbose (bool): show log messages.

    Returns: None
    """
    if dst.exists() and rewrite and dst.is_symlink():
        if verbose:
            cli.secho(f"Symbolic link exists: {dst} Unlinking", fg='cyan')
        dst.unlink()
    elif not dst.exists() and dst.is_symlink():
        if verbose:
            cli.secho(f"Symbolic link is broken: {dst} Unlinking", fg='yellow')
        dst.unlink()
    elif dst.exists() and not dst.is_symlink():
        cli.secho("Can't create symlink. The file or directory: "
                  f"{dst} already exists.", bold=True, fg='red')
        return
    elif dst.exists() and not rewrite:
        return

    if verbose:
        cli.secho(f"Creating symlink: {dst}", fg='green', bold=True)

    dst.resolve().symlink_to(src.resolve())


@cli.command()
@cli.argument('yaml_file', type=cli.Path(exists=True))
@cli.argument('src', type=cli.Path(exists=True))
@cli.argument('dst', type=cli.Path(exists=True))
@cli.option('--rewrite/--no-rewrite', default=False,
            help="Overwrite thesymbolic links if exist.")
@cli.option('--verbose', is_flag=True, help="Enables verbose mode.")
@cli.version_option(version="1.0.0", prog_name="lnmc")
def lnmc(yaml_file: str, src: str, dst: str, rewrite: bool,
         verbose: bool) -> None:
    """lnmc allows to create symbolic links in batches.

    The files, directories and sub-directories that are going to be targeted to
    create the symbolic links are specified in a yaml file.

    $ lnmc directories.yaml ~/destination_directory source_directory/
    """
    if verbose:
        cli.echo(f"Reading {cli.style(yaml_file, fg='green')} file.")
    dirs = yaml_read(yaml_file)

    for directory in dirs:
        src_path = pathlib.Path(src).joinpath(directory)

        if dirs[directory] is None:
            subdirs = src_path.iterdir()
        else:
            subdirs = dirs[directory]

        for item in subdirs:
            if hasattr(item, 'name'):
                item = item.name

            symlink_create(src_path / item, pathlib.Path(dst).joinpath(item),
                           rewrite, verbose)


if __name__ == "__main__":
    lnmc()
