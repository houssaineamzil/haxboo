import asyncio
import math
import random
import time
from typing import Union
from assets.guessword import wordList
from assets.eightball import eightball
import aiohttp
import discord
from discord.ext import commands

from utils.config import Config


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config()

    @commands.command()
    async def ping(self, context: commands.Context):
        """
        Get the bot's current websocket and API latency.
        """
        # delete user's message to keep the channels clean.
        await context.message.delete()

        try:
            start_time = time.time()
            message = await context.send(
                embed=discord.Embed(
                    description=f"Testing Ping..."
                )
            )
            end_time = time.time()

            await message.edit(
                embed=discord.Embed(
                    description=f"Pong! {round(self.bot.latency * 1000)}ms\n"
                    f"API: {round((end_time - start_time) * 1000)}ms"
                )
            )

            # todo: remove this later.
            # await context.send(
            #     embed=discord.Embed(
            #         color=self.config.colors["warning"],
            #         description=f"This command is currently under development, and it's not working right now. Please check it out later!"
            #     )
            # )

        except Exception as exception:
            print(exception)

    @commands.command(name="8ball")
    async def eightball(self, context: commands.Context, *, question: str):
        """
        Get the bot's current websocket and API latency.
        """
        # delete user's message to keep the channels clean.

        try:
            answer = random.choice(eightball)

            await context.message.reply(
                embed=discord.Embed(
                    description=f"> {question}\n"
                    f"> **{answer}**"
                ),
                delete_after=17.5
            )
            await context.message.delete()

        except Exception as exception:
            print(exception)

    @commands.command()
    async def joke(self, context: commands.Context):
        """
        Sends a Dad Joke!
        """
        # delete user's message to keep the channels clean.
        await context.message.delete()

        try:
            headers = {"Accept": "application/json"}
            async with aiohttp.ClientSession() as aiosession:
                async with aiosession.get("https://icanhazdadjoke.com", headers=headers) as get:
                    assert isinstance(get, aiohttp.ClientResponse)
                    response = await get.json()
                await aiosession.close()

            return await context.send(
                embed=discord.Embed(
                    description=response["joke"]
                ),
                delete_after=17.5
            )

        except Exception as exception:
            print(exception)

    @commands.command()
    async def wheel(self, context: commands.Context):
        """
        Sends a Dad Joke!
        """
        # delete user's message to keep the channels clean.
        await context.message.delete()

        try:
            # todo: remove this later.
            return await context.send(
                embed=discord.Embed(
                    color=self.config.colors["warning"],
                    description=f"This command is currently under development, and it's not working right now. Please check it out later!"
                )
            )

        except Exception as exception:
            print(exception)

    @commands.command()
    async def flip(self, context: commands.Context):
        """
        View your work stars.
        """
        # delete user's message to keep the channels clean.
        await context.message.delete()

        try:
            async def download_image(source, savepath):
                async with aiohttp.ClientSession() as aiosession:
                    async with aiosession.get(source) as response:
                        if response.status == 200:
                            response = await response.read()
                            with open(savepath, "wb") as file:
                                file.write(response)
                    await aiosession.close()

            await download_image("https://i.imgur.com/sq6ZDOx.png", "assets/flip/heads.png")
            await download_image("https://i.imgur.com/N5ixRZI.png", "assets/flip/tails.png")

            message = await context.send(
                embed=discord.Embed(
                    description=f"choose a face (`heads` or `tails`)!\n"
                )
            )

            choice = await self.bot.wait_for("message", check=lambda response: response.author == context.message.author)
            choice = choice.content
            choice = choice.lower().strip()
            choice = "none" if choice not in ["heads", "tails"] else choice

            pick = random.choice(
                [
                    ("assets/flip/heads.png", "Heads!"),
                    ("assets/flip/tails.png", "Tails!")
                ]
            )
            link = pick[0]
            text = pick[1]
            files = [discord.File(link, 'coin.png')]

            if choice == "none":
                return await message.edit(
                    embed=discord.Embed(
                        description=f"I only accept `heads` or `tails` as answers"
                    ),
                    delete_after=7.5
                )

            if choice == "heads":
                if pick[1] == "Heads!":
                    return await message.edit(
                        embed=discord.Embed(
                            description=f"🎉 Good job you guessed it right!\n"
                            f"It's {text}"
                        ),
                        attachments=files,
                        delete_after=7.5
                    )
                else:
                    return await message.edit(
                        embed=discord.Embed(
                            description=f"😑 Pfff you dumbass!\n"
                            f"It's {text}"
                        ),
                        attachments=files,
                        delete_after=7.5
                    )
            if choice == "tails":
                if pick[1] == "Tails!":
                    return await message.edit(
                        embed=discord.Embed(
                            description=f"🎉 Good job you guessed it right!\n"
                            f"It's {text}"
                        ),
                        attachments=files,
                        delete_after=7.5
                    )
                else:
                    return await message.edit(
                        embed=discord.Embed(
                            description=f"😑 Pfff you dumbass!\n"
                            f"It's {text}"
                        ),
                        attachments=files,
                        delete_after=7.5
                    )

            # todo: remove this later.
            # await context.send(
            #     embed=discord.Embed(
            #         color=self.config.colors["warning"],
            #         description=f"This command is currently under development, and it's not working right now. Please check it out later!"
            #     )
            # )

        except Exception as exception:
            print(exception)

    @commands.command()
    async def slots(self, context: commands.Context):
        """
        View your work stars.
        """
        # delete user's message to keep the channels clean.
        await context.message.delete()

        try:
            emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"

            message = await context.send(
                embed=discord.Embed(
                    description=f"**| 🍇 | 🍇 | 🍇 |**"
                )
            )

            for i in range(5):
                a, b, c = [random.choice(emojis) for g in range(3)]
                await message.edit(
                    embed=discord.Embed(
                        description=f"**| {a} | {b} | {c} |**"
                    ),
                    delete_after=7.5
                )

            if a == b == c:
                await context.send(
                    embed=discord.Embed(
                        description=f"All matching, you won! 🎉"
                    ),
                    delete_after=7.5
                )
            elif (a == b) or (a == c) or (b == c):
                await context.send(
                    embed=discord.Embed(
                        description=f"2 in a row, you won! 🎉"
                    ),
                    delete_after=7.5
                )
            else:
                await context.send(
                    embed=discord.Embed(
                        description=f"No match, you lost! 😢"
                    ),
                    delete_after=7.5
                )

        except Exception as exception:
            print(exception)

    @commands.group()
    async def guess(self, context: commands.Context):
        """
        View your work stars.
        """
        # delete user's message to keep the channels clean.
        if context.invoked_subcommand is None:
            await context.message.delete()

            try:
                return await context.send_help(str(context.command))

            except Exception as exception:
                print(exception)

    @guess.command(name="word")
    async def guess_word(self, context: commands.Context):
        """
        View your work stars.
        """
        # delete user's message to keep the channels clean.
        await context.message.delete()

        try:
            word = random.choice(wordList)
            # todo fix this
            # shuffled = ("").join(list(word).sort(function () { return 0.5 - Math.random() }));
            shuffled = ''.join(random.sample(word, len(word)))
            # shuffled = word

            # todo: add three button to geuss the true word
            message = await context.send(
                embed=discord.Embed(
                    description=f"Guess the word!\n"
                    f"> **{shuffled}**"
                ),
            )

            answer = await self.bot.wait_for("message", check=lambda response: response.author == context.message.author)
            answer = answer.content
            answer = answer.lower().strip()

            if answer == word:
                return await message.edit(
                    embed=discord.Embed(
                        description=f"🎉 Good job you guessed it right!\n"
                        f"It's **{word}**"
                    ),
                    delete_after=7.5
                )
            if answer != word:
                return await message.edit(
                    embed=discord.Embed(
                        description=f"😑 Pfff you dumbass!\n"
                        f"You can't even guess **{word}**"
                    ),
                    delete_after=7.5
                )

            # todo: remove this later.
            return await context.send(
                embed=discord.Embed(
                    color=self.config.colors["warning"],
                    description=f"This command is currently under development, and it's not working right now. Please check it out later!"
                )
            )

        except Exception as exception:
            print(exception)

    @guess.command(name="number")
    async def guess_number(self, context: commands.Context):
        """
        View your work stars.
        """
        # delete user's message to keep the channels clean.
        await context.message.delete()

        try:
            numbers = [int(random.randint(0, 9999)) for i in range(4)]
            number = numbers[random.randint(0, 3)]

            # todo: add four button to geuss the right number
            message = await context.send(
                embed=discord.Embed(
                    description=f"Guess the number!\n"
                    f"options:\n"
                    f"> **{numbers[0]}**\n"
                    f"> **{numbers[1]}**\n"
                    f"> **{numbers[2]}**\n"
                    f"> **{numbers[3]}**"
                ),
                delete_after=10
            )

            answer = await self.bot.wait_for("message", check=lambda response: response.author == context.message.author)
            answer = answer.content
            answer = answer.lower().strip()

            if answer == number:
                return await message.edit(
                    embed=discord.Embed(
                        description=f"🎉 Good job you guessed it right!\n"
                        f"It's **{number}**"
                    ),
                    delete_after=7.5
                )
            if answer != number:
                return await message.edit(
                    embed=discord.Embed(
                        description=f"😑 Pfff you dumbass!\n"
                        f"You can't even guess **{number}**"
                    ),
                    delete_after=7.5
                )

        except Exception as exception:
            print(exception)

    @commands.command()
    async def highlow(self, context: commands.Context):
        """
        View your work stars.
        """
        # delete user's message to keep the channels clean.
        await context.message.delete()

        try:
            number2 = random.randint(0, 9999)
            # todo fix this

            # todo: add three button to geuss the true word
            await context.send(
                embed=discord.Embed(
                    description=f"Guess higher or lower!\n"
                    f"> **{number2}**"
                ),
                delete_after=7.5
            )

            answer = await self.bot.wait_for("message", check=lambda response: response.author == context.message.author)
            answer = answer.content
            answer = answer.lower().strip()
            answer = "none" if answer not in ["higher", "lower"] else answer
            number = random.randint(0, 9999)

            if answer == "none":
                await context.send(
                    embed=discord.Embed(
                        description=f"I only accept `higher` or `lower` as answers"
                    ),
                    delete_after=7.5
                )

            if answer == "higher":
                if number >= number2:
                    await context.send(
                        embed=discord.Embed(
                            description=f"🎉 Good job you guessed it right!\n"
                            f"**{number}** is higher than **{number2}**"
                        ),
                        delete_after=7.5
                    )
                else:
                    await context.send(
                        embed=discord.Embed(
                            description=f"😑 Pfff you dumbass!\n"
                            f"**{number}** is not higher than **{number2}**"
                        ),
                        delete_after=7.5
                    )
            if answer == "lower":
                if number <= number2:
                    await context.send(
                        embed=discord.Embed(
                            description=f"🎉 Good job you guessed it right!\n"
                            f"**{number}** is lower than **{number2}**"
                        ),
                        delete_after=7.5
                    )
                else:
                    await context.send(
                        embed=discord.Embed(
                            description=f"😑 Pfff you dumbass!\n"
                            f"**{number}** is not lower than **{number2}**"
                        ),
                        delete_after=7.5
                    )

        except Exception as exception:
            print(exception)

    @commands.command()
    async def blackjack(self, context: commands.Context):
        """
        View your work stars.
        """
        # delete user's message to keep the channels clean.
        await context.message.delete()

        try:
            # todo: remove this later.
            return await context.send(
                embed=discord.Embed(
                    color=self.config.colors["warning"],
                    description=f"This command is currently under development, and it's not working right now. Please check it out later!"
                )
            )

        except Exception as exception:
            print(exception)

    @commands.command()
    async def roulette(self, context: commands.Context, space: Union[str, int]):
        """
        View your work stars.
        """
        # delete user's message to keep the channels clean.
        await context.message.delete()

        try:
            first, second, third = ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34'], [
                '2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35'], ['3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36']
            slots = {'00': 'green', '0': 'green', '1': 'red', '2': 'black', '3': 'red', '4': 'black', '5': 'red', '6': 'black', '7': 'red', '8': 'black', '9': 'red', '10': 'black', '11': 'black', '12': 'red', '13': 'black', '14': 'red', '15': 'black', '16': 'red', '17': 'black',
                     '18': 'red', '19': 'red', '20': 'black', '21': 'red', '22': 'black', '23': 'red', '24': 'black', '25': 'red', '26': 'black', '27': 'red', '28': 'black', '29': 'black', '30': 'red', '31': 'black', '32': 'red', '33': 'black', '34': 'red', '35': 'black', '36': 'red'}

            # check space
            if space.lower() not in ["odd", "even", "black", "red", "1st", "2nd", "3rd", "first", "second", "third", "1-12", "13-24", "25-36", "1-18", "19-36"]:
                try:
                    space = int(space)
                    if not (space > 0 and space < 36):
                        return await context.send(
                            embed=discord.Embed(
                                description=f"Incorrect space type!"
                            )
                        )

                except Exception as exception:
                    print(exception)

            # get space type
            spaceType = "string"
            try:
                space = int(space)
                spaceType = "int"
            except:
                space = str(space)

            # spinning
            await context.send(
                embed=discord.Embed(
                    description=f"You have placed your bet on `{space}`."
                )
            )
            await context.send(
                embed=discord.Embed(
                    description=f"Spinning..."
                ),
                delete_after=1
            )

            multiplicator = None

            if space in ["odd", "even", "black", "red", "1-18", "19-36"]:
                multiplicator = 2
            elif str(space).lower() in ["1st", "2nd", "3rd", "first", "second", "third", "1-12", "13-24", "25-36"]:
                multiplicator = 3
            elif spaceType == "int":
                multiplicator = 35

            result = random.choice(list(slots.keys()))

            if str(space).lower() == "black" and slots[result] == "black":
                return await context.send(
                    embed=discord.Embed(
                        description=f"🎉 Good job you did it! **X{str(multiplicator)}**\n"
                        f"You choose `{space}` the ball landed on: `{slots[result]} {result}`!"
                    ),
                    delete_after=7.5
                )
            if str(space).lower() == "red" and slots[result] == "red":
                return await context.send(
                    embed=discord.Embed(
                        description=f"🎉 Good job you did it! **X{str(multiplicator)}**\n"
                        f"You choose `{space}` the ball landed on: `{slots[result]} {result}`!"
                    ),
                    delete_after=7.5
                )

            if str(space).lower() == "even" and (int(result) % 2) == 0:
                return await context.send(
                    embed=discord.Embed(
                        description=f"🎉 Good job you did it! **X{str(multiplicator)}**\n"
                        f"You choose `{space}` the ball landed on: `{slots[result]} {result}`!"
                    ),
                    delete_after=7.5
                )
            if str(space).lower() == "odd" and (int(result) % 2) != 0:
                return await context.send(
                    embed=discord.Embed(
                        description=f"🎉 Good job you did it! **X{str(multiplicator)}**\n"
                        f"You choose `{space}` the ball landed on: `{slots[result]} {result}`!"
                    ),
                    delete_after=7.5
                )

            if str(space).lower() in ["first", "1st"] and str(result) in first:
                return await context.send(
                    embed=discord.Embed(
                        description=f"🎉 Good job you did it! **X{str(multiplicator)}**\n"
                        f"You choose `{space}` the ball landed on: `{slots[result]} {result}`!"
                    ),
                    delete_after=7.5
                )
            if str(space).lower() in ["second", "2nd"] and str(result) in second:
                return await context.send(
                    embed=discord.Embed(
                        description=f"🎉 Good job you did it! **X{str(multiplicator)}**\n"
                        f"You choose `{space}` the ball landed on: `{slots[result]} {result}`!"
                    ),
                    delete_after=7.5
                )
            if str(space).lower() in ["third", "3rd"] and str(result) in third:
                return await context.send(
                    embed=discord.Embed(
                        description=f"🎉 Good job you did it! **X{str(multiplicator)}**\n"
                        f"You choose `{space}` the ball landed on: `{slots[result]} {result}`!"
                    ),
                    delete_after=7.5
                )

            if str(space).lower() == "1-12" and int(result) in range(1, 13):
                return await context.send(
                    embed=discord.Embed(
                        description=f"🎉 Good job you did it! **X{str(multiplicator)}**\n"
                        f"You choose `{space}` the ball landed on: `{slots[result]} {result}`!"
                    ),
                    delete_after=7.5
                )
            if str(space).lower() == "13-24" and int(result) in range(13, 25):
                return await context.send(
                    embed=discord.Embed(
                        description=f"🎉 Good job you did it! **X{str(multiplicator)}**\n"
                        f"You choose `{space}` the ball landed on: `{slots[result]} {result}`!"
                    ),
                    delete_after=7.5
                )
            if str(space).lower() == "25-36" and int(result) in range(25, 37):
                return await context.send(
                    embed=discord.Embed(
                        description=f"🎉 Good job you did it! **X{str(multiplicator)}**\n"
                        f"You choose `{space}` the ball landed on: `{slots[result]} {result}`!"
                    ),
                    delete_after=7.5
                )
            if str(space).lower() == "1-18" and int(result) in range(1, 19):
                return await context.send(
                    embed=discord.Embed(
                        description=f"🎉 Good job you did it! **X{str(multiplicator)}**\n"
                        f"You choose `{space}` the ball landed on: `{slots[result]} {result}`!"
                    ),
                    delete_after=7.5
                )
            if str(space).lower() == "19-36" and int(result) in range(19, 37):
                return await context.send(
                    embed=discord.Embed(
                        description=f"🎉 Good job you did it! **X{str(multiplicator)}**\n"
                        f"You choose `{space}` the ball landed on: `{slots[result]} {result}`!"
                    ),
                    delete_after=7.5
                )

            if spaceType == "int" and int(space) == int(result):
                return await context.send(
                    embed=discord.Embed(
                        description=f"🎉 Good job you did it! **X{str(multiplicator)}**\n"
                        f"You choose `{space}` the ball landed on: `{slots[result]} {result}`!"
                    ),
                    delete_after=7.5
                )

            else:
                return await context.send(
                    embed=discord.Embed(
                        description=f"😑 Pfff you dumbass!\n"
                        f"You choose `{space}` the ball landed on: `{slots[result]} {result}`!"
                    ),
                    delete_after=7.5
                )

        except Exception as exception:
            print(exception)

    @commands.command()
    async def dice(self, context: commands.Context):
        """
        Get the bot's current websocket and API latency.
        """
        # delete user's message to keep the channels clean.
        await context.message.delete()

        try:
            message = await context.send(
                embed=discord.Embed(
                    description=f"Rolling the dices 🎲..."
                )
            )

            bot_dice = random.randint(1, 6)
            user_dice = random.randint(1, 6)

            if user_dice > bot_dice:
                await message.edit(
                    embed=discord.Embed(
                        description=f"🎉 Good job you won 😒!\n"
                        f"You got `{user_dice}` and I got `{bot_dice}`!"
                    ),
                    delete_after=7.5
                )

            if user_dice == bot_dice:
                await message.edit(
                    embed=discord.Embed(
                        description=f"😑 Pfff You got lucky this time!\n"
                        f"You got `{user_dice}` and I got `{bot_dice}`!"
                    ),
                    delete_after=7.5
                )

            if user_dice < bot_dice:
                await message.edit(
                    embed=discord.Embed(
                        description=f"😑 Pfff you dumbass!\n"
                        f"You got `{user_dice}` and I got `{bot_dice}`!"
                    ),
                    delete_after=7.5
                )

        except Exception as exception:
            print(exception)

    @commands.command()
    async def rps(self, context: commands.Context):
        """
        Get the bot's current websocket and API latency.
        """
        # delete user's message to keep the channels clean.
        await context.message.delete()

        try:
            await context.send(
                embed=discord.Embed(
                    description=f"Choose your weapon! (`rock`, `paper` or `scissors`)"
                ),
                delete_after=7.5
            )

            choice = await self.bot.wait_for("message", check=lambda response: response.author == context.message.author)
            choice = choice.content
            choice = choice.lower().strip()
            choice = "none" if choice not in [
                "rock", "paper", "scissors"] else choice

            bot_choice = random.choice(["rock", "paper", "scissors"])

            if choice == "none":
                return await context.send(
                    embed=discord.Embed(
                        description=f"I only accept `rock`, `paper` or `scissors` as a weapon"
                    ),
                    delete_after=7.5
                )

            if choice == "rock":
                if bot_choice == "rock":
                    await context.send(
                        embed=discord.Embed(
                            description=f"😑 You got lucky this time!\n"
                            f"You choose `{choice}` and I choose `{bot_choice}`!"
                        ),
                        delete_after=7.5
                    )
                if bot_choice == "paper":
                    await context.send(
                        embed=discord.Embed(
                            description=f"😑 Pfff you dumbass, you lost!\n"
                            f"You choose `{choice}` and I choose `{bot_choice}`!"
                        ),
                        delete_after=7.5
                    )
                if bot_choice == "scissors":
                    await context.send(
                        embed=discord.Embed(
                            description=f"🎉 Good job you won 😒!\n"
                            f"You choose `{choice}` and I choose `{bot_choice}`!"
                        ),
                        delete_after=7.5
                    )
            if choice == "paper":
                if bot_choice == "rock":
                    await context.send(
                        embed=discord.Embed(
                            description=f"🎉 Good job you won 😒!\n"
                            f"You choose `{choice}` and I choose `{bot_choice}`!"
                        ),
                        delete_after=7.5
                    )
                if bot_choice == "paper":
                    await context.send(
                        embed=discord.Embed(
                            description=f"😑 You got lucky this time!\n"
                            f"You choose `{choice}` and I choose `{bot_choice}`!"
                        ),
                        delete_after=7.5
                    )
                if bot_choice == "scissors":
                    await context.send(
                        embed=discord.Embed(
                            description=f"😑 Pfff you dumbass, you lost!\n"
                            f"You choose `{choice}` and I choose `{bot_choice}`!"
                        ),
                        delete_after=7.5
                    )
            if choice == "scissors":
                if bot_choice == "rock":
                    await context.send(
                        embed=discord.Embed(
                            description=f"😑 Pfff you dumbass, you lost!\n"
                            f"You choose `{choice}` and I choose `{bot_choice}`!"
                        ),
                        delete_after=7.5
                    )
                if bot_choice == "paper":
                    await context.send(
                        embed=discord.Embed(
                            description=f"🎉 Good job you won 😒!\n"
                            f"You choose `{choice}` and I choose `{bot_choice}`!"
                        ),
                        delete_after=7.5
                    )
                if bot_choice == "scissors":
                    await context.send(
                        embed=discord.Embed(
                            description=f"😑 You got lucky this time!\n"
                            f"You choose `{choice}` and I choose `{bot_choice}`!"
                        ),
                        delete_after=7.5
                    )

        except Exception as exception:
            print(exception)


async def setup(bot):
    await bot.add_cog(Main(bot))
