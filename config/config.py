from dotenv import load_dotenv
load_dotenv()

import os

#
# ? Bot
# This is the prefix for the bot


prefix = "?b "

# This is the version of the bot
version = 1.0

# This is the author of the bot
author = "houssaineamzil#4491"

# Put your user ID here
owner_id = 736533260263489587

# If you do not know what your token is, you can get it on your bot's control panel page on
# https://discordapp.com/developers/applications/me
token = os.environ.get("DISCORD_TOKEN")

# ? Colors
colors = {
	"main": 0xF9FAFB,
	"info": 0x60A5FA,
	"success": 0x4ADE80,
	"warning": 0xFBBF24,
	"error": 0xF87171,
}

# ? Status
# default status messages
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
# Debug the bot? Setting this to yes will debug things by logging them with a [DEBUG] prefix.
debug = False

# The channel ID to log certain things to a channel
logging_channel_id = 874247382169178172

# H = Hour, M = Minute, S = Second
logging_time_format = "%H:%M:%S"

# m = Month, d = Day, Y = Year
logging_date_format = "%m-%d-%Y"
