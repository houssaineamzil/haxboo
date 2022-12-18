import asyncio
import os
import platform
import random
import subprocess
import sys
import time

import discord
import humanize
import nest_asyncio
import psutil
from discord.ext import commands, tasks

from utils import cache
from utils.config import Config
from utils.logger import Log

nest_asyncio.apply()

# The Main extensions.
extensions = [
    "main",
]

# The change.log.
change_log = []


class Bot(commands.AutoShardedBot):
    def __init__(self):
        self.config = Config()
        self.log = Log()
        self.process = psutil.Process()
        super().__init__(
            owner_id=self.config.owner_id,
            intents=discord.Intents.all(),
            command_attrs=dict(hidden=True),
            prefix=self.get_prefix,
            command_prefix=self.get_prefix,
            allowed_mentions=discord.AllowedMentions(
                roles=False,
                everyone=False
            ),
            fetch_offline_members=False,
            case_insensitive=True
        )

    # ? functions
    # This code sets up the status of the bot.
    @tasks.loop(minutes=5.0)
    async def presence_change(self):
        await self.change_presence(activity=discord.Game(random.choice(self.config.statuses)))

    # This code sets up the bot.
    async def setup(self):
        print(">>> running setup...")
        for extension in extensions:
            await self.load_extension(f"commands.{extension}")
            print(f"		| {extension} cog loaded")
        print(">>> setup complete.")

    # This code runs the bot.
    async def run(self):
        try:
            await self.setup()
            print(">>> running bot...")
            await super().start(
                self.config._token,
                reconnect=True
            )
        except Exception as e:
            self.log.error(f"Error when logging in: {e}")
            self.log.info(f'Restarting in 10s...')
            time.sleep(10)
            subprocess.call([sys.executable, "main.py"])

    # This code restarts the bot.
    async def _restart_bot(self):
        try:
            await self.logout()
            subprocess.call([sys.executable, "main.py"])
        except Exception:
            pass
            raise

    # This code shuts down the bot.
    async def _shutdown_bot(self):
        try:
            await self.logout()
        except Exception:
            pass
            raise

    # This code closes the 'aiohttp' session.
    async def _close(self):
        await super().close()

    # This code gets the prefix.
    @cache.cache()
    async def get_prefix(self, message):
        return commands.when_mentioned_or(*[self.config.prefix, ""])(self, message)

    # ? events
    # This code gets executed when the bot has successfully connected to Discord.
    async def on_connect(self):
        print(f">>> Connected!")

        self.presence_change.start()

    # This code gets executed when shard {x} has successfully connected to Discord.
    async def on_shard_connect(self, shard):
        print(f">>> Shard number {shard} is connected.")

    # This code gets executed when the bot has disconnected from Discord.
    async def on_disconnect(self):
        print(f"Bot disconnected")
        self.presence_change.cancel()
        await super().wait_until_ready()
        await asyncio.sleep(10)
        self.presence_change.start()

    # This code gets executed when shard {x} has disconnected from Discord.
    async def on_shard_disconnect(self, shard):
        print(f">>> Shard number {shard} is disconnected.")
        self.presence_change.cancel()
        await super().wait_until_ready()
        await asyncio.sleep(10)
        self.presence_change.start()

    # This code gets executed when the bot is done preparing the data received from Discord.
    async def on_ready(self):
        print(">>> syncing commands...")
        await bot.tree.sync()
        print(">>> syncing complete.")
        mem = self.process.memory_full_info()
        print("════════════════════════════════════════════════")
        print(f"Logged On As : {bot.user.id} / {bot.user}")
        print(f"Time : {time.asctime()}")
        print(f"RAM: Using {humanize.naturalsize(mem.rss)}")
        print(
            f"VRAM:{humanize.naturalsize(mem.vms)} of which {str(humanize.naturalsize(mem.uss))} is unique to this process"
        )
        print(
            f"Running on: {platform.system()} {platform.release()} ({os.name})"
        )
        print("════════════════════════════════════════════════")

    # This code gets executed when shard {x} is done preparing the data received from Discord.
    async def on_shard_ready(self, shard):
        print(f">>> Shard number {shard} is ready.")

    # This code gets executed when the bot has resumed a session.
    async def on_resumed(self):
        print(">>> Reconnected to discord!")

    # This code gets executed when shard {x} has resumed a session.
    async def on_shard_resumed(self, shard):
        print(f">>> Shard number {shard} is reconnected to discord!")

    # This code gets executed when an event raises an uncaught exception.
    async def on_error(self, error, *args, **kwargs):
        if error == "on_command_error":
            await args[0].send("Something went wrong.")

        raise

    # This code gets executed when a message is created and sent.
    async def on_message(self, message: discord.Message):
        if message.author == bot.user or message.author.bot:
            return

        await self.process_commands(message)

    # This code gets executed when an exception was raised
    async def on_command_error(self, context: commands.Context, error):
        if hasattr(context.command, 'on_error'):
            return
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.NoPrivateMessage):
            return await context.send(
                embed=discord.Embed(
                    color=self.config.colors["warning"],
                    description=await self.language.get(f"This command can only be ran on servers.", context)
                ),
                delete_after=15.0
            )
        if isinstance(context.channel, discord.DMChannel):
            return await context.send(
                embed=discord.Embed(
                    color=self.config.colors["warning"],
                    description=await self.language.get(
                        f"An error occurred while trying to run this command, this is most likely because it was ran in a private "
                        f"message channel. Please try running this command on a server.",
                        context
                    )
                ),
                delete_after=15.0
            )
        if isinstance(error, commands.MissingPermissions):
            return await context.send(
                embed=discord.Embed(
                    color=self.config.colors["warning"],
                    description=f"You can't use this command as you're missing the following permissions:\n"
                    f"`{', '.join(error.missing_permissions)}`.",
                ),
                delete_after=15.0
            )
        if isinstance(error, commands.BotMissingPermissions):
            return await context.send(
                embed=discord.Embed(
                    color=self.config.colors["warning"],
                    description=f"It seems I'm missing the following permissions for this command:\n"
                    f"`{', '.join(error.missing_permissions)}`.",
                ),
                delete_after=15.0
            )
        if isinstance(error, commands.NSFWChannelRequired):
            return await context.send(
                embed=discord.Embed(
                    color=self.config.colors["warning"],
                    description=f"NSFW commands can only be used in NSFW marked channels.",
                ).set_image(url="https://i.imgur.com/oe4iK5i.gif"),
                delete_after=15.0
            )
        if isinstance(error, commands.CommandOnCooldown):
            cool_time = int(error.retry_after)
            cool_time = bot.utilities.seconds2delta(cool_time)
            cool_time = bot.utilities.delta2string(cool_time)
            return await context.send(
                embed=discord.Embed(
                    color=self.config.colors["warning"],
                    description=f"[`{context.command.name}`]\nYou are on cooldown! Try again in **{cool_time}**.",
                ),
                delete_after=15.0
            )
        if isinstance(error, commands.CheckFailure):
            return await context.send(
                embed=discord.Embed(
                    color=self.config.colors["warning"],
                    description=f"You cannot use this command"
                ),
                delete_after=15.0
            )
        if isinstance(error, commands.DisabledCommand):
            return await context.send(
                embed=discord.Embed(
                    color=self.config.colors["warning"],
                    description=await self.language.get(f"This command has been disabled.", context)
                ),
                delete_after=15.0
            )
        
        # In case the bot failed to send a message to the channel, the try except pass statement is to prevent another
        # error
        try:
            return await context.send(
                embed=discord.Embed(
                    color=self.config.colors["warning"],
                    description=f"An error occurred while processing this command: `{error}`.",
                ),
                delete_after=15.0
            )
        except:
            pass

        self.log.error(
            f"An error occurred while executing the {context.command.qualified_name} command: {error}."
        )


bot = Bot()


# before invoke
@bot.before_invoke
async def before_invoke(context: commands.Context):
    await context.channel.typing()


# This code gets executed when preprocessing a command
@bot.before_invoke
async def on_command_preprocess(context: commands.Context):
    if isinstance(context.channel, discord.DMChannel):
        guild = "Private Message"
    else:
        guild = f"{context.guild.id}/{context.guild.name}"
    bot.log.info(
        f"[Command] [{guild}] [{context.author.id}/{context.author}]: {context.message.content}"
    )


# This code starts the bot
# bot.close()
# bot.run()
try:
    asyncio.run(bot.run())
except KeyboardInterrupt:
    asyncio.run(bot.close())
    # todo: cancel tasks
except Exception as e:
    bot.log.error(f"[ERROR] {e}")
finally:
    bot.log.warning("I'm going to sleep, master!")
