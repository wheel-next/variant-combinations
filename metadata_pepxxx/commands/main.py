# #!/usr/bin/env python3

import argparse
from importlib.metadata import entry_points

import metadata_pepxxx

def main():
    registered_commands = entry_points(group='metadata_pepxxx.actions')

    parser = argparse.ArgumentParser(prog="metadata_pepxxx")
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s version: {metadata_pepxxx.__version__}",
    )
    parser.add_argument(
        "command",
        choices=registered_commands.names,
    )
    parser.add_argument(
        "args",
        help=argparse.SUPPRESS,
        nargs=argparse.REMAINDER,
    )

    args = argparse.Namespace()
    parser.parse_args(namespace=args)

    main_fn = registered_commands[args.command].load()
    return main_fn(args.args)
