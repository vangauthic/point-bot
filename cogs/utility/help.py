import discord
import yaml
from discord import app_commands
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

embed_color = discord.Color.from_str(data['DefaultStyles']['EMBED_COLOR'])
daily_reward = data['PointRewards']['DAILY']

class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    #Daily claim command
    @app_commands.command(name="help", description="Get help on the bot")
    async def help(self, interaction: discord.Interaction) -> None:
        help_desc = f"""
## Help
Thank you for using {self.bot.user.name}! Below is information you may find useful about the bot.

### Features
- Claim daily points
- Automatically updated leaderboard
- Translate messages
- Manage user points
- Earn points for interacting with the server

### Commands
- `/claim` - Claim your daily points
- `/checkpoints` - Check your or another user's points
- Translate - Translate a message to another language (App Command)

### Staff Commands
- `/points add` - Add points to a user
- `/points remove` - Remove points from a user
"""
        embed = discord.Embed(description=help_desc, color=embed_color)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)
        
async def setup(bot):
    await bot.add_cog(HelpCog(bot))