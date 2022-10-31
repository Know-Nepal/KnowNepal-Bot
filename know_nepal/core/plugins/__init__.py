import typing as t

import aiohttp
from know_nepal.config import bot_config

_ValueT = t.TypeVar("_ValueT")
T = t.TypeVar("T")


def _chunk(iterator: t.Iterator[_ValueT], max: int) -> t.Iterator[list[_ValueT]]:
    chunk: list[_ValueT] = []
    for entry in iterator:
        chunk.append(entry)
        if len(chunk) == max:
            yield chunk
            chunk = []

    if chunk:
        yield chunk


async def get_all_committers():
    headers = {"Authorization": f"Token {bot_config.github_token}"}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(
            f"https://api.github.com/orgs/{bot_config.github_org}/repos"
        ) as response:
            data = await response.json()

            repos = [repo["name"] for repo in data]
        all_committers = []
        for repo in repos:
            async with session.get(
                f"https://api.github.com/repos/{bot_config.github_org}/{repo}/commits"
            ) as response:
                data = await response.json()

            commits = [commit["author"]["login"].lower() for commit in data]
            all_committers += commits

        return list(set(all_committers))
