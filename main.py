import datetime
import discord
from discord import FFmpegPCMAudio
from discord.ext.commands import has_permissions
from discord.ext import commands

import requests
def kelvin_to_celsius(kelvin):
    celcius = kelvin - 273.15
    return celcius
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = "a183867e11072cb21eede02960128429"
CITY = "Opwijk"
url = f"https://api.openweathermap.org/data/2.5/weather?lat=50.9690529&lon=4.1896665&appid={API_KEY}"
response = requests.get(url.format(CITY)).json()
temp_kelvin = response['main']['temp']
temp_celcius = kelvin_to_celsius(temp_kelvin)
feels_like_kelvin = response['main']['feels_like']
feels_like_celcius = kelvin_to_celsius(feels_like_kelvin)
humidity = response['main']['humidity']
description = response['weather'][0]['description']
sunrise_time = datetime.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
sunset_time =  datetime.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])

queues = {}
queue = {}

def check_queue(ctx, id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)

def run_discord_bot():
    token = 'You_Tried'
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix='seal', intents=intents)

    @client.event
    async def on_ready():
      print(f'{client.user} is now running')
      print("------------------------------")

    @client.command()
    @has_permissions(kick_members=True)
    async def kick(ctx, member: discord.Member, *, reason = None):
        await member.kick(reason=reason)
        await ctx.reply(f'User {member} has been sent to the (temporary) underworld!')
    @kick.error
    async def kick_error(error, ctx):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('You cannot send people to the (temporary) underworld! ')

    @client.command()
    @has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, reason = None):
        await member.ban(reason=reason)
        await ctx.reply(f'User {member} has been sent to the underworld.')
    @kick.error
    async def ban_error(error, ctx):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('You cannot send people to the underworld! ')


    @client.command()
    async def hello(ctx):
      await ctx.reply("Hello, I am Sealbot")

    @client.command()
    async def weather(ctx):
        await ctx.reply(f"Temperature in {CITY}: {temp_celcius:.2f}*C"
               f"\nTemperature in {CITY} feels like : {feels_like_celcius}*C" 
              f"\nHumidity in {CITY}: {humidity}%"
               f"\nGeneral Weather in {CITY}: {description}"
               f"\nSun rises in {CITY} at {sunrise_time} local time."
               f"\nSun sets in {CITY} at {sunset_time} local time. ")
    @client.command(pass_context = True)
    async def join(ctx):
        if(ctx.author.voice):
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
        else:
            await ctx.reply("You are not in a voice channel, enter a voice channel and try again!")


    @client.command(pass_context = True)
    async def leave(ctx):
        if (ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
            await ctx.reply("I left the voice channel")
        else:
            await ctx.reply("I am not in a voice channel")

    @client.command()
    @commands.has_role('Admin')
    async def die(ctx):
        exit()

    @client.command()
    async def musichelp(ctx):
        await ctx.reply("```Current songs:\n-----------------\nExample: songcommand - artisname\nICantFixYou - The Living Tombstone\nFlyAway - TheFatRat\nCrabRave - Noisestorm"
                       "\nVivaLaVida - Coldplay\nGigaChadThemePhonk - g3oxem\nO-Zone - Dragostea Din Tei\nFeelGoodInc. - Gorrilaz"
                        "\nEverybodyDanceNow - C&C Music Factory```")

    @client.command()
    async def pause(ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client
        voice_channel.pause()
        print('pause')

    @client.command()
    async def resume(ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client
        voice_channel.resume()
        print('resume')

    @client.command()
    async def stop(ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client
        voice_channel.stop()
        print('resume')




    @client.command()
    async def play(ctx, arg):
           voice = ctx.guild.voice_client
           source = FFmpegPCMAudio(arg + '.mp3')
           player = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id))
           await ctx.reply(f"I will now play {arg}")
    @client.command()
    @commands.has_role('Admin')
    async def rules(ctx):
        await ctx.send("```Rules:\n---------------------```\nhttps://media.discordapp.net/attachments/873087608522174484/984426708583202836/giphy.gif")

    @client.command()
    async def playingaudio(ctx):
        if ctx.voice_client.is_playing():
            await ctx.reply("Playing audio :)")
        else:
            await ctx.reply("Nothing is playing")


    @client.command(pass_context = True)
    async def queue(ctx, arg):
        voice = ctx.guild.voice_client
        source = FFmpegPCMAudio(arg + '.mp3')
        guild_id = ctx.message.guild.id
        if guild_id in queues:
            queues[guild_id].append(source)
            await ctx.reply(f"I added {arg} to the queue")
        else:
            queues[guild_id] = [source]
            await ctx.reply(f"{arg} isn't in my music library!")



    client.run(token)
if __name__ == '__main__':
  run_discord_bot()
