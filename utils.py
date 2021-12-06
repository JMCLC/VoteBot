import discord
import time

def createPoll(author, title):
    poll = discord.Embed(title = title, description="Reajam com ✅ ou ❌.",  color=0xd10a07)
    poll.set_author(name=author.display_name, icon_url=author.display_avatar)
    return poll

def newEmbed(title):
    return discord.Embed(title=title, color = 0xd10a07)

def PollSuccess(poll):
    yes = 0
    no = 0
    for reaction in poll.reactions:
        if reaction.emoji == '✅':
            yes = reaction.count
        elif reaction.emoji == '❌':
            no = reaction.count
    if yes > no and yes > 2:
        return True
    return False

def getMemberFromMention(ctx, user):
    for channel in ctx.guild.channels:
        if channel.type.name == "voice" and len(channel.members) > 0:
            if ctx.author in channel.members:
                for member in channel.members:
                    mention = member.mention
                    if '!' in mention:
                        mention = mention.replace("!", "")
                    if mention == user:
                        return member
    return

def getUserNameFromMention(ctx, user):
    res = user
    for channel in ctx.guild.channels:
        if channel.type.name == "voice" and len(channel.members) > 0:
                for member in channel.members:
                    mention = member.mention
                    if '!' in mention:
                        mention = mention.replace("!", "")
                    if mention == user:
                        res = member.display_name
    return res

def isUserInSameVoiceChannel(ctx, user):
    for channel in ctx.guild.channels:
        if channel.type.name == "voice" and len(channel.members) > 0:
            if ctx.author in channel.members:
                for member in channel.members:
                    mention = member.mention
                    if '!' in mention:
                        mention = mention.replace("!", "")
                    if mention == user:
                        return True
    return False

def isUserInCooldown(cooldowns, cooldownTime, user):
    if user in cooldowns and int(time.time()) - cooldowns[user] <= cooldownTime:
            return True
    return False