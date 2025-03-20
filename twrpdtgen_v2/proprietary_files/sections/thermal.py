#
#
# Copyright (C) 2025 The LineageOS Project
# Copyright (C) 2025 xXHenneBXx
# SPDX-License-Identifier: Apache-2.0
#

from twrpdtgen_v3.proprietary_files.section import Section, register_section

class ThermalSection(Section):
	name = "Thermal"
	interfaces = [
		"android.hardware.thermal",
	]
	hardware_modules = [
		"thermal",
	]
	properties_prefixes = {
		"vendor.sys.thermal.": False,
	}

class ThermalQcomSection(Section):
	name = "Thermal (Qualcomm)"
	interfaces = [
		"vendor.qti.hardware.limits",
	]
	binaries = [
		"thermal-engine",
	]
	libraries = [
		"libthermalclient",
	]

class ThermalXiaomiSection(Section):
	name = "Thermal (Xiaomi)"
	binaries = [
		"mi_thermald",
	]

class ThermalConfigsSection(Section):
	name = "Thermal configs"
	folders = [
		"etc/temperature_profile"
	]
	patterns = [
		"etc/thermal.*.\.conf",
	]

register_section(ThermalSection)
register_section(ThermalQcomSection)
register_section(ThermalXiaomiSection)
register_section(ThermalConfigsSection)
