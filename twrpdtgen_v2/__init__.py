# Copyright (C) 2025 The LineageOS Project
# Copyright (C) 2025 The xXHenneBXx
# Copyright (C) 2025 The SebaUbuntu
#
# SPDX-License-Identifier: Apache-2.0
#
"""twrpdtgen_v2 module."""

from pathlib import Path

from twrpdtgen_v2.proprietary_files.section import register_sections

__version__ = "2.0.5"

module_path = Path(__file__).parent
sections_path = module_path / "proprietary_files" / "sections"
current_path = Path.cwd()

register_sections(sections_path)
