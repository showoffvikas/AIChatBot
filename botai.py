import discord
import responses
from discord.ext import commands

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        if response:
            await message.author.send(response) if is_private else await message.channel.send(response)
        else:
            print("Empty response received.")
    except Exception as e:
        print(f"Error sending message: {e}")

def run_discord_bot():
  #  TOKEN = 
    client = commands.Bot(command_prefix=">", intents=discord.Intents.all())
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
    @client.event
    async def on_message(message):
        if message.author.bot:
          return
        print(message)
        print(f"Received message: {message.content}")
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})")
        await send_message(message, user_message, is_private=False)
    client.run(TOKEN)       
