import os

import discord
from discord.ext import tasks, commands

from dotenv import load_dotenv

import getNews

load_dotenv(verbose = True)

# the function that runs the bot
def run_discord_bot():
    TOKEN = os.getenv("TOKEN")
    intents = discord.Intents.default()
    intents.message_content = True
    # use '.' before command in discord for this bot to respond
    bot = commands.Bot(command_prefix = ".", intents = intents)

    # iterating twice a day to get recent news
    @tasks.loop(hours = 12)
    async def scrape():
        result = getNews.getTodayNews()

        if result != 0:
            print(result)
            embed = discord.Embed(title = result[0], url = result[2], description = "새로운 포켓몬 뉴스가 도착했습니다!", color = discord.Color.from_rgb(231, 0, 9))
            embed.set_thumbnail(url = result[1])

            channel = bot.get_channel(1160171194344034374)
            await channel.send(embed = embed)

    @scrape.before_loop
    async def scrape_before():
        await bot.wait_until_ready()

    @bot.event
    async def on_ready():
        print(f"{bot.user} is now running!")

        if not scrape.is_running():
            scrape.start()

        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)

    @bot.tree.command(name = "help")
    async def help(ctx: discord.Interaction):
        await ctx.response.send_message('이전 뉴스들을 확인하려면 "/prevnews"를 입력하세요.', ephemeral = True)

    @bot.tree.command(name = "prevnews")
    async def prevNews(ctx: discord.Interaction):
        allNews = getNews.getPrevNews()
        embeds = []

        for news in allNews:
            embed = discord.Embed(title = news[0], url = news[2], description = f"{str(allNews.index(news) + 1)}번째 오래된 뉴스", color = discord.Color.from_rgb(231, 0, 9))
            embed.set_thumbnail(url = news[1])
            embed.add_field(name = "업데이트 날짜:", value = news[3], inline = False)
            embeds.append(embed)

        await ctx.response.send_message(embeds = embeds)

    bot.run(TOKEN)