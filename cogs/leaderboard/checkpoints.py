import discord
import aiosqlite
import yaml
from discord import app_commands
from discord.ext import commands
from typing import Optional

from utils import check_user, get_points, update_leaderboard

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

embed_color = discord.Color.from_str(data['DefaultStyles']['EMBED_COLOR'])

class CheckPointsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    #Checkpoints command
    @app_commands.command(name="checkpoints", description="Check a users points!")
    @app_commands.describe(user="Who's points would you like to check?")
    async def checkpoints(self, interaction: discord.Interaction, user: Optional[discord.Member]) -> None:
        is_self = False
        if user is None:
            user = await self.bot.fetch_user(interaction.user.id)
            is_self = True

        await check_user(user.id, interaction.guild_id)
        user_points = await get_points(user.id, interaction.guild_id)
        description = f"""
### POINTS
`{user_points}`
"""
        
        embed = discord.Embed(description=description, color=embed_color)
        embed.set_thumbnail(url=user.avatar.url)
        embed.set_author(name=user.name, icon_url=user.avatar.url)
        embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url) if is_self is False else None

        await interaction.response.send_message(embed=embed, ephemeral=True if is_self is True else False)
        await update_leaderboard(self.bot)

async def setup(bot):
    await bot.add_cog(CheckPointsCog(bot))