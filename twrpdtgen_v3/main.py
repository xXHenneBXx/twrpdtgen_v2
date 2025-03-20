# Copyright (C) 2025 The LineageOS Project
# Copyright (C) 2025 The xXHenneBXx
# Copyright (C) 2025 The SebaUbuntu
#
# SPDX-License-Identifier: Apache-2.0
#

from argparse import ArgumentParser
from pathlib import Path
from sebaubuntu_libs.liblocale import setup_locale
from sebaubuntu_libs.liblogging import setup_logging

from twrpdtgen_v3 import __version__ as version, current_path
from twrpdtgen_v3.device_tree import DeviceTree

def main():
	setup_logging()

	print(f"TWRP device tree generator\n"
	      f"Version {version}\n")

	parser = ArgumentParser(prog='python3 -m twrpdtgen_v3')
	parser.add_argument("dump_path", type=Path,
	                    help="path to an Android dump made with dumpyara")
	parser.add_argument("-o", "--output", type=Path, default=current_path / "output",
	                    help="custom output folder")

	args = parser.parse_args()

	setup_locale()

	dump = DeviceTree(args.dump_path)
	dump.dump_to_folder(args.output)
	dump.cleanup()

	print(f"\nDone! You can find the device tree in {str(args.output)}")
