#    Copyright Frank V. Castellucci
#    SPDX-License-Identifier: Apache-2.0

# -*- coding: utf-8 -*-

"""BCS to Json generator."""

import argparse
import ast
import inspect
import os
import pathlib
import sys

from pathlib import Path

PROJECT_DIR = pathlib.Path(os.path.dirname(__file__))
PARENT = PROJECT_DIR.parent

sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PARENT))
sys.path.insert(0, str(os.path.join(PARENT, "pysui")))


import pysui.sui.sui_common.bcstoj as ntree


def parse_args(
    in_args: list, default_folder: str, input_file_default: str
) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        add_help=True,
        usage="%(prog)s [options] command [--command_options]",
        description="",
    )
    parser.add_argument(
        "-i",
        "--input",
        dest="python_input_file",
        required=False,
        default=input_file_default,
        help=f"The Python input file containing BCS constructs to convert to JSON. Default to '{input_file_default}'",
    )
    parser.add_argument(
        "-t",
        "--target-folder",
        dest="target_output_folder",
        default=default_folder,
        required=False,
        help=f"The folder where the JSON output is written to. Default to '{default_folder}'",
    )
    return parser.parse_args(in_args)


def main():
    """Main execution for jtobcs."""
    res_path = Path(inspect.getfile(inspect.currentframe())).parent
    sample_file = res_path / "bcs_samp.py"

    args_parsed = parse_args(sys.argv[1:].copy(), os.getcwd(), str(sample_file))
    source_module = Path(args_parsed.python_input_file)
    if source_module.exists():
        pre_module: ast.Module = ast.parse(
            source_module.read_text(encoding="utf8"), source_module, "exec"
        )
        parse_tree: ntree.Tree = ntree.Tree("classes")
        decls = ntree.Declarations(parse_tree.root)
        decls.visit(pre_module)
        # Get the name of the tail of the input python module as the 'module' name in json
        fname = source_module.stem
        jstr = parse_tree.emit_json(fname)

        print(jstr)

        # fpath = res_path / f"{fname}.json"
        # fpath.write_text(jstr, encoding="utf8")
    else:
        raise ValueError(f"{source_module} does not exist.")


if __name__ == "__main__":
    main()
