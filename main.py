import discord
from discord.ext import commands

import asyncio

from config import TOKEN, message_about_covid

class covidBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        print('logged on as', self.user)

    async def on_message(self, message):
        pass

    @commands.command(name='about')
    async def about(self, ctx):
        await ctx.send(message_about_covid)

    @commands.command(name='stats')
    async def stats(self, ctx):
        await ctx.send(f'Заражено в 🇷🇺 России: {count_in_russia}\nЗаражено в 🗺️ мире: {count_in_world} чел.👥')

    @commands.command(name='change_region')
    async def change_region(self, ctx, region_name):
        await ctx.send(f'В {region_name} заражено {count_in_region} чел.👥')


bot = commands.Bot(command_prefix='!')
bot.add_cog(covidBot(bot))
bot.run(TOKEN)