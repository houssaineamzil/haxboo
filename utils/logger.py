import codecs
import logging
import logging.handlers
import os
import sys
import time
import zipfile

import colorlog


debugging = False


class TimedCompressedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
	""" Extended version of TimedRotatingFileHandler that compress logs on rollover. """

	def doRollover(self):
		"""
		do a rollover; in this case, a date/time stamp is appended to the filename
		when the rollover happens.  However, you want the file to be named for the
		start of the interval, not the current time.  If there is a backup count,
		then we have to get a list of matching filenames, sort them and remove
		the one with the oldest suffix.
		"""

		self.stream.close()
		# get the time that this sequence started at and make it a TimeTuple
		t = self.rolloverAt - self.interval
		time_tuple = time.localtime(t)
		time_name = time.strftime(self.suffix, time_tuple)
		dfn = "logs/" + time_name + ".log"
		if os.path.exists(dfn):
			os.remove(dfn)
		os.rename(self.baseFilename, dfn)
		# print "%s -> %s" % (self.baseFilename, dfn)
		if self.encoding:
			self.stream = codecs.open(self.baseFilename, 'w', self.encoding)
		else:
			self.stream = open(self.baseFilename, 'w')
		self.rolloverAt = self.rolloverAt + self.interval
		if os.path.exists(dfn + ".zip"):
			os.remove(dfn + ".zip")
		file = zipfile.ZipFile(dfn + ".zip", "w")
		file.write(dfn, time_name + ".log", zipfile.ZIP_DEFLATED)
		file.close()
		os.remove(dfn)


class Log:
	def __init__(self):
		if len(logging.getLogger("").handlers) > 1:
			return

		shandler = logging.StreamHandler(stream = sys.stdout)
		shandler.setFormatter(
			colorlog.LevelFormatter(
				fmt = {
					"DEBUG": "{log_color}[{levelname}] {message}",
					"INFO": "{log_color}[{levelname}] {message}",
					"WARNING": "{log_color}[{levelname}] {message}",
					"ERROR": "{log_color}[{levelname}] {message}",
					"CRITICAL": "{log_color}[{levelname}] {message}"
				},
				log_colors = {
					"DEBUG": "cyan",
					"INFO": "white",
					"WARNING": "yellow",
					"ERROR": "red",
					"CRITICAL": "bold_red"
				},
				style = "{",
				datefmt = ""
			)
		)
		shandler.setLevel(logging.DEBUG)
		logging.getLogger(__package__).addHandler(shandler)
		logging.getLogger(__package__).setLevel(logging.DEBUG)
		self.setupRotator()

	@staticmethod
	def setupRotator(date_format = "%m-%d-%Y", time_format = "%H:%M:%S"):
		if not os.path.exists("logs"):
			os.mkdir("logs")
		rotator = TimedCompressedRotatingFileHandler("logs/latest.log", "d", 1, encoding = "UTF-8")
		rotator.setFormatter(
			logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", f"{date_format} {time_format}")
		)
		logging.getLogger(__package__).addHandler(rotator)

	@staticmethod
	def enableDebugging():
		global debugging
		debugging = True

	@staticmethod
	def debug(message: str):
		if debugging:
			logging.getLogger(__package__).debug(message)

	@staticmethod
	def info(message: str):
		logging.getLogger(__package__).info(message)

	@staticmethod
	def warning(message: str):
		logging.getLogger(__package__).warning(message)

	@staticmethod
	def error(message: str):
		logging.getLogger(__package__).error(message)

	@staticmethod
	def critical(message: str):
		logging.getLogger(__package__).critical(message)
