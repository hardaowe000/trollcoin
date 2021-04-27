import discord, pyrebase
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
import os, sys, json, asyncio, aioconsole, random

# while True:
#   input(random.randint(1, 5))

# token = os.environ['token']
token = "ODM0ODEwOTY4MjY0NTQwMTgy.YIGUTA.xv5e-oWC9gMO85b-HvtAsX2DsVk"
firebaseConfig = {
  "apiKey": "AIzaSyA5S9AvDZX_HxTlKV5Q7YQRyo0uvm9hOEM",
  "authDomain": "trollcoinpy.firebaseapp.com",
  "databaseURL": "https://trollcoinpy-default-rtdb.firebaseio.com",
  "projectId": "trollcoinpy",
  "storageBucket": "trollcoinpy.appspot.com",
  "messagingSenderId": "71836853150",
  "appId": "1:71836853150:web:be7289cee49bb9fbc6ec8f",
  "measurementId": "G-85GBYPG44C"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

data = db.child("users")

# class thousandaire:
#   id = 836405383735017523
intents = discord.Intents().default()
intents.members = True
client = commands.Bot(command_prefix = "tc!",intents=intents)
prefix = "tc!"
slash = SlashCommand(client, sync_commands=True)
# https://discord.com/api/oauth2/authorize?client_id=834810968264540182&permissions=2419313873&scope=bot%20applications.commands


lesgo = ["lest go","lesgo","lestgo", "letsgo","lesco","les go","lets go", "letsa go", "lets a go", "let's go","letsago","letsa go"]
join_messages = [
  "Everyone welcome our newest thousandaire, {}!",
  "{} has ascended to new levels",
  "{} has joined the ranks of the TrollCoin thousandaires!",
  "GG {}, welcome to heaven!",
  "{} has popped into our lovely server"
]

yo = open(os.path.join(sys.path[0], "guilds.txt"), 'r')
guilds=yo.readlines()
print(guilds)
guild_ids = [int(f.rstrip("\n")) for f in guilds] # 742422199368941629
print(guild_ids)
yo.close()

open_channels = [834813365648883744,711347029611118722,836243222094151730]

@slash.slash(
  guild_ids = guild_ids,
  name="ping",
  description="pong",
)
async def _ping(ctx):
  await ctx.send("Pong!")

@slash.slash(
  guild_ids = guild_ids,
  name="gamble",
  description="gamble an integer amount for a chance to earn 133%",
  options=[
    create_option(
      name="type",
      description="gamble type", 
      option_type=3, 
      required=True,
      choices=[
        create_choice(
          name="133%",
          value="133%"
        ),
        create_choice(
          name="Double",
          value="Double"
        )
      ]
    ),
    create_option(
      name="amount",
      description="gamble amount",
      option_type=4,
      required=True
    )
  ]
)
async def _gamble(ctx,type:str,amount:int):
  # try:
  rdata = open(os.path.join(sys.path[0], "data.txt"),'r+')
  pdata = json.loads(rdata.read())
  gamble_type=type
  gamble_amount=amount
  gamble_endamount=amount
  if str(ctx.author.id) not in pdata.keys():
    await ctx.send(content="You don't have an account! Type tc!create to make an account.")
  else:
    if gamble_amount > pdata[str(ctx.author.id)] + 1:
      await ctx.send(content=f"We're very sorry, but you don't have enough money to gamble!")
    elif gamble_amout > 999999:
      await ctx.send(content="Holy crap, chill out lol, the limit is 999,999~~TC~~ to prevent abuse. Thanks for understanding.")
    else:

      pdata[str(ctx.author.id)] = pdata[str(ctx.author.id)] - gamble_amount

      if gamble_type == "Double":
        gamble_end = random.randint(1,3)
      elif gamble_type == "133%":
        gamble_end = random.randint(1,2)
      
      if gamble_end == 1:
        success = "successfully!"
        if gamble_type == "Double":
          gamble_endamount *= 2
        elif gamble_type == "133%":
          gamble_endamount *= 1.33
      else:
        success = "and lost :(."
        if gamble_type == "Double":
          gamble_endamount *= .5
        elif gamble_type == "133%":
          gamble_endamount *= .66
      gamble_endamount = round(gamble_endamount,2)

      pdata[str(ctx.author.id)] = pdata[str(ctx.author.id)] + gamble_endamount

      rdata.seek(0)
      rdata.write(json.dumps(pdata))
      rdata.truncate()

      await ctx.send(content=f"You've gambled {gamble_amount} {gamble_type} {success} {gamble_endamount}~~TC~~ has been deposited back into your bank account.")
  rdata.close()
  # except:
  #  await ctx.send(content="Oh no, there was an error! Maybe it was because you didn't format this command properly... not sure.")

async def manual_input():
  while True:
    x=""
    x = await aioconsole.ainput(f"tc$manual : ")
    if x != "":
      if x == "tc$empty":
        x = "||\n||"
      await client.get_channel(834813365648883744).send(x)
    else: continue
def CE(**info):
  info.setdefault('title','TrollCoin')
  info.setdefault('description','No description was provided for this embed')
  info.setdefault('color', discord.Color.from_rgb(252, 255, 51))
  embed = discord.Embed(title=info['title'],description=info['description'],color=info['color'])
  embed.set_footer(text='Made by Elephant#5716 and Sounds About Right#9270 2021')

  return embed

def helpEmbed():
  embed = discord.Embed(
    title="TrollCoin Help",
    color=discord.Color.from_rgb(252,255,51),
    description="Hello!! Thank you for adding me, here is a list of commands:"

  )
  embed.add_field(
    name = "tc! Commands:",
    value="**create** - create an account.\n**balance** - see your balence (or others by mentioning them).\n**send <usermention> <intvalue>** - sends a specified amount of ~~TC~~ to the mentioned user.\n**ascend** - buy a ticket to Le Troll Supreme for 1k.\n**gamblehelp** - I will dm you the probability stats for gambling.\n", # \n**advancedhelp** - DMs you literally everything you could possibly do with the bot
    inline=True
  )
  embed.add_field(
    name="Slash Commands:",
    value="**ping** - pong\n**gamble** - gamble a specified amount for a specified return with a specified chance of success/failure",
    inline=True
  )
  embed.set_footer(text='Made by Elephant#5716 and Sounds About Right#9270 2021')

  return embed

@client.event
async def on_message(message):
  try:print(f"[{message.guild.name}] [{message.channel.name}] {message.author} : {message.content}")
  except:pass
  pm = message.content.lower()
  if message.channel.id in open_channels:
    if message.author == client.user:
      return
    elif pm.startswith(prefix+"test"):
      await message.channel.send(embed=CE(description = "You hailed?"))
    elif pm.startswith(prefix+"help"):
      await message.channel.send(embed=helpEmbed())
    elif pm.startswith(prefix+"create"):

      user_data = data.child(str(message.author.id)).get()

      if user_data.val() == None:
        await message.channel.send(f"Whoops, <@{message.author.id}>, you have an account already!")
      else:
        data.child(str(message.author.id)).set({"tc_amount":50})
        await message.channel.send(f"Thank you <@{message.author.id}>, your account has been created!")

    elif pm.startswith(prefix+"balence") or pm.startswith(prefix+"balance"):
      user_data = data.child(str(message.author.id)).get()
      if message.mentions == []:
        if user_data.val() != None:
          await message.channel.send(f"<@{message.author.id}>, you have {user_data.val()['tc_amount']}~~TC~~!")
        elif user_data.val()==None:
          await message.channel.send(f"<@{message.author.id}>, you don't have an account! Type tc!create to create an account.")
      elif message.mentions != [] and data.child(str(message.mentions[0].id)).get().val() != None:
        # print(data.child(str(message.mentions[0].id)).get().val())
        await message.channel.send(f"{message.mentions[0].name} has {data.child(str(message.mentions[0].id)).get().val()['tc_amount']}~~TC~~.")
      elif message.mentions !=[] and data.child(str(message.mentions[0].id)).get().val() == None:
        await message.channel.send(f"{message.mentions[0].name} doesn't have an account. You know what would be epic? Telling them to make one!")

    elif pm.startswith(prefix+"send"):
      rdata = open(os.path.join(sys.path[0], "data.txt"),'r+')
      pdata = json.loads(rdata.read())
      try:
        if message.mentions == []:
          await message.channel.send(f"Oh yikes, <@{message.author.id}>, you need to mention (ping) someone for this command, mate!")
        elif str(message.author.id) not in pdata.keys():
          await message.channel.send(f"<@{message.author.id}>, you don't have an account! Type tc!create to make an account.")
        elif str(message.mentions[0].id) not in pdata.keys():
          await message.channel.send(f"{message.mentions[0].name} doesn't have an account. You know what would be epic? Telling them to make one!")
        else:
          # print(pm.split())
          transfer_amount = round(float(pm.split()[-1]),2)
          # print(transfer_amount)
          if pdata[str(message.author.id)] < transfer_amount+1:
            await message.channel.send(f"<@{message.author.id}>, you don't have enough TrollCoin for this transfer! :(")
          else:
            pdata[str(message.author.id)] = pdata[str(message.author.id)] - transfer_amount
            pdata[str(message.mentions[0].id)] = pdata[str(message.mentions[0].id)] + transfer_amount
            rdata.seek(0)
            rdata.write(json.dumps(pdata))
            rdata.truncate()
            await message.channel.send(f"<@{message.author.id}>, your transfer of {transfer_amount} to {message.mentions[0].name} was successful!")
    
      except:
        await message.channel.send("Yikes, something went wrong. Perhaps it's because you formatted this command incorrectly. It should be tc!send <usermention> <intamount>. Ignore the <>'s. Good luck!'")
      rdata.close()
    elif pm.startswith(prefix+"gamblehelp"):
      dm = await message.author.create_dm()
      await message.add_reaction("✔️")
      await dm.send(embed = CE(title="Gambling Help",description="**133%** - 1/2 of 133% your amount, 1/2 66% your amount.\n**double** - 1/3 chance of 200% your amount, 2/3 chance of 50% your amount.\n\nHappy gambling!"))
    elif pm.startswith(prefix+"ascend"):
      rdata = open(os.path.join(sys.path[0], "data.txt"),'r+')
      pdata = json.loads(rdata.read())
      if pdata[str(message.author.id)] < 1001:
        await message.channel.send(f"<@{message.author.id}>, you don't have enough TrollCoin to ascend! :(")
      else:
        sure_message = await message.channel.send("You are about to spend 1k~~TC~~ on an invite to TrollCoin heaven. Are you sure if you want to do this?")
        await sure_message.add_reaction("✔️")
        # await sure_message.add_reaction("❌")
        def check(reaction,user):
          return user == message.author and str(reaction.emoji) == "✔️"
        try:
          await client.wait_for("reaction_add",timeout=30,check=check)
        except asyncio.TimeoutError:
          await sure_message.reply("Ok, maybe next time :)")
        else:
          pdata[str(message.author.id)] = pdata[str(message.author.id)] - 1000
          temp_inv = await client.get_channel(836267451574124564).create_invite(unique=True,max_uses=1)
          dm = await message.author.create_dm()
          await dm.send(content=temp_inv)
          rdata.seek(0)
          rdata.write(json.dumps(pdata))
          rdata.truncate()


      rdata.close()
    else: pass
  if pm.startswith("le") and pm in ["".join([x,"o"*(len(pm)-len(x))]) for x in lesgo]:
    await message.add_reaction("👉")
    await message.add_reaction("👶")
    await message.add_reaction("👈")

@client.event
async def on_member_join(member):
  print(member.guild.id)
  if member.guild.id == 836241112561614851:
    await member.add_roles(discord.Object(836405383735017523))
    await client.get_channel(836267451574124564).send(content=random.choice(join_messages).format("<@"+str(member.id)+">"))
  else:pass

@client.event
async def on_guild_join(guild):
  global guild_ids
  print("Joined a guild")
  yo = open(os.path.join(sys.path[0], "guilds.txt"), 'r+')
  guilds=yo.readlines()
  print(guilds)
  guild_ids = [int(f.rstrip("\n")) for f in guilds] # 742422199368941629
  print(guild_ids)
  if guild.id not in guild_ids:
    guild_ids.append(guild.id)
    yo.write(f"\n{int(guild.id)}")
  print(guild_ids)
  
  yo.close()
  await guild.channels[0].send(embed=helpEmbed())

@client.event
async def on_ready(): 
  print("Client info:")
  print()
  print("{0.user} Has been successfully updated!".format(client))
  await client.change_presence(activity = discord.Game(name="tc!help")) # Sets status 
  await client.get_channel(834813365648883744).send(embed = CE(description = "I'm alive"))
  asyncio.create_task(manual_input())

client.run(token)