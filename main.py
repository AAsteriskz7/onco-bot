"""
Code is used to take the input from the discord bot, server link: https://discord.gg/ztpTEAtXY8
The bot can take two inputs, image input or text input, the image input goes through openCV and
identifies if it looks like melanoma (skin cancer). The text input takes an address as an input
and returns a list of nearby hospitals for the user if needed.
"""
import os
import discord
from dotenv import load_dotenv

load_dotenv()

IMAGE_FOLDER = r'C:\Users\avsad\OneDrive\Desktop\Programming\onco-bot\images'
# Function below clears the image folder every time a new image is recieved
def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        os.remove(file_path)

# Turns on the discord bot when file is run, is always checking for text or message input
class MyClient(discord.Client):
    async def on_ready(self): # logging the bot in
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.attachments:
            # Image input handling
            clear_folder(IMAGE_FOLDER)
            
            for attachment in message.attachments:
                if attachment.filename.endswith(('.png', '.jpg', '.jpeg')):
                    save_path = os.path.join(IMAGE_FOLDER, attachment.filename)
                    await attachment.save(save_path)
                    await message.channel.send("Hello World!")  # Send "Hello World!" to the channel
        elif message.content:
            # Text input handling
            print(f"Message from {message.author}: {message.content}")

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
token = os.environ.get('TOKEN')
client.run(token)
