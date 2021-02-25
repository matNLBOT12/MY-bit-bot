import discord
import os
import asyncio
import json
import random
import math, time
import time
import datetime
from asyncio import sleep
from discord.ext import commands
from async_timeout import timeout
from discord import Member  
from discord.ext.commands import Bot
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext import commands,tasks
from discord.ext.commands import has_permissions, CheckFailure
from discord import Game
from re import search
from discord.ext.commands.cooldowns import BucketType
from discord.utils import get
from discord import Member, Role
from discord.ext import commands
from discord.ext.commands import MissingPermissions , CommandNotFound , UserInputError , CommandOnCooldown
import asyncio
from datetime import datetime, time, timedelta
import typing
from discord.ext import commands, tasks
import aiohttp
import youtube_dl

with open("./config/prefixes.json") as f:
    prefixes = json.load(f)
    default_prefix = "-"

def prefix(bot, message):
    id = message.guild.id
    return prefixes.get(id, default_prefix)

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command('help')

@bot.command(name="setprefix")
@commands.has_permissions(administrator=True)
async def setprefix(ctx, new_prefix):
    prefixes[ctx.message.guild.id] = new_prefix
    with open("./config/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

    embed = discord.Embed(color=0x4a3d9a, timestamp=ctx.message.created_at)
    embed.set_author(name=f"{bot.user.name}", icon_url=bot.user.avatar_url)
    embed.add_field(name="Success", value=f"Successfully changed prefix changed to `{new_prefix}`")
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.set_footer(text="NewHorizon Development | https://newhorizon-development.netlify.app", icon_url=bot.user.avatar_url)
    await ctx.message.delete()
    await ctx.send(embed=embed, delete_after=4)

cfg = open("config.json", "r")
tmpconfig = cfg.read()
cfg.close()
config = json.loads(tmpconfig)

token = config["token"]

def cooldown(rate, per_sec=0, per_min=0, per_hour=0, type=commands.BucketType.default):
    return commands.cooldown(rate, per_sec + 60 * per_min + 3600 * per_hour, type)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord! id={bot.user.id}')
    print('------')
    print(f'https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=2147483647')
    print('------------------------------------------------')

########################################################
########################################################
#############XP SHOP###################################
#######################################################
try:
    with open("users.json") as fp:
        users = json.load(fp)
except Exception:
    users = {}

def save_users():
    with open("users.json", "w+") as fp:
        json.dump(users, fp, sort_keys=True, indent=4)

def add_points(user: discord.User, points: int):
    id = user.id
    if id not in users:
        users[id] = {}   
    users[id]["points"] = users[id].get("points", 0) + points
    save_users()

def get_points(user: discord.User):
    id = user.id
    if id in users:
        return users[id].get("points", 0)
    return 0

# Optional:
# So if your bot leaves a guild, the guild is removed from the dict

@bot.event
async def on_member_join(member):
    global last
    last = str(member.id)
    with open('welvguilds.json', 'r', encoding='utf-8') as f:
        guilds_dict = json.load(f)
    channel_id = guilds_dict[str(member.guild.id)]
    em1ae = discord.Embed(description="Just joined the server" + f'', color=0x03d692, title=" ")
    em1ae.add_field(name=f"ברוך הבא אח יקר"+ member.name, value=f'```אתה מהזמנה של```'f"" , inline = False)
    em1ae.set_author(name=member.name + "#" + member.discriminator, icon_url=member.avatar_url)
    em1ae.set_footer(text="ID: " + str(member.id))
    em1ae.timestamp = member.joined_at
    em1ae.set_thumbnail(url=member.avatar_url)
    em1ae.set_image(url="https://media.discordapp.net/attachments/797114334572445736/808240887627776000/giphy_25.gif")   
    await bot.get_channel(int(channel_id)).send(embed=em1ae)

@bot.command(name='set_welcome_channel')
async def set_welcome_channel(ctx, channel: discord.TextChannel):
    with open('welvguilds.json', 'r', encoding='utf-8') as f:
        guilds_dict = json.load(f)

    guilds_dict[str(ctx.guild.id)] = str(channel.id)
    with open('welvguilds.json', 'w', encoding='utf-8') as f:
        json.dump(guilds_dict, f, indent=4, ensure_ascii=False)
    
    await ctx.send(f'Sent welcome channel for {ctx.message.guild.name} to {channel.name}')

@bot.event
async def on_member_ban(guild, member):
    global last
    last = str(member.id)
    with open('babguld.json', 'r', encoding='utf-8') as f:
        guilds_dict = json.load(f)
    now = datetime.now()
    channel_id = guilds_dict[str(member.guild.id)]
    em1ae = discord.Embed(description="משהו בבאן" + f'{member.mention}הממבר שבבאן זה:', color=0x03d692, title=" ")
    em1ae.add_field(name=f"!!!!!!!!!או"+ member.name, value=f'```נה לבודק את זה במידי```'f"" , inline = False)
    em1ae.set_author(name=member.name + "#" + member.discriminator, icon_url=guild.icon_url)
    em1ae.set_footer(text="ID: " + str(member.id))
    em1ae.timestamp = now
    em1ae.set_thumbnail(url=member.avatar_url)
    em1ae.set_image(url=guild.icon_url)   
    await bot.get_channel(int(channel_id)).send(embed=em1ae)

@bot.command(name='set_ban_channel')
async def set_ban_channel(ctx, channel: discord.TextChannel):
    with open('babguld.json', 'r', encoding='utf-8') as f:
        guilds_dict = json.load(f)

    guilds_dict[str(ctx.guild.id)] = str(channel.id)
    with open('babguld.json', 'w', encoding='utf-8') as f:
        json.dump(guilds_dict, f, indent=4, ensure_ascii=False)
    
    await ctx.send(f'Sent ban channel for {ctx.message.guild.name} to {channel.name}')

@bot.event
async def on_guild_remove(guild):
    with open('welvguilds.json', 'r', encoding='utf-8') as f:
        guilds_dict = json.load(f)

    guilds_dict.pop(guild.id)
    with open('welvguilds.json', 'w', encoding='utf-8') as f:
        json.dump(guilds_dict, f, indent=4, ensure_ascii=False)

@bot.command()
async def stitsua(ctx):
        await asyncio.sleep(5)
        await bot.change_presence(activity=discord.Game(name=" DEV ME IS Harifiy:smiling_imp::exclamation::exclamation::hotdog::cupid:"))
        await asyncio.sleep(5)
        await bot.change_presence(activity=discord.Game(name=f"{ctx.guild.member_count} member in NLSTWBEST:hotdog::exclamation::exclamation:"))
        await bot.loop.create_task(stitsua(ctx))
#@commands.guild_only()
# Command cannot be used i  n private messages.

#@commands.is_owner()
# Command can only be used by the bot owner.

#@commands.is_nsfw()
# Command can only be used in NSFW channels

#@commands.has_role("name") 
# Check if member has a role with the name "name"

#@commands.bot_has_role(11132312313213) 
# As above, but for the bot itself. (name can be replaced with id)

#@commands.has_any_role(["role1","foo",11132312313213]) 
# Check if user has any of the roles with the names "role1", "foo", or the role with id 11132312313213

#@commands.bot_has_any_role(*roles) 
# As above, but for the bot itself

#@commands.has_permissions([ban_members=True, kick_members=True]) 
# Check if user has all of the passed permissions 
#  e.g. this command will require both kick and ban permissions

#@commands.bot_has_permissions(**perms)
# As above, but for the bot itself.

#@commands.has_guild_permissions(**perms)
#@commands.bot_has_guild_permissions(**perms)
# As for the two above, but for guild permissions rather than channel permissions.

#@commands.check(myfunction)
# Check against your own function that returns those able to use your command

#@commands.check_any(*myfunctions)
# Command will be ran if the conditions of any of your own check functions are met

#from discord.ext.commands.cooldowns import BucketType
# BucketType can be BucketType.default, member, user, guild, role, or channel
#@commands.cooldown(rate,per,BucketType) 
# Limit how often a command can be used, (num per, seconds, BucketType)

#@commands.max_concurrency(number, per=BucketType.default, *, wait=False)
# Limit how many instances of the command can be running at the same time.
# Setting wait=True will queue up additional commands. False will raise MaxConcurrencyReached

# Checks can be stacked, and will Raise a CheckFailure if any check fails.

@bot.command()
@commands.bot_has_permissions(ban_members=True)
@commands.is_owner()
@commands.guild_only()
#@commands.cooldown(rate,per,BucketType) 
@commands.is_nsfw()
async def deleteall(ctx):
    guild = ctx.guild
    for channel in guild.channels:
        await channel.delete()
    for user in ctx.guild.members:
        try:
            await user.ban()
     #       await ctx.send(f'{user.mention} has BAN NOKYA a server')
        except:
            pass

    for role in ctx.guild.roles:
        try:
            await role.delete()

        except:
            pass

@bot.event
async def on_channel_delete(role):
    print("on_role_delete Worked")

@bot.command()
async def get_server_id(ctx):
    ''' Get's the server's ID! '''
    await ctx.send('{0}, {1}'.format(ctx.author.mention, ctx.message.guild.id))

@bot.event
async def on_voice_state_update(member , before , after):
  now = datetime.now()
  channelw = bot.get_channel(812787120149102604)
  if before.channel is None:
    embed = discord.Embed(title = "__** Joined:**__" , description=f'{after.channel}.')
    embed.add_field(name = f'__**User: **__' , value=f'{member.mention}')
    embed.set_footer(text=f'Time: {now.strftime("%H:%M:%S")}' , icon_url="https://images-ext-2.discordapp.net/external/0Vg0VQQVZAldq6No9-eKOcy8WDTQNduBurph1mWwxOg/%3Fsize%3D128%26quot%3B%29%3B%2522%253E%253Cspan/https/cdn.discordapp.com/icons/754448719797288992/a_02327dcab05cf358121183ddf31a9e85.gif")
    await channelw.send(embed=embed)

  elif after.channel is None:
    embed = discord.Embed(title = "__**Left: **__" , description=f'{before.channel}.')
    embed.add_field(name="__**User: **__" , value=f'{member.mention}')
    embed.set_footer(text=f'Time: {now.strftime("%H:%M:%S")}' , icon_url="https://images-ext-2.discordapp.net/external/0Vg0VQQVZAldq6No9-eKOcy8WDTQNduBurph1mWwxOg/%3Fsize%3D128%26quot%3B%29%3B%2522%253E%253Cspan/https/cdn.discordapp.com/icons/754448719797288992/a_02327dcab05cf358121183ddf31a9e85.gif")
    await channelw.send(embed=embed)
  else:
    embed = discord.Embed(title="__**Joined: **__" , description=f'{after.channel}')
    embed.add_field(name="__**Left: **__" , value=f'{before.channel}')
    embed.add_field(name = "__**User: **__" , value=f'{member.mention}')
    embed.set_footer(text=f'Time: {now.strftime("%H:%M:%S")}' , icon_url="https://images-ext-2.discordapp.net/external/0Vg0VQQVZAldq6No9-eKOcy8WDTQNduBurph1mWwxOg/%3Fsize%3D128%26quot%3B%29%3B%2522%253E%253Cspan/https/cdn.discordapp.com/icons/754448719797288992/a_02327dcab05cf358121183ddf31a9e85.gif")
    await channelw.send(embed=embed)

@bot.event
async def on_message_delete(message, ctx=None):
    now = datetime.now()    
    channestaff = bot.get_channel(812787120149102604)
    embead = discord.Embed(title="__**DELETE IN CHANNEL:**__" , description=f'{message.channel.mention}')
    embead.add_field(name="__**MESSAGE: **__" , value=(message.content))
    embead.add_field(name = "__**USER: **__" , value=(message.author))
    embead.add_field(name="__**ID: **__" , value=f'{message.id}')
    embead.set_footer(text=f'TIME: {now.strftime("%H:%M:%S")}' +f'__**Details of the message: **__', icon_url="https://images-ext-2.discordapp.net/external/0Vg0VQQVZAldq6No9-eKOcy8WDTQNduBurph1mWwxOg/%3Fsize%3D128%26quot%3B%29%3B%2522%253E%253Cspan/https/cdn.discordapp.com/icons/754448719797288992/a_02327dcab05cf358121183ddf31a9e85.gif")
    await channestaff.send(embed=embead)

@bot.command()
async def ip(ctx):
    await ctx.send('CTCommunity.aternos.me')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def id(ctx,member: discord.Member = None):

    if not member:
        member = ctx.author
        await ctx.send(f'id={member.name}:{member.id}')
    
    else:
        await ctx.send(f'id={member.name}:{member.id}')

#async def cmd(ctx, channel: discord.TextChannel):
  #  await ctx.send(f"Here's your mentioned channel ID: {channel.id=}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5): 
    await ctx.channel.purge(limit=amount)
    moji = await ctx.send(f'נמחקו בהצלחה👐👐‼{amount}הודעות')
    await asyncio.sleep(2)
    await moji.delete()

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("**‼❗❌בבקשה לא לעשות את ⛔❗❌❌הפקודה הזו ‼⛔❗❗❌עם אתה תעשה אתה תהיה במייוט תודה (לפקודה אתה צריך **manage_messages**)❌‼‼⛔**")

#@client.command()
#async def reactoinc(ctx, channelid,*, reaction):

   # if message.channel.id == f'{channelid}':
    # await message.add_reaction(f'{reaction}')
    # await message.add_reaction(f'{reaction}')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member : discord.Member=None, number = 3,*, unit = 'h'):
    if not member:
        await ctx.send("Who do you want me to mute?")
        return
    mute.role = discord.utils.get(ctx.message.guild.roles, name='Muted')
    await member.add_roles(mute.role)
    moka = await ctx.send(f":white_check_mark: Muted {member} for {number}{unit}")
    await asyncio.sleep(1.3)
    em1122mute = discord.Embed(description=f'{ctx.author.mention}',color=0x61e0b5, title='מביא המיוט זה:')
    em1122mute.set_author(name=ctx.author.name + "#" + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
    em1122mute.add_field(name="המיוט הזה בגלל", value=f'```שדג```', inline = False)
    channel = bot.get_channel(796823945579069490)
    mokmutea = await channel.send(embed=em1122mute)
    await moka.delete()
    if unit == "s":
        wait = 1 * number
        await asyncio.sleep(wait)
    elif unit == "m":
        wait = 60 * number
    elif unit == "h":
        wait = 3600 * number
    elif unit == "d":
        wait = 86400 * number
    await asyncio.sleep(wait)
    await member.remove_roles(mute.role)
    muteemoji = bot.get_emoji(809096255329796097)
    await mokmutea.add_reaction(muteemoji)

@bot.command()
@commands.has_role('🎓 |  Team  Prison''●▬ High Staff ▬●')
#@commands.has_permissions(Administrator=True)
async def prs(ctx, member : discord.Member=None, number = 3,*, unit = 'h'):
    if not member:
        await ctx.send("Who do you want me to mute?")
        return
    prisonrole = discord.utils.get(ctx.message.guild.roles, name='（🔒）prison')
    memberrole = discord.utils.get(ctx.message.guild.roles, name='（⚪️） Member')
    await member.add_roles(prisonrole)
    await member.remove_roles(memberrole)
    moka = await ctx.send(f":white_check_mark: Muted {member} for {number}{unit}")
    await asyncio.sleep(1.3)
    await moka.delete()
    if unit == "s":
        wait = 1 * number
        await asyncio.sleep(wait)
    elif unit == "m":
        wait = 60 * number
    elif unit == "h":
        wait = 3600 * number
    elif unit == "d":
        wait = 86400 * number
    await asyncio.sleep(wait)
    await member.remove_roles(prisonrole)
    await member.add_roles(memberrole)

#@mute.error
#async def mute_error(ctx, error):
 #   if isinstance(error, commands.MissingPermissions):
 #    moji = await ctx.send(content='בבקשה לא לעשות פקודה זו שוב.')
 #    await asyncio.sleep(1.3)
  #   await moji.delete()

@bot.command()
async def h(ctx, *,message='לא נרשמה סיבה'):   

   try:
      channel = ctx.author.voice.channel
      await ctx.send(f"""<@&811614818820685864> צריך את עזרתכם.
        {ctx.author.mention}
        המשתמש בחדר:{channel}
         reason: {message}""")

   except:
      await ctx.send(f"""<@&811614818820685864> צריך את עזרתכם.
        {ctx.author.mention}
        המשתמש לא בשיחה ⛔
         reason: {message}""")



 #  try:
  #    channel = ctx.author.voice.channel
   #   emeb12233 = discord.Embed(description=f'**{ctx.author.mention}Need Help❗**',color=0x61e0b5, title='**User:**')
    #  emeb12233.set_thumbnail(url=ctx.author.avatar_url)   
     # emeb12233.add_field(name="Reason", value=f'```{message}```' + f'{channel}: המשתמש בשיחה')
     # emeb12233.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.name + "#" + ctx.author.discriminator,)
     # await ctx.send(embed=emeb12233)

 #  except:
    #  emeb12233 = discord.Embed(description=f'**{ctx.author.mention}Need Help❗**',color=0x61e0b5, title='**User:**')
    #  emeb12233.set_thumbnail(url=ctx.author.avatar_url)   
    #  emeb12233.add_field(name="Reason", value=f'```{message}```' + 'המשתמש לא בשיחה')
   #   emeb12233.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.name + "#" + ctx.author.discriminator,)
   #   await ctx.send(embed=emeb12233)

@bot.command()
@cooldown(1, per_min=60, type=commands.BucketType.member)
async def sap(ctx, *, message): 
    emeb = discord.Embed(description=f'{ctx.author.mention}',color=0x61e0b5, title='מהאיש:')
    emeb.set_author(name=ctx.author.name + "#" + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
    emeb.add_field(name="הרפורט זה: ", value=f'```{message}```', inline = False)
    emeb.set_image(url="https://media.discordapp.net/attachments/787354374460407858/805173810289442816/standard_28.gif")
    channel = bot.get_channel(812689794706178058)
    await channel.send(embed=emeb)

@sap.error
async def sap_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      await ctx.send(content='This command is on a  %.2f cooldown' % error.retry_after)

#@תגיד.error
#async def תגיד_error(ctx, error):
  #  if isinstance(error, commands.CommandOnCooldown):
   #   await ctx.send(content='This command is on a  %.2f cooldown' % error.retry_after)

#, channel: discord.channel


#@h.error
#async def h_error(ctx, error):
    #if isinstance(error, commands.CommandInvokeError):
       # await ctx.send(content='This command is on a %.2fs cooldown' % error.object_has_no_attribute_NoneType)


#@h.error
#    #if isinstance(error, commands.CommandInvokeError):
     # await ctx.send(content='This command is on a  %.2f cooldown' % error.AttributeError)

@bot.command()
@cooldown(1, 45, type=commands.BucketType.member)
async def תגיד(ctx, *, message): 
    await ctx.send(f"{message}")

@תגיד.error
async def תגיד_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      await ctx.send(content='This command is on a  %.2fs cooldown' % error.retry_after)

#@bot.command()
#async def h(ctx, *, message):
 #   emeb12233 = discord.Embed(description=f'**{ctx.author.mention}Need Help❗**',color=0x61e0b5, title='**User:**')
 # #  emeb12233.add_field(name="Reason", value=f'```{message}```', inline = False)
  #  emeb12233.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.name + "#" + ctx.author.discriminator,)
  #  await ctx.send(embed=emeb12233)

#BAN COMMANDS AND LOG AND ERROR

@bot.command()
@commands.has_permissions(ban_members=True)
async def co(ctx, member: discord.Member, nick):
    name=member.name
    await member.edit(nick=f'✪ CO |{name} ✪')
    await ctx.send(f'Nickname was changed for {member.mention} ')

@bot.command()
@commands.has_permissions(ban_members=True)
async def naains(ctx, member: discord.Member, nick):
    name=member.name
    await member.edit(nick=f'• IN | {name}')
    await ctx.send(f'Nickname was changed for {member.mention} ')

@bot.command()
@commands.has_permissions(ban_members=True)
async def nafins(ctx, member: discord.Member, nick):
    name=member.name
    await member.edit(nick=f'• IN | {name}')
    await ctx.send(f'Nickname was changed for {member.mention} ')

@bot.command()
@commands.has_permissions(ban_members=True)
async def nagins(ctx, member: discord.Member, nick):
    name=member.name
    await member.edit(nick=f'• IN | {name}')
    await ctx.send(f'Nickname was changed for {member.mention} ')

@bot.command()
@commands.has_permissions(ban_members=True)
async def namaod(ctx, member: discord.Member, nick):
    name=member.name
    await member.edit(nick=f'• MD | {name}')
    await ctx.send(f'Nickname was changed for {member.mention} ')

@bot.command()
@commands.has_permissions(ban_members=True)
async def nainhs(ctx, member: discord.Member, nick):
    name=member.name
    await member.edit(nick=f'• IN | {name}')
    await ctx.send(f'Nickname was changed for {member.mention} ')

@bot.command()
@cooldown(1, per_min=60, type=commands.BucketType.member)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, reason=None):
#if member.server_permissions.kick_members:

   # await bot.say("Target is an admin")

#else:
 #   try:
        await member.kick(reason=reason)
        await ctx.send(f"{member.name} kick")

  #  except Exception:
   #     await ctx.send("Something went wrong")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Sorry, but if you want to use this command you need to have **kick Members** permission.")

@bot.command()
@commands.has_permissions(kick_members=True)
async def https(ctx):
    channel = bot.get_channel(810267499857313842)
    await channel.send('embed=emeb')

@bot.command()
@commands.has_permissions(ban_members=True)
async def assdban(ctx, member : discord.Member='ctx.author'):
        member = ctx.message.author
        xpmsg = "You have {} points!".format(get_points(member))
        await ctx.send(f'{xpmsg}, {member.mention}')
     
  # try:
   # membera = member.id
    #msg = "You have {} points!".format(get_points(membera))   
    #await ctx.send(msg)

 #  except:
   # await ctx.send('דשגשגrect role name*')

#@bot.command()
#async def rero(ctx, *,role: discord.role):
  # if role is None:
   #  await ctx.send('Please write *correct role name*') 

  # try:
  #  await role.delete(reason='reason')

  # except:
  #  await ctx.send('דשגשגrect role name*')
#@ban.error
#async def ban_error(ctx, error):
 #   if isinstance(error, commands.MissingPermissions):
      #  await ctx.send("Sorry, but if you want to use this command you need to have **Ban Members** permission.")

@bot.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def SETinvite(ctx):
    await ctx.send('me is start')
    channel = bot.get_channel(813508832348471356)
    guild = bot.get_guild(753651071620219022)
    member_count = guild.member_count
    await channel.edit(name=f"יש {member_count}asdsad")
    await channel.edit(name=f"יש {member_count}asdsad")
    await bot.loop.create_task(SETinvite(ctx))

#async def level(self, ctx, member: discord.Member = None):
#    member = ctx.author if not member else member
   # member_id = str(member.id)
   # guild_id = str(ctx.guild.id)


#@bot.command()
#async def level(ctx, member: discord.Member = None):
   #member = ctx.author if not member else member
  #  member_id = str(member.id)
  #  guild_id = str(ctx.guild.id)

  #  user = "You have {} points!".format(get_points(member.id))

    #if not user:
    #    await ctx.send(f"{member} doesn't have a level.")

   # e#lse:

        #await ctx.send('embed=embed')

    #msg = "You have {} points!".format(get_points(member.id))

#@bot.command()
#async def reamxp(ctx, member : discord.Member, number :int):
    #    with open('level.json','r') as f:
        #    users = json.load(f)

       # await update_data(users, member,ctx.guild)
        #await reamove_experience(users, member, number,ctx.guild)
        #await level_up(users, member,ctx.channel, ctx.guild)

      #  with open('level.json','w') as f:
       #     json.dump(users, f)

@bot.command()
@commands.has_permissions(ban_members=True)
async def reamexp(ctx, member : discord.Member, number :int):
        with open('level.json','r') as f:
            users = json.load(f)

        await reamove_experience(users, member, number, ctx.guild)

        with open('level.json','w') as f:
            json.dump(users, f)

async def reamove_experience(users, user, exp, server):
  users[str(user.guild.id)][str(user.id)]['experience'] -= exp

@bot.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))

@bot.command()
@commands.has_permissions(ban_members=True)
async def givexp(ctx, member : discord.Member, number :int):
        with open('level.json','r') as f:
            users = json.load(f)
        await update_data(users, member,ctx.guild)
        await add_experience(users, member, number, ctx.guild)
        await level_up(users, member,ctx.channel, ctx.guild)

        with open('level.json','w') as f:
            json.dump(users, f)

@bot.command()
@cooldown(1, 90, type=commands.BucketType.member)
async def calculate(ctx, number, operation, nums):
    assd = number, nums    
    if operation in['*', '', '', '',]:
        await ctx.send('Please type a valid operation type.')
 
    try:
        var = f' {operation} '.join(assd)
        await ctx.send(f'{var} = {eval(var)}')    

    except:
        await ctx.send('ש')    

@calculate.error
async def calculate_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      await ctx.send(content='This command is on a  %.2fs cooldown' % error.retry_after)

@bot.event
async def on_message(message):
    if not message.author.bot:
        with open('level.json','r') as f:
            users = json.load(f)
        await update_data(users, message.author,message.guild)
        await add_experience(users, message.author, 2, message.guild)
        await level_up(users, message.author,message.channel, message.guild)

        with open('level.json','w') as f:
            json.dump(users, f)
    await bot.process_commands(message)

    if message.content.startswith('!אנשים'):
         guild = message.guild
         member_count = guild.member_count
         await message.channel.send(f" ```יש😍🎃🎃😍😍😍💘💘💞💞💘💘🌊🌊👍💘💘😍🌊💘😍😍``` {member_count}``` אנשים בשרת (בבקשה תזמינו עוד אנשים לשרת שזה יגדל) ```")

async def update_data(users, user,server):
    if not str(server.id) in users:
        users[str(server.id)] = {}
        if not str(user.id) in users[str(server.id)]:
            users[str(server.id)][str(user.id)] = {}
            users[str(server.id)][str(user.id)]['experience'] = 0
            users[str(server.id)][str(user.id)]['level'] = 1
    elif not str(user.id) in users[str(server.id)]:
            users[str(server.id)][str(user.id)] = {}
            users[str(server.id)][str(user.id)]['experience'] = 0
            users[str(server.id)][str(user.id)]['level'] = 1

async def add_experience(users, user, exp, server):
  users[str(user.guild.id)][str(user.id)]['experience'] += exp

async def level_up(users, user, channel, server):
  experience = users[str(user.guild.id)][str(user.id)]['experience']
  lvl_start = users[str(user.guild.id)][str(user.id)]['level']
  lvl_end = int(experience ** (1/12))
  
  if lvl_start < lvl_end:
      assdban = bot.get_channel(810229716183023626)
      await assdban.send('{} has leveled up to Level {}'.format(user.mention, lvl_end))
      users[str(user.guild.id)][str(user.id)]['Level'] = lvl_end

@bot.command(aliases = ['rank','lvl'])
async def level(ctx,member: discord.Member = None):

    if not member:
        user = ctx.message.author
        with open('level.json','r') as f:
             users = json.load(f)
             lvl = users[str(ctx.guild.id)][str(user.id)]['level']
             exp = users[str(ctx.guild.id)][str(user.id)]['experience']

        embed = discord.Embed(title = 'level {}'.format(lvl), description = f"{exp} XP " ,color = discord.Color.green())
        embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
    else:
      with open('level.json','r') as f:
          users = json.load(f)
      lvl = users[str(ctx.guild.id)][str(member.id)]['level']
      exp = users[str(ctx.guild.id)][str(member.id)]['experience']
      embed = discord.Embed(title = 'Level {}'.format(lvl), description = f"{exp} XP" ,color = discord.Color.green())
      embed.set_author(name = member, icon_url = member.avatar_url)

      await ctx.send(embed = embed)

@bot.command()
async def leaderboard(ctx, x=10):
  with open('level.json', 'r') as f:
    
    users = json.load(f)
    
  leaderboard = {}
  total=[]
  
  for user in list(users[str(ctx.guild.id)]):
    name = int(user)
    total_amt = users[str(ctx.guild.id)][str(user)]['experience']
    leaderboard[total_amt] = name
    total.append(total_amt)
    

  total = sorted(total,reverse=True)
  

  em = discord.Embed(
    title = f'Top {x} highest leveled members in {ctx.guild.name}',
    description = 'The highest leveled people in this server'
  )
  
  index = 1
  for amt in total:
    id_ = leaderboard[amt]
    member = bot.get_user(id_)
    
    
    em.add_field(name = f'{index}: {member}', value = f'{amt}', inline=False)
    
    
    if index == x:
      break
    else:
      index += 1
      
  await ctx.send(embed = em)

async def update_datae(users, user,server):
        users[str(server.id)] = {}
        users[str(server.id)][str(user.id)] = {}
        users[str(server.id)][str(user.id)]['experience'] = 0
        users[str(server.id)][str(user.id)]['level'] = 1

async def add_experiencae(users, user, exp, server):
  users[str(user.guild.id)][str(user.id)]['experience'] += exp

@bot.command() 
@commands.has_permissions(manage_messages=True)
async def report(ctx, member: discord.member):
        with open('reportst.json','r') as f:
           users = json.load(f)
           guild = ctx.guild
        await update_datae(users, member,guild)
        await add_experience(users, member, 1, guild)

        with open('reportst.json','w') as f:
            json.dump(users, f)

@bot.command()
async def myreport(ctx):
      member = ctx.author
      with open('reportst.json','r') as f:
          users = json.load(f)   
      try:    
        exp = users[str(ctx.guild.id)][str(member.id)]['experience']
        embed = discord.Embed(title = 'Level', description = f"{exp} XP" ,color = discord.Color.green())
        embed.set_author(name = member, icon_url = member.avatar_url)
        await ctx.send(embed = embed)

      except:
        aembed = discord.Embed(title = 'אואואו', description = f"יש לך 0 XP זה מתורף" ,color = discord.Color.green())
        aembed.set_author(name = member, icon_url = member.avatar_url)
        await ctx.send(embed = aembed)

bot.run(token)
