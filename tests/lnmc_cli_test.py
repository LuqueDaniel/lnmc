import pytest
from click.testing import CliRunner

import lnmc

from .helpers import DST, SRC, YAML_TEST_FILE, files_setup


@pytest.mark.parametrize("copy", [True, False])
def test_cli(files_setup, copy: bool):
    """Test the full command."""
    runner = CliRunner()
    args = [str(YAML_TEST_FILE), str(SRC), str(DST), "--rewrite", "--verbose"]
    if copy:
        args.append("--copy")
    runner.invoke(lnmc.lnmc, args)
    directories = lnmc.yaml_read(YAML_TEST_FILE)

    for directory in directories:
        if not directories[directory]:
            for item in (SRC / directory).iterdir():
                assert (DST / item.name).exists()
            continue
        for item in directories[directory]:
            assert (DST / item).exists()
