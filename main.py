import discord
from discord.ext import commands

import asyncio

from config import TOKEN, message_about_covid, help_message

import pymorphy2

# count_in_russia = 'test'
# count_in_world = 'test'
# count_in_region = 2

class covidBot(commands.Cog):
    morph = pymorphy2.MorphAnalyzer()
    human = morph.parse('человек')[0]

    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        print('logged on as', self.user)

    async def on_message(self, message):
        pass

    @commands.command(name='about', brief='информация о коронавирусе')
    async def about(self, ctx):
        await ctx.send(message_about_covid)

    @commands.command(name='stats', brief='Показывает общую статистику')
    async def stats(self, ctx):
        await ctx.send(f'Заражено в 🇷🇺 России: {count_in_russia} чел.👥\nЗаражено в 🗺️ мире: {count_in_world} чел.👥')
        await ctx.send('test')

    @commands.command(name='region_stats', brief='"название области" - информация о регионе')
    async def change_region(self, ctx, region_first_name, region_second_name):
        if str(count_in_region).endswith('1'):
            await ctx.send(f'В {region_first_name} {region_second_name} заражен {count_in_region} {self.human.make_agree_with_number(count_in_region).word}.👥')
        else:
            await ctx.send(f'В "{region_first_name} {region_second_name}" заражены {count_in_region} {self.human.make_agree_with_number(count_in_region).word}.👥')


bot = commands.Bot(command_prefix='!')
bot.add_cog(covidBot(bot))
bot.run(TOKEN)
