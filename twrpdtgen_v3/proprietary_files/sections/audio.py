#
#
# Copyright (C) 2025 The LineageOS Project
# Copyright (C) 2025 xXHenneBXx
# SPDX-License-Identifier: Apache-2.0
#

from twrpdtgen_v3.proprietary_files.section import Section, register_section

class AudioSection(Section):
	name = "Audio"
	interfaces = [
		"android.hardware.audio",
		"android.hardware.audio.common",
		"android.hardware.audio.effect",
		"vendor.oplus.hardware.binaural_record",
		"vendor.oplus.hardware.virtual_device.audio",
		"vendor.qti.hardware.audiohalext",
	]
	hardware_modules = [
		"audio.binaural_record",
		"audio.primary",
		"audio.r_submix",
		"audio.usb",
		"audio.virtual",
	]
	properties_prefixes = {
		"aaudio.": False,
		"af.fast_track_multiplier": True,
		"audio.": False,
		"persist.audio.": False,
		"persist.vendor.audio.": False,
		"ro.audio.": False,
		"ro.qc.sdk.audio.": False,
		"ro.vendor.audio.": False,
		"tunnel.audio.": False,
		"use.voice.path.for.pcm.voip": True,
		"vendor.audio.": False,
		"vendor.audio_hal.": False,
		"vendor.voice.path.for.pcm.voip": True,
	}

class AudioFxModulesSection(Section):
	name = "Audio (FX modules)"
	folders = [
		"lib/soundfx",
		"lib64/soundfx",
	]

class AudioConfigsSection(Section):
	name = "Audio configs"
	filenames = [
		"audio_io_policy.conf",
		"audio_tuning_mixer.txt",
		"default_volume_tables.xml",
	]
	folders = [
		"etc/audio",
	]
	patterns = [
		"etc/audio_configs.*\.xml",
		"etc/audio_effects.*\.(conf|xml)",
		"etc/audio_platform_info.*\.xml",
		"etc/.*audio_policy.*\.xml",
		"etc/mixer_paths.*\.xml",
		"etc/sound_trigger_.*\.xml",
	]

class AudioCalibrationSection(Section):
	name = "Audio calibration"
	folders = [
		"etc/audio_param",
		"etc/lvacfs_params",
		"etc/smartpa_param",
		"etc/spatializer",
	]
	patterns = [
		"(.*/)?firmware/tfa98xx\..*",
	]

register_section(AudioSection)
register_section(AudioFxModulesSection)
register_section(AudioConfigsSection)
register_section(AudioCalibrationSection)
