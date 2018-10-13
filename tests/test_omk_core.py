
from click.testing import CliRunner

from omk_core.cli import main
from omk_core import tonal_arithmetic as ta


def test_main():
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert result.output == '()\n'
    assert result.exit_code == 0

def test_tonal_arithmetic():
    pass
