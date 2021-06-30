import os
import discord
import requests
import json
import urllib
import random
import html
import pyshorteners
from xml.dom.minidom import parseString
from discord.ext import commands
from replit import db

bot = commands.Bot(command_prefix='!')
yelp_token = os.environ['YELP_TOKEN']
pbotid = os.environ['PBOTID']
pcustid = os.environ['PCUSTID']
shorty = pyshorteners.Shortener()


@bot.command(name='cat', help='Responds with a random cat picture')
async def cat(ctx):
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    json_data = json.loads(response.text)
    catURL = json_data[0]["url"]
    await ctx.send(catURL)


@bot.command(name='pitch',
             help='Responds with a random sales pitch business idea')
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
    response = requests.get(
        "https://www.pandorabots.com/pandora/talk-xml?botid=" + pbotid +
        "&custid=" + pcustid + "&input=" + urllib.parse.quote(args))
    dom3 = parseString(response.text)
    name = dom3.getElementsByTagName('that')
    await ctx.send(name[0].firstChild.nodeValue)


@bot.command(name='yelp',
             help='Search yelp for businesses matching your search')
async def get_yelp(ctx, *, args):
    response = requests.get(
        "https://api.yelp.com/v3/businesses/search?location=64081&limit=10&term="
        + urllib.parse.quote(args),
        headers={"Authorization": "Bearer " + yelp_token})
    json_data = json.loads(response.text)
    results = "Here are some suggestions:"
    for business in json_data["businesses"]:
        results += '\n' + business['name'] + " " + str(
            business['rating']) + " stars. web: " + shorty.tinyurl.short(
                business['url'])
    await ctx.send(results)


@bot.command(name='meme', help="Get you a random meme from reddit")
async def get_meme(ctx):
    response = requests.get("https://meme-api.herokuapp.com/gimme/dankmemes")
    json_data = json.loads(response.text)
    memeURL = json_data["url"]
    await ctx.send(memeURL)


@bot.command(name='trivia', help="Displays a random trivia fact")
async def get_trivia(ctx):
    response = requests.get("https://opentdb.com/api.php?amount=1")
    json_data = json.loads(response.text)
    question = json_data["results"][0]["question"]
    correctAnswer = json_data["results"][0]["correct_answer"]
    incorrectAnswers = json_data["results"][0]["incorrect_answers"]
    incorrectSize = len(incorrectAnswers)
    allAnswers = [correctAnswer, incorrectAnswers[0]]
    if incorrectSize > 1:
        allAnswers.append(incorrectAnswers[1])
        allAnswers.append(incorrectAnswers[2])
    random.shuffle(allAnswers)
    result = question + '\n' + "A: " + allAnswers[
        0] + '\n' + "B: " + allAnswers[1]
    if incorrectSize > 1:
        result += '\n' + "C: " + allAnswers[2] + '\n' + "D: " + allAnswers[3]
    result += '\n' + "Correct Answer : " + "||" + correctAnswer.ljust(
        50, ' ') + "||"
    unescapedResult = html.unescape(result)
    await ctx.send(unescapedResult)


@bot.command(
    name='playtrivia',
    help=
    "Shows a random trivia fact that can then be answered for points using !answer"
)
async def get_playtrivia(ctx):
    #check to see if there's already a question in context
    correctLetter = db["CURRENT_TRIVIA_ANSWER"]
    if correctLetter != "":
        await ctx.send('Calm your tits man, one question at a time')
    else:
        response = requests.get("https://opentdb.com/api.php?amount=1")
        json_data = json.loads(response.text)
        question = json_data["results"][0]["question"]
        correctAnswer = json_data["results"][0]["correct_answer"]
        incorrectAnswers = json_data["results"][0]["incorrect_answers"]
        incorrectSize = len(incorrectAnswers)
        allAnswers = [correctAnswer, incorrectAnswers[0]]
        if incorrectSize > 1:
            allAnswers.append(incorrectAnswers[1])
            allAnswers.append(incorrectAnswers[2])
        random.shuffle(allAnswers)
        result = question + '\n' + "A: " + allAnswers[
            0] + '\n' + "B: " + allAnswers[1]
        if incorrectSize > 1:
            result += '\n' + "C: " + allAnswers[2] + '\n' + "D: " + allAnswers[
                3]
        unescapedResult = html.unescape(result)
        #set correct answer in db so we can check the answer later
        correctIndex = allAnswers.index(correctAnswer)
        correctLetter = ["A", "B", "C", "D"][correctIndex]
        db["CURRENT_TRIVIA_ANSWER"] = correctLetter
        await ctx.send(unescapedResult)


@bot.command(
    name='answer',
    help=
    'Use to answer the most recently asked trivia question by passing in the letter of the correct answer'
)
async def answer(ctx, arg):
    if arg.strip().upper() not in ["A", "B", "C", "D"]:
        await ctx.send('Send in a valid letter answer, dummy')
    else:
        correctLetter = db["CURRENT_TRIVIA_ANSWER"]
        if correctLetter not in ["A", "B", "C", "D"]:
            await ctx.send(
                'There doesn\'t seem to be a trivia question awaiting an answer'
            )
        else:
            db["CURRENT_TRIVIA_ANSWER"] = ""
            if (arg.strip().upper() == correctLetter):
                currentValue = 0
                member_id = ctx.author.id
                if str(member_id) + "_TRIVIAPOINTS" in db:
                    currentValue = db[str(member_id) + "_TRIVIAPOINTS"]
                currentValue += 1
                db[str(member_id) + "_TRIVIAPOINTS"] = currentValue
                await ctx.send('Correct!\n' + ctx.author.display_name +
                               ' now has ' + str(currentValue) +
                               ' trivia points')
            else:
                await ctx.send('Wrong, idiot!')


@bot.command(name='howsmartis', help='See how many trivia points a user has')
async def howsmartis(ctx, arg):
    member_id = int(arg.strip('<@!>'))
    member = await bot.fetch_user(member_id)
    currentValue = 0
    if str(member_id) + "_TRIVIAPOINTS" in db:
        currentValue = db[str(member_id) + "_TRIVIAPOINTS"]
    await ctx.send('{0.display_name} has {1} trivia points'.format(
        member, currentValue))


@bot.command(name='ping', help='Ping the bot to text name', hidden=True)
async def ping(ctx):
    await ctx.send('Pong ' + format(ctx.author.display_name))


@bot.command(name='lookup', help='Display info on a member')
async def lookup(ctx, arg):
    member_id = int(arg.strip('<@!>'))
    member = await bot.fetch_user(member_id)
    await ctx.send('{0}\nNickname: {0.display_name}'.format(member))


@bot.command(name='niceone', help='Give one cool guy point to a user')
async def niceone(ctx, arg):
    member_id = int(arg.strip('<@!>'))
    member = await bot.fetch_user(member_id)
    currentValue = 0
    if str(member_id) + "_CGPOINTS" in db:
        currentValue = db[str(member_id) + "_CGPOINTS"]
    currentValue += 1
    db[str(member_id) + "_CGPOINTS"] = currentValue
    await ctx.send('{0.display_name} has {1} cool guy points'.format(
        member, currentValue))


@bot.command(name='howcoolis',
             help='Check how many cool guy points a user has')
async def howcoolis(ctx, arg):
    member_id = int(arg.strip('<@!>'))
    member = await bot.fetch_user(member_id)
    currentValue = 0
    if str(member_id) + "_CGPOINTS" in db:
        currentValue = db[str(member_id) + "_CGPOINTS"]
    await ctx.send('{0.display_name} has {1} cool guy points'.format(
        member, currentValue))


@bot.command(name='kanye', help='Get some inspiration from Yeezus')
async def kanye(ctx):
    response = requests.get("https://api.kanye.rest/")
    json_data = json.loads(response.text)
    # create a quote like embed: https://cog-creators.github.io/discord-embed-sandbox/
    embed = discord.Embed(title=json_data['quote'])
    embed.set_author(
        name="Kanye West",
        icon_url=
        "https://freepngimg.com/download/kanye_west/11-2-kanye-west-png-pic.png"
    )
    await ctx.send(embed=embed)


bot.run(os.environ['TOKEN'])
