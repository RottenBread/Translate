import os
import sys
import json
import urllib.request
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
client_id = "-" # 개발자센터에서 발급받은 Client ID 값
client_secret = "-" # 개발자센터에서 발급받은 Client Secret 값

def detectCountry(getMsg):
    try:
        query = urllib.parse.quote(getMsg)
        data = "query=" + query
        url = "https://openapi.naver.com/v1/papago/detectLangs"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        response_body = response.read()
        result = response_body.decode('utf-8')
        result2 = json.loads(result)
        result3 = result2['langCode']
        return result3
    except:
        pass

def autoTranslate(getMsg, getCountry):
    query = urllib.parse.quote(getMsg)
    data = f"source={getCountry}&target=ko&text=" + query
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    response_body = response.read()
    result = response_body.decode('utf-8')
    result2 = json.loads(result)
    result3 = result2['message']['result']['translatedText']
    return result3

@bot.command()
async def 번역(ctx, *, msg):
    result = detectCountry(msg)
    try:
        result2 = autoTranslate(msg, result)
        embed = discord.Embed(title= ":book: 번역", color = 0x00ff00)
        embed.add_field(name = f'{result} -> ko', value = f'{result2}')
        embed.set_footer(text = "번역봇")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/579272051282542595/1101400352533794957/png-transparent-google-translate-translation-computer-icons-google-removebg-preview.png")
        await ctx.send(embed = embed, reference=ctx.message)
    except:
        embed = discord.Embed(title= ":book: 번역", color = 0xa63641)
        embed.add_field(name = 'Error', value = "번역체는 한글일 수 없습니다.")
        embed.set_footer(text = "번역봇")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/579272051282542595/1101400352533794957/png-transparent-google-translate-translation-computer-icons-google-removebg-preview.png")
        await ctx.send(embed = embed, reference=ctx.message)

bot.run('-')
