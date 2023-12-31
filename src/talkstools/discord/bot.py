import discord

from talkstools.utils import get_secret

intents = discord.Intents.default()
intents.message_content = True


def get_discord_secret() -> str:
    return get_secret("DISCORD_TOKEN")


def post_to_discord(channel: str, message: str):
    client = discord.Client(intents=intents)

    channel_name = "seminars"

    @client.event
    async def on_ready():
        print(f"{client.user} has connected to discord!")
        for guild in client.guilds:
            channel = discord.utils.get(guild.text_channels, name=channel_name)
            if channel is not None:
                # for message in messages:
                #     await channel.send(message)
                await channel.send(message)
        await client.close()

    try:
        token = get_discord_secret()
        client.run(token)
    except Exception as e:
        raise e
