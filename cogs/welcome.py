import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def create_welcome_image(self, username: str, user_avatar_url: str, server_icon_url: str, output_path: str = "welcome.png"):
        # Create a base image with a background color
        width, height = 600, 300
        background_color = (70, 130, 180)  # Steel blue
        img = Image.new("RGB", (width, height), color=background_color)
        draw = ImageDraw.Draw(img)
        
        # Download and open the user's avatar
        response = requests.get(user_avatar_url)
        avatar = Image.open(BytesIO(response.content)).convert("RGBA")
        avatar = avatar.resize((100, 100))  # Resize as needed
        
        # Download and open the server icon
        response = requests.get(server_icon_url)
        server_icon = Image.open(BytesIO(response.content)).convert("RGBA")
        server_icon = server_icon.resize((100, 100))
        
        # Paste the avatar and server icon onto the base image
        img.paste(avatar, (20, 100), avatar)
        img.paste(server_icon, (width - 120, 100), server_icon)
        
        # Add welcome text in the center
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except IOError:
            font = ImageFont.load_default()
        
        text = f"Welcome, {username}!"
        text_width, text_height = draw.textsize(text, font=font)
        text_x = (width - text_width) / 2
        text_y = (height - text_height) / 2
        draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))
        
        # Save the final image
        img.save(output_path)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Get the user's avatar URL; using .avatar.url for discord.py v2.x
        user_avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        
        # Get the server icon URL if available
        server_icon_url = member.guild.icon.url if member.guild.icon else "https://example.com/default_server_icon.png"

        # Create the welcome image
        self.create_welcome_image(member.name, user_avatar_url, server_icon_url)
        
        # Create an embed to display the welcome image
        embed = discord.Embed(
            title="Welcome!",
            description=f"Welcome to the server, {member.mention}!",
            color=discord.Color.green()
        )
        embed.set_image(url="attachment://welcome.png")
        
        # Send the embed in a specific channel (update the channel name as needed)
        channel = discord.utils.get(member.guild.text_channels, name="general")
        if channel:
            with open("welcome.png", "rb") as file:
                discord_file = discord.File(file, filename="welcome.png")
                await channel.send(embed=embed, file=discord_file)

def setup(bot):
    bot.add_cog(WelcomeCog(bot))
