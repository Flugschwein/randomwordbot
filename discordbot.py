from discord.ext import commands
import requests
import random

wordlist = requests.get('http://www-personal.umich.edu/~jlawler/wordlist')
wordlist = wordlist.content.splitlines()
print(wordlist)

bot = commands.Bot(command_prefix='!',
                   )

@bot.command()
async def word(ctx):
    """This returns a random english word"""
    await ctx.send(random.choice(wordlist).decode())

if __name__ == '__main__':
    bot.run('TOKEN')
