import discord
import os
import requests
import traceback

from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

REPORTCHANNELID = os.getenv('REPORTCHANNELID')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
TOKEN = os.getenv('TOKEN')
FORUMSESSION = os.getenv('FORUMSESSION')

def getbio(username):
    url = f'https://forum.beammp.com/u/{username}.json'
    cookies = {
        '_t': TOKEN,
        '_forum_session': FORUMSESSION
    }
    response = requests.get(url, cookies=cookies)
    if response.status_code == 200:
        result = response.json()
        usersection = result['user']
        aboutme = usersection['bio_raw']
        return aboutme
    else:
        print(f"error code: {response.status_code}")

class ContinueUsername(discord.ui.View):
    def __init__(self, username: str):
        super().__init__()
        self.value = None
        self.username = username
    
    @discord.ui.button(label="Continue", style=discord.ButtonStyle.green)
    async def _continue(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            aboutme = getbio(self.username)
            phrase = interaction.user.id*2
            if str(aboutme) != str(phrase):
                failEmbed = discord.Embed(
                    title="Verification Failed",
                    description="The authentication process has failed, please retry and ensure you enter the correct values."
                )
                await interaction.response.send_message(embed=failEmbed, ephemeral=True)
            else:
                successEmbed = discord.Embed(
                    title="Verification Successful",
                    description="The authentication was completed and you should recieve your roles and nickname shortly."
                )
                await interaction.response.send_message(embed=successEmbed, ephemeral=True)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)

class Verify(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client=client

    @commands.Cog.listener()
    async def on_ready(self):
        print("./cogs/verify.py/Verify/on_ready :: loaded")
    
    @app_commands.command(name="verify", description="Begin verification process with BeamMP")
    async def verify(self, interaction: discord.Interaction, beammp_username: str):
        try:
            phrase = interaction.user.id*2
            submitEmbed = discord.Embed(
                title="Account Verification",
                description=f"Please change your [BeamMP Forum About Me](https://forum.beammp.com/u/{beammp_username}/preferences/profile) to the following phrase:\n```{phrase}```"
            )
            submitEmbed.set_footer(text="v0.1.0")
            await interaction.response.send_message(embed=submitEmbed, view=ContinueUsername(username=beammp_username), ephemeral=True)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
        
async def setup(client):
    await client.add_cog(Verify(client))