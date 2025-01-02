import discord
import aiosqlite
import sqlite3
import yaml
from discord.ext import commands
from discord import app_commands
from typing import Literal

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

embed_color = data['DefaultStyles']['EMBED_COLOR']

async def check_tables():
    await user_points()
    await saved_messages()
    await daily_rewards()

async def refresh_table(table: str):
    if table == "User Points":
        await user_points(True)
    elif table == "Saved Messages":
        await saved_messages(True)
    elif table == "Daily Rewards":
        await daily_rewards(True)

async def user_points(delete: bool = False):
    async with aiosqlite.connect('database.db') as db:
        if delete:
            try:
                await db.execute('DROP TABLE user_points')
                await db.commit()
            except sqlite3.OperationalError:
                pass

        try:
            await db.execute('SELECT * FROM user_points')
        except sqlite3.OperationalError:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS user_points (
                    user_id INTEGER,
                    guild_id INTEGER,
                    points INTEGER DEFAULT 0
                )
            """)
            await db.commit()

async def saved_messages(delete: bool = False):
    async with aiosqlite.connect('database.db') as db:
        if delete:
            try:
                await db.execute('DROP TABLE saved_messages')
                await db.commit()
            except sqlite3.OperationalError:
                pass

        try:
            await db.execute('SELECT * FROM saved_messages')
        except sqlite3.OperationalError:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS saved_messages (
                    message_id INTEGER,
                    channel_id INTEGER,
                    guild_id INTEGER,
                    identifier STRING
                )
            """)
            await db.commit()

async def daily_rewards(delete: bool = False):
    async with aiosqlite.connect('database.db') as db:
        if delete:
            try:
                await db.execute('DROP TABLE daily_rewards')
                await db.commit()
            except sqlite3.OperationalError:
                pass

        try:
            await db.execute('SELECT * FROM daily_rewards')
        except sqlite3.OperationalError:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS daily_rewards (
                    user_id INTEGER,
                    guild_id INTEGER,
                    last_claim INTEGER
                )
            """)
            await db.commit()

class SQLiteCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="refreshtable", description="Refreshes a SQLite table!")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(table="What table should be refreshed?")
    async def refreshtable(self, interaction: discord.Interaction, table: Literal["User Points", "Saved Messages", "Daily Rewards"]) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)

        if await self.bot.is_owner(interaction.user):
            await refresh_table(table)
            embed = discord.Embed(description=f"Successfully refreshed the table **{table}**!", color=embed_color)
        else:
            embed = discord.Embed("You do not have permission to use this command!", color=discord.Color.red())
        
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(SQLiteCog(bot))