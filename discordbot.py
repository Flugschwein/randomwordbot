from discord.ext import commands
import requests
import random

with open('english-words/words_alpha.txt', 'r') as words, open('blacklist.txt', 'r') as black:
    wordlist = requests.get('http://www-personal.umich.edu/~jlawler/wordlist')
    wordlists = {
        'long': set(map(str.rstrip, words.readlines())),
        'short': set(map(bytes.decode, wordlist.content.splitlines())),
    }
    blacklist = set(map(str.rstrip, black.readlines()))
    standard = 'short'
    maximum_words = 20

bot = commands.Bot(command_prefix='$')


@bot.command()
async def word(ctx, *words):
    """Returns a random english word.
    You can also choose to only get words out of a specific list or to get more than one word.
    !word list count returns count words out of list.
    Use !lists to get available lists.
    """
    if len(words) > 2:
        await ctx.send('Only provide 2 arguments.')
        return
    elif words:
        count = 1
        chosen_list = standard
        for arg in words:
            try:
                count = int(arg)
            except ValueError:
                if arg in wordlists.keys():
                    chosen_list = arg
        random_words = random.sample(wordlists[chosen_list] - blacklist, k=min([count, maximum_words]))
        await ctx.send('\n'.join(random_words))
    else:
        await ctx.send(random.sample(wordlists[standard] - blacklist, 1)[0])


@bot.command()
async def random_wiki(ctx, *args):
    """Returns random Wikipedia entry.
     Use language code (e.g. de or en) to choose language."""
    if len(args) == 1:
        lang = args[0]
    else:
        lang = 'en'
    rand_entry = requests.get(f'https://{lang}.wikipedia.org/wiki/Special:Random')
    await ctx.send(f'<{rand_entry.url}>')


@bot.command()
async def blacklist_word(ctx, *args):
    """Adds word(s) to the blacklist."""
    global blacklist
    for word in args:
        if word in blacklist:
            await ctx.send(f'{word} is already in blacklist.')
        else:
            with open('blacklist.txt', 'a') as f:
                f.write(word + '\n')
                blacklist.add(word)
            await ctx.send(f'Blacklisted {word}')


@bot.command()
async def remove_from_blacklist(ctx, word):
    """Removes word from the blacklist."""
    global blacklist
    if word not in blacklist:
        await ctx.send(f'{word} is not in the blacklist.')
    else:
        blacklist.remove(word)
        with open('blacklist.txt', 'w') as f:
            f.write('\n'.join(blacklist))
        await ctx.send(f'Removed {word} from the blacklist.')


@bot.command()
async def check_word(ctx, arg):
    """Checks if word exists on any list."""
    if arg in blacklist:
        await ctx.send(f'{arg} is in the blacklist.')
    else:
        contain_word = []
        for key in wordlists:
            if arg in wordlists[key]:
                contain_word.append(key)
        if not contain_word:
            await ctx.send(f'{arg} is not in any list.')
        else:
            await ctx.send(f'{arg} is in the following list(s): {", ".join(contain_word)}')


@bot.command()
async def lists(ctx):
    """Returns available wordlists."""
    await ctx.send(f'Available lists: {", ".join(wordlists.keys())}')


@bot.event
async def on_ready():
    print('Ready to go!')


if __name__ == '__main__':
    bot.run('TOKEN')
