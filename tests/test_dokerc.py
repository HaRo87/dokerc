from click.testing import CliRunner
from dokerc import dokerc


def test_info():
    runner = CliRunner()
    result = runner.invoke(dokerc.info)
    assert result.exit_code == 0
    assert 'DokerC a small CLI client for the Doker Backend.\n' in result.output
