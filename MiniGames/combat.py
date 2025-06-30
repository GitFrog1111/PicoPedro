import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import random
import base64
import time

if 'Combat' not in st.session_state:
    st.session_state.Combat = {
        'Selection': None,
        'Turn': 'Player',

        'Enemy': {
        'Face': {'Image': 'Dog.png', 'Name': 'god', 'Heal': 50, 'Damage': 1},
        'FieldItems': [],
        'Inventory': [
            {'Image': 'Dog.png', 'Name': 'fencer', 'Heal': 3, 'Damage': 4},
            {'Image': 'Dog.png', 'Name': 'shield', 'Heal': 10, 'Damage': 1},
            {'Image': 'Dog.png', 'Name': 'Dog', 'Heal': 3, 'Damage': 1},
            {'Image': 'Dog.png', 'Name': 'Longsword', 'Heal': 1, 'Damage': 2},
            {'Image': 'Dog.png', 'Name': 'Shortsword', 'Heal': 5, 'Damage': 6},
            {'Image': 'Dog.png', 'Name': 'Longbow', 'Heal': 1, 'Damage': 9}
        ]
        },
        
        'Player': {
            'Face': {'Image': 'Dog.png', 'Name': 'lel', 'Heal': 50, 'Damage': 1},
            'FieldItems': [],
            'Inventory': [
                {'Image': 'Dog.png', 'Name': 'house', 'Heal': 8, 'Damage': 1},
                {'Image': 'Dog.png', 'Name': 'gold', 'Heal': 6, 'Damage': 1},
                {'Image': 'Dog.png', 'Name': 'crossbow', 'Heal': 5, 'Damage': 8},
                {'Image': 'Dog.png', 'Name': 'Lol', 'Heal': 2, 'Damage': 10},
                {'Image': 'Dog.png', 'Name': 'circus', 'Heal': 3, 'Damage': 4},
                {'Image': 'Dog.png', 'Name': 'totem', 'Heal': 3, 'Damage': 4},
                {'Image': 'Dog.png', 'Name': 'troll', 'Heal': 3, 'Damage': 8},
                
            ]
        }
        
    }

numbermap = {
    1: "❶",
    2: "❷",
    3: "❸",
    4: "❹",
    5: "❺",
    6: "❻",
    7: "❼",
    8: "❽",
    9: "❾",
    10: "❿"
}

@st.dialog("Combat")
def Combat():
    
    def AITakeTurn():
        if st.session_state.Combat['Turn'] == 'Enemy':

            #get data
            largestenemydamage = 0
            largestenemydamage_index = 0
            print("Len: ", len(st.session_state.Combat['Enemy']['FieldItems']))
            for i in range(len(st.session_state.Combat['Enemy']['FieldItems'])):
                if st.session_state.Combat['Enemy']['FieldItems'][i]['Damage'] > largestenemydamage:
                    largestenemydamage = st.session_state.Combat['Enemy']['FieldItems'][i]['Damage']
                    largestenemydamage_index = i

            lowestplayerheal = 9999
            lowestplayerheal_index = 0
            for i in range(len(st.session_state.Combat['Player']['FieldItems'])):
                if st.session_state.Combat['Player']['FieldItems'][i]['Heal'] < lowestplayerheal:
                    lowestplayerheal = st.session_state.Combat['Player']['FieldItems'][i]['Heal']
                    lowestplayerheal_index = i
            
            largestenemyheal = 0
            largestenemyheal_index = 0
            for i in range(len(st.session_state.Combat['Enemy']['FieldItems'])):
                if st.session_state.Combat['Enemy']['FieldItems'][i]['Heal'] > largestenemyheal:
                    largestenemyheal = st.session_state.Combat['Enemy']['FieldItems'][i]['Heal']
                    largestenemyheal_index = i
                    
            largestplayerdamage = 0
            largestplayerdamage_index = 0
            for i in range(len(st.session_state.Combat['Player']['FieldItems'])):
                if st.session_state.Combat['Player']['FieldItems'][i]['Damage'] > largestplayerdamage:
                    largestplayerdamage = st.session_state.Combat['Player']['FieldItems'][i]['Damage']
                    largestplayerdamage_index = i
            
            #number of enemy items
            numberofenemyitems = len(st.session_state.Combat['Enemy']['FieldItems'])
            #number of player items
            numberofplayeritems = len(st.session_state.Combat['Player']['FieldItems'])



            #If nothing on field - place
            if len(st.session_state.Combat['Enemy']['FieldItems']) == 0:
                print('no items on field, placing item')
                #pick random item from inventory
                random_item = random.randint(0, len(st.session_state.Combat['Enemy']['Inventory']))
                Action('EnemyInventory', ['Enemy', random_item])

                return
            
            #Elif any of their items damage > your health - kill you
            if largestenemydamage > st.session_state.Combat['Player']['Face']['Heal']:
                print('enemy item damage > player health, attacking face')
                Action('EnemyAttackFace', ['Enemy', largestenemydamage_index])
                
                return

            #Elif ai can be killed next round - heal with highest health item
            if st.session_state.Combat['Enemy']['Face']['Heal'] < largestplayerdamage:
                print('enemy face heal < player damage, healing')
                Action('EnemyHeal', ['Enemy', largestenemyheal_index])
                
                return
        

            if numberofenemyitems > 3:
                print('enemy has more than 3 items, attacking player with highest damage item')
                Action('EnemyAttack', ['Enemy', largestplayerdamage_index], ['Enemy', largestenemydamage_index])
                
                return
            else:
                #pick random between 
                # ⁃ attack player with highest damage item
                # ⁃ Place item
                AttackOrPlace = random.randint(0, 2)
                if AttackOrPlace == 0:
                    print('enemy attacking player with highest damage item')
                    Action('EnemyAttack', ['Enemy', largestplayerdamage_index], ['Enemy', largestenemydamage_index])
                    return
                elif AttackOrPlace == 1:
                    print('enemy placing item')
                    random_item = random.randint(0, len(st.session_state.Combat['Enemy']['Inventory']) - 1)
                    Action('EnemyInventory', ['Enemy', random_item])
                    return
                elif AttackOrPlace == 2:
                    print('attacking player face')
                    Action('EnemyAttackFace', ['Enemy', largestenemydamage_index])
                    return




    def DestroyCards():
        EnemyCards = st.session_state.Combat['Enemy']['FieldItems']
        PlayerCards = st.session_state.Combat['Player']['FieldItems']
        for i in EnemyCards:
            if i['Heal'] <= 0:
                EnemyCards.remove(i)

        for i in PlayerCards:
            if i['Heal'] <= 0:
                PlayerCards.remove(i)
                

    def Action(action = None, selected1 = None, selected2 = None):
        
        if action == 'Attack':
            st.session_state.Combat['Enemy']['FieldItems'][selected2[1]]['Heal'] -= st.session_state.Combat['Player']['FieldItems'][selected1[1]]['Damage']
            file_ = open("static/Attack.gif", "rb")
            contents = file_.read()
            data_url = base64.b64encode(contents).decode("utf-8")
            file_.close()
            st.markdown(f'<img src="data:image/gif;base64,{data_url}" width="100">', unsafe_allow_html=True)
            
        
        if action == 'AttackFace':
            st.session_state.Combat['Enemy']['Face']['Heal'] -= st.session_state.Combat['Player']['FieldItems'][selected1[1]]['Damage']
            
        if action == 'PlayerInventory':
            st.session_state.Combat['Player']['FieldItems'].append(st.session_state.Combat['Player']['Inventory'][selected1[1]])
            st.session_state.Combat['Player']['Inventory'].remove(st.session_state.Combat['Player']['Inventory'][selected1[1]]) 
            
        
        if action == 'EnemyInventory':
            st.session_state.Combat['Enemy']['FieldItems'].append(st.session_state.Combat['Enemy']['Inventory'][selected1[1]])
            #st.session_state.Combat['Enemy']['Inventory'].remove(st.session_state.Combat['Enemy']['Inventory'][selected1[1]]) 
            

        if action == 'EnemyHeal':
            st.session_state.Combat['Enemy']['Face']['Heal'] += st.session_state.Combat['Enemy']['FieldItems'][selected1[1]]['Heal']
            st.session_state.Combat['Enemy']['FieldItems'].remove(st.session_state.Combat['Enemy']['FieldItems'][selected1[1]])
            

        if action == 'EnemyAttack':
            st.session_state.Combat['Player']['FieldItems'][selected1[1]]['Heal'] -= st.session_state.Combat['Enemy']['FieldItems'][selected2[1]]['Damage']
            
            
        if action == 'EnemyAttackFace':
            st.session_state.Combat['Player']['Face']['Heal'] -= st.session_state.Combat['Enemy']['FieldItems'][selected1[1]]['Damage']
            


        st.session_state.Combat['Selection'] = None

        if st.session_state.Combat['Turn'] == 'Player':
            st.session_state.Combat['Turn'] = 'Enemy'
        else:
            st.session_state.Combat['Turn'] = 'Player'
        

    def HandleSelections(type, selected):
        LastSelected = st.session_state.Combat['Selection']
        
        if type == 'PlayerInventory':
            Action('PlayerInventory', [type, selected])
            st.session_state.Combat['Selection'] = None

        #if nothing selected they must choose a player card
        if LastSelected == None and type == 'Player':
            st.session_state.Combat['Selection'] = [type, selected]

        #if a player card is selected they can choose a different player card
        if LastSelected != None and type == 'Player':
            st.session_state.Combat['Selection'] = [type, selected]
        
        #if card is selected (forced to be a player card)and they choose an enemy card, attack
        elif LastSelected != None and type == 'Enemy':
            Action('Attack', LastSelected, [type, selected])
        
        #if card is selected (forced to be a player card) and they choose enemy face, attack face
        elif LastSelected != None and type == 'EnemyFace':
            Action('AttackFace', LastSelected, [type, selected])


    def RenderCard(type, index):
        if type == 'EnemyFace':
            image = st.session_state.Combat['Enemy']['Face']['Image']
        elif type == 'Enemy' or type == 'Player':
            image = st.session_state.Combat[type]['FieldItems'][index]['Image']
        elif type == 'PlayerInventory':
            image = st.session_state.Combat['Player']['Inventory'][index]['Image']

        card_css_styles = f"""
                        button {{
                            background-image: url('http://localhost:8501/app/static/placeholders/{image}');
                            background-size: cover;
                            background-position: center;
                            color: transparent; /* To hide any button text, as label is empty */
                            border-radius: 8px;
                            width: 50px;
                            height: 65px;
                            margin-left: auto; /* Horizontally center the button in its column cell */
                            margin-right: auto;
                            display: block; /* Necessary for margin: auto to work for block elements */
                        }}
                    """
        with stylable_container(key=f'{type}_{index}', css_styles=card_css_styles):
            st.button(
                label="", # Empty label as per example
                on_click=HandleSelections,
                args=(type, index),
                key=f'{type}_{index}'
            )

        if type == 'Enemy' or type == 'Player':
            st.markdown(f"<p style='text-align: center; color: #09C478; margin-top: -82px; margin-left: -50px; font-size: 20px;'>{st.session_state.Combat[type]['FieldItems'][index]['Heal']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; color: #DF22D3; margin-top: -98px; margin-right: -50px; font-size: 20px;'>{st.session_state.Combat[type]['FieldItems'][index]['Damage']}</p>", unsafe_allow_html=True)
        
        if type == 'EnemyFace':
            st.markdown(f"<p style='text-align: center; color: #09C478; margin-top: 0px; font-size: 30px;'>{st.session_state.Combat['Enemy']['Face']['Heal']}</p>", unsafe_allow_html=True)
            
        if type == 'PlayerInventory':
            st.markdown(f"<p style='text-align: center; color: #09C478; margin-top: -82px; margin-left: -50px; font-size: 20px;'>{st.session_state.Combat['Player']['Inventory'][index]['Heal']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; color: #DF22D3; margin-top: -98px; margin-right: -50px; font-size: 20px;'>{st.session_state.Combat['Player']['Inventory'][index]['Damage']}</p>", unsafe_allow_html=True)
        
    def RenderBoard():
        
        with st.container(border=False):
            #render enemy face
            PicCols = st.columns([1, 0.8, 1])
            with PicCols[1]:
                RenderCard('EnemyFace', 0)
            #st.container(border=False, height = 5)
            
            ## Playing board
            #render enemy field items
            with st.container(border=True):
                _, center, _ = st.columns([1, 4, 1])
                with center:
                    if len(st.session_state.Combat['Enemy']['FieldItems']) > 0:
                        EnemyFieldColumns = st.columns(len(st.session_state.Combat['Enemy']['FieldItems']))
                    else:
                        EnemyFieldColumns = st.columns(1)
                
                if len(st.session_state.Combat['Enemy']['FieldItems']) > 0:
                    for i in range(len(st.session_state.Combat['Enemy']['FieldItems'])):
                        with EnemyFieldColumns[i]:
                            RenderCard('Enemy', i)
                
                                        
                #no mans land
                st.container(border=False, height = 15)
                
                #render player field items
                if len(st.session_state.Combat['Player']['FieldItems']) > 0:
                    _, center, _ = st.columns([1, min(len(st.session_state.Combat['Player']['FieldItems']), 4), 1])
                    with center:
                        PlayerFieldColumns = st.columns(len(st.session_state.Combat['Player']['FieldItems']))
                    for i in range(len(PlayerFieldColumns)):
                        with PlayerFieldColumns[i]:
                            RenderCard('Player', i)

            ## end of playing board
            #render inventory
            with st.container(border=False):
                if len(st.session_state.Combat['Player']['Inventory']) > 0:
                    _, center, _ = st.columns([1, min(len(st.session_state.Combat['Player']['Inventory']), 4), 1])
                    with center:
                        InventoryColumns = st.columns(len(st.session_state.Combat['Player']['Inventory']))
                    for i in range(len(InventoryColumns)):
                        with InventoryColumns[i]:
                            RenderCard('PlayerInventory', i)

            st.container(border=False, height = 15)
            st.markdown(f'<p style="text-align: center;">{st.session_state.Combat["Player"]["Face"]["Heal"]}</p>', unsafe_allow_html=True)
            
        #render player deck
        # with st.container(border=True):
        #     _, center, _ = st.columns([1, 4, 1])
        #     with center:
        #         PlayerDeckColumns = st.columns(len(st.session_state.Combat['Player']['Deck']))
        #     for i in range(len(PlayerDeckColumns)):
        #         with PlayerDeckColumns[i]:
        #             RenderCard(st.session_state.inventory[i])

    Board = st.empty()
    
    with Board:
        DestroyCards()
        AITakeTurn()
        DestroyCards()
        RenderBoard()
        
        

st.session_state.inCombat = False
if st.button("Combat"):
    st.session_state.inCombat = True
    Combat()

if st.button("rerun"):
    st.rerun()

