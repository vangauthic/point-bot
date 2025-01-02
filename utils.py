import discord
import aiosqlite
import yaml

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

admin_guild_id = data['General']['ADMIN_GUILD_ID']
leaderboard_channel_id = data['General']['LEADERBOARD_CHANNEL_ID']
embed_color = discord.Color.from_str(data['DefaultStyles']['EMBED_COLOR'])

async def check_user(user_id: int, guild_id: int):
    async with aiosqlite.connect('database.db') as db:
        cursor = await db.execute('SELECT * FROM user_points WHERE user_id=? AND guild_id=?', (user_id, guild_id))
        check = await cursor.fetchone()
        if check is None:
            await db.execute('INSERT INTO user_points (user_id, guild_id) VALUES (?, ?)', (user_id, guild_id))
            await db.commit()

async def edit_points(user_id: int, guild_id: int, points: int, protocol: str):
    async with aiosqlite.connect('database.db') as db:
        cursor = await db.execute('SELECT * FROM user_points WHERE user_id=? AND guild_id=?', (user_id, guild_id))
        check = await cursor.fetchone()
        if check is None:
            await db.execute('INSERT INTO user_points (user_id, guild_id) VALUES (?, ?)', (user_id, guild_id))
            await db.commit()
        
        await db.execute(f'UPDATE user_points SET points=points{protocol}? WHERE user_id=? AND guild_id=?', (points, user_id, guild_id))
        await db.commit()

async def get_points(user_id: int, guild_id: int) -> int:
    async with aiosqlite.connect('database.db') as db:
        cursor = await db.execute('SELECT * FROM user_points WHERE user_id=? AND guild_id=?', (user_id, guild_id))
        check = await cursor.fetchone()
        if check is None:
            await db.execute('INSERT INTO user_points (user_id, guild_id) VALUES (?, ?)', (user_id, guild_id))
            await db.commit()
            return 0
        return check[2]

async def update_leaderboard(bot: discord.Client):
    description = ""
    guild = await bot.fetch_guild(admin_guild_id)

    async with aiosqlite.connect('database.db') as db:
        cursor = await db.execute('SELECT * FROM user_points WHERE guild_id=? ORDER BY points DESC LIMIT 10', (guild.id,))
        all_points = await cursor.fetchall()
        medals = ["🥇", "🥈", "🥉"]
        for index, user in enumerate(all_points):
            member = await guild.fetch_member(user[0])
            if member is not None:
                medal = medals[index] if index < 3 else ""
                description += f"{medal} {member.mention}: {user[2]}\n"

        cursor = await db.execute('SELECT * FROM saved_messages WHERE guild_id=? AND identifier=?', (guild.id, "leaderboard"))
        check = await cursor.fetchone()
        
        if check is not None:
            channel = await guild.fetch_channel(check[1])
            message = await channel.fetch_message(check[0])
            embed = discord.Embed(title="Leaderboard", description=description, color=embed_color)
            await message.edit(embed=embed)
        else:
            channel = await guild.fetch_channel(leaderboard_channel_id)
            embed = discord.Embed(title="Leaderboard", description=description, color=embed_color)
            leaderboard_msg = await channel.send(embed=embed)
            await db.execute('INSERT INTO saved_messages (message_id, channel_id, guild_id, identifier) VALUES (?, ?, ?, ?)', (leaderboard_msg.id, channel.id, guild.id, "leaderboard"))
            await db.commit()

def translate_time(time: int) -> str:
    hours = time // 3600
    minutes = (time % 3600) // 60
    seconds = time % 60
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
        
    return " ".join(parts)