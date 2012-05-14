import tuned.plugins
import tuned.logs
import tuned.monitors
from tuned.plugins.decorator import *
import os
import struct
import glob

log = tuned.logs.get()

class AudioPlugin(tuned.plugins.Plugin):
	"""
	Plugin for tuning audio cards powersaving options.
	"""

	@classmethod
	def _get_default_options(cls):
		return {
			"ac97_powersave"      : None,
			"hda_intel_powersave" : None,
			"dynamic_tuning"      : False,
		}

	def cleanup(self):
		pass

	def update_tuning(self):
		pass

	def _ac97_powersave_file(self):
		return "/sys/module/snd_ac97_codec/parameters/power_save"

	@command_set("ac97_powersave")
	def _set_ac97_powersave(self, value):
		value = self._config_bool(value, "Y", "N")
		if value is None:
			log.warn("Incorrect ac97_powersave value.")
			return

		sys_file = self._ac97_powersave_file()
		if not os.path.exists(sys_file):
			return

		tuned.utils.commands.write_to_file(sys_file, value)

	@command_get("ac97_powersave")
	def _get_ac97_powersave(self, value):
		sys_file = self._ac97_powersave_file()
		if not os.path.exists(sys_file):
			return None
		return tuned.utils.commands.read_file(sys_file)

	def _hda_intel_powersave_file(self):
		return "/sys/module/snd_hda_intel/parameters/power_save"

	@command_set("hda_intel_powersave")
	def _set_hda_intel_powersave(self, value):
		sys_file = self._hda_intel_powersave_file()
		if not os.path.exists(sys_file):
			return
		tuned.utils.commands.write_to_file(sys_file, value)

	@command_get("hda_intel_powersave")
	def _revert_hda_intel_powersave(self, value):
		sys_file = self._hda_intel_powersave_file()
		if not os.path.exists(sys_file):
			return None
		return tuned.utils.commands.read_file(sys_file)