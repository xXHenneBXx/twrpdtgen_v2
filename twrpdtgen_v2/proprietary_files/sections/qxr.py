#
#
# Copyright (C) 2025 The LineageOS Project
# Copyright (C) 2025 xXHenneBXx
# SPDX-License-Identifier: Apache-2.0
#

from twrpdtgen_v2.proprietary_files.section import Section, register_section

class QxrSection(Section):
	name = "QXR"
	interfaces = [
		"vendor.qti.hardware.qxr",
	]

register_section(QxrSection)
