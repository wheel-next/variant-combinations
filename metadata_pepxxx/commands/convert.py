import argparse
import json
import logging
from pathlib import Path

import tomlkit

from metadata_pepxxx.variants_to_json import get_combinations

logger = logging.getLogger(__name__)


def convert(args) -> int:
    parser = argparse.ArgumentParser(prog="metadata_pepxxx convert")

    parser.add_argument(
        "-i",
        "--input_file",
        type=str,
        default=None,
        required=True,
        help="Variants.conf Source File.",
    )

    parser.add_argument(
        "-o",
        "--output_file",
        type=str,
        default=None,
        required=True,
        help="Path to save the converted file at.",
    )

    parser.add_argument(
        "-w",
        "--overwrite",
        action="store_true",
        help="Allow overwrite an already existing file.",
        default=False,
    )

    parser.add_argument(
        "-f",
        "--format",
        type=str,
        choices=["json"],
        required=True,
        help="Conversion format used.",
    )

    parsed_args = parser.parse_args(args)

    input_file = Path(parsed_args.input_file)
    if not input_file.exists():
        raise FileNotFoundError(f"Impossible to find: `{input_file}`.")

    output_file = Path(parsed_args.output_file)
    if output_file.exists() and not parsed_args.overwrite:
        raise FileExistsError(f"The file {output_file} already existing. "
                              "Please pass the flag `--overwrite` to ignore.")

    logger.info(f"Input File: `{input_file}`")
    logger.info(f"Output File: `{output_file}`")
    logger.info(f"Format: `{parsed_args.format}`")

    match parsed_args.format:

        case "json":
            export_conffile_to_json(input_file, output_file)

        case _:
            raise NotImplementedError(f"Unknown format: `{parsed_args.format=}`")

    return 0


def export_conffile_to_json(input_f: Path, output_f: Path) -> None:
    with input_f.open(mode="rb") as f:
        data = tomlkit.load(f)

    with output_f.open(mode="w") as outfile:
        json.dump(list(get_combinations(data)), outfile, indent=4)
