import logging

import hikari
import lightbulb
import miru
from know_nepal.config import bot_config
from know_nepal.core.models import User
from know_nepal.core.plugins import _chunk, get_all_committers
from lightbulb.ext import tasks
from miru.ext import nav

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


@github.command
@lightbulb.add_checks(
    lightbulb.bot_has_guild_permissions(hikari.Permissions.ADMINISTRATOR)
)
@lightbulb.command("list", "List all the registered people!")
@lightbulb.implements(lightbulb.SlashCommand)
async def list_command(ctx: lightbulb.Context) -> None:
    users = await User.all()
    user_list = [
        f"**User:** <@{user.id}>\n**GitHub Username:** `{user.github_username}`"
        for user in users
    ]

    fields = [
        hikari.Embed(
            title="List of Registered Users",
            description="\n\n".join(user),
            color=0x00FF00,
        )
        for _, user in enumerate(_chunk(user_list, 5))
    ]

    navigator = nav.NavigatorView(pages=fields)
    await navigator.send(ctx.interaction)
    await navigator.wait()


@tasks.task(m=1, wait_before_execution=True, auto_start=True)
async def give_contributor_role():
    try:
        users = await User.all()
        committers = await get_all_committers()
        for user in users:
            if user.github_username.lower() in committers:
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
    miru.load(bot)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(github)
