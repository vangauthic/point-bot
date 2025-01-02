import discord
import yaml
import requests
import aiosqlite
import logging
from discord.ext import commands, tasks
from utils import update_leaderboard

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

admin_guild_id = data['General']['ADMIN_GUILD_ID']
leaderboard_channel_id = data['General']['LEADERBOARD_CHANNEL_ID']
embed_color = discord.Color.from_str(data['DefaultStyles']['EMBED_COLOR'])

class ActiveLeaderboardCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    def cog_load(self):
        self.update_leaderboard.start()

    @tasks.loop(minutes=20)
    async def update_leaderboard(self):
        await update_leaderboard(self.bot)

    @update_leaderboard.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(ActiveLeaderboardCog(bot))