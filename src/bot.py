import discord
from emails import write_email
from config import REMINDER, ANNOUNCE
from debug import debug


def post_to_discord(config, talk, seminar, mode):

    client = discord.Client()
    channel_name = seminar.channel

    if mode == ANNOUNCE:
        intro = write_email(
            config, seminar, "discord-announce-intro.txt", talk)
        messages = [intro]
    elif mode == REMINDER:
        message = write_email(config, seminar, "discord-reminder.txt", talk)
        messages = [message]
    else:
        debug(config, "Mode not configured to send discord messages.")
        exit(1)

    @client.event
    async def on_ready():
        debug(config, f"{client.user} has connected to discord!")
        for guild in client.guilds:
            channel = discord.utils.get(guild.text_channels, name=channel_name)
        for message in messages:
            await channel.send(message)
        await client.close()

    client.run(config.discord)
