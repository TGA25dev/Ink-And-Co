#Ink&Co (Ink and Co) is a Discord community bot made for the Ink Corp Discord server.
#Copyright (C) 2024  TGA25dev

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as published
#by the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.

#You should have received a copy of the GNU Affero General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.


import discord
from discord import app_commands
from datetime import datetime
from datetime import timedelta
import pytz
import asyncio
import random
import os
import requests
import dotenv
import json
import time
import re
from blagues_api import BlaguesAPI
from blagues_api import BlagueType


with open("JSON Files/bot_config_data.json", 'r', encoding='utf-8') as file:
    data = json.load(file)

for entry in data:    
 bot_mode_lc = entry["bot_mode_lc"]
 bot_mode_hc = entry["bot_mode_hc"]
 bot_mode_def = entry["bot_mode_def"]
 TGA25_ID = entry["TGA25 ID"]
 timezone = entry["Timezone"]
 version_note_text = entry["Version Note"]
 default_bot_nick_text = entry["Default Bot Nick"]
 version_number = entry["Version Number"]
 streamer_name = entry["Streamer Name"]

 goomink_news_channel_id = entry["goomink_news_channel_id"]
 news_role_id = entry["news_role_id"]
 twitch_role_id = entry["twitch_role_id"]

 help_command_id = entry["help_command_id"]
 effacer_dm_command_id = entry["effacer_dm_command_id"]
 info_command_id = entry["info_command_id"]
 dev_info_command_id = entry["dev_info_command_id"]
 admin_command_id = entry["admin_command_id"]
 joke_command_id = entry["joke_command_id"]
 server_info_command_id = entry["server_info_command_id"]
 

#PATH

DEFAULT_PATH = os.getcwd() 

IMAGES_PATH = f"Images"

TEXT_PATH = f"Text_Files"

def printer_timestamp():
   return datetime.now().strftime("\033[1;90m %Y-%m-%d %H:%M:%S \033[0m")

test = dotenv.load_dotenv(f"{DEFAULT_PATH}/Token/{bot_mode_lc}_bot.env")
token = os.getenv(f"{bot_mode_hc}_BOT_TOKEN")

global start_time
start_time = datetime.now()

print(f"\033[1m{printer_timestamp()} Token has been loaded ! \033[0m")

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.all()) 
        self.synced = False 

client = aclient()

dotenv.load_dotenv(f"{DEFAULT_PATH}/Token/blagues_api.env")
blagues_token = os.getenv(f"Blagues_Token")

print(f"{printer_timestamp()} Blagues API token has been loaded !")

dotenv.load_dotenv(f"{DEFAULT_PATH}/Token/twitch_client_secret.env")
twitch_client_secret = os.getenv(f"Twitch_Secret")

print(f"{printer_timestamp()} Twitch secret token has been loaded !")

dotenv.load_dotenv(f"{DEFAULT_PATH}/Token/twitch_client_id.env")
twitch_client_id = os.getenv(f"Twitch_Client_Id")

print(f"{printer_timestamp()} Twitch client id token has been loaded !")


dotenv.load_dotenv(f"{DEFAULT_PATH}/Token/twitch_access_token.env")
twitch_access_token = os.getenv(f"Twitch_Access_Token")

print(f"{printer_timestamp()} Twitch access token has been loaded !")

url = 'https://id.twitch.tv/oauth2/token'
payload = {
    'client_id': twitch_client_id,
    'client_secret': twitch_client_secret,
    'grant_type': 'client_credentials'
}

async def check_shutdown_file():
    if os.path.isfile("shutdown.txt"):
        print(f"{printer_timestamp()} shutdown.txt file exist. \033[91m Bot is stopping... \033[0m")
        os.remove("shutdown.txt") 
        await client.close()
        await asyncio.sleep(5)  
        os._exit(0)
    else:
        print(f"{printer_timestamp()} shutdown.txt file doesn't exist. \033[94m Bot is starting... \033[0m")

asyncio.run(check_shutdown_file())

is_ready = False


# Function to read the value of first_use_msg from a file
def read_first_use_msg():
    if os.path.exists("first_use_msg.txt"):
        with open("first_use_msg.txt", "r") as file:
            return file.read().strip() == "True"
    else:
        return False

# Function to write the value of first_use_msg to a file
def write_first_use_msg(value):
    with open("first_use_msg.txt", "w") as file:
        file.write(str(value))

# Initialize first_use_msg by reading its value from the file
first_use_msg = read_first_use_msg()

@client.event
async def on_ready():
    global first_use_msg
    await client.wait_until_ready()
    print(f"{printer_timestamp()} Bot ready !")

    try:
        bot_start_infos_embed = discord.Embed(
            title="**Lancement en cours... ⏳**",
            description="**Le bot est en train de démarrer. Veuillez patienter...**"
        )

        USER_DM = await client.fetch_user(TGA25_ID)
        startup_message = await USER_DM.send(embed=bot_start_infos_embed)

        await tree.sync()
        print(f"{printer_timestamp()} Commands Synced !")

        print(f"{printer_timestamp()} Logged in as {client.user.name} !")

        profile_image_path = f"{IMAGES_PATH}/Bot Logo/default_image_{bot_mode_lc}_bot.png"

        profile_image = open(profile_image_path, "rb")
        pfp = profile_image.read()

        await client.user.edit(avatar=pfp) #NE PAS OUBLIER DE REACTIVER !!!

        print(f"{printer_timestamp()} Profile image sucessfully restablished to default !")

        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"/help | {version_number}"))
        print(f"{printer_timestamp()} Bot Status has been corectly set up !")

        asyncio.create_task(twitch_loop())
        print(f"{printer_timestamp()} Twitch loop has been corectly created ! ")

        if not first_use_msg:
            # Send the startup message only if it's the first time
            
            first_use_embed = discord.Embed(
                title="Bonjour tout le monde! :wave:",
                description="*Comme vous le voyez le bot en ligne !*\n\n**Voici quelques infos utiles :**",
            )
            first_use_embed.add_field(name="", value="- Quand <@730446810887356508> sera en live vous recevrez un ping dans ce salon", inline=False)
            first_use_embed.add_field(name="", value="- Récupérez votre rôle de notification dès maintenant <id:customize>", inline=False)
            first_use_embed.add_field(name="", value="- Pour proposez une **feature** ou poser une **question** postez votre message ici <#1267166601791148063>", inline=False)
            first_use_embed.add_field(name="**Bonne journée à tous** :grin:", value="TGA25")
            first_use_embed.set_footer(text=version_note)

            twitch_message_channel = client.get_channel(goomink_news_channel_id)
            msg = await twitch_message_channel.send(embed=first_use_embed)
            print(f"{printer_timestamp()} First use message has been sent in channel {twitch_message_channel.name} !")

            await msg.add_reaction("✨")
            await msg.add_reaction("👌")
            await msg.pin()

            # Update first_use_msg to True after sending the message
            first_use_msg = True
            write_first_use_msg(first_use_msg)

        print(f"{printer_timestamp()} Twitch Loop starting in 30 seconds...")

        bot_start_infos_embed.title = ":green_circle: Succès ! :green_circle:"
        bot_start_infos_embed.description = "**Le bot a correctement démarré !**"

        await asyncio.sleep(3)

        await startup_message.edit(embed=bot_start_infos_embed)

        with open("JSON Files/Global Data/starting_time_average.json", 'r') as file:
            time_data = json.load(file)

        end_time = datetime.now()
        time_taken = round((end_time - start_time).total_seconds(), 1)

        time_data.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "time_taken": time_taken
        })

        # Save the updated data back to the file
        with open("JSON Files/Global Data/starting_time_average.json", 'w') as file:
            json.dump(time_data, file)

        time_taken_values = [entry['time_taken'] for entry in time_data]

        average_time_taken = round(sum(time_taken_values) / len(time_taken_values), 1)

        print(f"{printer_timestamp()}\033[1;92m All startup operations have been completed in {time_taken}s ! \033[0m\033[1;35m(average is {average_time_taken}s)\033[0m")

        global is_ready
        is_ready = True

    except Exception as e:
        print(f"{printer_timestamp()} \033[1;91mAn error has occured during bot starting : \033[0m \033[91m{e} \033[0m")

        bot_start_infos_embed.title="**:red_circle: Une erreur est survenue lors du démarage du bot :red_circle: **"
        bot_start_infos_embed.description=f"**Detail de l'erreur :** `{e}`"
        
        USER_DM = await client.fetch_user(TGA25_ID)
        await startup_message.edit(embed=bot_start_infos_embed)
        print(f"{printer_timestamp()} \033[1;34mWaiting....\033[0m")

        await asyncio.sleep(10)
        print(f"{printer_timestamp()} \033[1;33mBot stoping....\033[0m")

        await client.close()
        os._exit(0)

       

#BOT DISCONECT EVENT HANDLING

@client.event
async def on_disconnect():
    print(f"{printer_timestamp()} Bot disconnected. Reconnecting...")

    while not client.is_closed():
        try:
            await client.login(token)
            print(f"{printer_timestamp()} Reconnected successfully.")
            break
        except Exception as e:
            print(f"{printer_timestamp()} Reconnect failed. Retrying in 15 seconds... Error: {e}")
            await asyncio.sleep(15)


#VARIABLES         
restart_time = datetime.now()
tree = app_commands.CommandTree(client)
maintenance_mode = False
france_tz = pytz.timezone(timezone)
version_note = f"{version_note_text}"
default_bot_nick = f"{default_bot_nick_text}"

def generate_current_time_timestamp():
   discord_current_time = datetime.now(france_tz)
   current_time_timestamp = int(discord_current_time.timestamp())
   return current_time_timestamp



#EVENTS

@client.event
async def on_message(message):
    greeting_trigger_pattern = re.compile(r"\b(?:hi|hello|salut|bonjour|hey|helo|salu|salutation|salutations|coucous|coucou)\b", re.IGNORECASE)

    # Make sure the bot doesn't respond to its own messages
    if message.author == client.user:
        return

    if greeting_trigger_pattern.search(message.content):
        # Add a reaction for greeting trigger
        await message.add_reaction("👋")

#EMBEDS

 #Help Embed
help_embed = discord.Embed(
        title="Help",
        description="Voici toutes mes commandes :",
        color=discord.Color.from_rgb(252, 165, 119)
)

help_embed.add_field(name=f"</blague:{joke_command_id}>", value="Raconte une blague", inline=False) 

help_embed.add_field(name=f"</effacer-dm:{effacer_dm_command_id}>", value="Supprime tout les messages privés avec le bot", inline=False)

help_embed.add_field(name=f"</info:{info_command_id}>", value="Affiche les informations du bot", inline=False)

help_embed.add_field(name=f"</devinfo:{dev_info_command_id}>", value="Affiche des informations sur le développeur du bot", inline=False)

help_embed.add_field(name=f"</info-serveur:{server_info_command_id}>", value="Affiche des informations sur ce serveur", inline=False)

help_embed.add_field(name=f"</help:{help_command_id}>", value="Affiche ceci", inline=False)

help_embed.add_field(name=f"</admin:{admin_command_id}>", value="Affiche le panel d'administration du bot ***Commande réservée aux admins***", inline=False)

help_embed.set_footer(text=version_note)

 #Warning Timeout Embed

warning_timeout_embed = discord.Embed(
    color=discord.Color.from_rgb(245, 129, 66)
        
)
warning_timeout_embed.add_field(name="Attention ! 🚨", value="Vous n'avez qu'**1 minute** pour utiliser les modules.")

 #Maintenance Embed

maintenance_embed = discord.Embed(
    title="**Maintenance 🚧**",
    description="Une maintenance est en cours...👷",
    color=discord.Color.from_rgb(240, 206, 17)
        
)
maintenance_embed.set_footer(text=version_note)

 #End Maintenance Embed

end_maintenance_embed = discord.Embed(
    title="**Fini ! :green_circle:**",
    description="La maintenance est maintenant terminée... :white_check_mark:",
    color=discord.Color.from_rgb(68, 242, 129)
        
)
end_maintenance_embed.set_footer(text=version_note)


 #Error Embed 

error_embed = discord.Embed(
    title="**Oups ! :face_with_monocle:**",
    description="Une erreur est survenue...",
    
    color=discord.Color.from_rgb(235, 64, 52)
        
)
error_embed.add_field(name= "L'erreur a été transmise au développeur :electric_plug:", value="*Ceci ne devrait pas arriver...*\nMerci d'en informer l'équipe !")
error_embed.set_footer(text=version_note)


 #Dev Info Embed



dev_info_embed = discord.Embed(


        description="**Informations sur le developpeur du bot**",
        color=discord.Color.from_rgb(134, 27, 242)

        
        
)
dev_info_embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/845327664143532053/65a0b52e2a7b881a64c5769d8f12f359.png?size=512")
dev_info_embed.add_field(name="**Bonjour ! :wave: **", value="Moi c'est <@845327664143532053> <:activedevbadge:1107235074757373963>", inline=False)
dev_info_embed.add_field(name=f"**Développeur**", value="*Développeur Python <:logo_python_arabot:1108367929457791116>*", inline=True)
dev_info_embed.add_field(name="**Youtubeur** <:logo_youtube_arabot:1108368195489910836>", value="*Clique* [ici](https://www.youtube.com/channel/UCCxw1YVUMs5czQuhTkJH3eQ)", inline=True)
dev_info_embed.set_footer(text=version_note)

 #Command Unavalaible Embed

unavaileble_command_embed = discord.Embed(
   title="**Oups ! :face_with_monocle: **",
   description="Cette commande revient bientôt...",
   color=discord.Color.from_rgb(66, 135, 245),
   
)
unavaileble_command_embed.set_footer(text=version_note)


#BUTTON VIEWS

 #Button View Delete Bot
        

 #Button View Status

class ButtonView_status(discord.ui.View):
    def __init__(self, message):
        super().__init__(timeout=None)
        self.message = message
        

#En ligne

    @discord.ui.button(style=discord.ButtonStyle.primary, label="En ligne", custom_id="button1", emoji="🟢")
    async def button1_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message(content="Statut du bot : **En ligne**", ephemeral=True)
        await client.change_presence(status=discord.Status.online)
#Inactif

    @discord.ui.button(style=discord.ButtonStyle.primary, label="Inactif", custom_id="button2", emoji="🌙")
    async def button2_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message(content="Statut du bot : **Inactif**", ephemeral=True)
        await client.change_presence(status=discord.Status.idle)
#Ne pas deranger

    @discord.ui.button(style=discord.ButtonStyle.primary, label="Ne pas déranger", custom_id="button3", emoji="🔕")
    async def button3_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message(content="Statut du bot : **Ne pas déranger**", ephemeral=True)
        await client.change_presence(status=discord.Status.dnd) 

#Hors ligne

    @discord.ui.button(style=discord.ButtonStyle.primary, label="Hors ligne", custom_id="button4", emoji="❌")
    async def button4_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message(content="Statut du bot : **Hors ligne**", ephemeral=True)
        await client.change_presence(status=discord.Status.offline)                 

#Invisible

    @discord.ui.button(style=discord.ButtonStyle.primary, label="Invisible", custom_id="button5", emoji="👻")
    async def button5_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message(content="Statut du bot : **Invisible**", ephemeral=True)
        await client.change_presence(status=discord.Status.invisible)  

 
   
             
 #Button View Parameters

class ButtonView_settings(discord.ui.View):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(timeout=None)
        self.bot = client

    @discord.ui.button(style=discord.ButtonStyle.danger, label="Supprimer le bot", custom_id="delete_bot_button")
    async def button_delete_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content="**Êtes-vous sûr ?** (Le bot pourra être ajouté à nouveau avec un lien d'invitation)\nRépondez `oui` pour supprimer le bot de ce serveur. :grey_question:", ephemeral=True, delete_after=35)

        try:
            confirm_response = await self.bot.wait_for(
                "message",
                check=lambda m: m.author == interaction.user and m.channel == interaction.channel,
                timeout=30  # You can adjust the timeout duration
            )

            if confirm_response.content.lower() == "oui":
                # Delete the bot from the server
               await confirm_response.delete()
               print(f"{printer_timestamp()} Bot deleted from server: {interaction.guild.name} ({interaction.guild.id})")
               await interaction.edit_original_response(content="**Le bot a bien été supprimé... **:cry:")

               await interaction.guild.leave()
                
            else:
                await interaction.edit_original_response(content="**Opération annulée...** :x:")
                await confirm_response.delete()
        
        except asyncio.TimeoutError:
            await interaction.edit_original_response(content="***Temps écoulé.*** Veuillez réessayer. :alarm_clock:")    
        

    @discord.ui.button(style=discord.ButtonStyle.primary, label="Réinitialiser le profil", custom_id="button_reset", emoji="🔄")
    async def button1_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        bot_user = interaction.guild.me
        await bot_user.edit(nick=None)


        default_profile_image_path = f"{IMAGES_PATH}/Bot Logo/default_image_{bot_mode_lc}_bot.png"

        default_profile_image = open(default_profile_image_path, "rb")
        pfp = default_profile_image.read()
        
        await client.user.edit(avatar=pfp)
        await interaction.response.send_message("Le profil du bot a été réinitialisé. ✅", ephemeral=False)

    @discord.ui.button(style=discord.ButtonStyle.primary, label="Arrêt", custom_id="button_shutdown", emoji="🔴")
    async def button2_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
     user = interaction.user
     await interaction.response.defer()
     filename = "shutdown.txt"
     with open(filename, 'w') as f:
        pass   
     await asyncio.sleep(1)
     await interaction.message.edit(content="⬜⬜⬜⬜", view=self)
     await asyncio.sleep(1)
     await interaction.message.edit(content="🟩⬜⬜⬜", view=self)
     await asyncio.sleep(1)
     await interaction.message.edit(content="🟩🟩⬜⬜", view=self)
     await asyncio.sleep(1)
     await interaction.message.edit(content="🟩🟩🟩⬜", view=self)
     await asyncio.sleep(1)
     await interaction.message.edit(content="🟩🟩🟩🟩", view=self)
  
     await asyncio.sleep(5)
     await interaction.message.edit(content="☠️", view=self)
     await asyncio.sleep(2)

     print(f"{printer_timestamp()} The bot has been stopped by {user.name} !")

     await client.close()
     os._exit(0) 

     

    @discord.ui.button(style=discord.ButtonStyle.primary, label="Maintenance", custom_id="button_maintenance", emoji="🚧")
    async def button3_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        global maintenance_mode
        maintenance_mode=True
        await interaction.response.send_message("Mode maintenance **activé** 👷 !", ephemeral=True)
        await client.change_presence(activity=discord.Activity(status=discord.Status.do_not_disturb ,name="la maintenance 👷", type=discord.ActivityType.watching))

    @discord.ui.button(style=discord.ButtonStyle.primary, label="Fin de la maintenance", custom_id="button_end_maintenance", emoji="🛠️")
    async def button4_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
     await interaction.response.send_message("Mode maintenance **désactivé** 👷 !", ephemeral=True)

     await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="de retour...🎉"))  
          
     await asyncio.sleep(10)
     global maintenance_mode
     maintenance_mode=False

     #Find the guild objetc
     guild = discord.utils.get(client.guilds)
     if not guild:
        print(f"{printer_timestamp()} Guild not found!")
        return

     twitch_message_channel = client.get_channel(goomink_news_channel_id)

     # Find the role object
     role = guild.get_role(news_role_id)
     if role is None:
      print(f"{printer_timestamp()} The news role was not found on the server !")
      msg = await twitch_message_channel.send(f"", embed=end_maintenance_embed)
      
     # Sending message to the channel
     else:
        msg = await twitch_message_channel.send(f"{role.mention}", embed=end_maintenance_embed)
        
     await msg.add_reaction("👌")
     await msg.add_reaction("🚧")
     print(f"{printer_timestamp()} End maintenance message has been sent in channel : {twitch_message_channel.name} !")
     await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"/help | {version_number}"))

#SELECT VIEWS  

 #Select Admin Menu

class AdminSelectMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)

        options = [
            discord.SelectOption(label="Statuts", value="status_embed_option", emoji="🟢"),
            discord.SelectOption(label="Paramètres", value="parameters_embed_option", emoji="⚙️"),
            discord.SelectOption(label="Informations", value="information_embed_option", emoji="ℹ️"),
          
        ]
        
        select = discord.ui.Select(options=options, placeholder="Options d'administration", min_values=1, max_values=1)
        select.callback = self.select_callback
        self.add_item(select)

    
    async def select_callback(self, interaction):
          
        info_embed1 = discord.Embed(
        title="Infos",
        color=discord.Color.from_rgb(60, 240, 132)
        )
        info_embed1.add_field(name="**Ping 🏓**", value=f"*{round(client.latency, 2)}* ms de latence", inline=False)
        info_embed1.add_field(name="**Date & Heure 🕐**", value=f"Nous sommes le <t:{generate_current_time_timestamp()}:D> et il est <t:{generate_current_time_timestamp()}:t>", inline=False)
        info_embed1.add_field(name="**Dernier redémarrage 🔄**", value=f"<t:{int(restart_time.timestamp())}>", inline=False) # Bot restart date and time field
        info_embed1.add_field(name="**Langage de programmation 🌐**", value="*Python* <:logo_python_arabot:1108367929457791116>", inline=False) # Bot restart date and time field
        info_embed1.set_footer(text=version_note)

        selected_option = interaction.data['values'][0]

        if selected_option == "status_embed_option":
            await interaction.response.edit_message(content="Modifiez le **statut** du bot :")
            await interaction.channel.send(view=ButtonView_status(interaction))
            
            
        elif selected_option == "parameters_embed_option":
            await interaction.response.edit_message(content="Modifiez les **parametres** du bot :")
            await interaction.channel.send(view=ButtonView_settings(interaction))

        else:

         await interaction.response.send_message(embed=info_embed1, ephemeral=True)

                

#COMMANDS

@tree.command(name="blague", description="Raconte une blague")
async def joke_command(interaction: discord.Interaction):
    blagues = BlaguesAPI(blagues_token)

    blague = await blagues.random(disallow=[BlagueType.GLOBAL, BlagueType.DEV])

    joke = blague.joke
    answer = blague.answer
    type_blague = blague.type

    hc_type_blague = type_blague[0].upper() + type_blague[1:]
    joke_embed = discord.Embed(
    title="",
        description="",
        color=discord.Color.from_rgb(60, 240, 132)
        )
    joke_embed.add_field(name=f"{joke}", value=f"||{answer}||")
    joke_embed.set_footer(text=f"{hc_type_blague} • Demandée à {datetime.now(france_tz).strftime('%H:%M')} par {interaction.user.global_name} | BlaguesAPI")

    await interaction.response.send_message(embed=joke_embed)


@tree.command(name="info-serveur", description="Affiche des informations à propos serveur")
async def server_info(interaction: discord.Interaction):
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message(content="Vous ne pouvez pas utiliser cette commande dans les dm ! :no_entry_sign:", ephemeral=True)
    else:
        #     
        if interaction.guild.premium_tier == 0:
            guild_boost_level = f"Aucun boost"

        elif interaction.guild.premium_tier == 1:
            guild_boost_level = f"Niveau 1 {interaction.guild.premium_subscription_count} boost(s)"

        elif interaction.guild.premium_tier == 2:
            guild_boost_level = f"Niveau 2 {interaction.guild.premium_subscription_count} boost(s)"
    
        elif interaction.guild.premium_tier == 3:
            guild_boost_level = f"Niveau 3 {interaction.guild.premium_subscription_count} boost(s)"             

        bot_members = [member for member in interaction.guild.members if member.bot]
        text_channels = [channel for channel in interaction.guild.channels if isinstance(channel, discord.TextChannel) or isinstance(channel, discord.VoiceChannel)]

        server_stat_embed = discord.Embed(
        title="Quelques infos sur ce serveur :information_source:",
        
        description=f"*__{interaction.guild.name} ({interaction.guild.id})__*\n**{len(text_channels)} salons • {len(interaction.guild.threads)} fils • {len(interaction.guild.roles)} rôles • {len(bot_members)} bots**",
        color=discord.Color.from_rgb(3, 165, 252)
        )
        server_stat_embed.set_thumbnail(url=interaction.guild.icon)

        server_stat_embed.add_field(name="Membres :", value=interaction.guild.member_count, inline=True)

        server_stat_embed.add_field(name="Propriétaire :", value=f"<@{interaction.guild.owner.id}>", inline=True)

        server_stat_embed.add_field(name="Boost :", value=guild_boost_level)

        server_stat_embed.add_field(name="Création du serveur", value=f"<t:{int(interaction.guild.created_at.timestamp())}:F>")

        bot_member = interaction.guild.get_member(client.user.id)

        server_stat_embed.add_field(name="Date d'ajout du bot :", value=f"<t:{(int(bot_member.joined_at.timestamp()))}:F>")
                      
        server_stat_embed.set_footer(text=version_note)

        await interaction.response.send_message(embed=server_stat_embed)


@tree.command(name="effacer-dm", description="Supprime tout DM du bot")
async def delete_dm(interaction: discord.Interaction):
    # Check if the command is sent in a DM
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message(content=":hourglass_flowing_sand: Tous les messages du bot sont en cours de suppression.....\n\n(Vous serez notifié quand ce sera fini. :information_source:)", ephemeral=True)

        # Fetch the bot's sent messages in the DM
        bot_messages = []
        async for message in interaction.channel.history(limit=None):
            if message.author == interaction.client.user:
                bot_messages.append(message)

        # Delete each bot message
        for message in bot_messages:
            await message.delete()
            await asyncio.sleep(1)

        await interaction.edit_original_response(content="Tous les messages du bot ont étés supprimés :white_check_mark: !")
        user_to_dm = await client.fetch_user(interaction.user.id)
        notification_message = await user_to_dm.send(content="🔔")
        await notification_message.delete()


    else:
     await interaction.response.send_message("Cette commande n'est utilisable que dans les DM !", ephemeral=True)


@tree.command(name="admin", description="Affiche le panel d'administration du bot")
async def admin_panel(interaction: discord.Interaction):
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message(content="Vous ne pouvez pas utiliser cette commande dans les dm ! :no_entry_sign:", ephemeral=True)
    else:
        command_name = interaction.data['name']
        user_id = interaction.user.id
        command_id = interaction.data['id']
        guild_name = interaction.guild.name
        
        USER_DM = await client.fetch_user(TGA25_ID)

        try:
            if interaction.user.id == TGA25_ID:
                view = AdminSelectMenu()
                await interaction.response.send_message(content="Administration du bot :", view=view, ephemeral=True)
            else:
                await interaction.response.send_message("Tu n'es pas autorisé a utiliser cette commande ! :no_entry_sign: ", ephemeral=True)

        except Exception as e:
            error_dminfo_embed = discord.Embed(
                title="**:red_circle: Une erreur est survenue sur l'un des serveurs :red_circle: **",
                description=f"**Erreur causée par** <@{user_id}>",
                color=discord.Color.from_rgb(245, 170, 66)
            )

            error_dminfo_embed.add_field(name="Details :",
                                         value=f"Erreur survenue <t:{generate_current_time_timestamp()}:R> dans le serveur `{guild_name}`",
                                         inline=True)
            error_dminfo_embed.add_field(name="**Commande :**", value=f"`{command_name}`", inline=True)
            error_dminfo_embed.add_field(name="**ID de la commande :**", value=f"`{command_id}`", inline=True)
            error_dminfo_embed.add_field(name="Erreur :", value=f"`{e}`", inline=False)
            error_dminfo_embed.set_footer(text=f"{version_note}")

            await USER_DM.send(embed=error_dminfo_embed)
            await interaction.response.send_message(embed=error_embed, ephemeral=True)


@tree.command(name="help", description="Affiche les commandes disponibles")
async def embed_command(interaction: discord.Interaction):
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message(content="Vous ne pouvez pas utiliser cette commande dans les DM ! :no_entry_sign:", ephemeral=True)
    else:  
        user_id = interaction.user.id
        command_name = interaction.data['name']
        command_id = interaction.data['id']
        guild_name = interaction.guild.name
        USER_DM = await client.fetch_user(TGA25_ID)

        if maintenance_mode:
                await interaction.response.send_message(embed=maintenance_embed, ephemeral=True)
                return

        try:
            await interaction.response.send_message(embed=help_embed, ephemeral=False)
        except Exception as e:
                error_dminfo_embed = discord.Embed(
                    title="**:red_circle: Une erreur est survenue sur l'un des serveurs :red_circle: **",
                    description=f"**Erreur causée par** <@{user_id}>",
                    color=discord.Color.from_rgb(245, 170, 66)
                )

                error_dminfo_embed.add_field(
                    name="Details :", value=f"Erreur survenue <t:{generate_current_time_timestamp()}:R> dans le serveur `{guild_name}`", inline=True)
                error_dminfo_embed.add_field(
                    name="**Commande :**", value=f"`{command_name}`", inline=True)
                error_dminfo_embed.add_field(
                    name="**ID de la commande :**", value=f"`{command_id}`", inline=True)
                error_dminfo_embed.add_field(
                    name="Erreur :", value=f"`{e}`", inline=False)
                error_dminfo_embed.set_footer(text=f"{version_note}")

                await USER_DM.send(embed=error_dminfo_embed)
                await interaction.response.send_message(embed=error_embed, ephemeral=True)


@tree.command(name="info", description="Affiche des informations à propos du bot")
async def embed_command(interaction: discord.Interaction):
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message(content="Vous ne pouvez pas utiliser cette commande dans les dm ! :no_entry_sign:", ephemeral=True)
    else:
            user_id = interaction.user.id
            command_name = interaction.data['name']
            command_id = interaction.data['id']
            guild_name = interaction.guild.name
            USER_DM = await client.fetch_user(TGA25_ID)

            if maintenance_mode:
                await interaction.response.send_message(embed=maintenance_embed, ephemeral=True)
                return

            try:
                # Create the embed
                info_embed2 = discord.Embed(
                    title="Infos",
                    color=discord.Color.from_rgb(60, 240, 132)
                )
                info_embed2.add_field(name="**Ping 🏓**", value=f"*{round(client.latency, 2)}* ms de latence", inline=False)
                info_embed2.add_field(name="**Date & Heure 🕐**", value=f"Nous sommes le <t:{generate_current_time_timestamp()}:D> et il est <t:{generate_current_time_timestamp()}:t>", inline=False)
                info_embed2.add_field(name="**Dernier redémarrage 🔄**", value=f"<t:{int(restart_time.timestamp())}>", inline=False)
                info_embed2.add_field(name="**Langage de programmation 🌐**", value="*Python* <:logo_python_arabot:1108367929457791116>", inline=False)
                info_embed2.set_footer(text=version_note)

                await interaction.response.send_message(embed=info_embed2, ephemeral=False)

            except Exception as e:
                error_dminfo_embed = discord.Embed(
                    title="**:red_circle: Une erreur est survenue sur l'un des serveurs :red_circle: **",
                    description=f"**Erreur causée par** <@{user_id}>",
                    color=discord.Color.from_rgb(245, 170, 66)
                )

                error_dminfo_embed.add_field(
                    name="Details :", value=f"Erreur survenue il y a à <t:{generate_current_time_timestamp()}:R> dans le serveur `{guild_name}`", inline=True)
                error_dminfo_embed.add_field(
                    name="**Commande :**", value=f"`{command_name}`", inline=True)
                error_dminfo_embed.add_field(
                    name="**ID de la commande :**", value=f"`{command_id}`", inline=True)
                error_dminfo_embed.add_field(
                    name="Erreur :", value=f"`{e}`", inline=False)
                error_dminfo_embed.set_footer(text=f"{version_note}")

                await USER_DM.send(embed=error_dminfo_embed)
                await interaction.response.send_message(embed=error_embed, ephemeral=True)


@tree.command(name="devinfo", description="Affiche des informations à propos du développeur")
async def dev_info_command(interaction: discord.Interaction):
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message(content="Vous ne pouvez pas utiliser cette commande dans les dm ! :no_entry_sign:", ephemeral=True)
    else:
            command_name = interaction.data['name']
            user_id = interaction.user.id
            command_id = interaction.data['id']
            guild_name = interaction.guild.name
            USER_DM = await client.fetch_user(TGA25_ID)

            try:
                emoji_id = 1107235074757373963  # Replace with the ID of your custom emoji
                myemoji = client.get_emoji(emoji_id)
                await interaction.response.send_message(content=myemoji, embed=dev_info_embed)

            except Exception as e:
                error_dminfo_embed = discord.Embed(
                    title="**:red_circle: Une erreur est survenue sur l'un des serveurs :red_circle: **",
                    description=f"**Erreur causée par** <@{user_id}>",
                    color=discord.Color.from_rgb(245, 170, 66)
                )

                error_dminfo_embed.add_field(
                    name="Details :", value=f"Erreur survenue <t:{generate_current_time_timestamp()}:R> dans le serveur `{guild_name}`", inline=True)
                error_dminfo_embed.add_field(
                    name="**Commande :**", value=f"`{command_name}`", inline=True)
                error_dminfo_embed.add_field(
                    name="**ID de la commande :**", value=f"`{command_id}`", inline=True)
                error_dminfo_embed.add_field(
                    name="Erreur :", value=f"`{e}`", inline=False)
                error_dminfo_embed.set_footer(text=f"{version_note}")

                await USER_DM.send(embed=error_dminfo_embed)
                await interaction.response.send_message(embed=error_embed, ephemeral=True)


#Twitch Live Alert Loop

async def twitch_loop():
   while not is_ready:
        await asyncio.sleep(30)
        print(f"{printer_timestamp()} Twitch Loop has been started !")

        headers = {
        'Client-Id': f'{twitch_client_id}',
        'Authorization': f'Bearer {twitch_access_token}',
        }

   previous_status = None

   

   while True:
     response = requests.get(f"https://api.twitch.tv/helix/streams?user_login={streamer_name}", headers=headers)

    # Ensure the request was successful
     if response.status_code == 200:
        user_info = json.loads(response.text)   

        if not user_info['data']:
            current_status = f"{streamer_name} is offline..."
        else:
            current_status = f"{streamer_name} is online !"
            # Additional information if online
            user_name = user_info["data"][0]["user_name"]
            user_id = user_info["data"][0]["user_id"]
            user_login = user_info["data"][0]["user_login"]
            game_name = user_info["data"][0]["game_name"]
            title = user_info["data"][0]["title"]
            thumbnail_url = user_info["data"][0]["thumbnail_url"]

            timestamp = int(time.time())  # Get current Unix timestamp
            thumbnail_url_with_timestamp = f"{thumbnail_url}.{timestamp}"

            width = 300
            height = 200
            resized_thumbnail_url = thumbnail_url_with_timestamp.replace('{width}', str(width)).replace('{height}', str(height))

        if current_status != previous_status:
            print(f"{printer_timestamp()} {current_status}")
            if current_status == f"{streamer_name} is online !":
                print(f"{printer_timestamp()} -----------------------")
                print(f"{printer_timestamp()} User Name: {user_name}")
                print(f"{printer_timestamp()} User Id = {user_id}")
                print(f"{printer_timestamp()} Game Name: {game_name}")
                print(f"{printer_timestamp()} Title: {title}")
                print(f"{printer_timestamp()} Thumbnail URL: {resized_thumbnail_url}")
                print(f"{printer_timestamp()} Live URL : https://twitch.tv/{user_login}")
                print(f"{printer_timestamp()} -----------------------")
                

                live_url = f"https://twitch.tv/{user_login}"

                 # Replace with your channel ID
                twitch_message_channel = client.get_channel(goomink_news_channel_id)


                if twitch_message_channel:
                 
                 twitch_live_embed = discord.Embed( 
                 title=f"🔴 LIVE 🔴",
                 description="",
                 color=discord.Color.from_rgb(136, 3, 252)        
                 )
                 twitch_live_embed.add_field(name="", value=f"***{user_name}*** est en live sur *__{game_name}__* <:logo_twitch_arabot:1151919627983659148>", inline=False)
                 twitch_live_embed.add_field(name=f"", value=f"{title}", inline=True)
                 
                 twitch_live_embed.add_field(name="", value= f":rocket: **Venez voir en cliquant** [ici]({live_url}) :rocket:", inline=False)

                 twitch_live_embed.set_image(url=resized_thumbnail_url)

                 twitch_live_embed.set_footer(text=f"{version_note}")

                 
                #Find the guild objetc
                guild = discord.utils.get(client.guilds)
                if not guild:
                 print("Guild not found!")
                 return


                # Find the role object
                role = guild.get_role(twitch_role_id)
                if role is None:
                 print(f"The news role was not found on the server !")
                 await twitch_message_channel.send(content="@everyone",embed=twitch_live_embed)

                else: 
                 await twitch_message_channel.send(content=f"{role.mention}",embed=twitch_live_embed)
                print(f"{printer_timestamp()} Twitch Live Alert has been sent ! (in channel : {twitch_message_channel})")

            previous_status = current_status

     else:
        if response.status_code == 429:
            print(f"{printer_timestamp()} Twitch API system is being  rate limited !!")
            USER_DM = await client.fetch_user(TGA25_ID)
            await USER_DM.send(content="***__Twitch API system is being  rate limited !!__**\n*Please check the [console](https://portal.daki.cc/)*")
        else:    

         print(f"{printer_timestamp()} Request returned status code {response.status_code}")
         
         USER_DM = await client.fetch_user(TGA25_ID)

         error_data = response.json()
         error_message = error_data.get("message", "No error message provided")
         error_status = error_data.get("status", "No status provided")

         await USER_DM.send(content=f"Twitch API system returned status code **{error_status}** : `{error_message}`\nThe bot has been stopped\nPlease check the [console](https://portal.daki.cc/)")
         await client.close()


     await asyncio.sleep(15)


client.run(token)