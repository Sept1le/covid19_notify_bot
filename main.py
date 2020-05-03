import discord
from discord.ext import commands

import asyncio

from config import TOKEN, message_about_covid, region_statsg

from parse import Parser

import pymorphy2
import progressbar

count_in_russia = 'test'
count_in_world = 'test'
# count_in_region = 2

class covidBot(commands.Cog):
    morph = pymorphy2.MorphAnalyzer()
    human = morph.parse('человек')[0]

    def __init__(self, bot):
        self.bot = bot
        self.p = Parser()

    @commands.command(name='about', brief='информация о коронавирусе')
    async def about(self, ctx):
        await ctx.send(message_about_covid)

    @commands.command(name='stats', brief='Показывает общую статистику')
    async def stats(self, ctx):
        await ctx.send(f'Заражено в 🇷🇺 России: {None} чел.👥\nЗаражено в 🗺️ мире: {None} чел.👥')

    @commands.command(name='region_stats', brief='"название области" "обл." - информация о регионе')
    async def change_region(self, ctx, region_first_name, region_second_name):
        city = ' '.join([region_first_name, region_second_name])

        await ctx.send(f'({city}) ↗ Всего случаев: {self.p.region_all(city)}\n⌚Сегодня: {self.p.region_new(city)}\n🦠Болеет: {self.p.region_sick(city)}\n💊Выздоровело: {self.p.region_healthy(city)}\n💀Умерло: {self.p.region_dead(city)}')

    @commands.command(name='regions_stats', brief='информация по регионам РФ')
    async def regions_stats(self, ctx):
        msg = []
        await ctx.send('Это может занять некотрое время. Подождите...👨🏿‍💻')
        regions = self.p.region_list()

        for i in progressbar.progressbar(regions):
            msg.append(f'({i}) ↗ Всего случаев: {self.p.region_all(i)} ⌚Сегодня: {self.p.region_new(i)} 🦠Болеет: {self.p.region_sick(i)} 💊Выздоровело: {self.p.region_healthy(i)} 💀Умерло: {self.p.region_dead(i)}\n')
            msg.append('')

        for i in msg:
            await ctx.send(i)


bot = commands.Bot(command_prefix='!')
bot.add_cog(covidBot(bot))
bot.run(TOKEN)
