import os
import discord
from dotenv import load_dotenv
from gps import get_nearest_hospitals

load_dotenv()

IMAGE_FOLDER = r'C:\Users\avsad\OneDrive\Desktop\Programming\onco-bot\images'

def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        os.remove(file_path)

# Turns on the discord bot, always check for inputs
class MyClient(discord.Client):
    async def on_ready(self):  # logging the bot in
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.attachments:
            # Image input
            clear_folder(IMAGE_FOLDER)
            for attachment in message.attachments:
                if attachment.filename.endswith(('.png', '.jpg', '.jpeg')):
                    save_path = os.path.join(IMAGE_FOLDER, attachment.filename)
                    await attachment.save(save_path)
                    await message.channel.send("sent an image!")  # if image is sent, replied in the channel with this.

        elif message.content:
            # Text input 
            print(f"Message from {message.author}: {message.content}")

            # get hospital data
            address_input = message.content
            hospitals = get_nearest_hospitals(address_input)
            
            if hospitals:
                response = "Here are the nearest hospitals:\n"
                for i, hospital in enumerate(hospitals, start=1):
                    response += f"{i}. {hospital['name']} - {hospital['address']}\n"
            else:
                response = "No hospitals found for the given address."
            
            await message.channel.send(response)  # Bot replies with hospital info

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
token = os.environ.get('TOKEN')
client.run(token)
