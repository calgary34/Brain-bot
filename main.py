from discord.ext import commands
import discord
import os
import sympy as sy
import requests
import json
client = commands.Bot(command_prefix="b ")
client.remove_command("help")
x,y = sy.symbols('x y')
@client.event
async def on_message(message):
  if client.user.mentioned_in(message):
    await message.channel.send("The prefix is 'b'")
@client.event
async def on_message(msg):
  msg.content = msg.content.lower()
  await client.process_commands(msg)
@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		em = discord.Embed(title="Invalid Command", description=f"{str(error)}. Try `b help` for a list of commands.", color=0x275ef4)
		await ctx.send(embed=em)
@client.event
async def on_member_join(member):
  channel = client.get_channel('814245318060933140')
  if channel:
    await client.send_message(channel,f'Welcome <@{member.id}>!')
@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="For `b help`"))
    print(client.user, "Is Ready")
@client.command()
async def ping(ctx):
  await ctx.send('Pong!')
@client.command(aliases=['calculate'])
async def calc(ctx,*,exp):
  try:
    result=str(sy.N(sy.S(exp)))
    result=result.replace("*","\*")
    result=result.replace("**","^")
    em=discord.Embed(title="Result",description=result)
    await ctx.send(embed=em)
  except:
    await ctx.send('Error.')
@client.command()
async def solve(ctx,exp,exp2):
  try:
    result=str(list(sy.solveset(sy.Eq(sy.S(exp),sy.S(exp2)))))
    result=result.replace("*","\*")
    result=result.replace("**","^")
    em=discord.Embed(title="Solution(s)",description=result)
    await ctx.send(embed=em)
  except:
    await ctx.send('Error.')
@solve.error
async def solve_error(ctx, error):
  await ctx.send("Error.")
@client.command(aliases=['diff'])
async def derivative(ctx,exp,n):
  try:
    result=str(sy.diff(sy.S(exp),sy.Symbol(n)))
    result=result.replace("*","\*")
    result=result.replace("**","^")
    em=discord.Embed(title="Result",description=result)
    await ctx.send(embed=em)
  except:
    await ctx.send('Error.')
@derivative.error
async def derivative_error(ctx, error):
  await ctx.send("Error.")
@client.command(aliases=['antidiff'])
async def antiderivative(ctx,exp,n):
  try:
    result=str(sy.integrate(sy.S(exp),sy.Symbol(n)))
    result=result.replace("*","\*")
    result=result.replace("**","^")
    em=discord.Embed(title="Result",description=result)
    await ctx.send(embed=em)
  except Exception as e:
    print(e)
    await ctx.send('Error.')
@antiderivative.error
async def antiderivative_error(ctx, error):
  await ctx.send("Error.")
@calc.error
async def calc_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("You better give me an expression to evaluate!")
@client.command(aliases=['elem'])
async def element(ctx,name):
  data=json.loads(requests.get(f'https://chemistrydata.herokuapp.com/elements/{name}').text)
  if "status" in data:
    await ctx.send('Element not found.')
  else:
    em=discord.Embed(title=f"Data for {name}")
    em.add_field(name="Symbol",value=str(data['symbol']))
    em.add_field(name="Atomic Number",value=str(data['number']))
    em.add_field(name="Category",value=str(data['category']))
    em.add_field(name="Period",value=str(data['period']))
    em.add_field(name="Appearance",value=str(data['appearance']))
    em.add_field(name="Atomic Mass",value=str(data['atomic_mass']))
    em.add_field(name="Density",value=str(data['density']))
    em.add_field(name="Atomic Mass",value=str(data['atomic_mass']))
    em.add_field(name="Phase at room temperature",value=str(data['phase']))
    em.add_field(name="Molar Heat Capacity",value=str(data['molar_heat']))
    em.add_field(name="Electron Configuration",value=str(data['electron_configuration']))
    em.add_field(name="Electron Affinity",value=str(data['electron_affinity']))
    em.add_field(name="Melting Point",value=str(data['melt']))
    em.add_field(name="Boiling Point",value=str(data['boil']))
    em.add_field(name="Discoverer",value=str(data['discovered_by']))
    await ctx.send(embed=em)
@element.error
async def element_error(ctx, error):
  print(error)
  await ctx.send('Error.')
@client.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(
        title="Help",
        description=
        "List of commands in Brain Bot. Remember to put `b ` before each command.")
    em.add_field(
        name="Commands",
        value=
        "`calc`,`help`,`ping`,`derivative`,`antiderivative`",inline=False
    )
    await ctx.send(embed=em)
class HelpCommand:
    def __init__(self, title, desc, usage, aliases):
        self.title = title
        self.desc = desc
        self.desc = desc
        self.aliases = aliases
        self.usage = usage
        self.em = discord.Embed(
            title=self.title, description=self.title, color=self.color)
        self.em.add_field(name="Description", value=desc,inline=False)
        self.em.add_field(name="Usage", value=usage,inline=False)
        self.em.add_field(name='Aliases', value=aliases,inline=False)
@help.command(
    name='calc', aliases=['calculate'], pass_context=True)
async def help_calc(ctx):
    cmd = HelpCommand(
        'Help on `calc`',
        "Calculates the given expression.",
        "`b calc`", "`calculate`")
    await ctx.send(embed=cmd.em)
@help.command(
    name='ping', pass_context=True)
async def help_ping(ctx):
    cmd = HelpCommand(
        'Help on `ping`',
        "Bot returns `Pong!`.",
        "`b ping`", "None")
    await ctx.send(embed=cmd.em)
@help.command(
    name='solve', pass_context=True)
async def help_solve(ctx):
    cmd = HelpCommand(
        'Help on `solve`',
        "Solves equations. ",
        "`b solve <left side of equation> <right side of equation>`", "None")
    await ctx.send(embed=cmd.em)
@help.command(
    name='derivative', pass_context=True)
async def help_derivative(ctx):
    cmd = HelpCommand(
        'Help on `derivative`',
        "Calculates the derivative of functions.",
        "`b derivative <expression> <variable>`", "`diff`")
    await ctx.send(embed=cmd.em)
@help.command(
    name='antiderivative', pass_context=True)
async def help_antiderivative(ctx):
    cmd = HelpCommand(
        'Help on `antiderivative`',
        "Calculates the antiderivative of functions.",
        "`b derivative <expression> <variable>`", "`antidiff`")
    await ctx.send(embed=cmd.em)
client.run(os.getenv("TOKEN"))