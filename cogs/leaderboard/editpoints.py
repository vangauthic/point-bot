import discord
import aiosqlite
import yaml
from discord import app_commands
from discord.ext import commands
from typing import Optional

from utils import check_user, edit_points, get_points, update_leaderboard

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

embed_color = discord.Color.from_str(data['DefaultStyles']['EMBED_COLOR'])
staff_role_id = data['General']['STAFF_ROLE_ID']
staff_users = data['General']['STAFF_USERS']

class EditPointsCog(commands.GroupCog, name='points'):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    #Add points
    @app_commands.command(name="add", description="Add points to a user!")
    @app_commands.describe(user="What user do you want to add points to?")
    @app_commands.describe(amount="How many points would you like to add?")
    async def add(self, interaction: discord.Interaction, user: discord.Member, amount: int) -> None:
        staff_role = interaction.guild.get_role(staff_role_id)
        if staff_role:
            if staff_role in interaction.user.roles or interaction.user.id in staff_users:
                await check_user(user.id, interaction.guild_id)
                await edit_points(user.id, interaction.guild_id, amount, "+")
                await update_leaderboard(self.bot)

                user_points = await get_points(user.id, interaction.guild_id)

                embed = discord.Embed(description=f"You have added `{amount}` points to {user.mention}.\nThey now have `{user_points}` points.", color=embed_color)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title="ERROR", description="You do not have permission to use this command!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="ERROR", description="Unable to fetch Staff Role", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        

    #Remove points
    @app_commands.command(name="remove", description="Remove points from a user!")
    @app_commands.describe(user="What user do you want to remove points from?")
    @app_commands.describe(amount="How many points would you like to remove?")
    async def remove(self, interaction: discord.Interaction, user: discord.Member, amount: int) -> None:
        staff_role = interaction.guild.get_role(staff_role_id)
        if staff_role:
            if staff_role in interaction.user.roles or interaction.user.id in staff_users:
                user_points = await get_points(user.id, interaction.guild_id)
                if user_points - amount < 0:
                    embed = discord.Embed(title="ERROR", description="User points can not be below 0!", color=discord.Color.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return
                
                await check_user(user.id, interaction.guild_id)
                await edit_points(user.id, interaction.guild_id, amount, "-")
                await update_leaderboard(self.bot)

                user_points = await get_points(user.id, interaction.guild_id)

                embed = discord.Embed(description=f"You have removed `{amount}` points from {user.mention}.\nThey now have `{user_points}` points.", color=embed_color)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title="ERROR", description="You do not have permission to use this command!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="ERROR", description="Unable to fetch Staff Role", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
async def setup(bot):
    await bot.add_cog(EditPointsCog(bot))