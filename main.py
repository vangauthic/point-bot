import discord
import aiosqlite
import yaml
import sys
import logging
from utils import check_user, edit_points
from discord.ext import commands
from cogs.functions.sqlite import check_tables

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

token = data["General"]["TOKEN"]
activity = data["General"]["ACTIVITY"].lower()
doing_activity = data["General"]["DOING_ACTIVITY"]
status = data["General"]["STATUS"].lower()
embed_color = data["DefaultStyles"]["EMBED_COLOR"]

msg_reward = data["PointRewards"]["MESSAGE"]
reaction_reward = data["PointRewards"]["REACTION"]
voice_reward = data["PointRewards"]["VOICE"]
invite_reward = data["PointRewards"]["INVITE"]

initial_extensions = [
'cogs.functions.sqlite',

'cogs.leaderboard.activeupdate',
'cogs.leaderboard.checkpoints',
'cogs.leaderboard.claim',
'cogs.leaderboard.editpoints',

'cogs.utility.help',
'cogs.utility.translate'
]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if status == "online":
    _status = getattr(discord.Status, status)
elif status == "idle":
    _status = getattr(discord.Status, status)
elif status == "dnd":
    _status = getattr(discord.Status, status)
elif status == "invisible":
    _status = getattr(discord.Status, status)
else:
    sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Status: {bcolors.ENDC}{bcolors.OKCYAN}{status}{bcolors.ENDC}
{bcolors.OKBLUE}Valid Options: {bcolors.ENDC}{bcolors.OKGREEN}{bcolors.UNDERLINE}online{bcolors.ENDC}{bcolors.OKGREEN}, {bcolors.UNDERLINE}idle{bcolors.ENDC}{bcolors.OKGREEN}, {bcolors.UNDERLINE}dnd{bcolors.ENDC}{bcolors.OKGREEN}, or {bcolors.UNDERLINE}invisible{bcolors.ENDC}
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 7
""")

if activity == "playing":
    if doing_activity == "":
        sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Doing Activity: {bcolors.OKBLUE}It Must Be Set!
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 5
""")
    else:
        _activity = discord.Game(name=doing_activity)
elif activity == "watching":
    if doing_activity == "":
        sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Doing Activity: {bcolors.OKBLUE}It Must Be Set!
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 5
""")
    else:
        _activity = discord.Activity(name=doing_activity, type=discord.ActivityType.watching)
elif activity == "listening":
    if doing_activity == "":
        sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Doing Activity: {bcolors.OKBLUE}It Must Be Set!
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 5
""")
    else:
        _activity = discord.Activity(name=doing_activity, type=discord.ActivityType.listening)
elif activity == "competing":
    if doing_activity == "":
        sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Doing Activity: {bcolors.OKBLUE}It Must Be Set!
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 5
""")
    else:
        _activity = discord.Activity(name=doing_activity, type=discord.ActivityType.competing)
else:
    sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Activity: {bcolors.ENDC}{bcolors.OKCYAN}{activity}{bcolors.ENDC}
{bcolors.OKBLUE}Valid Options: {bcolors.ENDC}{bcolors.OKGREEN}{bcolors.UNDERLINE}playing{bcolors.ENDC}{bcolors.OKGREEN}, {bcolors.UNDERLINE}watching{bcolors.ENDC}{bcolors.OKGREEN}, {bcolors.UNDERLINE}competing{bcolors.ENDC}{bcolors.OKGREEN}, or {bcolors.UNDERLINE}listening{bcolors.ENDC}
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 4
""")

intents = discord.Intents.all()

class PointTracker(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix = '.',
            intents = intents,
            token = token,
            activity = _activity,
            status = _status
        )

    async def on_ready(self):
        print(f'{client.user} is connected!')

        print('Checking local databases...')
        await check_tables()
        print('Checked')

        print('Attempting to sync slash commands...')
        await self.tree.sync()
        print('Synced')

    async def setup_hook(self):
        for extension in initial_extensions:
            await self.load_extension(extension)

client = PointTracker()

#Initalize each user in the database
@client.event
async def on_member_join(member: discord.Member):
    await check_user(member.id, member.guild.id)

    #Award points to users who invited the user who joined
    invites = await member.guild.invites()
    if invites:
        for invite in invites:
            if invite.inviter == member:
                continue
            else:
                await edit_points(invite.inviter.id, member.guild.id, invite_reward, "+")

#Add points for each message sent
@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    
    await check_user(message.author.id, message.guild.id)
    await edit_points(message.author.id, message.guild.id, msg_reward, "+")

#Add points for each reaction added
@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    if user == client.user:
        return
    
    await check_user(user.id, reaction.message.guild.id)
    await edit_points(user.id, reaction.message.guild.id, reaction_reward, "+")

#Take points for each reaction removed
@client.event
async def on_reaction_remove(reaction: discord.Reaction, user: discord.User):
    if user == client.user:
        return
    
    await check_user(user.id, reaction.message.guild.id)
    await edit_points(user.id, reaction.message.guild.id, reaction_reward, "-")

#Add points for joining voice channels
@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if before.channel is None and after.channel is not None:
        await check_user(member.id, member.guild.id)
        await edit_points(member.id, member.guild.id, voice_reward, "+")

#Add points for creating invites
@client.event
async def on_invite_create(invite: discord.Invite):
    if invite.inviter == client.user:
        return
    
    await check_user(invite.inviter.id, invite.guild.id)
    await edit_points(invite.inviter.id, invite.guild.id, invite_reward, "+")

client.run(token)