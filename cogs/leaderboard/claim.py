import discord
import aiosqlite
import yaml
from discord import app_commands
from discord.ext import commands
from datetime import datetime as DT

from utils import check_user, edit_points, get_points, update_leaderboard, translate_time

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

embed_color = discord.Color.from_str(data['DefaultStyles']['EMBED_COLOR'])
daily_reward = data['PointRewards']['DAILY']

class ClaimPointsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    #Daily claim command
    @app_commands.command(name="claim", description="Claim your daily points")
    async def claim(self, interaction: discord.Interaction) -> None:
        await check_user(interaction.user.id, interaction.guild_id)
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute('SELECT * FROM daily_rewards WHERE user_id = ? AND guild_id = ?', (interaction.user.id, interaction.guild_id))
            check = await cursor.fetchone()
            current_time = int(DT.now().timestamp())

            if check:
                last_claim = check[2]
                if current_time - last_claim < 86400:
                    wait_time = translate_time(86400 - (current_time - last_claim))
                    embed = discord.Embed(title="ERROR", description=f"You have already claimed your daily reward!\nPlease wait `{wait_time}`", color=discord.Color.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return
                else:
                    await edit_points(interaction.user.id, interaction.guild_id, daily_reward, "+")
                    await db.execute('UPDATE daily_rewards SET last_claim = ? WHERE user_id = ? AND guild_id = ?', (current_time, interaction.user.id, interaction.guild_id))
            else:
                await edit_points(interaction.user.id, interaction.guild_id, daily_reward, "+")
                await db.execute('INSERT INTO daily_rewards (user_id, guild_id, last_claim) VALUES (?, ?, ?)', (interaction.user.id, interaction.guild_id, current_time))

            user_points = await get_points(interaction.user.id, interaction.guild_id)
            embed = discord.Embed(description=f"You have claimed your daily reward!\nYou now have `{user_points}` points!", color=embed_color)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            await db.commit()
            await update_leaderboard(self.bot)
        
async def setup(bot):
    await bot.add_cog(ClaimPointsCog(bot))