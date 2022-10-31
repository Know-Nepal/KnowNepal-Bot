import logging

import hikari
import lightbulb
from know_nepal.config import bot_config
from know_nepal.core.models import User
from know_nepal.core.plugins import get_all_committers
from lightbulb.ext import tasks

github = lightbulb.Plugin("GitHub", "Plugin that stores GitHub commands")
logger = logging.getLogger(__name__)


@github.command
@lightbulb.option("username", "Your github username")
@lightbulb.command("register", "Register to get contributor role", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def register_command(ctx: lightbulb.Context, username: str) -> None:
    user = await User.get_or_none(github_username=username)
    if not user:
        await User.create(
            id=ctx.author.id,
            github_username=username,
            guild_id=ctx.guild_id,
        )
    else:
        user.github_username = username

    await ctx.respond(
        embed=hikari.Embed(
            description=f"Successfully registered!\n Username: {username}",
            color=0x00FF00,
        ),
        flags=hikari.MessageFlag.EPHEMERAL,
    )


@tasks.task(m=1, wait_before_execution=True, auto_start=True)
async def give_contributor_role():
    try:
        users = await User.all()
        committers = await get_all_committers()
        for user in users:
            if user.github_username in committers:
                await github.bot.rest.add_role_to_member(
                    user.guild_id,
                    user.id,
                    bot_config.role_id,
                )
    except Exception as e:
        logger.warning(e)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(github)
    tasks.load(bot)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(github)
