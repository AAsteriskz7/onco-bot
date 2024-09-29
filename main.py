import os
import discord
from dotenv import load_dotenv # type: ignore
from gps import get_nearest_hospitals
from cv import label

load_dotenv()

IMAGE_FOLDER = r'C:\\Users\\avsad\\OneDrive\\Desktop\\Programming\\onco-bot\\images'

def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        os.remove(file_path)

class MyClient(discord.Client):
    async def on_ready(self):  # logging the bot in
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.attachments:
            # Clear the folder
            clear_folder(IMAGE_FOLDER)
            
            for attachment in message.attachments:
                if attachment.filename.endswith(('.png', '.jpg', '.jpeg')):
                    # Save the file in the folder
                    save_path = os.path.join(IMAGE_FOLDER, attachment.filename)
                    await attachment.save(save_path)
                    
                    # Use the full path to the image
                    if label(save_path):  # Pass full path
                        await message.channel.send("Based on the information provided, there are some signs that could indicate melanoma. It’s important to consult with a healthcare professional as soon as possible for a thorough examination and diagnosis. Early detection and treatment are crucial. Please take care and seek medical advice promptly. If you need a list of hospitals near you, just type your address in the textbox below.")
                    else:
                        await message.channel.send("Based on the information provided, there don’t appear to be any signs of melanoma. However, it’s always a good idea to keep monitoring your skin and consult with a healthcare professional if you notice any changes or have concerns. Regular check-ups are important for maintaining your health.")

        elif message.content:
            # Text input 
            print(f"Message from {message.author}: {message.content}")

            # get hospital data
            address_input = message.content
            hospitals = get_nearest_hospitals(address_input)
            
            # Check if hospitals is a string (error message) or a list
            if isinstance(hospitals, str):
                response = hospitals  # It's an error message
            else:
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
