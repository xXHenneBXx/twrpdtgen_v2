# Copyright (C) 2025 The LineageOS Project
# Copyright (C) 2025 The xXHenneBXx
# Copyright (C) 2025 The SebaUbuntu
#
# SPDX-License-Identifier: Apache-2.0
#

from datetime import datetime
from os import chmod
from pathlib import Path
from sebaubuntu_libs.libandroid.device_info import DeviceInfo
from sebaubuntu_libs.libandroid.fstab import Fstab
from sebaubuntu_libs.libandroid.partitions.partitions import Partitions
from sebaubuntu_libs.libandroid.props import BuildProp
from sebaubuntu_libs.liblogging import LOGI
from sebaubuntu_libs.libpath import is_relative_to
from sebaubuntu_libs.libreorder import strcoll_files_key
from shutil import rmtree
from stat import S_IRWXU, S_IRGRP, S_IROTH

from twrpdtgen_v2.proprietary_files.proprietary_files_list import ProprietaryFilesList
from twrpdtgen_v2.templates import render_template
from twrpdtgen_v2.utils.boot_configuration import BootConfiguration
from twrpdtgen_v2.utils.format_props import dump_partition_build_prop

class DeviceTree:
	"""Class representing an Android device tree."""
	def __init__(self, path: Path):
		"""Given a path to a dumpyara dump path, generate a device tree by parsing it."""
		self.path = path

		self.current_year = str(datetime.now().year)

		LOGI("Figuring out partitions scheme")
		self.partitions = Partitions(self.path)

		self.system = self.partitions.system
		self.vendor = self.partitions.vendor

		LOGI("Parsing build props and device info")
		self.build_prop = BuildProp()
		for partition in self.partitions.get_all_partitions():
			self.build_prop.import_props(partition.build_prop)
		print(self.build_prop)
		self.device_info = DeviceInfo(self.build_prop)
		print(self.device_info)

		LOGI("Parsing fstab")
		fstabs = [
			file for file in self.vendor.files
			if (is_relative_to(file.relative_to(self.vendor.path), "etc")
		        and file.name.startswith("fstab."))
		]
		assert fstabs, "No fstab found"
		fstab = fstabs[0]
		self.fstab = Fstab(fstab)

		# Let the partitions know their fstab entries if any
		for partition in self.partitions.get_all_partitions():
			partition.fill_fstab_entry(self.fstab)

		LOGI("Extracting boot image")
		self.boot_configuration = BootConfiguration(self.path)

		LOGI("Getting list of rootdir files")
		self.rootdir_bin_files = [file for file in self.vendor.files
		                          if is_relative_to(file.relative_to(self.vendor.path), "bin")
		                          and file.suffix == ".sh"]
		self.rootdir_bin_files.sort(key=strcoll_files_key)

		self.rootdir_etc_files = [file for file in self.vendor.files
		                          if is_relative_to(file.relative_to(self.vendor.path), "etc/init/hw")]
		self.rootdir_etc_files.sort(key=strcoll_files_key)

		recovery_resources_location = (self.boot_configuration.recovery_aik_manager.ramdisk_path
		                               if self.boot_configuration.recovery_aik_manager
		                               else self.boot_configuration.boot_aik_manager.ramdisk_path)
		self.rootdir_recovery_etc_files = [file for file in recovery_resources_location.iterdir()
		                                   if is_relative_to(file.relative_to(recovery_resources_location), ".")
		                                   and file.suffix == ".rc"]
		self.rootdir_recovery_etc_files.sort(key=strcoll_files_key)

		LOGI("Generating proprietary files list")
		self.proprietary_files_list = ProprietaryFilesList(
			[value for value in self.partitions.get_all_partitions()]
		)

	def dump_to_folder(self, folder: Path):
		"""Dump all makefiles, blueprint and prebuilts to a folder."""
		if folder.is_dir():
			rmtree(folder)
		folder.mkdir(parents=True)

		# Makefiles/blueprints
		self._render_template(folder, "Android.bp", comment_prefix="//")
		self._render_template(folder, "Android.mk")
		self._render_template(folder, "AndroidProducts.mk")
		self._render_template(folder, "BoardConfig.mk")
		self._render_template(folder, "device.mk")
		self._render_template(folder, "extract-files.sh")
		self._render_template(folder, "twrp_device.mk", out_file=f"twrp_{self.device_info.codename}.mk")
		self._render_template(folder, "README.md")
		self._render_template(folder, "setup-makefiles.sh")

		# Set permissions
		chmod(folder / "extract-files.sh", S_IRWXU | S_IRGRP | S_IROTH)
		chmod(folder / "setup-makefiles.sh", S_IRWXU | S_IRGRP | S_IROTH)

		# Proprietary files list
		(folder / "proprietary-files.txt").write_text(
				self.proprietary_files_list.get_formatted_list(self.device_info.build_description))

		# Dump build props
		for partition in self.partitions.get_all_partitions():
			dump_partition_build_prop(partition.build_prop, folder / f"{partition.model.name}.prop")

		# Dump boot image prebuilt files
		prebuilts_path = folder / "prebuilts"
		prebuilts_path.mkdir()

		self.boot_configuration.copy_files_to_folder(prebuilts_path)

		# Dump rootdir
		rootdir_path = folder / "rootdir"
		rootdir_path.mkdir()

		self._render_template(rootdir_path, "rootdir_Android.bp", "Android.bp", comment_prefix="//")
		self._render_template(rootdir_path, "rootdir_Android.mk", "Android.mk")

		# rootdir/bin
		rootdir_bin_path = rootdir_path / "bin"
		rootdir_bin_path.mkdir()

		for file in self.rootdir_bin_files:
			(rootdir_bin_path / file.name).write_bytes(file.read_bytes())

		# rootdir/etc
		rootdir_etc_path = rootdir_path / "etc"
		rootdir_etc_path.mkdir()

		for file in self.rootdir_etc_files + self.rootdir_recovery_etc_files:
			(rootdir_etc_path / file.name).write_bytes(file.read_bytes())

		(rootdir_etc_path / self.fstab.fstab.name).write_text(self.fstab.format())

		# Manifest
		(folder / "manifest.xml").write_text(str(self.vendor.manifest))

	def cleanup(self) -> None:
		"""
		Cleanup all the temporary files.

		After you call this, you should throw away this object and never use it anymore.
		"""
		self.boot_configuration.cleanup()

	def _render_template(self, *args, comment_prefix: str = "#", **kwargs):
		return render_template(
			*args,
			boot_configuration=self.boot_configuration,
			comment_prefix=comment_prefix,
			current_year=self.current_year,
			device_info=self.device_info,
			fstab=self.fstab,
			rootdir_bin_files=self.rootdir_bin_files,
			rootdir_etc_files=self.rootdir_etc_files,
			rootdir_recovery_etc_files=self.rootdir_recovery_etc_files,
			partitions=self.partitions,
			**kwargs,
		)
