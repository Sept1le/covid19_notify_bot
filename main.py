import discord
from discord.ext import commands

import asyncio

from config import TOKEN, message_about_covid, region_statsg

from parse import Parser

import pymorphy2
import progressbar


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
        self.p.get_world()
        r = self.p.rus_stats()
        w = self.p.world_stats()
        await ctx.send(f'Росиия 🇷🇺 ↗ Всего случаев: {r[0]} ⌚Сегодня: {r[1]} 🦠Болеет: {r[2]} 💊Выздоровело: {r[3]} 💀Умерло: {r[4]}\n')
        await ctx.send(f'Мир🗺️ ↗ Всего случаев: {w[0]} ⌚Сегодня: {w[1]} 🦠Болеет: {w[2]} 💊Выздоровело: {w[3]} 💀Умерло: {w[4]}\n')

    @commands.command(name='region_stats', brief='"название области" "обл." - информация о регионе')
    async def change_region(self, ctx, region_first_name, region_second_name):
        city = ' '.join([region_first_name, region_second_name])
        self.p.get_russian_regions()
        await ctx.send(f'({city}) ↗ Всего случаев: {self.p.region_all(city)}\n⌚Сегодня: {self.p.region_new(city)}\n🦠Болеет: {self.p.region_sick(city)}\n💊Выздоровело: {self.p.region_healthy(city)}\n💀Умерло: {self.p.region_dead(city)}')

    @commands.command(name='regions_stats', brief='информация по регионам РФ')
    async def regions_stats(self, ctx):
        self.p.get_russian_regions()
        msg = []
        await ctx.send('Это может занять некотрое время. Подождите...👨🏿‍💻')

        for i in self.p.russian_dic:
            msg.append(f'({i}) ↗ Всего случаев: {self.p.region_all(i)} ⌚Сегодня: {self.p.region_new(i)} 🦠Болеет: {self.p.region_sick(i)} 💊Выздоровело: {self.p.region_healthy(i)} 💀Умерло: {self.p.region_dead(i)}\n')
            msg.append('-')

        for i in msg:
            await ctx.send(i)


    @commands.command(name='world_stats', brief='информация по странам')
    async def regions_stats(self, ctx):
        self.p.get_world()
        msg = []
        await ctx.send('Это может занять некотрое время. Подождите...👨🏿‍💻')

        for i in self.p.world_dic:
            msg.append(f'({i}) ↗ Всего случаев: {self.p.world_all(i)} ⌚Сегодня: {self.p.world_new(i)} 🦠Болеет: {self.p.world_sick(i)} 💊Выздоровело: {self.p.world_healthy(i)} 💀Умерло: {self.p.world_dead(i)}\n')
            msg.append('-')

        for i in msg:
            await ctx.send(i)


bot = commands.Bot(command_prefix='!')
bot.add_cog(covidBot(bot))
bot.run(TOKEN)
