import os
import discord
from discord.ext import commands
from config import EMBEDS_COLOR, BOT_TOKEN, CUSTOM PREFIX
bot = commands.Bot(command_prefix="CUSTOM_PREFIX")

successful_cogs = []
failed_cogs = []

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        cog_name = f"cogs.{filename[:-3]}"  # Remove .py extension
        try:
            bot.load_extension(cog_name)
            successful_cogs.append(filename[:-3])
        except Exception as e:
            print(f"Failed to load cog '{cog_name}': {e}")
            failed_cogs.append(filename[:-3])

if successful_cogs:
    print("Successfully loaded cogs: " + ", ".join(successful_cogs))
if failed_cogs:
    print("Failed to load cogs: " + ", ".join(failed_cogs))

# You can also use EMBEDS_COLOR in your bot or cogs as needed, for example:
print(f"Using EMBEDS_COLOR: {EMBEDS_COLOR}")

# Run the bot with your token
bot.run("BOT_TOKEN")
