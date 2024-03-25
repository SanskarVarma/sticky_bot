import disnake
from disnake.ext import commands
from disnake import Embed
import config


bot = commands.Bot(command_prefix='=', intents=disnake.Intents.all())

stickies_enabled = True  #this will keep a check for <stickstop> and <stickstart>
stored_messages = []     #all the stickies are stored in it

@bot.event
async def on_ready():
    print(f'✅ Logged in as sticky_bot ')

@bot.command()
async def stick(ctx, *, message: str):
    if stickies_enabled:
        stored_messages.append(message)
        await ctx.send(f'Stored stick: {message}')
    else:
        await ctx.send("Stickies pinning is currently disabled.")

@bot.command()
async def stickstop(ctx):
    global stickies_enabled
    stickies_enabled = False
    await ctx.send("Stickies pinning has been stopped.")

@bot.command()
async def stickstart(ctx):
    global stickies_enabled
    stickies_enabled = True
    await ctx.send("Stickies pinning has been started.")

@bot.command()
async def showstick(ctx):
    if stored_messages:
        await ctx.send("Stored Stickies:")
        for msg in stored_messages:
            if isinstance(msg, str):
                await ctx.send(msg)
            elif isinstance(msg, Embed):
                await ctx.send(embed=msg)
    else:
        await ctx.send("No messages stored.")

@bot.command()
async def stickremove(ctx):
    global stored_messages
    stored_messages = []
    await ctx.send("All stickied messages have been removed.")

@bot.command()
async def getstickies(ctx):
    if stored_messages:
        await ctx.send("Stored Stickies:")
        for msg in stored_messages:
            if isinstance(msg, str):
                await ctx.send(msg)
            elif isinstance(msg, Embed):
                await ctx.send(embed=msg)
    else:
        await ctx.send("No messages stored.")

@bot.command()
async def stickembed(ctx, *, description: str):
    embed = Embed(description=description)
    stored_messages.append(embed)
    await ctx.send("Embed sticky created and stored successfully!")

@bot.command()
async def stickwebhook(ctx, name: str):
    author = ctx.author
    avatar_url = author.avatar.url if author.avatar else author.default_avatar.url
    
    embed = Embed(title=name, description="User's profile picture:", color=author.color)
    embed.set_image(url=avatar_url)
    
    stored_messages.append(embed)
    await ctx.send("Embed sticky with custom name and user's profile picture created and stored successfully!")

@bot.event
async def on_message(message):
    if not message.content.startswith(bot.command_prefix):
        if stickies_enabled and stored_messages and message.author != bot.user:
            last_sticky = stored_messages[-1]
            
            async for msg in message.channel.history(limit=5):
                if msg.author == bot.user and (isinstance(msg, disnake.Message) or isinstance(msg, disnake.Embed)):
                    await msg.delete()
                    break
            
            if isinstance(last_sticky, str):
                await message.channel.send(last_sticky)
            elif isinstance(last_sticky, Embed):
                await message.channel.send(embed=last_sticky)
    
    await bot.process_commands(message)

bot.run(config.TOKEN)
