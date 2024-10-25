import shlex
import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from parameterized import parameterized

from metadata_pepxxx import __version__

ARTIFACT_FILES = [
    "tests/artifacts/variants1.conf",
    "tests/artifacts/variants2.conf",
    "tests/artifacts/variants3.conf",
    "tests/artifacts/variants4.conf",
]


class TestConvertVariantsCommand(unittest.TestCase):

    def setUp(self):
        self.cmd = "metadata_pepxxx convert"


    def run_command(self, command: str):
        return subprocess.run(  # noqa: S603
            shlex.split(command),
            capture_output=True,
            text=True,
            check=False,
        )

    @parameterized.expand(ARTIFACT_FILES)
    def test_valid_command(self, input_file):
        """Test the a valid command to ensure it works with success."""
        input_file = Path(input_file)

        with TemporaryDirectory() as tempdir:
            outfile = Path(tempdir) / "output.json"
            result = self.run_command(
                f"{self.cmd} --input_file={input_file} --output_file={outfile} "
                "--format json",
            )
            assert result.returncode == 0
            assert f"Input File: `{input_file}`" in result.stdout
            assert f"Output File: `{outfile}`" in result.stdout
            assert "Format: `json`" in result.stdout

    @parameterized.expand(ARTIFACT_FILES)
    def test_requires_overwrite_flag_command(self, input_file):
        """Test the a valid command to ensure it works with success."""
        input_file = Path(input_file)

        with TemporaryDirectory() as tempdir:
            outfile = Path(tempdir) / "output.json"
            result1 = self.run_command(
                f"{self.cmd} --input_file={input_file} --output_file={outfile} "
                "--format json",
            )
            assert result1.returncode == 0
            result2 = self.run_command(
                f"{self.cmd} --input_file={input_file} --output_file={outfile} "
                "--format json",
            )
            assert result2.returncode != 0
            assert "FileExistsError:" in result2.stderr
            assert "Please pass the flag `--overwrite` to ignore." in result2.stderr

    @parameterized.expand(ARTIFACT_FILES)
    def test_requires_format_flag_command(self, input_file):
        """Test the a valid command to ensure it works with success."""
        input_file = Path(input_file)

        with TemporaryDirectory() as tempdir:
            outfile = Path(tempdir) / "output.json"
            result = self.run_command(
                f"{self.cmd} --input_file={input_file} --output_file={outfile}",
            )
            assert result.returncode != 0
            assert "the following arguments are required: -f/--format" in result.stderr

    def test_file_doesnt_exist_command(self):
        """Test the version command to ensure it returns the correct version."""
        result = self.run_command(
            f"{self.cmd} --input_file=idontexist.conf --output_file=aa.json -f json",
        )
        assert result.returncode != 0
        assert "FileNotFoundError: Impossible to find" in result.stderr

    def test_invalid_command(self):
        """Test the behavior when an invalid command is provided."""
        result = self.run_command(
            f"{self.cmd} --input_file=idontexist.conf invalid_flag -o out.json -f json",
        )
        assert result.returncode != 0
        assert "unrecognized arguments: invalid_flag" in result.stderr

    def test_version_output(self):
        """Test the help command to ensure the help message is displayed."""
        result = self.run_command("metadata_pepxxx --version")
        assert result.returncode == 0
        assert result.stdout.strip() == f"metadata_pepxxx version: {__version__}"

    def test_help_output(self):
        """Test the help command to ensure the help message is displayed."""
        result = self.run_command("metadata_pepxxx --help")
        assert result.returncode == 0
        assert "usage: metadata_pepxxx [-h] [--version] {convert}" in result.stdout
        assert "-h, --help  show this help message and exit" in result.stdout
        assert "--version   show program's version number and exit" in result.stdout

    def test_help_convert_output(self):
        """Test the help command to ensure the help message is displayed."""
        result = self.run_command("metadata_pepxxx convert --help")
        assert result.returncode == 0
        assert "usage: metadata_pepxxx convert [-h]" in result.stdout
        assert "-i, --input_file INPUT_FILE" in result.stdout
        assert "-o, --output_file OUTPUT_FILE" in result.stdout
        assert "-w, --overwrite" in result.stdout
        assert "-f, --format {json}" in result.stdout


if __name__ == "__main__":
    unittest.main()
