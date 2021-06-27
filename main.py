import os
import requests
import json
import urllib
from xml.dom.minidom import parseString
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
yelp_token = os.environ['YELP_TOKEN']
pbotid = os.environ['PBOTID']
pcustid = os.environ['PCUSTID']

@bot.command(name='cat', help='Responds with a random cat picture')
async def cat(ctx):
  response = requests.get("https://api.thecatapi.com/v1/images/search")
  json_data = json.loads(response.text)
  catURL = json_data[0]["url"]
  await ctx.send(catURL)

@bot.command(name='pitch', help='Responds with a random sales pitch business idea')
async def get_pitch(ctx):
  response = requests.get("https://itsthisforthat.com/api.php?text")
  await ctx.send(response.text)

@bot.command(name='zen', help='Responds with a random zen quote')
async def get_quote(ctx):
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]["q"] + " -" + json_data[0]["a"]
  await ctx.send(quote)

@bot.command(name='mom', help='Responds with a random Yo Momma! joke')
async def get_momjoke(ctx):
  response = requests.get("https://api.yomomma.info/")
  json_data = json.loads(response.text)
  joke = json_data["joke"]
  await ctx.send(joke)

@bot.command(name='dad', help='Responds with a random dad joke')
async def get_dadjoke(ctx):
  response = requests.get("https://icanhazdadjoke.com/slack")
  json_data = json.loads(response.text)
  joke = json_data["attachments"][0]["fallback"]
  await ctx.send(joke)

@bot.command(name='ama', help='Ask me anything')
async def get_test(ctx, *, args):
  response = requests.get("https://www.pandorabots.com/pandora/talk-xml?botid=" + pbotid + "&custid=" + pcustid + "&input=" + urllib.parse.quote(args))
  dom3 = parseString(response.text)
  name = dom3.getElementsByTagName('that')
  await ctx.send(name[0].firstChild.nodeValue)

bot.run(os.environ['TOKEN'])
