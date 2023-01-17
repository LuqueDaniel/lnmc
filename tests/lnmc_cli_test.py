from pathlib import Path

import pytest
from click.testing import CliRunner

import lnmc

from .helpers import DST, YAML_TEST_FILE, create_test_tree


@pytest.mark.parametrize("copy", [True, False], ids=("copy", "symlink"))
def test_cli(create_test_tree, tmp_path: Path, copy: bool):
    """Test the full command."""
    args = [str(YAML_TEST_FILE), str(tmp_path), str(DST), "--rewrite", "--verbose"]
    if copy:
        args.append("--copy")
    runner = CliRunner()
    runner.invoke(lnmc.lnmc, args)

    directories = lnmc.yaml_read(YAML_TEST_FILE)
    for directory in directories:
        if not directories[directory]:
            assert Path(DST / f"dir_to_copy/file {directory}.txt").exists()
            continue
        for item in directories[directory]:
            assert Path(DST / item).exists()
