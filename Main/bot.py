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

bot = commands.Bot(command_prefix = commands.when_mentioned_or('zim='))
bot.remove_command('help')
# @bot.command(name='99')
# async def nine_nine(ctx):
#
#     brooklyn_99_quotes = [
#         'I\'m the human form of the 💯 emoji.',
#         'Bingpot!',
#         (
#             'Cool. Cool cool cool cool cool cool cool, '
#             'no doubt no doubt no doubt no doubt.'
#         ),
#     ]
#
#     response = random.choice(brooklyn_99_quotes)
#     await ctx.send(response)
@bot.event
async def on_ready():
    guild = discord.utils.find(lambda g:g.name == GUILD, bot.guilds)
    print(
        f'{bot.user} has connected to Discord!\n'
        f'{guild.name}(id: {guild.id})\n'
    )
    members=', '.join([member.name for member in guild.members])
    print(f'Guild Members:{members}')
#
# @bot.event
# async def on_member_join(member):
#     await member.create_dm()
#     await member.dm_channel.send(
#         f'''Hi, welcome to the guild where I,
#             {bot.user.name} am tested!'''
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
        response = f'The Debate Will Start {message.content}'
        await message.channel.send(response)

    if message.content == 'raise-exception':
        raise discord.DiscordException

    await bot.process_commands(message)

@bot.command(name='show')
async def show_member(ctx,id=None):

#error was caused by not defining guild
    guild = discord.utils.find(lambda g:g.name == GUILD, bot.guilds)
    for guilds in bot.guilds:
        print(guilds)
#error was caused by not using name variable of instance
    members = ', '.join([members.name for members in guild.members])
    message = members + f' the default role of this guild is \'{guild.default_role.name[1:]}\''
    await ctx.send(message)

@bot.command(name='send')
async def send_dm(ctx, role, msg=f'Hi. You are a member of '):
    guild = discord.utils.find(lambda g:g.name == GUILD, bot.guilds)
    rolesMentioned = discord.utils.find(lambda r:r, ctx.message.role_mentions)
    if rolesMentioned != None:
        print(rolesMentioned)
        for member in rolesMentioned.members:
            print(type(member))
            await member.create_dm()
            print('dm channel created!')
            await member.dm_channel.send(f'{msg} {rolesMentioned.name}!')
            print('dm should have been sent!')#bot do not have dm_channel attribute

@bot.command(name='end', brief='Command to shut me down', help='Invoke me by @ mentioning me and typing \'end\' after or typing \'zim=end\'. This will shut me down and you won\'t be able to command me anymore.')
async def ending(ctx):
    await bot.logout()

@bot.command(name='addroles')
async def add_roles(ctx, id=None):
    guild = discord.utils.find(lambda g:g.name == GUILD, bot.guilds)
    for roles in guild.roles:
        if str(roles) == 'ZimBot - Tester':
            role = roles

    for member in guild.members:
        if member.id == int(id):
            await member.add_roles(role)
            # await bot.add_role(member, role) # dont use bot.add_role. Its outdated!
            await ctx.send(f'I changed {member.name}\'s role to "{str(role)}"')

@bot.command(name='leave')
async def leave_guild(ctx,id = None):
    if id != None:
        guildImLeaving = discord.utils.find(lambda g:g.id == int(id), bot.guilds)
        print(guildImLeaving.name)
        await guildLeaving.leave()

    else:
        guildImLeaving = ctx.guild
        await guildImLeaving.leave()

@bot.command(name='help', brief='A help command', help='A command to help give information to end users. Add "commands" after the help command to get a list of commands available to you.')
async def help_info(ctx, *args):
    parameters = {'title':'Mr.ZimBot', type:'rich', 'description':'The place to find out about me: Mr.ZimBot!', 'timestamp':'2020-09-27', 'color':255}
    embeddedMessage=discord.Embed.from_dict(parameters)
    for arg in args:
        possibleCommand=discord.utils.find(lambda c:c.name == arg, bot.commands)
        if arg=='commands':
            embeddedMessage.add_field(name='help for commands',value='Commands:\n'+'\n'.join(f'{c.name}---{c.brief}' for c in bot.commands))
        if possibleCommand != None:
            embeddedMessage.add_field(name=possibleCommand.name,value=possibleCommand.help)
    await ctx.send(embed=embeddedMessage)


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN)
