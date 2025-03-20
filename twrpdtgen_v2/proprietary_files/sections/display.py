#
#
# Copyright (C) 2025 The LineageOS Project
# Copyright (C) 2025 xXHenneBXx
# SPDX-License-Identifier: Apache-2.0
#

from twrpdtgen_v2.proprietary_files.section import Section, register_section

class DisplaySection(Section):
	name = "Display"
	interfaces = [
		"android.hardware.graphics.allocator",
		"android.hardware.graphics.bufferqueue",
		"android.hardware.graphics.common",
		"android.hardware.graphics.composer",
		"android.hardware.graphics.composer3",
		"android.hardware.graphics.mapper",
		"android.hardware.memtrack",
		"com.motorola.hardware.display.panel",
		"com.motorola.hardware.display.touch",
		"vendor.display.color",
		"vendor.display.config",
		"vendor.display.postproc",
		"vendor.mediatek.hardware.composer_ext",
		"vendor.mediatek.hardware.mms",
		"vendor.mediatek.hardware.pq",
		"vendor.oplus.hardware.displaycolorfeature",
		"vendor.oplus.hardware.displaypanelfeature",
		"vendor.qti.hardware.display.allocator",
		"vendor.qti.hardware.display.color",
		"vendor.qti.hardware.display.composer",
		"vendor.qti.hardware.display.config",
		"vendor.qti.hardware.display.mapper",
		"vendor.qti.hardware.display.mapperextensions",
		"vendor.qti.hardware.display.postproc",
		"vendor.qti.hardware.qdutils_disp",
		"vendor.xiaomi.hardware.displayfeature",
	]
	hardware_modules = [
		"copybit",
		"displayfeature",
		"displaypanel",
		"gralloc",
		"hwcomposer",
		"memtrack",
		"vulkan",
	]
	libraries = [
		"libsdedrm",
		"libsdm-color",
		"libsdm-diag",
		"libsdmextension",
	]
	folders = [
		"lib/egl",
		"lib64/egl",
	]
	properties_prefixes = {
		"debug.egl.": False,
		"debug.sf.": False,
		"persist.displayfeature.": False,
		"persist.sys.sf.": False,
		"persist.vendor.dc_backlight.": False,
		"persist.vendor.dfps.": False,
		"ro.gfx.driver.": False,
		"ro.hardware.egl": True,
		"ro.hardware.vulkan": True,
		"ro.hwui.": False,
		"ro.opengles.": False,
		"ro.surface_flinger.": False,
		"ro.vendor.cabc.": False,
		"ro.vendor.colorpick_adjust": True,
		"ro.vendor.dfps.": False,
		"ro.vendor.display.": False,
		"ro.vendor.fps.": False,
		"ro.vendor.hbm_backlight.": False,
		"ro.vendor.histogram.": False,
		"ro.vendor.mi_sf.": False,
		"ro.vendor.whitepoint_calibration_enable": True,
		"vendor.display.": False,
		"vendor.gralloc.": False,
	}

class DisplayPixelworksSection(Section):
	name = "Display (Pixelworks)"
	interfaces = [
		"vendor.pixelworks.hardware.display",
		"vendor.pixelworks.hardware.display.iris",
		"vendor.pixelworks.hardware.feature",
		"vendor.pixelworks.hardware.feature.irisfeature",
	]
	patterns = [
		"(.*/)?firmware/pxlw_.*\..*",
	]

class DisplayConfigsSection(Section):
	name = "Display configs"
	folders = [
		"etc/display",
		"etc/inparm",
	]
	patterns = [
		"etc/ltm_*",
		"etc/mdss_*",
		"etc/qdcm_*",
	]

class DisplayFirmwareSection(Section):
	name = "Display firmware"
	folders = [
		"gpu/kbc",
	]
	patterns = [
		"(.*/)?firmware/a[0-9]+_.*\..*",
		"(.*/)?firmware/iris.*\..*",
	]

register_section(DisplaySection)
register_section(DisplayPixelworksSection)
register_section(DisplayConfigsSection)
register_section(DisplayFirmwareSection)
