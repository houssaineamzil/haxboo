import os
import shutil

from config.config import *
from utils.logger import Log


class Defaults:
	prefix = "?b "
	version = 1.0
	author = "houssaineamzil#4491"
	owner_id = None
	token = None
	# ? Colors
	colors = { }
	# ? Status
	statuses = [
		"with you!",
		"with Høussaine!",
		f"{prefix}help",
		"with humans!"
	]
	activity = "games!"
	activity_type = "playing" or "watching" or "listening" or "competing"
	status_type = "online" or "idle" or "dnd"
	# ? Logging
	debug = False
	logging_channel_id = None
	logging_time_format = None
	logging_date_format = None


class Config:
	def __init__(self):
		if not os.path.isfile("config/config.py"):
			if not os.path.isfile("config/config.py.example"):
				Log.critical(
					"There is no \"config.py.example\" file in the \"config\" folder! Please go to the GitHub repo and download "
					"it and then put it in the \"config\" folder!"
				)
				os._exit(1)
			else:
				shutil.copy("config/config.py.example", "config/config.py")
				Log.warning(
					"Created the \"config.py\" file in the config folder! Please edit the config and then run the bot again!"
				)
				os._exit(1)

		# ? Bot
		self.prefix = prefix or Defaults.prefix
		self.version = version or Defaults.version
		self.author = author or Defaults.author
		self.owner_id = owner_id or Defaults.owner_id
		self._token = token or Defaults.token
		# ? Colors
		self.colors = colors or Defaults.colors
		# ? Status
		self.statuses = statuses or Defaults.statuses
		self.activity = activity or Defaults.activity
		self.activity_type = activity_type or Defaults.activity_type
		self.status_type = status_type or Defaults.status_type
		# ? Logging
		self.debug = debug or Defaults.debug
		self.logging_channel_id = logging_channel_id or Defaults.logging_channel_id
		self.logging_time_format = logging_time_format or Defaults.logging_time_format
		self.logging_date_format = logging_date_format or Defaults.logging_date_format
		
		self.check()

	def check(self):
		if not self._token:
			Log.critical("No token was specified in the config, please put your bot's token in the config.")
			os._exit(1)

		if not self.owner_id:
			Log.critical("No owner ID was specified in the config, please put your ID for the owner ID in the config")
			os._exit(1)
