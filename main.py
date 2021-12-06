import json
import discord
import utils
import time
import random
from discord.commands import Option


bot = discord.Bot()

config = json.load(open('config.json'))
guild = int(config['guildId'])
pollTime = int(config['pollTime'])
cooldownTime = int(config['cooldown'])
cooldowns = {}

@bot.slash_command(guild_ids=[guild], default_permission=True)
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
        await utils.getMemberFromMention(ctx, target).move_to(None)
        cooldowns[target] = int(time.time())
        chance = random.randint(1, 100)
        if chance <= int(config['selfkick']):
            author = ctx.author.mention
            if '!' in author:
                author = author.replace("!", "")
            if (target != author):
                await utils.getMemberFromMention(ctx, author).move_to(None)
                await message.edit(embed = utils.newEmbed(message.embeds[0].title + " User foi kickado e por sorte o mongo que criou a votação também"))
        else:
            await message.edit(embed = utils.newEmbed(message.embeds[0].title + " User foi kickado"))
    else:
        await message.edit(embed = utils.newEmbed(message.embeds[0].title + " A Poll falhou"))

bot.run(config['token'])