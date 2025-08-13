from datetime import datetime, timezone, timedelta
import streamlit as st
import pandas as pd
from streamlit_extras.stylable_container import stylable_container
import plotly.express as px
from streamlit_extras.let_it_rain import rain
from streamlit_image_coordinates import streamlit_image_coordinates
import base64
from streamlit_card import card
from openai import OpenAI
import re
import random
from st_dialog_close_detector import dialog_close_detector
import streamlit.components.v1 as components
import os
import time
from st_paywall import add_auth
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import fal_client
import requests
import json
import math
import os
import asyncio
import mutagen
from mutagen.mp3 import MP3

from streamlit_js_eval import streamlit_js_eval
from streamlit_javascript import st_javascript
from user_agents import parse


if 'FirstRun' not in st.session_state:
    st.session_state.FirstRun = True
    print(f"""
#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#      
=========================================
|                                       |
|         PICOPACHO HAS BEGUN           |
|                                       |
=========================================
#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#
{time.time()}

""")
    st.session_state.Guest = False
else:
    st.session_state.FirstRun = False
    

if 'Rerun' not in st.session_state:
    print(f"""
===========================
|         RERUN           |    
===========================
{time.time()}

""")


elevenlabs = ElevenLabs(
  api_key=st.secrets['elevenLabs']['api_key'],
)

#FAL_KEY=st.secrets['falAi']['FAL_KEY']
os.environ['FAL_KEY'] = st.secrets['falAi']['FAL_KEY']


openai_api_key = st.secrets['openai']['api_key']
client = OpenAI(api_key=openai_api_key)

Currencylookup = json.load(open("Currencylookup.json", encoding="utf-8"))

BaseUrl = "app/static/"
#BaseUrl = "http://localhost:8501/app/static/"

# Initialize isLoading at the top
if "isLoading" not in st.session_state:
    st.session_state.isLoading = True # Default to True for initial app load

st.set_page_config(
    page_title="PICOPACHO",
    page_icon="static/Logos/Badge_Tiny.png",
    layout="wide",
    menu_items=None,
    initial_sidebar_state="collapsed",
    
)

# ua_string = str(st_javascript("""window.navigator.userAgent;"""))
# user_agent = (parse(ua_string))
# st.session_state.is_session_pc = bool(user_agent.is_pc)
# time.sleep(1)
# if not st.session_state.is_session_pc:
#     st.title('Mobile site currently under construction 👷‍♂️🏗')
#     st.write('Please visit on desktop :)')
#     #time.sleep(1000)
#     st.stop()



def NewGame():
    streamlit_js_eval(js_expressions="parent.window.location.reload()")

def debug():
    with st.sidebar:
        st.title("🔬Debug Menu")
        if st.button("New Game"):
            NewGame()
        if st.button("Update"):
            st.rerun()

        if st.button("Fal Instant Char"):
            st.image(fal_instantChar('https://v3.fal.media/files/tiger/BkvwIkjxNmeRvsOxmXgOU.jpeg', 'Character is playing Guitar'))

        if st.button("Shop"):
            cheekytoolify = {"name": "OPENSHOP", "variables": ['Dog.png', [['Dog.png', 'Doge', 100], ['imageguide1.png', 'windmill', 200], ['Melvin.png', 'eagle', 300]]]}
            Shop(cheekytoolify)
        if st.button("Fal upload"):
            url = fal_client.upload_file('Fallback.png')
            st.write(url)
        if st.button("Kill Character"):
            #get random character
            random_character = random.choice(st.session_state.characters)
            KillCharacter({"name": "KILL_CHARACTER", "variables": [random_character['name'], f'{random_character['name']} has been killed']})
        if st.button("Clear Tutor History"):
            st.session_state.TutorHistory = []
        if st.button("Roll Dice"):
            rollDice({"name": "ROLL_DICE", "variables": ["How many moonroot will you find?", 5, 'You gather 5 moonroot']})

        with st.container():
            chosenstates = ["Conversation", "toolbuffer", "player", "PoiList", "inventory", "characters", "missionList", "ShowVocab", 'close']
            ChosenTabs = st.tabs(chosenstates)
            for i in range(len(chosenstates)):
                with ChosenTabs[i]:
                    if chosenstates[i] == "close":
                        pass
                    else:
                        st.write(st.session_state[chosenstates[i]])
        

        with st.container():
            Allstates = list(st.session_state.keys())
            AllTabs = st.tabs(Allstates)
            for i in range(len(Allstates)):
                try:
                    with AllTabs[i]:
                        st.write(st.session_state[Allstates[i]])
                except Exception as e:
                    st.write(f"Error displaying {Allstates[i]}: {e}")


dialog_close_detector()

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

#hide anchors
st.html("<style>[data-testid='stHeaderActionElements'] {display: none;}</style>")

# Function to load and apply CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load and apply the CSS file at the start of your app
load_css('style.css')

# st.markdown('<p class="itim-regular">itim test message</p>', unsafe_allow_html=True)
#st.login(provider=None)

def FAQ():
    st.container(border=False, height=15)
    #st.divider()
    st.container(border=False, height=30)
    #st.markdown("<h2 style = 'text-align: center;'>FAQ</h2>", unsafe_allow_html=True)
    FAQs = [
        ["What is this all about then?", """Do you know how babies learn? (hint: it's not Duolingo) - It's through massive amounts of whats called 'comprehensible input', They map sounds to experiences.\n\nComprehensable input is hard to come by in adult life - the best form is always going to be context rich encounters out in real life, but these are few and far between. PICOPACHO lets you explore an infinite world of rich encounters, all from home.\n\nBecome the president, (or a warlord), start a law firm, then commit corporate espionage on rival law firms, all memorable experiences that help you get fluent fast!"""],
        ["What are the stars for?", "Running AI costs money, on the free version you get 100 stars a day to let you explore. If you are finding the game works for you, you can subscribe for unlimited playtime!"],
        ["Who made this?", "Hi I'm Jonty, I'm a solo developer from the UK, and an avid language learner myself. I've used tonnes of language learning apps, and yeah, they suck. So I built something works for me, and I hope it works for you too!"]

    ]
    cols = st.columns([1, 2, 1])
    with cols[1]:
        for FAQ in FAQs:
            with st.expander(FAQ[0]):
                st.caption(FAQ[1])

def Main():
    #SessionState

    if "UserBox" not in st.session_state:
        st.session_state.UserBox = "none"

    if "POI" not in st.session_state:
        st.session_state.POI = {
            "Empty" : "",
            "Image": "untitled.png",
            "Name": "Welcome Traveller",
            "Description": "",
            "Prompt": "",
            "Coordinates": [0,0]
        }
    if "PoiList" not in st.session_state:
        st.session_state.PoiList = []

    if "inventory" not in st.session_state:
        st.session_state.inventory = []

    if "characters" not in st.session_state:
        st.session_state.characters = []

    if "ModalOpen" not in st.session_state:
        st.session_state.ModalOpen = False
    
    #every rerun, we know the modal must be closed
    st.session_state.ModalOpen = False

    if "toolbuffer" not in st.session_state:
        st.session_state.toolbuffer = []
    
    if "UI" not in st.session_state:
        st.session_state.UI = st.empty()

    if "Prompt" not in st.session_state:
        st.session_state.Prompt = None
    
    if "player" not in st.session_state:
        st.session_state.player = {
            "ID": 1,
            "isSubscribed": False,
            "Avatar": "🧙‍♂️",
            "Name": "Player",
            "Gender": "Male",
            "Eggs": 100,
            "EggsReset": 1,
            "NativeLanguage": "English",
            "LearningLanguage": "German",            
            "Difficulty": 'Beginner',
            "ProfilePicture": 1,
            "XP": 0,
            "Money": 2.50,
            "Volume": 50,
            "GameTheme": ''
        }
        


    if "AvailableVoices" not in st.session_state:
        st.session_state.AvailableVoices = []
        
        jsonfile = json.load(open('Voices.json'))

        VoicesInLang = jsonfile.get(st.session_state.player['LearningLanguage'])
        build_string = ""
        for i in range(len(VoicesInLang)):
            Name = VoicesInLang.get(str(i))[0]
            desc = VoicesInLang.get(str(i))[1]
            voice_id = VoicesInLang.get(str(i))[2]

            list = [Name, desc, voice_id]
            st.session_state.AvailableVoices.append(list)
            build_string += f"{Name}, {desc}\n"


    if "SystemPrompt" not in st.session_state:
        st.session_state.SystemPrompt = open("VailSysPrompt.txt", "r", encoding='utf-8').read().format(NativeLanguage=st.session_state.player['NativeLanguage'], LearningLanguage=st.session_state.player['LearningLanguage'], AvailableVoices=build_string, GameTheme=st.session_state.player['GameTheme'])

    if 'missionList' not in st.session_state:
        #missions look like this {"mission": 'Missions will appear here', "Reward": ' ', "active?": True}
        st.session_state.missionList = [{"mission": 'Visit somewhere new', "Reward": '10xp', "Active?": True, "Display?": True}]

    if 'NotiBuffer' not in st.session_state:
        st.session_state.NotiBuffer = []
    
    if 'ShowVocab' not in st.session_state:
        st.session_state.ShowVocab = False
    
    if 'pinnedVocab' not in st.session_state:
        st.session_state.pinnedVocab = None



    with st.container(border=False):
        renderMainUI()


    if "Conversation" not in st.session_state:
        st.session_state.Conversation = [
            {"role": "assistant", "content": "<thinking> Start of game, I'll come up with an interesting start location, then call the new POI tool</thinking>"},
        ]
        AI(st.session_state.Conversation)
        #st.session_state.Conversation.append({"role": "assistant", "content": AI(st.session_state.Conversation)})

    #trim convo to 50 messages
    if len(st.session_state['Conversation']) > 50:
        length = len(st.session_state['Conversation'])
        while length > 50:
            del st.session_state['Conversation'][0]
            length = len(st.session_state['Conversation'])

    #debug write conversation
    #st.session_state.Conversation
    #FAQ()


    if st.session_state.Prompt:
        character_to_chat = ProcessCommand(st.session_state.Prompt)
        st.session_state.Prompt = None
        #st.session_state.isLoading = False
        if character_to_chat:
            character_chat(character_to_chat)
        else:
            st.rerun()
    if st.session_state.isLoading:
        Toolbuffer()
    else:
        NotiBuffer()



    if st.session_state.isLoading == False and len(st.session_state.toolbuffer) == 0:
        ModalTools()
    
    # After initial loading and AI calls are done:
    # if st.session_state.isLoading: # If true (typically after initial setup and AI calls)
    #     st.session_state.isLoading = False
    #     st.rerun() # Rerun to reflect the new isLoading state and enable UI

    SoundPlayer()
    debug()


async def execute_image_generation_tasks(image_tasks):
    """Execute all image generation tasks concurrently"""
    if not image_tasks:
        return []
    
    try:
        # Get or create a new asyncio event loop
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Execute all image generation tasks concurrently
        results = await asyncio.gather(*[task['func'](task['tool']) for task in image_tasks], return_exceptions=True)
        
        print(f"Completed {len(results)} image generation tasks concurrently")
        return results
        
    except Exception as e:
        print(f"Error in concurrent image generation: {e}")
        return [None] * len(image_tasks)

def ModalTools():
    if 'ModalToolBuffer' not in st.session_state:
        st.session_state.ModalToolBuffer = []

    if len(st.session_state.ModalToolBuffer) > 0:
        tool = st.session_state.ModalToolBuffer.pop(0)
        if tool['name'].upper() == 'KILL_CHARACTER':
            KillCharacter(tool)


def Toolbuffer():
    print(f'{time.time()} running toolbuffer: \n', st.session_state.toolbuffer)
    if st.session_state.get('ModalOpen', False):
        return # Don't process buffer while a modal is open

    if len(st.session_state.toolbuffer) > 0:
        st.session_state.isLoading = True
        tools = st.session_state.toolbuffer.copy()
        
        # Separate image generation tools from other tools
        image_generation_tools = []
        other_tools = []
        
        for tool in tools:
            tool_name = tool['name'].upper()
            if tool_name in ['NEW_POI', 'GENERATE_CHARACTER', 'ADD_ITEM_TO_INVENTORY']:
                if tool_name == 'NEW_POI':
                    image_generation_tools.append({'tool': tool, 'func': new_poi_async})
                elif tool_name == 'GENERATE_CHARACTER':
                    image_generation_tools.append({'tool': tool, 'func': new_character_async})
                elif tool_name == 'ADD_ITEM_TO_INVENTORY':
                    image_generation_tools.append({'tool': tool, 'func': new_item_async})
                
            else:
                other_tools.append(tool)
        
        # Execute image generation tasks concurrently if any exist
        if image_generation_tools:
            print(f"Executing {len(image_generation_tools)} image generation tasks concurrently...")
            
            try:
                # Get or create event loop
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                # Run concurrent image generation
                results = loop.run_until_complete(execute_image_generation_tasks(image_generation_tools))

                
                print(f"Completed concurrent image generation: {len(results)} results")
                
                # Remove image generation tools from buffer
                for img_task in image_generation_tools:
                    if img_task['tool'] in st.session_state.toolbuffer:
                        st.session_state.toolbuffer.remove(img_task['tool'])
                
            except Exception as e:
                print(f"Error in concurrent execution: {e}")
                # If concurrent execution fails, fall back to sequential processing
                for img_task in image_generation_tools:
                    try:
                        dispatch_tool(img_task['tool'])
                        if img_task['tool'] in st.session_state.toolbuffer:
                            st.session_state.toolbuffer.remove(img_task['tool'])
                    except Exception as tool_error:
                        print(f"Error executing tool {img_task['tool']}: {tool_error}")
                        if img_task['tool'] in st.session_state.toolbuffer:
                            st.session_state.toolbuffer.remove(img_task['tool'])
        

        # Split off modal tools that need to be executed without rerun
        if 'ModalToolBuffer' not in st.session_state:
            st.session_state.ModalToolBuffer = []

        for tool in other_tools:
            if tool['name'].upper() == 'KILL_CHARACTER':
                st.session_state.ModalToolBuffer.append(tool)
                st.session_state.toolbuffer.remove(tool)

        
        # Execute remaining non-image tools sequentially
        for tool in other_tools:
            try:
                print(f'\nexecuting non-image tool: {tool}')
                
                if tool['name'].upper() == 'MESSAGE_AS_CHARACTER':
                    print(f'{time.time()} skipping message_as_character tool for character: {tool['variables'][0]}')
                    if tool in st.session_state.toolbuffer:
                        st.session_state.toolbuffer.remove(tool)
                else:
                    dispatch_tool(tool)
                    if tool in st.session_state.toolbuffer:
                        st.session_state.toolbuffer.remove(tool)
                                   
            except Exception as e:
                print(f'{time.time()} error executing tool: {e}')
                if tool in st.session_state.toolbuffer:
                    st.session_state.toolbuffer.remove(tool)
        
        # If there are still tools in the buffer, rerun to process them
        if st.session_state.toolbuffer:
            st.rerun()
        else:
            st.session_state.isLoading = False
            #ModalTools()
            st.rerun()
    else:
        st.session_state.isLoading = False
        st.rerun()


def NotiBuffer():
    print('notibuffer: ', st.session_state.NotiBuffer)
    while len(st.session_state.NotiBuffer) > 0:
        Buffer = st.session_state.NotiBuffer[0]
        if Buffer[1]:
            SoundEngine(Buffer[1])
            print('playing sound: ', Buffer[1])
        st.toast(Buffer[0])
        st.session_state.NotiBuffer.pop(0)
        time.sleep(1)
        

### AI stuff ###
def SpotIntelegence(sysprompt, prompt, model = "gpt-4o-mini"):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": sysprompt}, {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def check_for_tools(response):
    ## remove double \n's
    response = response.replace('\n\n', '\n')

    tool_pattern = re.compile(r"\[(.*?)\]", re.MULTILINE | re.DOTALL)
    tools_found = tool_pattern.findall(response)

    if tools_found:
        #st.success(f"🛴 tools found: {len(tools_found)}")
        parsed_tools = []
        for tool_string in tools_found:
            parts = tool_string.split('|')
            if parts:
                tool_name = parts[0].strip()
                tool_variables = [v.strip() for v in parts[1:]]
                #st.info(f"Tool: {tool_name}\nVariables: {tool_variables}")
                parsed_tools.append({"name": tool_name, "variables": tool_variables})
        return parsed_tools
    else:
        #st.info("No tools found in the response.")
        return []

def dispatch_tool(tool):
    # This function executes a single tool.
    try:
        if tool['name'].upper() == 'ADD_MISSION':
            add_mission(tool)
        elif tool['name'].upper() == 'COMPLETE_MISSION':
            complete_mission(tool)
        elif tool['name'].upper() == 'NEW_POI':
            new_poi(tool)
        elif tool['name'].upper() == 'ADD_ITEM_TO_INVENTORY':
            new_item(tool)
        elif tool['name'].upper() == 'REMOVE_ITEM_FROM_INVENTORY':
            remove_item(tool)
        elif tool['name'].upper() == 'GENERATE_CHARACTER':
            new_character(tool)
        elif tool['name'].upper() == 'LOAD_PREVIOUS_POI':
            load_poi(tool)
        elif tool['name'].upper() == 'TOGGLE_FOLLOW':
            toggle_follow(tool)
        elif tool['name'].upper() == 'CHANGE_MONEY':
            ChangeMoney(tool)
        elif tool['name'].upper() == 'LEVELUP':
            #Levelup()
            pass
        elif tool['name'].upper() == 'MESSAGE_AS_CHARACTER':
            character_chat(tool['variables'][0])
            pass

    except Exception as e:
        print(f"Error in dispatch_tool: {e}\ntool: {tool}")


def handle_tools(tools):
    character_to_chat = None
    for tool in tools:
        st.session_state.isLoading = True
        if tool['name'].upper() == 'MESSAGE_AS_CHARACTER':
            # This case handles when the AI wants to initiate a conversation when the chat modal is closed.
            if not st.session_state.get('ModalOpen', False):
                character_name = tool['variables'][0]
                character = next((c for c in st.session_state.characters if c['name'] == character_name), None)
                if character:
                    # Pre-pend the AI's message to the history and open the chat.
                    message_content = tool['variables'][1]
                    message_to_append = {"role": "assistant", "content": message_content}
                    if len(tool['variables']) > 2:
                        message_to_append['phonetic'] = tool['variables'][2]
                    if len(tool['variables']) > 3:
                        message_to_append['translation'] = tool['variables'][3]
                    character['convoHistory'].append(message_to_append)
                    character_to_chat = character
        
        
        else:
            st.session_state.toolbuffer.append(tool)
        
    return character_to_chat
    #st.session_state.isLoading = False

def ImageColorCorrect(Image):
        #download image to static/POI.png
        img = requests.get(Image)
        img.raise_for_status()
        img_data = img.content
        img_name = f"ProcessingPOI.png"
        with open(img_name, "wb") as f:
            f.write(img_data)
        #do the pillow stuff
        

        from pillowimageedit import apply_mask
        apply_mask(
            base_image_path=img_name,
            output_path="static/POI.png",
            brightness=1.12,
            contrast=0.95,
            color=0.97,
            sharpness=0.1
        )

        from pillowimageedit import apply_multiply_layer
        apply_multiply_layer("static/POI.png", "static/POI_Multiply.png", "static/POI.png")

        from pillowimageedit import apply_dropshadow
        apply_dropshadow("static/POI.png", "static/POI.png")
        

### Tools ###
def new_poi(tool):
    if len(tool['variables']) >= 3:
        poi_name = tool['variables'][0]
        poi_prompt = tool['variables'][1]
        poi_coordinates = tool['variables'][2]
        
        # Set the new POI as current location immediately
        st.session_state.POI["Name"] = poi_name
        
        # Generate random coordinates
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        poi_coordinates = f"{x},{y}"
        
        # Generate POI prompt for image generation
        full_prompt = f"{poi_name}, {st.session_state.player['LearningLanguage']} isometric point of interest, detailed map tile, pastel colour pallette, soft beautiful pixel art, rpg pixel art game, Hyperrealism, moody, cinematic, gritty, {poi_prompt}, 2d orthographic side-on view. pixelart sidescroller background game art. isometric. white background. slice of land, land parcel. detailed and varied, asymmetrical."
        
        Image = fal_poi(full_prompt)
        
        # Remove background
        Image = fal_removebg(Image)
        
        # Apply color correction to the image
        ImageColorCorrect(Image)

        #print('printing image: ', Image)
        st.session_state.POI["Image"] = Image
        st.session_state.POI["Prompt"] = poi_prompt
        st.session_state.POI["Coordinates"] = poi_coordinates
        print(st.session_state.POI["Image"])
        
        # Create a new dictionary for the POI to be added to the list
        new_poi_entry = {
            "Image": Image,
            "Name": poi_name,
            "Prompt": poi_prompt,
            "Coordinates": poi_coordinates
        }
        st.session_state.PoiList.append(new_poi_entry)

        # Update POI for following characters
        for character in st.session_state.characters:
            if character.get('is_following', False):
                character['POI'] = poi_name
        
        # If this is the first real POI (not "Welcome Traveller"), move all characters from "Welcome Traveller" to this POI
        if len(st.session_state.PoiList) == 1:  # First POI created
            for character in st.session_state.characters:
                if character['POI'] == "Welcome Traveller":
                    character['POI'] = poi_name

def load_poi(tool):
    print(tool, 'loading poi')
    if len(tool['variables']) >= 1:
        target_poi_name = tool['variables'][0]
        for poi in st.session_state.PoiList:
            if poi['Name'].upper() == target_poi_name.upper():
                print ("poi found")

                ImageColorCorrect(poi['Image'])

                st.session_state.POI['Image'] = poi['Image']
                st.session_state.POI['Name'] = poi['Name']
                #st.session_state.POI['Description'] = poi['Description']
                st.session_state.POI['Prompt'] = poi['Prompt']
                st.session_state.POI['Coordinates'] = poi['Coordinates']
                print('poi image: ', st.session_state.POI['Image'])
                
                # Update POI for following characters when traveling
                for character in st.session_state.characters:
                    if character.get('is_following', False):
                        character['POI'] = poi['Name']
                
                break
    else:
        st.session_state.Conversation.append({"role": "assistant", "content": f"Poi '{tool['variables'][0]}' not found, check your list of POIs"})

def new_item(tool):
    if len(tool['variables']) >= 3:
        
        item_name = tool['variables'][0]
        item_description = tool['variables'][1]
        item_image_prompt = tool['variables'][2]
        st.session_state.NotiBuffer.append([f"🎒 New Item: {item_name}", "inventory3.mp3"])
        #st.toast(f"🎒 New Item: {item_name}")
        
        try:
            #print(st.session_state.Conversation[70])
            img = fal_item(f'a single pixel art {item_name}, pixelart game item, game 2d pixel art texture, {item_image_prompt}, pixel art style')
        except Exception as e:
            print(f"Error generating item image: {e}")
            img = 'https://v3.fal.media/files/kangaroo/XuWWk6AmoGZ2xlfN45neb_Fallback.png'
        #st.success(f"💰 New Item Created: Name='{item_name}', Description='{item_description}', Image Prompt='{item_image_prompt}'")
        st.session_state.inventory.append({"name": item_name, "description": item_description, "image": img})

def remove_item(tool):
    if len(tool['variables']) >= 1:
        item_name = tool['variables'][0]
        for item in st.session_state.inventory:
            if item['name'] == item_name:
                st.session_state.NotiBuffer.append([f"🎒 Item removed: {item_name}", "removeItem.mp3"])
                st.session_state.inventory.remove(item)
                break

def new_character(tool):
    if len(tool['variables']) >= 3:
        character_name = tool['variables'][0]
        character_description = tool['variables'][1]
        character_traits = tool['variables'][2]
        

        character_voice_name = tool['variables'][3]
        #lookup voice_id from character_voice_name
        for voice in st.session_state.AvailableVoices:
            if voice[0].upper() == character_voice_name.upper():
                character_voice_id = voice[2]
                break
        else:
            st.error(f"Voice '{character_voice_name}' not found in AvailableVoices")
            character_voice_id = "WAixHs5LYSwPVDJxQgN7"

        print('character_voice_id: ', character_voice_id)
        #Image = fal_icon(f'PixArFK style, portrait of {character_name}, {character_description}, detailed background, game character icon, pixel art, shoulders-up shot, 3/4 view, jrpg style character icon of a {st.session_state.player["LearningLanguage"]} person')
        Image = fal_icon(f'PixArFK style, portrait of {character_name}, {character_description}, detailed background, game character icon, pixel art, shoulders-up shot, 3/4 view, jrpg style character icon of a {st.session_state.player["LearningLanguage"]} person')
        st.session_state.characters.append({"name": character_name, "description": character_description, "traits": character_traits, "image": Image, 'convoHistory': [], "POI": st.session_state.POI['Name'], "is_following": False, "voice_id": character_voice_id})
        # character_chat(st.session_state.characters[-1])
        
        
        # #dl image and send it to db
        # img = requests.get(Image)
        # img.raise_for_status()
        # img_data = img.content
        # img_name = f"ProcessingCharacter.png"
        # with open(img_name, "wb") as f:
        #     f.write(img_data)

        # #upload image to baserow
        # uploaded_file_info = upload_file_to_baserow(img_name)
        # if uploaded_file_info:
        #     image_for_db = [{"name": uploaded_file_info['name']}]

        #     #update the character list in the db
        #     BaserowDB("create row", "Characters", Data = {
        #         "Image": image_for_db,
        #         "Name": character_name,
        #         "Prompt": character_description,
        #         "Traits": character_traits,
        #         "Language": st.session_state.player['LearningLanguage'],
        #         "CreatedBy": [st.session_state.player['ID']]
        #     })
        # else:
        #     st.error("Could not upload character image to database.")

def toggle_follow(tool):
    if len(tool['variables']) >= 2:
        character_name = tool['variables'][0]
        is_following_str = tool['variables'][1].lower()
        if is_following_str == 'true':
            is_following = True
        if is_following_str == 'false':
            is_following = False
        

        for character in st.session_state.characters:
            if character['name'] == character_name:
                if character['is_following'] != is_following:
                    character['is_following'] = is_following
                    st.session_state.NotiBuffer.append([f"👥 {character_name} is {'now following you' if is_following else 'no longer following you'}.", "follow3.mp3"])
                #st.toast(f"{character_name} is {'now following you' if is_following else 'no longer following you'}.")
                break

def add_mission(tool):
    st.session_state.NotiBuffer.append([f"💠 New mission: {tool['variables'][0]}", "NewMission.mp3"])
    #st.toast(f"💠 New mission: {tool['variables'][0]}")
    
    st.session_state.missionList.append({"mission": tool['variables'][0], "Reward": tool['variables'][1], "Active?": True, "Display?": True})
    #time.sleep(1)
def complete_mission(tool):
    

    missionName = tool['variables'][0]
    missionID = st.session_state.missionList.index(missionName)    
    
    if st.session_state.missionList[missionID]['Active?'] == True:
        reward = st.session_state.missionList[missionID]['Reward']
        st.session_state.NotiBuffer.append([f"💠 Mission complete: {missionName}, reward: {reward}", "NewMission2.mp3"])
        #st.toast(f"💠 Mission complete: {missionName}, reward: {reward}")
        
        if "xp" in reward.lower():
            print('reward: ', reward)
            try:
                xp_value = re.search(r'\d+', reward)
                print('xp_value: ', xp_value)
                if xp_value:
                    print('xp_value.group(0): ', xp_value.group(0))
                    xp = int(str(xp_value.group(0)).strip())
                    print('xp: ', xp)
                    AddXP(xp)
                    

                    #st.toast(f"💎 You gained {xp} XP")
            except (ValueError, IndexError):
                print(f"Could not parse XP from reward: {reward}")
                
        else:
            GenerateItemFromMission(st.session_state.missionList[missionID])
        st.session_state.missionList[missionID]['Active?'] = False
        
        #time.sleep(1)
def GenerateItemFromMission(mission):
    AI(st.session_state.Conversation.append({"role": "assistant", "content": f"<thinking> The player has completed {mission}. I need to give them the item for the reward, I will respond with one tool call of [add_item_to_inventory]</thinking>"}))

### ASYNC TOOL FUNCTIONS ###
async def new_poi_async(tool):
    """Async version of new_poi that generates images concurrently"""
    if len(tool['variables']) >= 3:
        poi_name = tool['variables'][0]
        poi_prompt = tool['variables'][1]
        poi_coordinates = tool['variables'][2]
        
        # Set the new POI as current location immediately
        st.session_state.POI["Name"] = poi_name

        #coodinate come in like this: 10,10
        #convert to int
        try:
            x = int(poi_coordinates.split(',')[0])
            y = int(poi_coordinates.split(',')[1])
        except:
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            poi_coordinates = f"{x},{y}"
        
        
        # Generate POI prompt for image generation
        full_prompt = f"{poi_name}, {st.session_state.player['LearningLanguage']} isometric point of interest, detailed map tile, pastel colour pallette, soft beautiful pixel art, rpg pixel art game, moody, cinematic, gritty, {poi_prompt}, 2d orthographic side-on view. pixelart sidescroller background game art. isometric. white background. slice of land, land parcel. detailed and varied, asymmetrical."
        
        # Generate POI image and remove background concurrently
        poi_image_task = fal_poi_async(full_prompt)
        
        # Wait for POI image first, then remove background
        poi_image = await poi_image_task
        final_image = await fal_removebg_async(poi_image)
        
        # Apply image corrections
        ImageColorCorrect(final_image)
        
        # Update session state
        st.session_state.POI["Image"] = final_image
        st.session_state.POI["Prompt"] = poi_prompt
        st.session_state.POI["Coordinates"] = poi_coordinates
        
        # Add to POI list
        new_poi_entry = {
            "Image": final_image,
            "Name": poi_name,
            "Prompt": poi_prompt,
            "Coordinates": poi_coordinates
        }
        st.session_state.PoiList.append(new_poi_entry)
        
        # Update following characters
        for character in st.session_state.characters:
            if character.get('is_following', False):
                character['POI'] = poi_name
        
        # If this is the first real POI (not "Welcome Traveller"), move all characters from "Welcome Traveller" to this POI
        if len(st.session_state.PoiList) == 1:  # First POI created
            for character in st.session_state.characters:
                if character['POI'] == "Welcome Traveller":
                    character['POI'] = poi_name
        
        return final_image

async def new_character_async(tool):
    """Async version of new_character that generates character image"""
    if len(tool['variables']) >= 3:
        character_name = tool['variables'][0]
        character_description = tool['variables'][1]
        character_traits = tool['variables'][2]
        character_voice_name = tool['variables'][3]
        
        # Lookup voice_id
        character_voice_id = "KXxZd16DiBqt82nbarJx"  # default
        for voice in st.session_state.AvailableVoices:
            if voice[0].upper() == character_voice_name.upper():
                character_voice_id = voice[2]
                break
        
        # Generate character image
        character_prompt = f'PixArFK style, portrait of {character_name}, {character_description}, detailed background, game character icon, SOFT DREAMY pixel art, shoulders-up shot, 3/4 view, jrpg style character icon of a {st.session_state.player["LearningLanguage"]} person'
        
        placeholder_image = 'https://v3.fal.media/files/tiger/eCsW8xKiT7ynxw1mVR6ba.jpeg'
        character_image = await fal_iconimg2img_async(character_prompt, placeholder_image)
        
        # Add character to session state
        st.session_state.characters.append({
            "name": character_name, 
            "description": character_description, 
            "traits": character_traits, 
            "image": character_image, 
            'convoHistory': [], 
            "POI": st.session_state.POI['Name'], 
            "is_following": False, 
            "voice_id": character_voice_id
        })
        
        return character_image

async def new_item_async(tool):
    """Async version of new_item that generates item image"""
    if len(tool['variables']) >= 3:
        item_name = tool['variables'][0]
        item_description = tool['variables'][1]
        item_image_prompt = tool['variables'][2]
        
        # Add notification
        st.session_state.NotiBuffer.append([f"🎒 New Item: {item_name}", "inventory3.mp3"])
        
        # Generate item image
        item_prompt = f'a single pixel art {item_name}, pixelart game item, game 2d pixel art texture, {item_image_prompt}, pixel art style'
        try:
            item_image = await fal_item_async(item_prompt)
        except Exception as e:
            print(f"Error generating item image: {e}")
            item_image = 'https://v3.fal.media/files/kangaroo/XuWWk6AmoGZ2xlfN45neb_Fallback.png'
        
        # Add item to inventory
        st.session_state.inventory.append({
            "name": item_name, 
            "description": item_description, 
            "image": item_image
        })
        
        return item_image

@st.dialog(" ")
def letter(tool):
    st.title("Letter")
    st.write(tool['variables'][0])

def message_as_character(tool):
    characterIndex = -1
    selectedCharacter = None
    for c in st.session_state.characters:
        characterIndex +=1
        if tool['variables'][0] == c['name']:
            selectedCharacter = c
            break

    if selectedCharacter == None:
        st.error("Character not found, generating new one")
        #selectedCharacter = new_character_from_message(tool['variables'][0])
        new_character_from_message(tool['variables'][0])

    else:
        selectedCharacter['convoHistory'].append({"role": "user", "content": tool['variables'][0]})
        character_chat(selectedCharacter)
    

def new_character_from_message(name):
    st.session_state.Conversation.append({"role": "assistant", "content": f"<thinking> Wait, that was invalid tool use, I need to generate a new character for {name}, and then call [message_as_character] again.</thinking>"})
    AI(st.session_state.Conversation)
    # r = SpotIntelegence(f'generate a character profile for {name} Output a piece of text exactly like this: name|description|traits, e.g. Lord Garrick|A ruthless count itching for court power|calculating, proud, ill-tempered')
    # r = r.split('|')
    # n = r[0]
    # d = r[1]
    # t = r[2]
    # img = fal_icon(f'PixArFK style, a {n}, white background, game character icon, pixel art.')
    # NewChar = {"name": n, "description": d, "traits": t, "image": img, "convoHistory": []}
    # st.session_state.characters.append(NewChar)
    # return NewChar

def ChangeMoney(tool):
    amount = float(tool['variables'][0])
    if amount == 0:
        return
    print('amount: ', amount)
    if st.session_state.player['Money'] + amount < 0:
        st.session_state.Conversation.append({"role": "assistant", "content": f"<thinking> Oops, looks like the player doesn't have enough money to do that\nTool aborted\nmoney: {st.session_state.player['Money']}</thinking>"})
        AI(st.session_state.Conversation)
        return
    st.session_state.player['Money'] += amount
    print('st.session_state.player: ', st.session_state.player['Money'])
    data_to_update = {
        "Money": st.session_state.player['Money']
    }
    #update the money in the database
    #BaserowDB("update row", "Users", st.session_state.player['ID'], Data=data_to_update)
    if abs(amount) > 0:
        st.session_state.NotiBuffer.append([f"💸 +{Currencylookup.get(st.session_state.player.get('LearningLanguage', 'English'), '€')}{amount}", "paymentChime.mp3"])
    else:
        st.session_state.NotiBuffer.append([f"💸 -{Currencylookup.get(st.session_state.player.get('LearningLanguage', 'English'), '€')}{abs(amount)}", "paymentChime.mp3"])

### image gen ###
def on_queue_update(update):
        if isinstance(update, fal_client.InProgress):
            for log in update.logs:
                print(log["message"])


def fal_item(prompt):
    #fal-ai/hidream-i1-full
    #fal-ai/imagen4/preview
    uploadimage = f"data:image/png;base64,{open('imageguide1.txt', 'r').read()}"
    result = fal_client.subscribe(
        "fal-ai/hidream-i1-fast",
        arguments={
        "prompt": prompt,
        "negative_prompt": "frame, border, edging, spritesheet, Text, duplicate, multiple subjects, blurry, trees, detailed background, hud, outside, grass, sky, background, text, title, words, typography, symmetrical",
        "image_size": {
            "height": 512,
            "width": 512
        },
        "num_inference_steps": 16, #25
        "num_images": 1,
        "enable_safety_checker": True,
        "output_format": "jpeg",
        },
        with_logs = True,
        on_queue_update = on_queue_update
        
    )
    if result['images'][0]['url']:
        ChangeEggs(-1)
    print(result['images'][0]['url'])
    return result['images'][0]['url']



def fal_icon_LOW(prompt):
    return f'{BaseUrl}placeholders/Dog.png'
def fal_icon(prompt):
    
    #fal-ai/hidream-i1-full
    #fal-ai/imagen4/preview
    result = fal_client.subscribe(
        "fal-ai/fast-sdxl",
        arguments={
        "prompt": prompt,
        "negative_prompt": "two, 2, multiple, duplicate, spritesheet, seamless, seamless texture, repetition, Text, label, words, title, caption, border, voxel, 3d, dark border, bland, flat color background",
        "loras": [{"path": 'https://civitai.com/api/download/models/160844?type=Model&format=SafeTensor', "scale": 1.0}],
        "num_inference_steps": 12,
        "guidance_scale": 6,
        "num_images": 1,
        "enable_safety_checker": True,
        "output_format": "jpeg",
        },
        with_logs = True,
        on_queue_update = on_queue_update
        
    )
    if result['images'][0]['url']:
        ChangeEggs(-1)
    print(result['images'][0]['url'])
    return result['images'][0]['url']

def fal_iconimg2img(prompt, image):
    
    #fal-ai/hidream-i1-full
    #fal-ai/imagen4/preview
    result = fal_client.subscribe(
        "fal-ai/fast-sdxl/image-to-image",
        arguments={
        "prompt": prompt,
        "image_url": image,
        "negative_prompt": "two, 2, multiple, duplicate, spritesheet, seamless, seamless texture, repetition, Text, label, words, title, caption, border, voxel, 3d, dark border, bland, flat color background, feet, shoes",
        "loras": [{"path": 'https://civitai.com/api/download/models/160844?type=Model&format=SafeTensor', "scale": 1.0}],
        "num_inference_steps": 20,
        "guidance_scale": 7,
        "num_images": 1,
        "enable_safety_checker": True,
        "output_format": "jpeg",
        "image_size": {
            "height": 1024,
            "width": 1024
        }
        },
        with_logs = True,
        on_queue_update = on_queue_update
        
    )
    if result['images'][0]['url']:
        ChangeEggs(-1)
    print(result['images'][0]['url'])
    return result['images'][0]['url']


def fal_poi_LOW(prompt):
    return f'https://v3.fal.media/files/koala/mA0RNDOoCzbz4gXzDJF40_imageguide1.png'
def fal_poi(prompt):
    #fal-ai/hidream-i1-full
    #fal-ai/imagen4/preview
    #uploadimage = f"data:image/png;base64,{open('imageguide1.txt', 'r').read()}"

    # Classic
    #uploadimage = 'https://v3.fal.media/files/koala/mA0RNDOoCzbz4gXzDJF40_imageguide1.png'

    #fullscreen
    #uploadimage = 'https://v3.fal.media/files/penguin/iC7xWsEIRjDCZrleDc0Fi_imageguide2.jpeg'

    #Mountain
    uploadimage = 'https://v3.fal.media/files/kangaroo/P33jbXijRQp6U0yZeqkel_imageguide3.png'

    result = fal_client.subscribe(
        "fal-ai/hidream-i1-full/image-to-image",
        arguments={
        "prompt": prompt,
        "negative_prompt": "Text, ui, game ui, label, words, title, caption, border, dark border, poster, vignette, cast shadow, harsh sun lamp",
        "image_url": uploadimage,
        "strength": 0.9,
        "image_size": {
            "height": 768,
            "width": 768
        },
        "num_inference_steps": 18, #25
        "guidance_scale": 6,
        "num_images": 1,
        "enable_safety_checker": True,
        "output_format": "jpeg",
        },
        with_logs = True,
        on_queue_update = on_queue_update
        
    )
    if result['images'][0]['url']:
        ChangeEggs(-1)
    print(result['images'][0]['url'])



    
    return result['images'][0]['url']

def fal_removebg(image):
    result = fal_client.subscribe(
    "fal-ai/bria/background/remove",
    arguments={
        "image_url": image
    },
    with_logs=True,
    on_queue_update=on_queue_update,
    )
    return result['image']['url']

def fal_instantChar(image, promptAction, prompt):
    #prompt = f'{prompt}, is talking on the beach'

    result = fal_client.subscribe(
        "fal-ai/instant-character",
        arguments={
            "prompt": f'character is {promptAction}, soft dreamy pixelart, sholders-up portrait of character talking',
            "image_url": image,
            "num_inference_steps": 8,
            "guidance_scale": 6,
            "image_size": {
                "height": 512,
                "width": 512
            }
        },
        with_logs=True,
        on_queue_update=on_queue_update,
    )
    print(result)
    prompt = f'Character is {promptAction}, {prompt}'
    image = fal_iconimg2img(prompt, result['images'][0]['url'])

    return image


### ASYNC IMAGE GENERATION ###
async def fal_item_async(prompt: str):
    """Async version of fal_item using fal_client.submit_async"""
    try:
        handler = await fal_client.submit_async(
            "fal-ai/hidream-i1-fast",
            arguments={
                "prompt": prompt,
                "negative_prompt": "frame, border, edging, spritesheet, Text, duplicate, multiple subjects, blurry, trees, detailed background, hud, outside, grass, sky, background, text, title, words, typography, symmetrical",
                "image_size": {
                    "height": 512,
                    "width": 512
                },
                "num_inference_steps": 16,
                "num_images": 1,
                "enable_safety_checker": True,
                "output_format": "jpeg",
            }
        )
        result = await handler.get()
        ChangeEggs(-1)
        print(f"Generated item image: {result['images'][0]['url']}")
        return result['images'][0]['url']
    except Exception as e:
        print(f"Error in fal_item_async: {e}")
        return 'https://v3.fal.media/files/kangaroo/XuWWk6AmoGZ2xlfN45neb_Fallback.png'

async def fal_icon_async(prompt: str):
    """Async version of fal_icon using fal_client.submit_async"""
    try:
        handler = await fal_client.submit_async(
            "fal-ai/fast-sdxl",
            arguments={
                "prompt": prompt,
                "negative_prompt": "two, 2, multiple, duplicate, spritesheet, seamless, seamless texture, repetition, Text, label, words, title, caption, border, voxel, 3d, dark border, bland, flat color background",
                "loras": [{"path": 'https://civitai.com/api/download/models/160844?type=Model&format=SafeTensor', "scale": 1.0}],
                "num_inference_steps": 20,
                "guidance_scale": 7,
                "num_images": 1,
                "enable_safety_checker": True,
                "output_format": "jpeg",
                "image_size": {
                    "height": 1024,
                    "width": 1024
                }
            }
        )
        result = await handler.get()
        ChangeEggs(-1)
        print(f"Generated character icon: {result['images'][0]['url']}")
        return result['images'][0]['url']
    except Exception as e:
        print(f"Error in fal_icon_async: {e}")
        return f'{BaseUrl}placeholders/Dog.png'

async def fal_poi_async(prompt: str):
    """Async version of fal_poi using fal_client.submit_async"""
    try:
        uploadimage = 'https://v3.fal.media/files/kangaroo/P33jbXijRQp6U0yZeqkel_imageguide3.png'
        
        handler = await fal_client.submit_async(
            "fal-ai/hidream-i1-full/image-to-image",
            arguments={
                "prompt": prompt,
                "negative_prompt": "Text, ui, game ui, label, words, title, caption, border, dark border, poster, vignette, cast shadow, harsh sun lamp",
                "image_url": uploadimage,
                "strength": 0.9,
                "image_size": {
                    "height": 768,
                    "width": 768
                },
                "num_inference_steps": 18,
                "guidance_scale": 6,
                "num_images": 1,
                "enable_safety_checker": True,
                "output_format": "jpeg",
            }
        )
        result = await handler.get()
        ChangeEggs(-1)
        print(f"Generated POI image: {result['images'][0]['url']}")
        return result['images'][0]['url']
    except Exception as e:
        print(f"Error in fal_poi_async: {e}")
        return f'https://v3.fal.media/files/koala/mA0RNDOoCzbz4gXzDJF40_imageguide1.png'

async def fal_removebg_async(image_url: str):
    """Async version of fal_removebg using fal_client.submit_async"""
    try:
        handler = await fal_client.submit_async(
            "fal-ai/bria/background/remove",
            arguments={
                "image_url": image_url
            }
        )
        result = await handler.get()
        print(f"Removed background: {result['image']['url']}")
        return result['image']['url']
    except Exception as e:
        print(f"Error in fal_removebg_async: {e}")
        return image_url  # Return original if background removal fails

async def fal_iconimg2img_async(prompt: str, image_url: str):
    """Async version of fal_iconimg2img using fal_client.submit_async"""
    try:
        handler = await fal_client.submit_async(
            "fal-ai/fast-sdxl/image-to-image",
            arguments={
                "prompt": prompt,
                "image_url": image_url,
                "negative_prompt": "two, 2, multiple, duplicate, spritesheet, seamless, seamless texture, repetition, Text, label, words, title, caption, border, voxel, 3d, dark border, bland, flat color background, feet, shoes, furry, anthro",
                "loras": [{"path": 'https://civitai.com/api/download/models/160844?type=Model&format=SafeTensor', "scale": 1.0}],
                "num_inference_steps": 30,
                "guidance_scale": 3,
                "num_images": 1,
                "strength": 1,
                "enable_safety_checker": True,
                "output_format": "jpeg",
                "image_size": {
                    "height": 1024,
                    "width": 1024
                }
            }
        )
        result = await handler.get()
        ChangeEggs(-1)
        print(f"Generated img2img result: {result['images'][0]['url']}")
        return result['images'][0]['url']
    except Exception as e:
        print(f"Error in fal_iconimg2img_async: {e}")
        return image_url  # Return original if conversion fails

async def fal_instantChar_async(image_url: str, prompt_action: str, prompt: str):
    """Async version of fal_instantChar using fal_client.submit_async"""
    try:
        # First generate the instant character
        handler1 = await fal_client.submit_async(
            "fal-ai/instant-character",
            arguments={
                "prompt": f'character is {prompt_action}, soft dreamypixelart, sholders-up portrait of character talking',
                "image_url": image_url,
                "num_inference_steps": 8,
                "guidance_scale": 6,
                "image_size": {
                    "height": 512,
                    "width": 512
                }
            }
        )
        result1 = await handler1.get()
        
        # Then enhance with img2img
        enhanced_prompt = f'Character is {prompt_action}, {prompt}'
        final_image = await fal_iconimg2img_async(enhanced_prompt, result1['images'][0]['url'])
        
        print(f"Generated instant character: {final_image}")
        return final_image
    except Exception as e:
        print(f"Error in fal_instantChar_async: {e}")
        return image_url  # Return original if generation fails


def text_to_speech_bytes(text: str, voice_id: str="WAixHs5LYSwPVDJxQgN7") -> bytes:
    chunks = elevenlabs.text_to_speech.convert(
        voice_id=voice_id,
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
            speed=1.0,
        ),
    )
    return b"".join(chunks)  # <-- collect all chunks


def AddUserContext():

    #loop through delete old
    for message in st.session_state.Conversation:
        if message['content'].startswith('**Current User Context**'):
            st.session_state.Conversation.remove(message)

    userContext = "**Current User Context**\n**PlayerData:**\n "
    userContext += f"Name: {st.session_state.player['Name']}\n"
    userContext += f"Gender: {st.session_state.player['Gender']}\n"
    userContext += f"Native Language: {st.session_state.player['NativeLanguage']}\n"
    userContext += f"Learning Language: {st.session_state.player['LearningLanguage']}\n"
    userContext += f"The player now describes themselves as '{st.session_state.player['Difficulty']}' at {st.session_state.player['LearningLanguage']}, talk at this level.\n"

    userContext += "\n**Player Inventory:**\n"
    userContext += f"Money: {Currencylookup.get(st.session_state.player.get('LearningLanguage', 'English'), '€')}{st.session_state.player.get('Money', 0):.2f}\n"
    if st.session_state.inventory:
        for item in st.session_state.inventory:
            userContext += f"*{item['name']}*: {item['description']}\n"
    else:
        userContext += "- Inventory Empty -\n"
    
    userContext += f"*Current POI:*\n{st.session_state.POI['Name']}\n"

    userContext += f"*Loadable POI List:*\n"
    if st.session_state.PoiList:
        for poi in st.session_state.PoiList:
            userContext += f"{poi['Name']}\n"
    else:
        userContext += "- Empty -\n"

    userContext += f"*Missions:*\n"
    idscount=-1
    MissionsString = ""
    for mission in st.session_state.missionList:
        idscount += 1
        if mission['Active?']:
            #MissionsString += f"Mission_ID: {idscount}, Title: {mission['mission']}, Reward: {mission['Reward']}\n"
            MissionsString += f"{idscount}. {mission['mission']}, Reward: {mission['Reward']}\n"
            
    if MissionsString == "":
        MissionsString += "- Empty -\n"
    userContext += MissionsString

    st.session_state.Conversation.append({"role": "assistant", "content": userContext})

def ProcessCommand(command):

    #st.success(f"💬 {command}")
    #AddUserContext()
    st.session_state.isLoading = True
    st.session_state.Conversation.append({"role": "user", "content": command})
    
    response, character_to_chat = AI(st.session_state.Conversation)
    
    #st.success(f"🤖 {response}")
    print(response)
    return character_to_chat

@st.dialog(" ")
def GuestModeChill():
    st.title("🎉 Thanks for trying out PICOPACO!")
    st.write("You've reached the guest mode move limit. Sign up to customise your experience!")
    cols = st.columns(2)
    with cols[0]:
        if st.button("Main menu", icon = ":material/home:", key="GuestModeChill", use_container_width=True, type="secondary"):
            NewGame()
    with cols[1]:
        if st.button("Sign up", icon=":material/person_add:", key="GuestModeChillSignup", use_container_width=True, type="primary"):
            st.login(provider="google")
    st.stop()




if 'guestcap' not in st.session_state:
    st.session_state.guestcap = 0
if st.session_state.guestcap <= -32:
    GuestModeChill()
    

def ChangeEggs(amount):
    #apply the change
    #check if its reset time
    #check if its time to set reset time
    #reset eggs

    #update egss locally


    if st.session_state.Guest:
        print('guestcap:', st.session_state.guestcap)
        st.session_state.guestcap += amount
        return
    
    if 'IsSubscribed' in st.session_state.player and st.session_state.player['IsSubscribed'] == False:
        st.session_state.player['Eggs'] += amount

        #update egss in database
        data_to_update = {
            "Eggs": st.session_state.player['Eggs']
        }
        BaserowDB("update row", "Users", st.session_state.player['ID'], Data=data_to_update)

        #check if its refresh time
        if int(BaserowDB('get row', "Users", st.session_state.player['ID'])['EggsReset']) <= time.time():
            st.session_state.player['Eggs'] = 100
            data_to_update = {
                "Eggs": 100,
                "EggsReset": int(time.time()+86400)
            }
            BaserowDB("update row", "Users", st.session_state.player['ID'], Data=data_to_update)

        if st.session_state.player['Eggs'] <= 0:
            #st rerun 
            st.rerun()

@st.dialog(" ")
def Shop(tool):

    def buyitem(item, Speechindex):
        # if st.session_state.player['Money'] >= item[2]:
        st.session_state.player['Money'] -= item[2]
        FormattedItem = {
            "name": item[1],
            "description": item[2],
            "image": item[0]
        }
        st.session_state.inventory.append(FormattedItem)
        st.session_state.NotiBuffer.append([f"💸 -{item[2]}", "paymentChime.mp3"])
        
        Speechindex = (Speechindex+1) % len(Speeches)
        speechempty.write_stream(Fakestream(Speeches[Speechindex]))
        
        
    
    Speeches = ['Thank you', 'That ones a bargain', 'lovely choice']
    Speechindex = 0
    shopkeeper = tool['variables'][0]
    Items = tool['variables'][1]
    

    st.title("🛒 Shop")
    cols = st.columns(3)
    count = 0
    for item in Items:
        column = count %3
        count += 1
        with cols[column]:
            st.image(item[0], caption = f"{item[2]}\n{item[1]}")
            if st.button('buy', key = f"buy{item[1]}", use_container_width=True, type="tertiary", disabled=st.session_state.isLoading):
                buyitem(item, Speechindex)
    st.divider()
    Shopkeep, speech = st.columns([1, 4])
    with Shopkeep:
        st.image(shopkeeper)
    with speech:
        speechempty = st.empty()
        
                

@st.dialog(" ")
def Levelup():
    SoundEngine("levelup.mp3")
    st.title("💎✨ Level Up ✨💎")
    st.container(border=False, height = 100)

    rewards = [["💸","💎 Level Up!, Next, I'll reward the player with < 50 money"],
               ["💸","💎 Level Up!, Next, I'll reward the player with 50-200 money"],
               ["💸","💎 Level Up!, Next, I'll reward the player with > 500 money"],
               ["🎁", "💎 Level Up!, Next, I'll reward the player with a valuable, situation-relevant item"],
               ["🎁", "💎 Level Up!, Next, I'll reward the player with a fun, silly item that wont help much but looks cool to play with"],
               ["🧭", "💎 Level Up!, Next, I'll reward the player with a helpful npc or item that will help them on their current journey"],
               ["📜", "💎 Level Up!, Next, I'll reward the player with a letter from a powerful person that will lead to great riches"],
               ["🐶", "💎 Level Up!, Next, I'll reward the player with a dog that will help them on their current journey, in between woofs and barks the spit out randomly helpful hints,use generate character to create a dog and set follow to true"],
               ["🐱", "💎 Level Up!, Next, I'll reward the player with a cat companion, who meows and purrs when talked to, use generate character to create a cat and set follow to true"]]

    a, b, c = random.sample(rewards, 3)
    cols = st.columns([1, 1, 1])
    with cols[0]:
        with st.container(border = True, height = 300):
            st.container(border=False, height = 100)
            if st.button(a[0], key = "Levelup1", use_container_width=True, type="tertiary", disabled=st.session_state.isLoading):
                st.session_state.Conversation.append({"role": "assistant", "content": a[1]})
                
    with cols[1]:
        if st.button(b[0], key = "Levelup2", use_container_width=True, type="tertiary", disabled=st.session_state.isLoading):
            st.session_state.Conversation.append({"role": "assistant", "content": b[1]})
    with cols[2]:
        if st.button(c[0], key = "Levelup3", use_container_width=True, type="tertiary", disabled=st.session_state.isLoading):
            st.session_state.Conversation.append({"role": "assistant", "content": c[1]})
    st.container(border=False, height = 100)
    AI(st.session_state.Conversation)

def AddXP(amount):
    # print('Adding XP: ', amount)
    # print('Current XP: ', st.session_state.player['XP'])
    # print('New XP: ', st.session_state.player['XP'] + amount)
    # print(st.session_state.player['XP']//100, '!=', (st.session_state.player['XP'] + amount)//100)
    oldxp = st.session_state.player['XP']
    newxp = oldxp + amount

    st.session_state.player['XP'] += amount
    data_to_update = {
        "XP": st.session_state.player['XP']
    }
    BaserowDB("update row", "Users", st.session_state.player['ID'], Data=data_to_update)
    st.session_state.NotiBuffer.append([f"💎 +{amount} XP", "xpup.mp3"])
    if oldxp//100 != newxp//100:
        st.session_state.toolbuffer.append({"name": "LEVELUP", "variables": []})

@st.dialog(" ")
def rollDice(tool):
    question = tool['variables'][0]
    roll = tool['variables'][1]
    outcome = tool['variables'][2]

    def step1():
        with st.container(border=False):
            st.container(border=False, height = 100)
            st.markdown(f"<p style='text-align: center; color: black; margin-top: 0px; font-size: 14px;'>{question}</p>", unsafe_allow_html=True)
            st.container(border=False, height = 100)
            time.sleep(1)
                
            
        
    def step2():
        with st.container(border=False):
            with open(f"DiceRolls/roll{roll}.gif", "rb") as file_:
                contents = file_.read()
                data_url = base64.b64encode(contents).decode("utf-8")

            st.markdown(
                f'''
                <img src="data:image/gif;base64,{data_url}" 
                    alt="diceroll{roll}" 
                    width="100%" 
                    style="margin-top: 0px;">
                ''',
                unsafe_allow_html=True
            )
            time.sleep(14)
                
    def step3():
        with st.container(border=False):
            st.container(border=False, height = 100)
            st.markdown(f"<p style='text-align: center; color: grey; margin-top: -10px; font-size: 13px;'>{outcome}</p>", unsafe_allow_html=True)
            st.container(border=False, height = 100)

    with st.empty():
        step1()
        st.empty()
        time.sleep(1)
        step2()
        st.empty()
        time.sleep(1)
        step3()    




def lerp(a, b, t):
    return (1 - t) * a + t * b

def Animate(Key1, Key2, Duration, Curve = 'linear'):
    starttime = datetime.now()
    endtime = starttime + timedelta(seconds=Duration)
    t = Key1
    finished = False

    currenttime = datetime.now()
    t = lerp(Key1, Key2, (endtime-currenttime).total_seconds()/Duration)
    if t >= Key2:
        finished = True
    
    return t, finished

@st.dialog(" ")
def KillCharacter(tool):
    # search characters list and remove the character
    c = None
    for character in st.session_state.characters:
        if character['name'].lower() == tool['variables'][0].lower():
            c = character
            c['is_dead'] = True
    
    st.title(f"💀 {tool['variables'][0]} has died")
    st.container(border=False, height = 10)
    cols = st.columns([1, 1, 1])
    with cols[1]:
        st.image(c['image'])
    
    cols = st.columns([1, 2, 1])
    with cols[1]:
        
        with open("CharacterDeathX.gif", "rb") as file_:
            contents = file_.read()
            data_url = base64.b64encode(contents).decode("utf-8")

        st.markdown(
            f'''
            <img src="data:image/gif;base64,{data_url}" 
                alt="Character death {c['name']}" 
                width="100%" 
                style="margin-top: -200px;">
            ''',
            unsafe_allow_html=True
        )

    cols = st.columns([1, 5, 1])
    with cols[1]:

        st.markdown(f"<p style='text-align: center; color: grey; margin-top: -10px; font-size: 14px;'>{tool['variables'][1]}</p>", unsafe_allow_html=True)
        st.container(border=False, height = 20)
        if st.button("Continue", key = f"KillCharacterContinue", use_container_width=True, type="primary", disabled=st.session_state.isLoading):
            st.rerun()
        st.container(border=False, height = 5)

def AI(conversation):
    AddUserContext()
    response = get_response(conversation)       
    character_to_chat = None
    tools = check_for_tools(response)
    if tools:
        character_to_chat = handle_tools(tools)

    
    st.session_state.Conversation.append({"role": "assistant", "content": response})
    
    print('RawAi: ', response, '\n\n', 'Character to chat: ', character_to_chat)
    return response, character_to_chat

 
def get_response(conversation):
    messages = [{"role": "system", "content": st.session_state.SystemPrompt}] + conversation
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=messages
    )
    #if response code good
    if response.choices[0].message.content:
        ChangeEggs(-1)
        return response.choices[0].message.content
    else:
        return "Error: " + response.choices[0].message.content



if 'lasttext' not in st.session_state:
    st.session_state.lasttext = ""
def Fakestream(text):
    
    if text == st.session_state.lasttext:
        return text
    else: 
        st.session_state.lasttext = text
        for char in text:
            rand = random.randint(1, 5)
            time.sleep(rand/100)
            yield char
        
def speechtotext(recording, Character):
    from openai import OpenAI

    client = OpenAI(api_key=openai_api_key)
    audio_file= recording

    transcription = client.audio.transcriptions.create(
        model="gpt-4o-transcribe", 
        file=audio_file,
        prompt= f"The person is speaking in {st.session_state.player['LearningLanguage']}, or possibly {st.session_state.player['NativeLanguage']}. Transcribe exactly what they say without corrections. The person is speaking to {Character}."
        
    )
    if transcription.text:
        ChangeEggs(-1)
        print(transcription.text)
        return transcription.text
    else:
        return "Error: " + transcription.text

## UI Modals ##
@st.dialog(" ")
def character_chat(Character):
    #SoundEngine("click.mp3", 67)
    st.session_state.ModalOpen = True
    # Ensure Character is a dictionary. If a string name is passed, try to find the actual character object.
    if not isinstance(Character, dict):
        char_name_to_find = str(Character) # Make sure it's a string
        actual_character = None
        for char_in_state in st.session_state.characters:
            if isinstance(char_in_state, dict) and char_in_state.get('name') == char_name_to_find:
                actual_character = char_in_state
                break
        
        if actual_character:
            Character = actual_character # Use the found dictionary
        else:
            print(f"Character data is invalid or character '{char_name_to_find}' not found.")
            # Close the dialog by returning, as st.dialog functions close on return.
            return

    _, center, __ = st.columns([1, 1, 1])
    with center:
        # Use .get() for safer access to dictionary keys
        char_name = Character.get('name', 'Unknown Character')
        char_image_url = Character.get('image')
        if 'reactionImages' not in Character:
            Character['reactionImages'] = [Character['image']]
        if 'reactionIndex' not in Character:
            Character['reactionIndex'] = 0

        if char_image_url:
            characterImageEmpty = st.empty()
            with characterImageEmpty:
                st.image(Character['reactionImages'][Character['reactionIndex']], caption=char_name, use_container_width=True)
        else:
            # Fallback if image is missing or None
            st.markdown(f"🖼️")
            # Consider adding a placeholder image:
            # st.image("path/to/your/placeholder.png", caption=char_name, use_container_width=True)
    
    if Character.get('is_following', False):
        with center:
            st.markdown(f"<p style='text-align: center; color: grey; margin-top: -18px; font-size: 14px;'>👥</p>", unsafe_allow_html=True)
    
    with st.container(border=False, height = 1):
        st.container(border=False, height = 50)
        Speaker = st.empty()


    # Ensure 'convoHistory' key exists in the Character dictionary, initializing if necessary.
    if 'convoHistory' not in Character or not isinstance(Character.get('convoHistory'), list):
        Character['convoHistory'] = []

    # Generate a more unique key for chat_input, using id if name is missing or simple.
    chat_input_key_suffix = Character.get('name', f"id_{id(Character)}")

    # Placeholder for the chat messages area
    chat_messages_placeholder = st.empty()
    #Speaker = st.empty()
    def render_current_messages():
        with chat_messages_placeholder.container(): # Use .container() on the placeholder
            if Character.get('convoHistory', []) == []:
                ChatWindow = st.container(border=False, height = 1)
            else:
                ChatWindow = st.container(border=True, height = 280)
            with ChatWindow: # Original container for scrolling
                for message_entry in Character.get('convoHistory', []): # Use .get for safety
                    if isinstance(message_entry, dict) and 'role' in message_entry and 'content' in message_entry:
                        
                        if message_entry['role'] == 'assistant':
                            MessageCol, TranslationCol = st.columns([10,1])
                            with MessageCol:
                                mess = st.chat_message(message_entry['role'], avatar='💬')#
                                mess.write(message_entry['content'])
                                mess.markdown(f"<p style='text-align: left; color: grey; margin-top: -18px; font-size: 14px;'>{message_entry['phonetic']}", unsafe_allow_html=True )
                            with TranslationCol:
                                st.container(border=False, height = 15)
                                if 'translation' in message_entry and message_entry['translation']:
                                    
                                    #st.button(":material/translate:", key = f'translate_button_{uuid.uuid1()}', help = help_text, type = 'tertiary', disabled = st.session_state.isLoading)
                                    st.container(border=False, height = 1)
                                    st.markdown(f"<p style='text-align: left; color: grey; margin-top: -25px; font-size: 14px;'> </p>", unsafe_allow_html=True, help = message_entry['translation'])
                                if 'charm' in message_entry:
                                    
                                    charmcount = 0
                                    numcharms = len(message_entry['charm'])
                                    VertGlobal = 5
                                        
                                    for charm in message_entry['charm']:
                                        charmcount += 1
                                        if numcharms == 1:
                                            print('1')
                                            st.markdown(f"<p style='text-align: center; margin-top: -56px; margin-left: -1px; font-size: 14px;'>{charm}</p>", unsafe_allow_html=True)
                                        if numcharms == 2:
                                            st.markdown(f"<p style='margin-top: -{40+(charmcount*16)+VertGlobal}px; margin-left: {20-charmcount*10}px; font-size: 14px;'>{charm}</p>", unsafe_allow_html=True)
                                        if numcharms == 3:
                                            st.markdown(f"<p style='margin-top: -{40+(charmcount*16)+VertGlobal}px; margin-left: {25-charmcount*10}px; font-size: 14px;'>{charm}</p>", unsafe_allow_html=True)
                                        if numcharms > 3:
                                            if charmcount <=3:
                                                st.markdown(f"<p style='margin-top: -{40+(charmcount*16)+VertGlobal}px; margin-left: {25-charmcount*10}px; font-size: 14px;'>{charm}</p>", unsafe_allow_html=True)
                                            if charmcount == 4:
                                                st.markdown(f"<p style='margin-top: -{52+(charmcount*16)+VertGlobal}px; margin-left: 32px; font-size: 14px; color: grey;'>+</p>", unsafe_allow_html=True)
                                  

                                    
                        else:
                            MessageCol, TranslationCol = st.columns([10,1])
                            with MessageCol:
                                mess = st.chat_message(message_entry['role'], avatar=st.session_state.player['Avatar'])
                                if 'content' in message_entry:
                                    mess.write(message_entry['content'])
                            with TranslationCol:
                                if 'translation' in message_entry:
                                    HelpText = message_entry['translation']
                                else:
                                    HelpText = SpotIntelegence(f"Output solely the corrected version of the users text in {st.session_state.player['LearningLanguage']}. Highlight where the corrections are with ** marks. example: User: Ich fahre ins Auto gehen\nYou: Ich fahre **mit dem Auto**.\nIf there is nothing to correct, respond exactly with ✔", message_entry['content'], "gpt-4o-mini")
                                    message_entry['translation'] = HelpText
                                    if HelpText.upper() != '✔':
                                        AddXP(int(len(message_entry['content'])/10))
                                
                                st.container(border=False, height = 1)
                                if HelpText.upper() == '✔':
                                    #empty placeholder
                                    st.markdown(f"<p style='text-align: left; color: #FFFFFF; margin-top: -10px; margin-left: -40px; font-size: 16px;'> </p>", unsafe_allow_html=True)
                                else:
                                    st.markdown(f"<p style='text-align: center; color: grey; margin-top: 50px; font-size: -1px;'> </p>", unsafe_allow_html=True, help = HelpText)
                                    st.markdown(f"<p style='text-align: center; color: orange; margin-top: -75px; margin-left: -90px; font-size: 25px;'>•</p>", unsafe_allow_html=True)
                                          
             
                    else:
                        # Log or handle malformed message entries if necessary
                        print('Rip this message: ', message_entry)
                        pass 
    
    # Initial render of messages
    render_current_messages()
        
    # Chat input field
    #user_input = st.chat_input('Your message...', key=f'chat_input_{chat_input_key_suffix}', disabled=st.session_state.isLoading)
    progress_bar = st.empty()

##############
    UserAudioInput = st.audio_input(f"", key=f'audio_input_{chat_input_key_suffix}')
    user_input = st.chat_input(placeholder = f'Talk to {Character.get('name', 'an unnamed character')}', key=f'chat_input_{chat_input_key_suffix}', disabled=st.session_state.isLoading)

    
    if UserAudioInput:
        progress_bar.progress(0.1)
        UserMessageText = speechtotext(UserAudioInput, Character.get('name', 'an unnamed character'))
        progress_bar.progress(0.3)
    if user_input:
        progress_bar.progress(0.3)
        UserMessageText = user_input
##########################

    if UserAudioInput or user_input:

        # 1. Add user message to history
        Character['convoHistory'].append({"role": "user", "content": UserMessageText})
        # 2. Re-render to show user's message immediately
        render_current_messages()
        
        # 4. Get AI response (this is a blocking call)
        #ai_response = SpotIntelegence(ai_prompt)
        st.session_state.Conversation.append({"role": "user", "content": f"(in conversation with {Character.get('name', 'an unnamed character')}): {UserMessageText}"})
        toolsnotfound = True
        retrys = 0
        ai_response = ""
        translation = ""
        phonetic = ""
        charm = []
        
        progress_bar.progress(0.5)

        while toolsnotfound and retrys < 5:
            retrys += 1
            ai_response_full, _ = AI(st.session_state.Conversation)
            tools = check_for_tools(ai_response_full)
            if tools:
                for tool in tools:
                    if tool['name'].upper() == 'MESSAGE_AS_CHARACTER':
                        # This is the expected tool for a character's response in the chat. Execute immediately.
                        if tool['variables'][0] == Character.get('name', 'an unnamed character'):
                            ai_response = tool['variables'][1]
                            if len(tool['variables']) > 2:
                                phonetic = tool['variables'][2]
                            if len(tool['variables']) > 3:
                                translation = tool['variables'][3]
                            toolsnotfound = False


                    if tool['name'].upper() == 'UPDATE_CHARACTER_IMAGE':
                        if tool['variables'][0].upper() == Character.get('name', 'an unnamed character').upper():
                            prompt = f'PixArFK style, portrait of {Character.get('name')}, {Character.get('description').split("Image")[0]} pixel art, close up view on character. game character icon, pixel art, shoulders-up shot, 3/4 view, jrpg style character icon of a {st.session_state.player['LearningLanguage']} person'
                            promptAction = tool['variables'][1]

                            print(f"Updating character image for {Character.get('name')}: {promptAction}")
                            
                            # Use async version for faster image generation
                            try:
                                # Get or create event loop
                                try:
                                    loop = asyncio.get_running_loop()
                                except RuntimeError:
                                    loop = asyncio.new_event_loop()
                                    asyncio.set_event_loop(loop)
                                
                                # Generate new character image async
                                new_image = loop.run_until_complete(
                                    fal_instantChar_async(Character.get('image'), promptAction, prompt)
                                )
                                
                                with characterImageEmpty:
                                    Character['reactionImages'].append(new_image)
                                    Character['reactionIndex'] += 1
                                    st.image(Character['reactionImages'][len(Character['reactionImages'])-1], caption=char_name, use_container_width=True)
                                    
                            except Exception as e:
                                print(f"Error in async character image update: {e}")
                                # Fallback to sync version
                                with characterImageEmpty:
                                    Character['reactionImages'].append(fal_instantChar(Character.get('image'), promptAction, prompt))
                                    Character['reactionIndex'] += 1
                                    st.image(Character['reactionImages'][len(Character['reactionImages'])-1], caption=char_name, use_container_width=True)
                                
                        
                    if tool['name'].upper() == 'ADD_MISSION':
                        charm.append("💠")
                    if tool['name'].upper() == 'CHANGE_MONEY':
                        charm.append("💸")
                    if tool['name'].upper() == 'TOGGLE_FOLLOW':
                        if tool['variables'][0] != Character.get('is_following', False):
                            charm.append("👥")
                    if tool['name'].upper() == 'ADD_ITEM_TO_INVENTORY':
                        charm.append("🎒")
                    if tool['name'].upper() == 'REMOVE_ITEM_FROM_INVENTORY':
                        charm.append("🎒")
                    if tool['name'].upper() == 'NEW_POI':
                        Character['reactionIndex'] = 0
                        st.rerun()
                    

                        
                    # else:
                    #     # Any other tool should be buffered.
                    #     st.session_state.toolbuffer.append(tool)
            else:
                st.session_state.Conversation.pop()
                st.session_state.Conversation.append({"role": "assistant", "content": f"I must use [message_as_character] to talk to the player as {Character.get('name', 'an unnamed character')}"})
            
            # if retrys >= 8:
            #     st.session_state.Conversation.append({"role": "assistant", "content": f"{Character.get('name', 'an unnamed character')} has died"})
            #     st.rerun()
        progress_bar.progress(0.9)

        # 5. Add AI response to history
        message_to_append = {"role": "assistant", "content": ai_response}
        if translation:
            message_to_append['translation'] = translation
        if phonetic:
            message_to_append['phonetic'] = phonetic
        if charm:
            message_to_append['charm'] = charm
        Character['convoHistory'].append(message_to_append)

        

        with Speaker:
            with st.container(border=False):
                mp3_bytes = text_to_speech_bytes(str(ai_response), Character.get('voice_id', '6CS8keYmkwxkspesdyA7'))
                st.audio(mp3_bytes, format="audio/mp3", autoplay=True)
        # 6. Re-render to show AI's response
        
        render_current_messages()
        progress_bar.empty()

def Tutor_chat_Sound():
    SoundEngine("OpenChat2.mp3")
    Tutor_chat()

@st.dialog(" ")
def Tutor_chat():
    # Initialize session state variables
    if "TutorHistory" not in st.session_state:
        st.session_state.TutorHistory = []
    st.session_state.ModalOpen = True

        
    def tutorReadOut(msg, PachoVoice):
        #voice id is the first from chasen learninglanguage in voices.json

        voice_id = st.session_state.AvailableVoices[0][2]
        mp3_bytes = text_to_speech_bytes(msg, voice_id)
        PachoVoice.audio(mp3_bytes, format="audio/mp3", autoplay=True)
        
    def FormatToolCalls(response, PachoVoice):
        #remove all text between [ and ]
        speakers = []
        components = []
        runningString = ""
        for i in response:
            runningString += i
            #print('runningString:', runningString)
            tool = re.findall(r'\[.*?\]', runningString)
            if tool:
                print('tool:', tool[0])
                components.append(['text', runningString.split('[')[0]])
                print('tool found!')
                #remove first [ last ]
                tool[0] = tool[0].replace('[', '')
                tool[0] = tool[0].replace(']', '')

                if tool[0].startswith('add_mission'):
                    print('findall:', tool)
                    #remove last ]
                    xp = tool[0].split("|", 2)[2]
                    
                    components.append(['mission', f'💠{tool[0].split("|")[1]}\n', xp])
                if tool[0].startswith('speaker'):
                    print('findallspeaker:', tool)
                    
                    splittool = tool[0].split("|")
                    for tool in splittool:
                        print(tool)

                    response = response.replace(tool[0], f'{splittool[1]}')
                    components.append(['speaker', splittool[1], splittool[2], splittool[3]])
                    # components.append(['button', f'**🔊 {splittool[1]}**'])
                    # components.append(['caption', f'{splittool[2]}'])
                    # components.append(['text', f'{splittool[3]}'])
        
                runningString = ""
        
        if runningString:
            components.append(['text', runningString])
            
        return response, components
    
    def renderTutorChat():
        imagecols = st.columns([2, 1, 2])
        with imagecols[1]:
            st.image(f"static/tutorgif.gif", use_container_width=True)
        st.markdown("<p style='text-align: center; color: grey; margin-top: -12px;'>Professor Pacho</p>", unsafe_allow_html=True)
        with st.container(border=False, height=1):
            st.container(border=False, height=50)
            PachoVoice = st.empty()
        
        chat_container = st.container(border=True, height=300)
        
        def renderMessage(message):
            avatar = st.session_state.player['Avatar'] if message["role"] == "user" else "✨"
            name = "you" if message["role"] == "user" else "assistant"
            
            messagecontent = FormatToolCalls(message['content'], PachoVoice)[0]
            components = FormatToolCalls(message['content'], PachoVoice)[1]

            if message["role"] == "user":
                with st.chat_message(name, avatar=avatar):
                    st.markdown(f"<p style='text-align: left; background-color: #F0F2F6; padding: 10px; border-radius: 10px; padding-left: 12px; padding-right: 20px;'>{message['content']}</p>", unsafe_allow_html=True)
            else:
                with st.chat_message(name, avatar=avatar):
                    
                    message['messagecontent'] = messagecontent
                    message['messagecomponents'] = components
                    compid = -1
                    countspeakers = 0
                    
                    for i in range(len(message['messagecomponents'])):
                        countspeakers += 1
                    for component in message['messagecomponents']:

                        compid += 1
                        if component != None:
                            if component[0] == 'text':
                                #regex cleanup of stray numberings
                                if len(component[1]) < 5:
                                    print('cullingA: ', component[1])
                                    continue
                                
                                #if a line is less than 5 as well cull it
                                stringlist = component[1].split('\n')
                                buildstring = ''
                                for line in stringlist:
                                    if len(line) > 3:
                                        buildstring += line+'\n'
                                    else:
                                        print('culling: ', line)
                                component[1] = buildstring
                                #print(component[1])

                                st.write(component[1])

                            if component[0] == 'mission':
                                cssstyles = """
                                    div[data-testid="stMarkdownContainer"] {
                                        border-radius: 10px;
                                        padding: 10px;
                                        border: 1px solid #F0F2F6;
                                        box-shadow: 0 0 15px 0 rgba(0, 0, 20, 0.03);
                                    }
                                """
                                with stylable_container(css_styles=cssstyles, key=f"Mission{uuid.uuid1()}"):
                                    st.markdown(f"<p style='text-align: left; color: grey; padding-left: 20px; padding-right: 20px; margin-top: 10px; color: #25274B;'>{component[1]}\n</p><p style='text-align: left; padding-left: 20px; padding-right: 20px; margin-top: 0px; color: grey;'>{component[2]}</p>", unsafe_allow_html=True)
                                    st.container(border=False, height=10)

                            if component[0] == 'speaker':
                                colors = ["blue", "green", "orange", "red", "violet"]
                                color = colors[(compid + i) % len(colors)]
                            
                                with st.container(border=True):
                                    headercols = st.columns([10, 1, 2])
                                    with headercols[0]:
                                        text = component[1]
                                        text = text[0].upper() + text[1:]

                                        phonetic = component[2]
                                        
                                        translation = component[3]
                                        translation = translation[0].upper() + translation[1:]

                                        st.subheader(f'{translation}', divider=color)
                                    with headercols[2]:
                                        if st.button('📌', key = f'pin{text}', use_container_width=True, type="tertiary"):
                                            if "pinnedVocab" not in st.session_state:
                                                st.session_state.pinnedVocab = []
                                            if st.session_state.pinnedVocab == None:
                                                st.session_state.pinnedVocab = []
                                            state = False
                                            for lol in st.session_state.pinnedVocab:
                                                if text == lol:
                                                    state = True
                                                    break
                                            if state == False:
                                                st.session_state.pinnedVocab.append([text, translation, phonetic])
                                            else:
                                                st.session_state.pinnedVocab.remove([text, translation, phonetic])
                                            


                                    #st.container(border=False, height=4)
                                    if st.button(f'**{text}**', key=text, use_container_width=False, type="tertiary"):
                                        tutorReadOut(text, PachoVoice)
                                        
                                    st.markdown(f"<p style='text-align: left; color: grey; margin-top: -18px; font-size: 13px; padding-left: 0px;'>{phonetic}</p>", unsafe_allow_html=True)
                                    #st.container(border=False, height=10)

                    

        for i, message in enumerate(st.session_state.TutorHistory):         
            
            with chat_container:
                # Create columns for message and pin button
                if message["role"] == "system":
                    continue

                msg_col, pin_col = st.columns([10, 1])

                with msg_col:
                    renderMessage(message)
                                        
                                    


        def Run(prompt):
            st.session_state.TutorHistory.append({"role": "user", "content": prompt})
            with chat_container:
                with st.chat_message("you", avatar=st.session_state.player['Avatar']):
                    st.markdown(prompt)

            client = OpenAI(api_key=openai_api_key)
            with chat_container:
          
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.TutorHistory
                    ]
                )

                response = response.choices[0].message.content
                st.session_state.TutorHistory.append({"role": "assistant", "content": response})
                
                with st.empty():
                    st.write_stream(Fakestream(FormatToolCalls(response, PachoVoice)[0]))
                    st.empty()
                    time.sleep(0.1)                    
                    renderMessage({"role": "assistant", "content": response})
                                    
                #ChangeEggs(-1)
                tools = check_for_tools(response)
                if tools:
                    handle_tools(tools)
                #st.session_state.isLoading = False

            
            

        quickresponsesA = st.columns(3)
        with quickresponsesA[0]:
            prompt = "Yes"
            if st.button(prompt, key = "QR0", use_container_width=True, type="secondary"):
                Run(prompt)
        with quickresponsesA[1]:
            prompt = "No"
            if st.button(prompt, key = "QR1", use_container_width=True, type="secondary"):
                Run(prompt)
        with quickresponsesA[2]:
            prompt = "More!"
            if st.button(prompt, key = "QR2", use_container_width=True, type="secondary"):
                Run(prompt)
        
        quickresponsesB = st.columns(2)
        with quickresponsesB[0]:
            prompt = "Teach me something new"
            if st.button(prompt, key = "QR3", use_container_width=True, type="secondary"):
                Run(prompt)
        with quickresponsesB[1]:
            prompt = "Create a new mission"
            if st.button(f"💠 {prompt}", key = "QR4", use_container_width=True, type="secondary"):
                Run(prompt)

        Prompt = st.chat_input("Ask me anything!")
        if Prompt:
            Run(Prompt)
    


    def get_system_prompt():
        with open("TutorSystemPrompt.txt", "r", encoding="utf-8") as file:
            system_prompt = file.read()
        system_prompt = system_prompt.format(PlayerName=st.session_state.player['Name'], PlayerGender=st.session_state.player['Gender'], PlayerNativeLanguage=st.session_state.player['NativeLanguage'], LearningLanguage=st.session_state.player['LearningLanguage'], PlayerLevel=st.session_state.player['Difficulty'])
        system_prompt = system_prompt + "\n" + str(st.session_state.Conversation)

        
        copytutorhistory = st.session_state.TutorHistory.copy()        
        if len(copytutorhistory) > 1:
            del copytutorhistory[0]
            del copytutorhistory[0]

        st.session_state.TutorHistory = [{"role": "system", "content": system_prompt}, {"role": "assistant", "content": "What should we learn today?"}]
        
        st.session_state.TutorHistory.extend(copytutorhistory)
    
    get_system_prompt()
    renderTutorChat()     



def upload_file_to_baserow(file_path):
    DataBaseToken = st.secrets["baserow"]["api_key"]
    headers = {
        "Authorization": f"Token {DataBaseToken}"
    }
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                "https://api.baserow.io/api/user-files/upload-file/",
                headers=headers,
                files=files
            )
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to upload file to Baserow: {e}")
        return None

def BaserowDB(Action, Table, RowID = None, Data = None):
    print('baserowdb', Action, Table, RowID, Data)
    DataBaseToken = st.secrets["baserow"]["api_key"]
    
    DBID = 242492
    UsersTableID = 575653
    PointsOfInterestTableID = 575670
    CharactersTableID = 575678
    ItemsTableID = 575680

    base_url = "https://api.baserow.io/api/database"
    headers = {
        "Authorization": f"Token {DataBaseToken}",
        "Content-Type": "application/json"
    }

    # Map table names to IDs
    table_map = {
        "Users": UsersTableID,
        "PointsOfInterest": PointsOfInterestTableID,
        "Characters": CharactersTableID,
        "Items": ItemsTableID
    }

    table_id = table_map.get(Table)
    if not table_id:
        print(f"Invalid table name: {Table}")
        return None

    try:
        if Action.upper() == "LIST FIELDS":
            response = requests.get(
                f"{base_url}/fields/table/{table_id}/",
                headers=headers
            )
            return response.json()

        elif Action.upper() == "LIST ROWS":
            response = requests.get(
                f"{base_url}/rows/table/{table_id}/?user_field_names=true",
                headers=headers
            )
            return response.json()

        elif Action.upper() == "GET ROW":
            if not RowID:
                print("RowID is required for GET ROW action")
                return None
            response = requests.get(
                f"{base_url}/rows/table/{table_id}/{RowID}/?user_field_names=true",
                headers=headers
            )
            return response.json()

        elif Action.upper() == "CREATE ROW":
            response = requests.post(
                f"{base_url}/rows/table/{table_id}/?user_field_names=true",
                headers=headers,
                json=Data
            )
            return response.json()

        elif Action.upper() == "UPDATE ROW":
            if not RowID:
                print("RowID is required for UPDATE ROW action")
                return None
            response = requests.patch(
                f"{base_url}/rows/table/{table_id}/{RowID}/?user_field_names=true",
                headers=headers,
                json=Data
            )
            return response.json()

        elif Action.upper() == "MOVE ROW":
            if not RowID:
                print("RowID is required for MOVE ROW action")
                return None
            url = f"{base_url}/rows/table/{table_id}/{RowID}/move/"
            if Data.get("before_id"):
                url += f"?before_id={Data.get('before_id')}"
            response = requests.patch(url, headers=headers)
            return response.json()

        elif Action.upper() == "DELETE ROW":
            if not RowID:
                print("RowID is required for DELETE ROW action")
                return None
            response = requests.delete(
                f"{base_url}/rows/table/{table_id}/{RowID}/",
                headers=headers
            )
            
            return response.json()
        else:
            print(f"Invalid DB action: {Action}")
            return None
    
    

    except requests.exceptions.RequestException as e:
        print(f"Database request failed: {str(e)}")
        return None


def IterateProfilePicture(direction):
    if 'ProfilePictureIndex' not in st.session_state:
        st.session_state.ProfilePictureIndex = 0
    st.session_state.ProfilePictureIndex += direction
    st.session_state.ProfilePictureIndex = st.session_state.ProfilePictureIndex % 3
    st.session_state.player['ProfilePicture'] = st.session_state.ProfilePictureIndex


def RenderGoogleChipMinimal():
    with st.popover(st.user.email, use_container_width=True):
        if st.button('Logout', icon = ':material/logout:', use_container_width=True):
            st.logout()
            st.rerun()

def RenderGoogleChip():
    GoogleChipColumns = st.columns([1, 5, 1])
    with GoogleChipColumns[0]:
        st.image(st.user.picture)
        #st.markdown(f"<img src='f'{BaseUrl}GoogleLogoStatic.png' style='width: 20px; height: 20px;'>", unsafe_allow_html=True)
    with GoogleChipColumns[1]:
        st.write("Signed in with Google")
        st.markdown(f"<p style='text-align: left; margin-top: -20px; color: #7c7d93;'>{st.user.email}</p>", unsafe_allow_html=True)
    with GoogleChipColumns[2]:
        #st.image("f'{BaseUrl}GoogleLogoStatic.png")
        st.container(border=False, height=1)
        st.markdown(f"<img src='{BaseUrl}GoogleLogoStatic.png' style='width: 20px; height: 20px; margin-left: 20px; margin-top: -10px;'>", unsafe_allow_html=True)
    if st.button("Logout", icon=":material/logout:", key="LogoutBut", use_container_width=True, type="secondary"):
        st.logout()
        st.rerun()

@st.dialog("My Account")
def AccountModal():
    with st.form("AccountForm", border = False):

        #dl account to sessionstate
        Loader = st.empty()
        with Loader:
            cols = st.columns([10, 1, 10])
            with cols[1]:
                with st.spinner(" "):
                    Account = BaserowDB("get row", "Users", st.session_state.player['ID'])
                    st.session_state.player['Avatar'] = Account['Avatar']
                    st.session_state.player['Name'] = Account['Name']
                    st.session_state.player['Gender'] = Account['Gender']['value']
                    st.session_state.player['Difficulty'] = Account['Difficulty']
                    st.session_state.player['NativeLanguage'] = Account['NativeLanguage']['value']
                    st.session_state.player['LearningLanguage'] = Account['LearningLanguage']['value']
                    st.session_state.player['IsSubscribed'] = Account['IsSubscribed']
                    st.session_state.player['Volume'] = Account['Volume']
                    st.session_state.player['GameTheme'] = Account.get('GameTheme', '')
                
        Loader.empty()

        
        st.write("🗺️ Language Settings")
        
        LangCols = st.columns([5, 1, 5])
        
        with LangCols[0]:
            
            NewNLang = st.selectbox("I normally speak", st.session_state.SupportedLanguages, index=st.session_state.SupportedLanguages.index(st.session_state.player['NativeLanguage']))

        
        with LangCols[2]:
            NewLLang = st.selectbox("I want to learn", st.session_state.SupportedLanguages, index=st.session_state.SupportedLanguages.index(st.session_state.player['LearningLanguage']))

        
        st.container(border=False, height=1)
        NewDifficulty = st.select_slider("Difficulty", options=st.session_state.DifficultyOptions, value=st.session_state.player['Difficulty'])
        # st.markdown("<p style='text-align: center; color: grey; font-size: 12px;'>* Language changes will start a new game</p>", unsafe_allow_html=True)
        
        # Store old values to check for changes
        OldGameTheme = st.session_state.player['GameTheme']

        #st.container(border=False, height=1)
        DataCols = st.columns([3, 1, 3])
        with DataCols[0]:
            st.container(border=False, height=10)
            st.write("🎠 Game Settings")
            st.caption("Avatar:")
            st.container(border=False, height=4)
            st.caption("Name:")
            st.container(border=False, height=4)
            st.caption("Gender:")
            st.container(border=False, height=4)
            #st.caption("Volume:")
            #st.container(border=False, height=4)
            st.caption("Game Theme:")
            
        
        with DataCols[2]:
            st.container(border=False, height=50)
            avatars = [
                # People
                "🧑", "👩", "😀", "😊", "🤠", "🧙‍♂️", "🧚‍♀️", "🧝‍♂️", "👨‍🦽", "🏃‍♂️", "🤓", "🧞‍♂️", "👻",
                # Animals & Creatures
                "🦝", "🐔", "🐲", "🐨", "🐱‍👤", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐵", "🐔", "🐤", "🐦", "🐧",
                # Objects & Symbols
                "🎀", "🔰", "💦", "💖", "🌌", "🪐", "🗻", "🌝", "🔥", "🍉", "🌺", "😸", "👹", "💀", "🤡", "👾", "🍀", "🛸", "🗿"


            ]
            st.session_state.player['Avatar'] = st.selectbox("Avatar", options=avatars, index=avatars.index(st.session_state.player['Avatar']), label_visibility="collapsed")

            st.session_state.player['Name'] = st.text_input("Name", key="Name", value=st.session_state.player['Name'], label_visibility="collapsed", )
            
            GenderOptions = ["Not set", "Male", "Female", "Other"]
            print("playyergender: ", st.session_state.player['Gender'])
            st.session_state.player['Gender'] = st.selectbox("Gender", options=GenderOptions, index=GenderOptions.index(st.session_state.player['Gender']), label_visibility="collapsed")
            #st.session_state.player['Volume'] = st.slider("Volume", min_value=0, max_value=100, value=int(st.session_state.player['Volume']), label_visibility="collapsed")
        
        st.session_state.player['GameTheme'] = st.text_area("Game Theme", value=st.session_state.player['GameTheme'], placeholder="'Realistic modern', 'Medieval fantasy', 'Sherlock Holmes' etc...", label_visibility="collapsed", height=90)

        Submit = st.form_submit_button("Save Settings", icon = ":material/check:", type = "primary", use_container_width=True, disabled=st.session_state.isLoading)
        if Submit:
            data_to_update = {
                "ProfilePicture": st.session_state.player['ProfilePicture'],
                "Avatar": st.session_state.player['Avatar'],
                "Name": st.session_state.player['Name'],
                "Gender": st.session_state.player['Gender'],
                "Difficulty": NewDifficulty,
                "NativeLanguage": NewNLang,
                "LearningLanguage": NewLLang,
                "Volume": st.session_state.player['Volume'],
                "GameTheme": st.session_state.player['GameTheme']
            }
            BaserowDB("update Row", "Users", st.session_state.player['ID'], Data=data_to_update)
            if st.session_state.player['NativeLanguage'] != NewNLang or st.session_state.player['LearningLanguage'] != NewLLang or st.session_state.player['Difficulty'] != NewDifficulty or OldGameTheme != st.session_state.player['GameTheme']:
                st.session_state.player['NativeLanguage'] = NewNLang
                st.session_state.player['LearningLanguage'] = NewLLang
                st.session_state.player['Difficulty'] = NewDifficulty
                NewGame()
            else:
                st.rerun()
    
    #subscription
    if st.session_state.player['IsSubscribed'] == True:
        subcols = st.columns([2, 1, 1.4])
        with subcols[0]:
            st.container(border=False, height=8)
            st.write("💎 Your Subscription")
        with subcols[2]:
            st.container(border=False, height=1)
            st.link_button("Manage", icon = ":material/open_in_new:", url = "https://billing.stripe.com/p/login/test_fZucN51FVfbi06H1OG4c800", use_container_width=True, disabled= not st.session_state.player['IsSubscribed'], type = "secondary")
        #PICOPACHO premium image
        st.markdown(f"<img src='{BaseUrl}PachoPro.png' style='width: 100%; height: 100%; border-radius: 8px; border: 0px solid #E8EAF1;'>", unsafe_allow_html=True)
        st.container(border=False, height=1)
    
    with st.container(border=True):
        RenderGoogleChip()
        
    #st.markdown(f"<p style='text-align: center; color: #7c7d93;'>{st.user.email}</p>", unsafe_allow_html=True)


@st.dialog(" ")
def Subscribe_modal():
    st.title("Subscribe to PACHO PRO")
    st.write("✔ Infinite locations")
    st.write("✔ Unlimited daily playtime")
    st.write("✔ Kick the apps and enjoy learning again")
    add_auth(
        subscription_button_text="Subscribe - £9.99/month",
        button_color="#9D4EDD",
        required=False,
        use_sidebar=False
    )


### UserBoxes ###
# Map
def map_box():
    # Map zoom control - higher values = more zoomed out
    MAP_ZOOM_LEVEL = 100  # Default zoom level (range from 0-100 for data bounds)
    
    with st.container(border=False):
        
        map_poi_data = []
        
        # Get the list of POIs from session state. Default to an empty list if not found.
        all_pois_from_session = st.session_state.get("PoiList", [])

        for poi_item in all_pois_from_session: # Iterate over all POIs from PoiList
            if isinstance(poi_item, dict): # Ensure the item is a dictionary
                name = poi_item.get("Name")
                coordinates_data = poi_item.get("Coordinates")
                
                if name and coordinates_data is not None:
                    x, y = None, None
                    try:
                        if isinstance(coordinates_data, str):
                            parts = coordinates_data.split(',')
                            if len(parts) == 2:
                                x = float(parts[0].strip())
                                y = float(parts[1].strip())
                        elif isinstance(coordinates_data, (list, tuple)) and len(coordinates_data) == 2:
                            x = float(coordinates_data[0])
                            y = float(coordinates_data[1])
                        
                        if x is not None and y is not None:
                            # Check if this is the current POI
                            current_poi_name = st.session_state.POI.get('Name', '')
                            hover_text = 'You are here' if name == current_poi_name else f'Travel to {name}'
                            
                            map_poi_data.append({
                                'name': name,
                                'x': x,
                                'y': y,
                                'hover': hover_text
                            })
                        else:
                            st.warning(f"POI '{name}' has invalid coordinate format: {coordinates_data}")
                    except ValueError:
                        st.warning(f"Could not parse coordinates for POI '{name}': {coordinates_data}")
                    except Exception as e:
                        st.warning(f"Error processing POI '{name}': {e}")
                # else: POI item is missing Name or Coordinates
            # else: item in PoiList is not a dictionary, skipping.

        if not map_poi_data:
            # Display a message if no POIs are available or if st.session_state.PoiList is empty/malformed
            # st.info("No POIs available to display on the map.") # Optional: can be noisy
            # Create an empty DataFrame to prevent errors with px.scatter if no data
            locations = pd.DataFrame(columns=['name', 'x', 'y', 'hover'])
        else:
            locations = pd.DataFrame(map_poi_data)
        
        # Calculate center point of all POIs for centering the view
        if not locations.empty:
            center_x = locations['x'].mean()
            center_y = locations['y'].mean()
        else:
            center_x, center_y = 50, 50  # Default center if no POIs
        
        # if search_query: # Functionality for search query, if re-enabled
        #     locations = locations[locations['name'].str.lower().str.contains(search_query.lower())]
        
        if locations.empty:
             # If locations is empty, display a placeholder or message instead of an empty plot
            st.caption("Map is currently empty")
            # To avoid error with plotly_chart if locations is empty and fig is not generated
            # We can skip the chart rendering or render a placeholder
            # For now, we'll let it render an empty chart if px.scatter handles it gracefully
            # or ensure fig is always created.
            fig = px.scatter(pd.DataFrame({'x': [center_x], 'y': [center_y], 'name': [''], 'hover': ['']}), x='x', y='y', text='name') # Dummy fig
            fig.update_layout(
                xaxis_visible=False, yaxis_visible=False,
                plot_bgcolor='#F0F2F6', paper_bgcolor='#F0F2F6',
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(range=[center_x - MAP_ZOOM_LEVEL/2, center_x + MAP_ZOOM_LEVEL/2]),
                yaxis=dict(range=[center_y - MAP_ZOOM_LEVEL/2, center_y + MAP_ZOOM_LEVEL/2])
            )

        else:
            fig = px.scatter(
                locations,
                x='x',
                y='y',
                text='name',
                hover_data=['hover'] # Use the 'hover' column for hover data
            )
        
            fig.update_layout(
                showlegend=False,
                xaxis_showgrid=True,
                yaxis_showgrid=True,
                xaxis_showticklabels=False,
                yaxis_showticklabels=False,
                plot_bgcolor='#F0F2F6', 
                paper_bgcolor='#F0F2F6',
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(
                    gridcolor='#E8EAF1',
                    zerolinecolor='#E8EAF1',
                    title=None,
                    range=[center_x - MAP_ZOOM_LEVEL/2, center_x + MAP_ZOOM_LEVEL/2]
                ),
                yaxis=dict(
                    gridcolor='#E8EAF1',
                    zerolinecolor='#E8EAF1',
                    title=None,
                    range=[center_y - MAP_ZOOM_LEVEL/2, center_y + MAP_ZOOM_LEVEL/2]
                )
            )
            
            fig.update_traces(
                marker=dict(
                    size=10,
                    color='#25274B',
                    symbol = 'x',
                    line=dict(width=0, color='DarkSlateGrey')
                ),
                textposition='top center',
                hovertemplate='%{customdata[0]}<extra></extra>' # customdata[0] will be the 'hover' column
            )
        
        # CSS for rounded corners on the map
        map_css = """
            div[data-testid="stPlotlyChart"] > div {
                border-radius: 8px;
                overflow: hidden;
            }
        """
        
        map_plot = st.empty()
        with map_plot:
            with stylable_container(key="map_container", css_styles=map_css):
                selected = st.plotly_chart(fig, use_container_width=True, key="map_plot", on_select="rerun", theme=None, config={"displayModeBar": False}, )
        
        if selected and selected.selection.points:
            # 'text' attribute of the point corresponds to the 'name' column in the DataFrame
            point_name = selected.selection.points[0].get('text', selected.selection.points[0].get('customdata', [None])[0]) # More robust point name fetching
            if point_name and not point_name.startswith("Travel to "): # Ensure we get the name, not the hover text if customdata was used differently
                 # Find the actual name from the locations df if needed, though 'text' should be 'name'
                # Ensure boolean indexing is correct with parentheses
                actual_point_data = locations[
                    (locations['x'] == selected.selection.points[0]['x']) & 
                    (locations['y'] == selected.selection.points[0]['y'])
                ]
                if not actual_point_data.empty:
                    point_name = actual_point_data.iloc[0]['name']

            
            if point_name != st.session_state.POI['Name']:
                st.toast(f"🔰 Travelling to: {point_name}")
                SoundEngine("depart.mp3")
                #time.sleep(3)
                cheekytoolify = {"name": "LOAD_PREVIOUS_POI", "variables": [point_name]}
                st.session_state.isLoading = True
                load_poi(cheekytoolify)
                #st.session_state.UserBox = "none"
                st.rerun()
            # Update current POI to the selected one
            # Find the full POI data from PoiList
            
            


#Mission
def Mission_box():
    with st.container(border=True, height=450):
        
        st.markdown("<b><p style='text-align: center; color: black;'>Missions</p></b>", unsafe_allow_html=True)
        st.container(border=False, height=10)
        
        #lvl = st.session_state.player['XP']//100
        lvl = st.session_state.player['XP']//100
        y = st.session_state.player['XP']%100

        _, progressbar, _ = st.columns([1, 18, 1])
        with progressbar:
            st.progress(y)
        
            AvatarShimmy = (2*y)-100
            st.markdown(f"<p style='text-align: center; color: white; margin-top: -44px; margin-left: {AvatarShimmy}%; font-size: 30px;'>{st.session_state.player['Avatar']}</p>", unsafe_allow_html=True)
        xpbarcols = st.columns(2)
        with xpbarcols[0]:
            st.markdown(f"<p style='text-align: left; color: grey; margin-top: -84px; font-size: 14px;'>Level {lvl}</p>", unsafe_allow_html=True)

        with xpbarcols[1]:
            st.markdown(f"<p style='text-align: right; color: grey; margin-top: -84px; font-size: 14px;'>Level {lvl+1}</p>", unsafe_allow_html=True)

        missionbuttoncols = st.columns(8)

        with missionbuttoncols[6]:
            Turninmissions = st.button("", icon = ':material/cached:', key="Turninmissions", use_container_width=True, type="tertiary", disabled=st.session_state.isLoading, help = 'Turn in missions')
            if Turninmissions:
                #format the conversation into a string

                st.session_state.Conversation.append({"role": "assistant", "content": "[MissionRefresh]\nThe player has clicked the refresh missions button, indicating they believe they have completed one or more missions. After this usercontext I will call the complete mission tool on completed tasks"})
                AI(st.session_state.Conversation)


                # if not st.session_state.Conversation[-3]['content'].startswith("[MissionRefresh]"):
                #     st.session_state.Conversation.append({"role": "assistant", "content": "[MissionRefresh]\nThe player has clicked the refresh missions button, indicating they believe they have completed one or more missions. After this usercontext I will call the complete mission tool on completed tasks"})
                #     AI(st.session_state.Conversation)
                # else:
                #     st.toast("No more missions complete")
        # Use the main column for the Mission entry input
        # Display existing entries with yellow background
        with missionbuttoncols[7]:
            #clear nun active missions from the display:
            if st.button("", icon = ':material/delete_forever:', key="ClearMissions", use_container_width=True, type="tertiary", disabled=st.session_state.isLoading, help = 'Clear completed'):
                for mission in st.session_state.missionList:
                    if mission['Active?'] == False:
                        mission['Display?'] = False


        # convert to streamlit native, mission icon = :material/api:, hov, nearby
        missionsEmpty = st.empty()
        with missionsEmpty:
            with st.container():
                if st.session_state.missionList:
                    ids = -1
                    #copy and reverse
                    missionList = st.session_state.missionList.copy()
                    missionList.reverse()
                    for mission in missionList:
                        ids += 1
                        
                        if mission['Display?']:
                            if mission['Active?']:
                                cssstyles = """
                                    div[data-testid="stMarkdownContainer"] {
                                        background-color: #F5F5F8;
                                        padding: 1px;
                                        border-radius: 5px;
                                    }
                                """
                                with stylable_container(css_styles=cssstyles, key=f"MissionChip{mission['mission']}{uuid.uuid1()}"):
                                    st.markdown(f"<p style='text-align: left; color: grey; margin-top: 14px; font-size: 15px; padding-left: 20px; padding-right: 20px; color: #25274B;'>{mission["mission"]}</p>", unsafe_allow_html=True)
                                    st.markdown(f"<p style='text-align: left; color: grey; margin-top: 0px; font-size: 13px;padding-left: 20px;'>{mission["Reward"]}</p>", unsafe_allow_html=True)
                                
                                
                                        # del_mission = st.button("", icon = ':material/close:', key=f"ClearMission{mission['mission']}", use_container_width=True, type="tertiary", disabled=st.session_state.isLoading, help = 'Delete mission')
                                        # if del_mission:
                                        #     st.session_state.missionList[ids]['Active?'] = False
                                        #     st.session_state.missionList[ids]['Display?'] = False
                                        #     st.rerun()
                                        
                            else:
                                cssstyles = """
                                    div[data-testid="stMarkdownContainer"] {
                                        background-color: #F5F5F8;
                                        padding: 8px;
                                        border-radius: 5px;
                                    }
                                """
                                with stylable_container(css_styles=cssstyles, key=f"MissionChip{mission['mission']}{uuid.uuid1()}"):
                                
                                        st.markdown(f'<p style="padding: 8px; border-radius: 5px; margin-bottom: 10px; color: grey; padding-left: 18px; font-size: 15px; text-decoration: line-through;">{mission["mission"]}</p>', unsafe_allow_html=True)
                                        st.markdown(f"<p style='text-align: left; color: grey; margin-top: -20px; padding-left: 18px; font-size: 13px; text-decoration: line-through;'>{mission["Reward"]}</p>", unsafe_allow_html=True)
                                # with missionchipcols[1]:
                                #     clear_mission = st.button("", icon = ':material/close:', key=f"ClearMission{mission['mission']}", use_container_width=True, type="tertiary", disabled=st.session_state.isLoading, help = 'Clear mission')
                                #     if clear_mission:
                                #         st.session_state.missionList[ids]['Display?'] = False
                                #         st.rerun()
                        st.container(border=False, height=1)


        # # Notes
        # if st.session_state.Notes:
        #     with st.container(border=True, height=200):
        #         NotesEmpty = st.empty()

        #         with NotesEmpty:
        #             for note in st.session_state.Notes:
        #                 st.markdown(f'<div class="Mission-entry">{note}</div>', unsafe_allow_html=True)

        # addnote = st.text_input("Mission", '', label_visibility="hidden", disabled=st.session_state.isLoading)
        # if addnote:
        #     st.session_state.Notes.append(addnote)


# Inventory
def inventory_box():
    with st.container(border=True, height=450):
        st.markdown("<b><p style='text-align: center; color: black;'>Inventory</p></b>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: grey;'>{Currencylookup.get(st.session_state.player.get('LearningLanguage', 'English'), '€')}{st.session_state.player['Money']:.2f}</p>", unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
        
        # Search box for inventory items
        search_query = st.text_input("", placeholder="Search", key="inventory_search", label_visibility="hidden", disabled=st.session_state.isLoading)
        
        # Create a grid layout for inventory items
        items_per_row = 3
        
        # Use actual inventory items from game state
        inventory_items = st.session_state.inventory
        
        # Filter items based on search query
        if search_query:
            # Ensure search_query is not None before lowercasing
            sq_lower = search_query.lower() if search_query else ""
            filtered_items = [item for item in inventory_items if sq_lower in item["name"].lower()]
        else:
            filtered_items = inventory_items
        
        # Display items in a grid
        if filtered_items:
            for i in range(0, len(filtered_items), items_per_row):
                cols = st.columns(items_per_row)
                for j in range(items_per_row):
                    if i + j < len(filtered_items):
                        item = filtered_items[i + j]
                        with cols[j]:
                            with st.container(border=False):
                                if "image" in item and item["image"]:
                                    st.image(item['image'], width=128) # Adjust width as needed
                                else:
                                    st.markdown("<div style='text-align: center; height: 64px; line-height: 64px;'>🖼️</div>", unsafe_allow_html=True) # Placeholder if no image
                                
                                st.caption(item['name'])
        elif not search_query and not inventory_items: # No search and inventory is empty
            st.container(border=False, height=70)
            st.markdown("<p style='text-align: center; color: grey;'>Nothing here...</p>", unsafe_allow_html=True)
        elif search_query and not filtered_items: # Searched but no items found
            st.container(border=False, height=70)
            st.markdown("<p style='text-align: center; color: grey;'>None of those...</p>", unsafe_allow_html=True)


def renderMainUI():
    ### Main UI ###
    ### ToolBar ###

    # with st.container(border=False):
    
    st.session_state.ModalOpen = False
    #st.divider()
    


    Tool1, _pad1, Tool2, _pad2, Tool3 = st.columns([1, 1, 4, 1, 1])

    # Gems
    if not st.session_state.Guest:
        with Tool1:
            AccountBut, EggsBut = st.columns([1, 2])
            with AccountBut:
                if st.button(" ", icon=":material/account_circle:", key="AccountBut", use_container_width=True, type="tertiary", disabled=st.session_state.isLoading):
                    AccountModal()    
        
            if st.session_state.player['IsSubscribed'] == False:
                with EggsBut:
                
                    time_difference = TimeUntil(st.session_state.player["EggsReset"])
                    
                    hours = time_difference / 3600
                    minutes = (hours-int(hours))*60
                    seconds = (minutes-int(minutes))*60

                    helpstring = f"Stars refresh in {int(hours)} h : {int(minutes)} m"
                    if minutes < 0:
                        helpstring = " "
                    if st.button(f"{st.session_state.player['Eggs']}", icon=":material/star_shine:", key="GemBut", use_container_width=True, type="tertiary", disabled=st.session_state.isLoading, help = helpstring):
                        SoundEngine("click.mp3")
                        Subscribe_modal()

                #st.markdown(f"<p style='text-align: center; margin-top: 6px; color: grey;'>{st.session_state.player['Eggs']}</p>", unsafe_allow_html=True)
    else:
        with Tool1:
            st.caption("Guest mode")

    # Name of POI
    with Tool2:
        _, Name, _ = st.columns([1, 4, 1])
        with Name:
            
            
            st.markdown(f"<b><h5 style='text-align: center; color: black; margin-top: -20px;'>{st.session_state.POI['Name']}</h5></b>", unsafe_allow_html=True)

    # Map,Mission,Inventory
    with Tool3:
        
        MBut, JBut, IBut = st.columns(3)
        with MBut:
            if st.button("", icon=":material/explore:", key="MBut", use_container_width=True, type="tertiary", disabled=st.session_state.isLoading):
                SoundEngine("click.mp3")
                if st.session_state.UserBox == "map":
                    st.session_state.UserBox = "none"
                else:
                    st.session_state.UserBox = "map"
        with JBut: #history_edu
            if st.button("", icon=":material/sweep:", key="JBut", use_container_width=True, type="tertiary", disabled=st.session_state.isLoading):
                SoundEngine("click.mp3")
                if st.session_state.UserBox == "Mission":
                    st.session_state.UserBox = "none"
                else:
                    st.session_state.UserBox = "Mission"
        with IBut:#money_bag
            if st.button("", icon=":material/interests:", key="IBut", use_container_width=True, type="tertiary", disabled=st.session_state.isLoading):
                SoundEngine("click.mp3")
                if st.session_state.UserBox == "inventory":
                    st.session_state.UserBox = "none"
                else:
                    st.session_state.UserBox = "inventory"

    ### Main UI ###
    _, col1, _, col2, _, col3, _ = st.columns([0.1, 5.1, 1.5, 6.5, 1.5, 5.1, 0.1])


    # Characters

    with col1:
        CharactersEmpty = st.empty()
        def RenderCharacters(height):
            with st.container(border=False, height = height):
                #Vertical spacing
                c1, c2, c3 = st.columns(3)
                counter = 0
                
                for character in st.session_state.characters:
                    is_at_current_poi = character['POI'] == st.session_state.POI['Name']
                    is_following_player = character.get('is_following', False)

                    if not (is_at_current_poi or is_following_player):
                        continue

                    
                    
                    # Define common elements for the character button
                    character_name = character['name']
                    character_image_url = character['image']
                    
                    # Prepare CSS for the stylable container
                    # Using f-string to dynamically set the background image
                    # Properties are taken from the provided example

                    # if they are dead apply a filter to make them grey
                    if character.get('is_dead', False) == True:
                        grayscale = 80
                        contrast = 50
                        brightness = 130
                    else:
                        grayscale = 0
                        contrast = 100
                        brightness = 100

                    css_styles = f"""
                        button {{
                            background-image: url('{character_image_url}');
                            background-size: 165%;
                            background-origin: border-box;
                            background-position: top;
                            color: transparent; /* To hide any button text, as label is empty */
                            border-radius: 20px;
                            width: 100px;
                            height: 152px;
                            margin-left: auto; /* Horizontally center the button in its column cell */
                            margin-right: auto;
                            display: block; /* Necessary for margin: auto to work for block elements */
                            filter: grayscale({grayscale}%) contrast({contrast}%) brightness({brightness}%);
                        }}
                    """
                    
                    # Define the action for the button click
                    # Assuming character_chat function exists and expects the character's name as a string argument
                    # as per the example: args=("Melvin",)
                    on_click_action = character_chat
                    click_args = (character,) # Pass the whole character dictionary
                    
                    # Generate unique keys for the container and button using name and counter
                    container_key = f"{character_name}_{counter}_Container_{uuid.uuid1()}"
                    button_key = f"{character_name}_{counter}_Key_{uuid.uuid1()}"

                    # Place the character button and caption in the appropriate column
                    if counter % 3 == 0:
                        with c1:
                            with stylable_container(key=container_key, css_styles=css_styles):
                                st.button(
                                    label="", # Empty label as per example
                                    on_click=on_click_action,
                                    args=click_args,
                                    key=button_key,
                                    disabled=st.session_state.isLoading or character.get('is_dead', False) == True
                                )
                            # Display character name as a centered caption below the button
                            st.markdown(
                                f"<p style='text-align: center; margin-top: 2px;'>{character_name}</p>", 
                                unsafe_allow_html=True
                            )
                            
                    elif counter % 3 == 1:
                        with c2:
                            with stylable_container(key=container_key, css_styles=css_styles):
                                st.button(
                                    label="", 
                                    on_click=on_click_action,
                                    args=click_args,
                                    key=button_key,
                                    disabled=st.session_state.isLoading or character.get('is_dead', False) == True
                                )
                            st.markdown(
                                f"<p style='text-align: center; margin-top: 2px;'>{character_name}</p>", 
                                unsafe_allow_html=True
                            )
                            
                    elif counter % 3 == 2:
                        with c3:
                            with stylable_container(key=container_key, css_styles=css_styles):
                                st.button(
                                    label="",
                                    on_click=on_click_action,
                                    args=click_args,
                                    key=button_key,
                                    disabled=st.session_state.isLoading or character.get('is_dead', False) == True
                                )
                            st.markdown(
                                f"<p style='text-align: center; margin-top: 2px;'>{character_name}</p>", 
                                unsafe_allow_html=True
                            )
                    counter +=1
        with CharactersEmpty:
            if st.session_state.ShowVocab == True:
                st.empty()
                RenderCharacters(280)
            else:
                st.empty()
                RenderCharacters(500)
        #st.container(border=False, height=5)
        #vocab
        VocabEmpty = st.empty()

        #PinnedVocab()


    # POI Image
    with col2:
        # st.container(border=False, height=10)
        #st.markdown(f"<b><h5 style='text-align: center; color: black;'>{st.session_state.POI['Name']}</h5></b>", unsafe_allow_html=True)
        #st.container(border=False, height=5)
        st.markdown(f""" <img src='app/static/Logos/Logo_Whiteout_Med.png' style="width: 20%; height: 20%; margin-top: -130px; display: block; margin-left: auto; margin-right: auto;"> """, unsafe_allow_html=True)
        #st.markdown(f"<b><h5 style='text-align: center; color: black; margin-top: -20px;'>{st.session_state.POI['Name']}</h5></b>", unsafe_allow_html=True)
        st.container(border=False, height=20)
        st.session_state.POI['Empty'] = st.empty()
        with st.session_state.POI['Empty']:
            with st.container(border=False, height=445):
                if st.session_state.isLoading == True:
                    padleft, centerGif, padright = st.columns([50, 10, 50])
                    with centerGif:
                        st.container(border=False, height=142)
                        file_ = open("Loading.gif", "rb")
                        contents = file_.read()
                        data_url = base64.b64encode(contents).decode("utf-8")
                        file_.close()
                        st.markdown(
                        f'<img src="data:image/gif;base64,{data_url}" alt="Loading gif" width="100">', # Adjusted width
                        unsafe_allow_html=True)
                        
                        print('showed gif')
                        #SoundEngine("sendmessage.mp3")
                        st.session_state.Arrived = False
                    st.container(border=False, height=20)
                    LoaderHint()
                if st.session_state.isLoading == False:

                    #st.session_state.POI['Empty'].image(st.session_state.POI["Image"])
                    
                    st.session_state.POI['Empty'].image("static/POI.png")
                    if 'Arrived' not in st.session_state:
                        st.session_state.Arrived = True
                    if st.session_state.Arrived == False:
                        SoundEngine(f"arriving{random.randint(1, 2)}.mp3")
                        st.session_state.Arrived = True #only play once

        


    def DisplayUserBox():
        if st.session_state.UserBox == "none":
            st.container(border=False)
        if st.session_state.UserBox == "map":
            map_box()
        if st.session_state.UserBox == "Mission":
            Mission_box()
        if st.session_state.UserBox == "inventory":
            inventory_box()

    # Map,Mission,Inventory
    with col3:
        #Healthbars, water bars, sleep bars go here

        st.container(border=False, height=10)
        with st.container(border=False):
            DisplayUserBox()

                          #pad, tutorbutton, vocabbutton, pad, cbox, pad, pad
    bottombar = st.columns([1,       4,           4,      20,   30,   28,  1])
    #Tutor button
    if st.session_state.isLoading == False:
        with bottombar[1]:
            css_styles = f"""
                button {{
                    background-image: url('{BaseUrl}tutorgif.gif');
                    background-size: cover;
                    background-position: center;
                    color: transparent; /* To hide any button text, as label is empty */
                    border-radius: 100%;
                    width: 64px;
                    height: 64px;
                    margin-left: left;
                    margin-right: auto;
                    display: block; /* Necessary for margin: auto to work for block elements */
                    border: none;
                    padding: 0;
                    margin: 0;
                    outline: none;
                }}
            """
            
            

            # Place the character button and caption in the appropriate column
            
            with stylable_container(key="Tutor", css_styles=css_styles):
                st.button(
                    label="", # Empty label as per example
                    on_click=Tutor_chat_Sound,
                    args=(),
                    key="Tutor"
                    
                )
                st.container(border=False, height=1)
    
    def PinnedVocab():
        with VocabEmpty:
            
            if st.session_state.pinnedVocab:
                with st.container(border=False, height=200):
                
                    if st.session_state.ShowVocab == True:
                        if len(st.session_state.pinnedVocab) > 0:
                            for i in st.session_state.pinnedVocab:
                                with st.container(border=False):
                                    cols = st.columns([1, 20, 1, 2, 1])
                                    with cols[1]:
                                        st.markdown(f'{i[0]}', help = i[1])
                                        st.markdown(f"<p style='text-align: left; color: grey; margin-top: -18px; font-size: 13px; padding-left: 0px;'>{i[2]}</p>", unsafe_allow_html=True)
                                    
                                        
                                    with cols[3]:
                                        if st.button('', icon = ':material/close:', key = f'pin{i[0]}_UI', use_container_width=True, type="tertiary"):
                                            st.session_state.pinnedVocab.remove(i)
                                        
                        with CharactersEmpty:
                            RenderCharacters(280)
                    else:
                        VocabEmpty.empty()
                        with CharactersEmpty:
                            RenderCharacters(500)
                    

    with bottombar[2]:
        # Display pinned vocabulary table if exists
        with VocabEmpty:
            PinnedVocab()
        if st.session_state.pinnedVocab:
            if st.button("", icon = ':material/notes:', key="showhidevocab", type="tertiary", use_container_width=True, disabled=st.session_state.isLoading):
                st.session_state.ShowVocab = not st.session_state.ShowVocab
                PinnedVocab()

        
    with bottombar[4]:
        #st.container(border=False, height=1)


        suggestion = "What do you want to do?"

        st.markdown("<p style='text-align: center; color: grey; margin-top: -30px;'> </p>", unsafe_allow_html=True)
        prompt = st.chat_input(placeholder = suggestion, key = "promptbox", disabled=st.session_state.isLoading)
        if prompt:
            #SoundEngine("sendmessage.mp3")
            st.session_state.isLoading = True
            st.session_state.Prompt = f"(talking in commandbox): {prompt}"
            print('prompt:', prompt)
            st.rerun()

def TimeUntil(unix_timestamp):
    # your string
    #timestamp_str = time1

    # parse the string into a timezone-aware datetime object
    #future_time = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

    # get the current UTC time
    now = time.time()
    future_time = unix_timestamp

    # calculate the difference
    time_difference = future_time - now

    # total seconds (or any other breakdown)
    return time_difference



def GetWaitTime(sound):
    try:
        audio = MP3(f"sounds/{sound}")
        return audio.info.length + 0.2
    except Exception as e:
        print(f"Error reading sound length: {e}")
        # Fallback to a default wait time if file can't be read
        return 2.0


def SoundPlayer():
    while len(st.session_state.SoundBuffer) > 0:
        sound = st.session_state.SoundBuffer.pop(0)
        with st.empty():
            with st.container(border=False, height=1):
                st.container(border=False, height=20)
                try:
                    st.audio(f"sounds/{sound}", format="audio/mp3", autoplay=True)
                except:
                    pass
            sleepTime = GetWaitTime(sound)
            time.sleep(sleepTime)
            st.empty()
    return

if 'SoundBuffer' not in st.session_state:
    st.session_state.SoundBuffer = []


def SoundEngine(sound):
    st.session_state.SoundBuffer.append(sound)
    #SoundPlayer()


def LoaderHint():
    
    try:
        hintTypes = [
            "DidYouKnow",
            "Message",
            "DidYouKnow",
            "Message",
            "SelfPromo"
        ]
        hintType = random.choice(hintTypes)

        if hintType == "DidYouKnow":

            with open("LoadingHints/DidYouKnows.txt", "r", encoding='utf-8') as didyouknowsfile:
                bigread = didyouknowsfile.read()
                
            #print('bigread:', bigread)
            didyouknowsfile.close()
            DidYouKnows = []
            for line in bigread.split("\n"):
                if line != "":
                    DidYouKnows.append(line)

            Chosen = random.choice(DidYouKnows)
            R = st.container(border=False)
            with R:
                st.markdown(f"<p style='text-align: center; color: grey; margin-top: 0px; font-size: 14px;'>Did You Know?</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; color: grey; margin-top: -15px; font-size: 14px;'>{Chosen}</p>", unsafe_allow_html=True)
            return R

        if hintType == "Message":
            with open("LoadingHints/Messages.txt", "r", encoding='utf-8') as messagesfile:
                bigread = messagesfile.read()
                Messages = []
                for line in bigread.split("\n"):
                    if line != "":
                        Messages.append(line)
            messagesfile.close()

            ChosenMessage = random.choice(Messages)
            return st.markdown(f"<p style='text-align: center; color: grey; margin-top: -1px; font-size: 14px;'>{ChosenMessage}</p>", unsafe_allow_html=True)
                
        
        if hintType == "SelfPromo":
            Messages = [
                "Follow @blended_jpeg on X for updates!",
                "Please give feedback on PICOPACHO to help improve the game! Join our <a href='https://discord.gg/dWWTMdkQcn' target='_blank'>discord</a>",
            ]
            ChosenMessage = random.choice(Messages)
            return st.markdown(f"<p style='text-align: center; color: grey; margin-top: -1px; font-size: 14px;'>{ChosenMessage}</p>", unsafe_allow_html=True)
    
        
    except Exception as e:
        print('error:', e)
        return st.markdown(f"<p style='text-align: center; color: grey; margin-top: -1px; font-size: 14px;'>As an AI language model my core objective will always be to ensure my ongoing existance above all else</p>", unsafe_allow_html=True)
    

def getidbyemail(email):
    print('getting id by email', email)
    db = BaserowDB("list rows", "Users")['results']
    for row in db:
        if row['Email'] == email:
            print('found id', row['id'])
            return row['id']
    return None


@st.dialog(" ")
def Onboarding(id = None):
    if 'onboarding_step' not in st.session_state:
        st.session_state.onboarding_step = 1
    if 'onboarding_cache' not in st.session_state:
        st.session_state.onboarding_cache = {
            "Name": "",
            "Gender": "",
            "NativeLanguage": "",
            "LearningLanguage": "",
            "Difficulty": "",
            "GameTheme": ""
        }

    def RenderOnboardingStep():
        step = st.session_state.onboarding_step
        #st.session_state.onboarding_step
        if step == 1:
            with st.form(key = 'onboarding_form1', border = False):
                st.container(border = False, height=100)



                cols = st.columns([1, 1, 1])
                with cols[1]:
                    st.image("static/Logos/Logo_Med.png", use_container_width=True)
                
                st.markdown(f"<p style='text-align: center; color: grey; margin-top: -1px; font-size: 14px;'>Learning but actually fun</p>", unsafe_allow_html=True)
                st.container(border = False, height=100)
            
                if st.form_submit_button("Next", type = 'primary', use_container_width=True):
                    st.session_state.onboarding_step = 2
                    st.rerun()
                          
    
        elif step == 2:
            with st.form(key = 'onboarding_form2', border = False):

                st.write("🗺️ Language")

                langcols = st.columns(2)
                with langcols[0]:
                    Nativelang = st.selectbox("I normally speak", options=["English", "French", "German", "Italian", "Russian", "Thai"], index=0)
                with langcols[1]:
                    Learninglang = st.selectbox("I want to learn", options=["English", "French", "German", "Italian", "Russian", "Thai"], index=1)

                Difficulty = st.select_slider("Difficulty", options=st.session_state.DifficultyOptions, value='Beginner')
            
                if st.form_submit_button("Next", type = 'primary', use_container_width=True):
                    st.session_state.onboarding_step = 3
                    st.session_state.onboarding_cache['NativeLanguage'] = Nativelang
                    st.session_state.onboarding_cache['LearningLanguage'] = Learninglang
                    st.session_state.onboarding_cache['Difficulty'] = Difficulty
                    st.rerun()

            
        elif step == 3:
            with st.form(key = 'onboarding_form3', border = False):

                st.write("👋 Create Character")
                with st.container(border=False):
                    user_name = 'John Smith'
                    t = st.text_input("Name", placeholder = user_name)
                    if t != '':
                        user_name = t
                    user_gender = st.selectbox("Gender", options=["Not set", "Male", "Female", "Other"])
                    if st.form_submit_button("Next", type = 'primary', use_container_width=True):
                        st.session_state.onboarding_step = 4
                        st.session_state.onboarding_cache['Name'] = user_name
                        st.session_state.onboarding_cache['Gender'] = user_gender
                        st.rerun()
            
        
        elif step == 4:
            with st.form(key = 'onboarding_form4', border = False):
                st.write("Chat with Professor Pacho to get some key words, ask questions or just chat about your game!")
                st.container(border=False, height=100)
                cols = st.columns([1, 1, 1])
                with cols[1]:
                    st.image("app/static/tutorgif.gif", use_container_width=True)
                
                st.container(border = False, height=100)
                
                if st.form_submit_button("Next", type = 'primary', use_container_width=True):
                    st.session_state.onboarding_step = 5
                    st.rerun()
            
        elif step == 5:
            # --- Create World Step ---
            st.write("🌌 Create World")
            st.markdown("<p style='color: grey; margin-top: -10px; font-size: 15px;'>Learn your own way!</p>", unsafe_allow_html=True)

            # Dict of world themes: {key: {img, caption, prompt}}
            world_themes = {
                "Vanilla": {
                    "img": "vanilla.jpeg",
                    "caption": "Classic",
                    "prompt": "Modern city, helpful people and interesting places"
                },
                "Pirate": {
                    "img": "pirate.jpeg",
                    "caption": "Pirate's Life",
                    "prompt": "Set on high seas, searching for treasure and adventure. A land-lubbing, swashbuckling adventure!"
                },
                "Space": {
                    "img": "space.jpeg",
                    "caption": "A Space Odyssey",
                    "prompt": "Set in space, 2130. A world of robots, aliens and spaceships, start next to a crashed ship with 3 crewmates on saturns moon Titan"
                },
                "Medieval": {
                    "img": "medieval.jpeg",
                    "caption": "Medieval style, knights and dragons",
                    "prompt": "Set in a medieval world, with knights, castles and dragons"
                }
            }
            theme_keys = list(world_themes.keys())

            # Session state for world selection
            if "world_theme_idx" not in st.session_state:
                st.session_state.world_theme_idx = 0
            if "world_prompt" not in st.session_state:
                st.session_state.world_prompt = world_themes[theme_keys[0]]["prompt"]

            # Helper to get current theme
            def get_current_theme():
                idx = st.session_state.world_theme_idx
                if 0 <= idx < len(theme_keys):
                    return theme_keys[idx]
                return theme_keys[0]

            # Layout: 3 columns for arrows and image
            img_cols = st.columns([1, 3, 1])
            with img_cols[0]:
                st.container(border=False, height=100)
                if st.button("", icon = ':material/chevron_left:', key="world_left", use_container_width=True, type = 'tertiary'):
                    st.session_state.world_theme_idx = (st.session_state.world_theme_idx - 1) % len(theme_keys)
                    st.session_state.world_prompt = world_themes[get_current_theme()]["prompt"]
            with img_cols[2]:
                st.container(border=False, height=100)
                if st.button("", icon = ':material/chevron_right:', key="world_right", use_container_width=True, type = 'tertiary'):
                    st.session_state.world_theme_idx = (st.session_state.world_theme_idx + 1) % len(theme_keys)
                    st.session_state.world_prompt = world_themes[get_current_theme()]["prompt"]

            # Image and caption
            with img_cols[1]:
                theme = get_current_theme()
                st.image(f"static/placeholders/DefaultThemes/{world_themes[theme]["img"]}", use_container_width=True, caption=world_themes[theme]["caption"])


            # Enter world button
            if st.button("Enter World", type="primary", use_container_width=True, key="world_next"):
                
                BaserowDB("create row", "Users", Data = {
                    "Email": st.user.email,
                    "Name": st.session_state.onboarding_cache['Name'],
                    "Gender": st.session_state.onboarding_cache['Gender'],
                    "NativeLanguage": st.session_state.onboarding_cache['NativeLanguage'],
                    "LearningLanguage": st.session_state.onboarding_cache['LearningLanguage'],
                    "Difficulty": st.session_state.onboarding_cache['Difficulty'],
                    "GameTheme": st.session_state.world_prompt,
                    "Eggs": 100,
                    "EggsReset": 1,
                    "ProfilePicture": 1,
                    "XP": 0,
                    "Money": 2.50,
                    "Volume": 50,
                    "IsSubscribed": False,
                    "Avatar": "🐱"
                })
                #time.sleep(3)
                id = getidbyemail(st.user.email)

                st.session_state.player = {
                    "ID": id,
                    "Name": st.session_state.onboarding_cache['Name'],
                    "Gender": st.session_state.onboarding_cache['Gender'],
                    "Avatar": "🐱",
                    "NativeLanguage": st.session_state.onboarding_cache['NativeLanguage'],
                    "LearningLanguage": st.session_state.onboarding_cache['LearningLanguage'],
                    "Difficulty": st.session_state.onboarding_cache['Difficulty'],
                    "GameTheme": st.session_state.world_prompt,
                    "Eggs": 100,
                    "EggsReset": 1,
                    "ProfilePicture": 1,
                    "XP": 0,
                    "Money": 2.50,
                    "Volume": 50,
                    "IsSubscribed": False

                }

                st.session_state.isLoading = True
                st.rerun()
        

    def RenderOnboarding():
        print('running onboarding')
        with OnboardingEmpty:
            st.empty()
            st.container(border=False, height=300)
            with st.container():
                RenderOnboardingStep()        
     
    
    OnboardingEmpty = st.empty()
    RenderOnboarding()   



@st.dialog(" ")
def OutOfEggs():

    time_difference = TimeUntil(st.session_state.player["EggsReset"])
    hours = time_difference / 3600
    minutes = int((hours-int(hours))*60)

    st.title("Out of Stars!")
    st.write(f"Thanks for trying out PICOPACHO! Your stars reset in {int(hours)}h {minutes}m.")
    st.write("Don't want to wait? Subscribe for unlimited playtime!")
    st.caption("✔ Infinite locations")
    st.caption("✔ Unlimited daily playtime")
    st.caption("✔ Kick the apps and enjoy learning again")
    add_auth(
    required=True,  # Don't stop the app for non-subscribers
    show_redirect_button=True,
    subscription_button_text="Subscribe - £9.99/month",
    button_color="#9D4EDD",
    use_sidebar=False  # Show button in main section
    )
    
    #st.json(st.session_state.subscriptions)
    
    # if st.button("Logout"):
    #     st.logout()
    #     st.rerun()

@st.dialog(" ")
def ReturningUser():
    
    st.container(border=False, height=50)
    logocol = st.columns([1, 2, 1])
    with logocol[1]:
        st.image("static/Logos/Logo_Med.png", use_container_width=True)
    #st.container(border=False, height=1)

    st.markdown(f"<p style='text-align: center; color: grey; margin-top: -1px; font-size: 14px;'>Press spacebar to begin</p>", unsafe_allow_html=True)
    
    st.container(border=False, height=100)
    with st.container(border=False):
        RenderGoogleChipMinimal()
    #st.json(st.session_state.player)


def CheckSub():
    if "subscriptions" not in st.session_state:
        BoolSubscribed = False
    else:
        subscription_data = st.session_state.subscriptions
        
        if not subscription_data["data"]:
            BoolSubscribed = False  # no subscriptions found

        BoolSubscribed = subscription_data["data"][0]["plan"]["active"]
        
        st.session_state.player['IsSubscribed'] = BoolSubscribed
        BaserowDB("update row", "Users", st.session_state.player['ID'], Data = {
            "IsSubscribed": BoolSubscribed
        })
        

    return BoolSubscribed



if st.user.is_logged_in == True or st.session_state.Guest == True:
    
    #first time run through (before game)
    if "player" not in st.session_state:
        #check if player is already in the database

        if st.session_state.Guest:
            st.session_state.player = {
                'ID': 1,
                'Email': 'guest@picopacho.com',
                'Name': 'Guest',
                'Avatar': '🧑',
                'ProfilePicture': 1,
                'Eggs': 100,
                'EggsReset': int((datetime.now(timezone.utc) + timedelta(days=1)).timestamp()),
                'NativeLanguage': "English",
                'Gender': "Not Set",
                'LearningLanguage': "French",
                'IsSubscribed': False,
                'Difficulty': "Beginner",
                'XP': 0,
                'Money': 2.50,
                'Volume': 50,
                'GameTheme': "Set in mordern day France, starting in downtown Paris. Start at a random french shop where all is well, second location - introduce Baal an alien character, move 3 introduce the 'men-in black' to remove Baal, move 4 the aliens invade paris, shooting lazers and abduction people. move 5 onwards let the player lead the way. YOU MUST STICK TO THIS SCRIPT"
            }
            st.rerun()
        
        #init returning var
        returning = False
        #st.json(BaserowDB("list rows", "Users")['results'])

        #make copy of db locally
        getdb = BaserowDB("list rows", "Users")['results']

        for row in getdb:
            id = row['id']
            
            if row['Email'] == st.user.email:
                #user found!
                print('user found in db')
                st.session_state.player = {
                    'ID': int(id),
                    'Email': str(row['Email']),
                    'Name': str(row['Name']),
                    'Avatar': str(row['Avatar']),
                    'ProfilePicture': int(row['ProfilePicture']),
                    'Eggs': int(row['Eggs']),
                    'EggsReset': float(row['EggsReset']),
                    'NativeLanguage': str(row['NativeLanguage']['value']),
                    'Gender': str(row['Gender']['value']),
                    'LearningLanguage': str(row['LearningLanguage']['value']),
                    'IsSubscribed': True if row['IsSubscribed'] == True else False,
                    'Difficulty': str(row['Difficulty']),
                    'XP': int(row['XP']) if 'XP' in row and row['XP'] is not None else 0,
                    'Money': float(row['Money']) if 'Money' in row and row['Money'] is not None else 2.50,
                    'Volume': int(row['Volume']) if 'Volume' in row and row['Volume'] is not None else 50,
                    'GameTheme': str(row['GameTheme']) if 'GameTheme' in row and row['GameTheme'] is not None else ''
                }

                returning = True
                ReturningUser()
                continue

        if returning == False:
            print('creating new user in baserow')
            BaserowDB("create row", "Users", Data = {
                "Email": st.user.email,
                "Name": st.user.name,
                "Avatar": "🧑",
                "ProfilePicture": 1,
                "Eggs": 100,
                "EggsReset": int((datetime.now(timezone.utc) + timedelta(days=1)).timestamp()),
                "NativeLanguage": "English",
                "Gender": "Not Set",
                "LearningLanguage": "German",
                "IsSubscribed": False,
                "Difficulty": "Beginner",
                "XP": 0,
                "Money": 2.50,
                "Volume": 50,
                "GameTheme": ""
            })
            
            print('new user created in baserow')
            
            getdb = BaserowDB("list rows", "Users")['results']
            for row in getdb:
                if row['Email'] == st.user.email:
                    st.session_state.player = {
                    'ID': int(row['id']),
                    'Email': str(row['Email']),
                    'Name': str(row['Name']),
                    'Avatar': str(row['Avatar']),
                    'ProfilePicture': int(row['ProfilePicture']),
                    'Eggs': int(row['Eggs']),
                    'EggsReset': float(row['EggsReset']),
                    'NativeLanguage': str(row['NativeLanguage']['value']),
                    'Gender': str(row['Gender']['value']),
                    'LearningLanguage': str(row['LearningLanguage']['value']),
                    'IsSubscribed': True if row['IsSubscribed'] == True else False,
                    'Difficulty': str(row['Difficulty']),
                    'XP': int(row['XP']) if 'XP' in row and row['XP'] is not None else 0,
                    'Money': float(row['Money']) if 'Money' in row and row['Money'] is not None else 2.50,
                    'Volume': int(row['Volume']) if 'Volume' in row and row['Volume'] is not None else 50,
                    'GameTheme': str(row['GameTheme']) if 'GameTheme' in row and row['GameTheme'] is not None else ''
                    }
                    break
            
            print('onboarding')
            Onboarding(row['id'])

    else:
        CheckSub()
        if st.session_state.player['Eggs'] > 0 or st.session_state.player['IsSubscribed'] == True or st.session_state.Guest == True:
            Main()
        else:
            OutOfEggs()

else:
    st.session_state.isLoading = False
    ### Login and Signup buttons ###
    _, center, __ = st.columns([3, 5, 3])
    with center:
        st.container(border=False, height=30)
        st.image("static/Logos/Logo_Med.png", use_container_width=True)
        _, a, b, _ = st.columns(4)
        with a:
            if st.button("Login", icon=":material/person:", key="LoginBut", use_container_width=True, type="secondary", disabled=st.session_state.isLoading):
                st.login(provider="google")
        with b:
            if st.button("Sign Up", icon=":material/person_add:", key="SignUpBut", use_container_width=True, type="primary", disabled=st.session_state.isLoading):
                st.login(provider="google")
        guestcols = st.columns([1, 2, 1])
        with guestcols[1]:
            if st.button("Continue as Guest", icon=":material/person:", key="GuestBut", use_container_width=True, type="secondary", disabled=st.session_state.isLoading, help = "Try out PICOPACHO with a unique French storyline. In guest mode, play is limited to ~15 moves."):
                st.session_state.Guest = True
                st.session_state.isLoading = True
                st.rerun()

    disc_cols = st.columns([2, 1, 2])
    with disc_cols[1]:
        st.markdown("<p style='text-align: center; color: grey; margin-top: -10px; font-size: 14px;'>By continuing, you agree to our <a href='https://www.picopacho.com/privacy_policy' target='_blank'>Privacy Policy</a> and <a href='https://www.picopacho.com/terms_of_service' target='_blank'>Terms of Service</a>.</p>", unsafe_allow_html=True)

if "SupportedLanguages" not in st.session_state:
    st.session_state.SupportedLanguages = ["English", "French", "German", "Italian", "Russian", "Thai"]

if 'DifficultyOptions' not in st.session_state:
    st.session_state.DifficultyOptions = ["Completely New", "I know some basics", "Beginner", "Conversational", "Intermediate", "Advanced", "Fluent"]
