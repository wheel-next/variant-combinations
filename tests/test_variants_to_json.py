import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from parameterized import parameterized_class

from metadata_pepxxx.commands.convert import export_conffile_to_json


def hash_file(file_path: Path):
    """Calculate the SHA-256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    with file_path.open(mode="rb") as f:
        # Read the file in chunks to avoid loading large files into memory
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


@parameterized_class([
    {"filepath": "tests/artifacts/variants1.conf"},
    {"filepath": "tests/artifacts/variants2.conf"},
    {"filepath": "tests/artifacts/variants3.conf"},
    {"filepath": "tests/artifacts/variants4.conf"},
])
class ConvertVariantsConfFileTest(unittest.TestCase):

    def setUp(self) -> None:
        self._file = Path(self.filepath)
        if not self._file.exists():
            raise FileNotFoundError(f"File not found: `{self._file}`")  # noqa: EM102, TRY003

    def test_export_to_json(self):

        with tempfile.TemporaryDirectory() as tempdir:
            outfile = Path(tempdir) / "output.json"

            export_conffile_to_json(self._file, outfile)

            with outfile.open() as f:
                json_converted = json.load(f)

            target_json_f = Path(str(self._file)[:-4] + "json")
            with target_json_f.open() as f:
                json_target = json.load(f)

            assert json_converted == json_target
            assert hash_file(outfile) == hash_file(target_json_f)


if __name__ == "__main__":
    unittest.main()
