from click.testing import CliRunner
import filecmp
import os
import pathlib
import tempfile
from dokerc import dokerc


def test_info():
    runner = CliRunner()
    result = runner.invoke(dokerc.info)
    assert result.exit_code == 0
    assert "DokerC a small CLI client for the Doker Backend.\n" in result.output


def test_init_with_default_values():
    default_config = os.path.join(pathlib.Path.cwd(), "tests", "files", "config.ini")
    with tempfile.TemporaryDirectory() as dir:
        config_path = os.path.join(dir, "config.ini")
        runner = CliRunner()
        result = runner.invoke(
            dokerc.cli, ["init", "--config=" + config_path], input="\n\n\nTigger\n"
        )

        assert not result.exception
        assert os.path.exists(config_path)
        assert filecmp.cmp(config_path, default_config)
