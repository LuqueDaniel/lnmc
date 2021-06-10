import pytest
from click.testing import CliRunner

import lnmc

from .helpers import DST, SRC, YAML_TEST_FILE, files_setup


@pytest.mark.parametrize("copy", ["--copy", "--no-copy", "--copy"])
def test_cli(files_setup, copy: str):
    """Test the full command."""
    runner = CliRunner()
    runner.invoke(
        lnmc.lnmc, [YAML_TEST_FILE, str(SRC), str(DST), copy, "--rewrite", "--verbose"]
    )
    directories = lnmc.yaml_read(YAML_TEST_FILE)

    for directory in directories:
        if not directories[directory]:
            for item in (SRC / directory).iterdir():
                assert (DST / item.name).exists()
            continue
        for item in directories[directory]:
            assert (DST / item).exists()
