import os
import discord
from emails import write_email
from config import REMINDER, ANNOUNCE
from debug import debug


def post_to_discord(config, talk, mode):
    client = discord.Client()

    channel_name = "seminars"

    if mode == ANNOUNCE:
        intro = write_email(config, "discord-announce-intro.txt", talk)
        abstract = write_email(config, "discord-announce-abstract.txt", talk)
        details = write_email(config, "discord-announce-details.txt", talk)
        messages = [intro, abstract, details]
    elif mode == REMINDER:
        message = write_email(config, "discord-reminder.txt", talk)
        messages = [message]
    else:
        debug(config, "Mode not configured to send discord messages.")
        exit(1)

    @client.event
    async def on_ready():
        print(f"{client.user} has connected to discord!")
        for guild in client.guilds:
            channel = discord.utils.get(guild.text_channels, name=channel_name)
        for message in messages:
            await channel.send(message)
        await client.close()

    client.run(config.discord)
