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

def getbio(username):
    url = 'https://forum.beammp.com/u/samisverycool.json'
    cookies = {
        '_t': 'gQWVSBtQCyFzP9mZHlyj3SIOuYcrNy1%2FIVZOPTiCG7OEbvCR6u4OqNsYROn4r1CIw6Dc5Tc7nAfHSnGd9JF8FVPAa1bCgS4Tm3oZIGb1rb%2B7evYiSYreb4PVie1gl7qL3r4X%2Bjq2CC6v9yBDQ%2Fu9eXyC2v61AEwPSdozgoMt%2FBzslDuP7KEF2kbYET5yOhmUAd%2BFSFTHESX8jOOUFZM%2BCq9ydYhrXg8J3fbnD0LbKY3UCGcQu8ZXgfmVc1eKqBIzK85GZwXU5FGhkzo3v%2FZqZgbLk%2FCSbYlr%2Fp13qa4Ee3yR2RxHzSTDGDA6zb%2Fx6To9QxotsENoJu4%3D--0l5mZuiw9ni1y1ae--K3bDhoYlHcm9DlIGq4fmwQ%3D%3D',
        '_forum_session': 'K1vPGwz8GyjMXCBVWrFhwQUL%2B4luFH48xlwtTuK4HCyBqRT8mm%2Fvudm9l4L73EZUPRbjzEvUTLimKTgaZc8IgIAHKTJoNSrJ9kWEJK%2B0u7Ez768w%2FL6E8DG6PGnN%2BPaddLr51n2zPG6r%2BYpH8Qyyx%2F5Go3C1GfIvfhXQUAVnK%2B72VzbYB3cBa0OadBDb92J2BjLPRta5dQ8MVXVK0M2ioIDpqmBcRH04Mz%2FahU2DsbdR7EJ6%2FbPnRscDajraX0gwfeS2pQmxsWOrm2CIewL0mu0D0jHm9R9H8obG3XVeRIpA0kxeQbXC0w5Xzj95j5ZGqjr0KTJ1mujg7gkWH67bXCFShAG6EOA6Bztaq1s0pOKmKx4dyJoRek%2FdHt3zMg%3D%3D--VRx9GGi1CA7KSijU--NiFMRBLxwh7Ak%2FF2LgccXQ%3D%3D'
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