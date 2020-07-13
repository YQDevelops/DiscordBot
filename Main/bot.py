# bot.py
import os
import re
import random

import discord
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix = '=')
@bot.command(name='99')
async def nine_nine(ctx):

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)
# @bot.event
# async def on_ready():
#     guild = discord.utils.find(lambda g:g.name == GUILD, bot.guilds)
#     print(
#         f'{bot.user} has connected to Discord!\n'
#         f'{guild.name}(id: {guild.id})\n'
#     )
#     members=', '.join([member.name for member in guild.members])
#     print(f'Guild Members:{members}')
#
# @bot.event
# async def on_member_join(member):
#     await member.create_dm()
#     await member.dm_channel.send(
#         f'''Hi, welcome to the guild where I, the magnanimous,
#          the magnificent, the amazing {bot.user.name} am tested!'''
#     )
#
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    debateFunctions= ['Initiating Debate. When would you like to start?','Okay.','Debate will commence in 5 hours',"I don't care. I'M the debate instructor, NOT you!"]

    if message.content == 'Start Debate':
        response = debateFunctions[0]
        await message.channel.send(response)

    pattern = re.compile(r'In [\d]+ (minute|hour|day)s?', re.I)
    match = pattern.finditer(message.content)
    if [matches for matches in match]!= []:
        response = f'The Debate Will Start i{message.content[1:]}'
        await message.channel.send(response, tts=True)

    if message.content == 'raise-exception':
        raise discord.DiscordException

@bot.command(name='show')
async def show_member(ctx):
#error was caused by not defining guild
    guild = discord.utils.find(lambda g:g.name == GUILD, bot.guilds)

#error was caused by not using name variable of instance
    members = ', '.join([members.name for members in guild.members])
    message = members + f'the default role of this guild is \'{guild.default_role}\''
    await ctx.send(message)

@bot.command(name='send')
async def send_dm(ctx):
    guild = discord.utils.find(lambda g:g.name == GUILD, bot.guilds)
    for member in guild.members:
        if member.name == 'WeiQian':
            await member.create_dm()
            print('dm channel created!')
            await member.dm_channel.send(f'Hi {member.name}!')
            print('dm should have been sent!')#bot do not have dm_channel attribute

@bot.command(name='end')
async def ending(ctx):
    await bot.logout()

@bot.command(name='addroles')
async def add_roles(ctx, id):
    guild = discord.utils.find(lambda g:g.name == GUILD, bot.guilds)

    for roles in guild.roles:
        if str(roles) == 'ZimBot - Tester':
            role = roles
    for member in guild.members:
        if member.id == int(id):
            await member.add_roles(role)
            # await bot.add_role(member, role) # dont use bot.add_role. Its old code!
            await ctx.send(f'I changed {member.name}\'s role to "{str(role)}"')

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN)
