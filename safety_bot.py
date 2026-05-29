import os
from discord.ext import commands
from datetime import timedelta

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Customize your list of banned words here (keep them lowercase)
BANNED_WORDS = ["fuck", "cunt", "cum", "dick", "shit", "ni-", "nigger", "azs", "ass", "f-", "azz", "$hit", "@ss", "fu-", "fuc","sh-", "s-", "bitch", "puto", "gaey", "gay", "puta"]

# This dictionary keeps track of how many warnings a user has
user_warnings = {}

@bot.event
async def on_ready():
    print(f"Connected gateway safety bar online.")
    print(f"The safety bar is online and protecting the server as {bot.user}")

@bot.event
async def on_message(message):
    # Prevent the bot from checking its own messages
    if message.author == bot.user:
        return

    # Check if any banned word is in the message
    message_content_lower = message.content.lower()
    if any(word in message_content_lower for word in BANNED_WORDS):
        try:
            # Delete the bad message first
            await message.delete()
            
            user_id = message.author.id
            
            # If they aren't in the warning list yet, give them their 1st warning
            if user_id not in user_warnings:
                user_warnings[user_id] = 1
                await message.channel.send(f"{message.author.mention}, that word is not allowed here! Consider this your only warning.")
            
            # If they already have a warning, time them out!
            else:
                # 30-second duration
                duration = timedelta(seconds=30)
                
                # Apply the timeout (it's called 'timeout' in discord.py)
                await message.author.timeout(duration, reason="Said a banned word after a warning.")
                await message.channel.send(f"{message.author.mention} has been timed out for 30 seconds for ignoring the warning.")
                
                # Reset their warning count so they start fresh after the timeout
                del user_warnings[user_id]

        except discord.Forbidden:
            print("Bot lacks permission to delete messages or moderate members.")
        except discord.HTTPException as e:
            print(f"Failed to process moderation: {e}")
            
    await bot.process_commands(message)

# Paste your actual token inside the quotes below
bot.run os.environ.get('DISCORD_TOKEN')
