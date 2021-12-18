import json
import discord
import utils
import time
import random
from discord.commands import permissions
from discord.commands import Option


bot = discord.Bot()

config = json.load(open('config.json'))
token = json.load(open("token.json"))
guild = int(token['guildId'])
guild2 = int(token['guildId2'])
pollTime = int(config['pollTime'])
cooldownTime = int(config['cooldown'])
cooldowns = {}

@bot.slash_command(guild_ids=[guild, guild2], default_permission=True)
async def votekick(ctx, target: Option(str, "Enter your Target")):
    """Create a vote to kick someone from your voice channel"""
    if '!' in target:
        target = target.replace("!", "")
    if not utils.isUserInSameVoiceChannel(ctx, target):
        await ctx.respond("Apenas podes kickar users que estejam no teu voice chat")
        return
    poll = utils.createPoll(ctx.author, f"Kickar: {utils.getUserNameFromMention(ctx, target)}!")
    await ctx.respond(embed = poll)
    message = ctx.channel.last_message
    if not message:
        print("ERROR: Message was Deleted")
        return
    await message.add_reaction("✅")
    await message.add_reaction("❌")
    time.sleep(pollTime)    
    if (utils.isUserInCooldown(cooldowns, cooldownTime, target)):
        await message.edit(embed = utils.newEmbed(message.embeds[0].title + " User está em cooldown"))
        return
    message = await ctx.channel.fetch_message(message.id)
    if not message:
        print("ERROR: Message was deleted")
        return
    if utils.PollSuccess(message):
        user = utils.getMemberFromMention(ctx, target)
        if user:
            await user.move_to(None)
        cooldowns[target] = int(time.time())
        chance = random.randint(1, 100)
        if chance <= int(config["clearChannel"]):
            channel = utils.getUserVoiceChannel(ctx)
            for member in channel.members:
                await member.move_to(None)
            await message.edit(embed = utils.newEmbed(message.embeds[0].title + " Por sorte toda a gente no canal foi kickada"))
        elif chance <= int(config['selfkick']):
            author = ctx.author.mention
            if '!' in author:
                author = author.replace("!", "")
            if (target != author):
                author = utils.getMemberFromMention(ctx, author)
                if author:
                    await author.move_to(None)
                    await message.edit(embed = utils.newEmbed(message.embeds[0].title + " User foi kickado e por sorte o mongo que criou a votação também"))
                else:
                    await message.edit(embed = utils.newEmbed(message.embeds[0].title + " O mongo que criou a votação saiu antes de poder ser kickado"))
        elif chance <= int(config["clearChannel"]):
            channel = utils.getUserVoiceChannel(ctx)
            for members in channel:
                await members.move_to(None)
            await message.edit(embed = utils.newEmbed(message.embeds[0].title + " Por sorte toda a gente no canal foi kickada"))
        elif not user:
            await message.edit(embed = utils.newEmbed(message.embeds[0].title + " User saiu antes de poder ser kickado"))
        else:
            await message.edit(embed = utils.newEmbed(message.embeds[0].title + " User foi kickado"))
    else:
        await message.edit(embed = utils.newEmbed(message.embeds[0].title + " A Poll falhou"))

@bot.slash_command(guild_ids=[guild, guild2])
@permissions.permission(user_id = int(token["defaultUser"]), permission = True)
async def changeconfig(ctx, target: Option(str, "Enter your Target"), value: Option(str, "Enter your new value")):
    """Change the values saved on config.json"""
    with open("config.json", "r") as jsonFile:
        data = json.load(jsonFile)
    if target in data:
        data[target] = value
        with open("config.json", "w") as jsonFile:
            json.dump(data, jsonFile)
        await ctx.respond(embed = utils.newEmbed("Valores alterados"))
    else:
        await ctx.respond(embed = utils.newEmbed("Este valor não existe"))

@bot.slash_command(guild_ids=[guild, guild2])
@permissions.permission(user_id = int(token["defaultUser"]), permission = True)
async def dumpconfig(ctx):
    """Dumps the content of config.json as a response"""
    with open("config.json", "r") as jsonFile:
        data = json.load(jsonFile)
    await ctx.respond(embed = utils.newEmbed("Valores Guardados: \n" + str(data)))

bot.run(token['token'])