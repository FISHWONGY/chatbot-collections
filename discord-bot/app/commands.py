from settings import app_config
from discord.ext import commands
import discord
import logging

logger = logging.getLogger(__name__)


status = discord.Status.online

bot = commands.Bot(
    command_prefix="!",
    intents=discord.Intents.all(),
    activity=discord.Activity(
        type=discord.ActivityType.competing, name="/help | !help"
    ),
)


@bot.event
async def on_ready():
    logger.info(f"We have logged in as {bot.user}")


@bot.command(help="Simple ping command")
async def ping(ctx, *, args):
    received_msg = "".join(args)

    logger.info(f"Received message: {received_msg} from user {ctx.author} ")

    await ctx.send("Pong!")


@bot.slash_command(
    name="ping",
    guild_ids=[app_config.DC_SER_ID],
    description="Ping slash command",
)
async def ping(ctx):
    await ctx.defer()
    await ctx.respond("Pong!")
