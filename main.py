import discord
import os
import requests
import json

client = discord.Client()
commands = ["list", "mom", "dad", "cat", "inspire", "epeen"]

def get_cat():
  response = requests.get("https://api.thecatapi.com/v1/images/search")
  json_data = json.loads(response.text)
  cat = json_data[0]["url"]
  return(cat)

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]["q"] + " -" + json_data[0]["a"]
  return(quote)

def get_momjoke():
  response = requests.get("https://api.yomomma.info/")
  json_data = json.loads(response.text)
  joke = json_data["joke"]
  return(joke)

def get_dadjoke():
  response = requests.get("https://icanhazdadjoke.com/slack")
  json_data = json.loads(response.text)
  joke = json_data["attachments"][0]["fallback"]
  return(joke)

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if "!inspire" in msg:
    quote = get_quote()
    await message.channel.send(quote)

  if "!cat" in msg:
    cat = get_cat()
    await message.channel.send(cat)

  if "!mom" in msg:
    momjoke = get_momjoke()
    await message.channel.send(momjoke)

  if "!dad" in msg:
    dadjoke = get_dadjoke()
    await message.channel.send(dadjoke)

  if "!list" in msg:
    await message.channel.send("I don't know much... but I know I love you.  And that may be all I need to know.  Also: " + ' '.join(commands))

  if "!epeen" in msg:
    await message.channel.send("╰⋃╯")


client.run(os.environ['TOKEN'])
