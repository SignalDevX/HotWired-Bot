import asyncio
import textwrap
import time

from contextlib import suppress
from discord import Color, Embed, Forbidden, Member
from discord.ext.commands import BadArgument, Bot, BucketType, Cog, Context, command, cooldown, has_permissions

from .utils import constants


class Common(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    # TODO : Add custom command support after db integration
    @command()
    async def hello(self, ctx: Context) -> None:
        """Greet a User."""
        await ctx.send("Hey there Buddy! How's it Going?")

    @command()
    @has_permissions(manage_messages=True)
    async def ping(self, ctx: Context) -> None:
        """Shows bot ping."""
        start = time.perf_counter()
        embed = Embed(title="Info", description="Pong!", color=Color.blurple())
        message = await ctx.send(embed=embed)
        end = time.perf_counter()
        duration = round((end - start) * 1000, 2)
        embed = Embed(title="Info", description=f":ping_pong: Pong! ({duration}ms)", color=Color.blurple())
        await message.edit(embed=embed)

    # TODO : after db integration, add Time Limit, and grand announcement, when the poll is over.
    @command(aliases=("poll",))
    async def vote(self, ctx: Context, title: str, *options: str) -> None:
        """
        Build a quick voting poll with matching reactions with the provided options.

        A maximum of 20 options can be provided, as Discord supports a max of 20
        reactions on a single message.
        """
        if len(options) < 2:
            raise BadArgument("Please provide at least 2 options.")
        if len(options) > 20:
            raise BadArgument("I can only handle 20 options!")

        codepoint_start = 127462  # represents "regional_indicator_a" unicode value
        options = {chr(i): f"{chr(i)} - {v}" for i, v in enumerate(options, start=codepoint_start)}
        embed = Embed(title=title, description="\n".join(options.values()))
        message = await ctx.send(embed=embed)
        for reaction in options:
            await message.add_reaction(reaction)

    # TODO : add github logo thumnail to embed, and some more content. like about ig.
    @command(aliases=["git"])
    async def github(self, ctx: Context) -> None:
        """GitHub repository"""
        await ctx.send(
            embed=Embed(
                title="Github Repo",
                description=f"[Click Here]({constants.github_repo_link}) to visit the Open Source Repo of HotWired",
                color=Color.dark_blue(),
            )
        )

    # TODO : beautify this timer with a realtime updating clock image.
    @command()
    @cooldown(1, 10, BucketType.user)
    async def countdown(self, ctx: Context, start: int) -> None:
        """A Countdown timer, that counts down from the specified time in seconds."""
        with suppress(Forbidden):
            await ctx.message.delete()

        embed = Embed(title="TIMER", description=start)
        message = await ctx.send(embed=embed)
        while start:
            minutes, seconds = divmod(start, 60)
            content = f"{minutes:02d}:{seconds:02d}"
            embed = Embed(title="TIMER", description=content)
            await message.edit(embed=embed)
            start -= 1
            await asyncio.sleep(1)
        await message.delete()

    @command(aliases=["asking"])
    async def howtoask(self, ctx: Context) -> None:
        """How to ask a Question."""
        embed = Embed(
            title="How To Ask a Question?",
            description=textwrap.dedent(
                """
                **1 ❯** Pick the appropriate channel
                **2 ❯** Post your question mentioning all the details
                **3 ❯** Ping the appropriate helper role or someone for your question
                **4 ❯** Patiently wait for a helper to respond
                """
            ),
            color=Color.blurple(),
        )
        img_url = "https://media.giphy.com/media/3ojqPGJAHWqC1VQPDk/giphy.gif"
        embed.set_image(url=img_url)
        await ctx.send("**A S K I N G   A   Q U E S T I O N ❓**")
        await ctx.send(embed=embed)

    @command(aliases=["thank", "ty"])
    async def thanks(self, ctx: Context, member: Member, *, reason: str = None) -> None:
        """Thank a User."""
        if ctx.author == member:
            embed = Embed(title="WARNING", description=f"{ctx.author.mention} **You Cannot Thank Yourself!**", color=Color.orange(),)
            await ctx.send(embed=embed)
        else:
            embed = Embed(
                title="THANKS",
                description=textwrap.dedent(
                    f"""
                    {member.mention} was thanked by {ctx.author.mention}!
                    {'**MESSAGE**:' + reason if reason else ''}
                    """
                ),
                color=Color.blurple(),
            )
            embed.set_image(url="https://media.giphy.com/media/6tHy8UAbv3zgs/giphy.gif")
            await ctx.send(embed=embed)


def setup(bot: Bot) -> None:
    bot.add_cog(Common(bot))
