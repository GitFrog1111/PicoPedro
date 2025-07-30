import streamlit as st
import random
from typing import List, Dict, Optional
import time
import uuid

st.set_page_config(layout="wide")

st.title("Rogues Gambit")

DeckOfCards = ['2 ♠', '2 ♥', '2 ♦', '2 ♣', '3 ♠', '3 ♥', '3 ♦', '3 ♣', '4 ♠', '4 ♥', '4 ♦', '4 ♣', '5 ♠', '5 ♥', '5 ♦', '5 ♣', '6 ♠', '6 ♥', '6 ♦', '6 ♣', '7 ♠', '7 ♥', '7 ♦', '7 ♣', '8 ♠', '8 ♥', '8 ♦', '8 ♣', '9 ♠', '9 ♥', '9 ♦', '9 ♣', '10 ♠', '10 ♥', '10 ♦', '10 ♣', 'J ♠', 'J ♥', 'J ♦', 'J ♣', 'Q ♠', 'Q ♥', 'Q ♦', 'Q ♣', 'K ♠', 'K ♥', 'K ♦', 'K ♣', 'A ♠', 'A ♥', 'A ♦', 'A ♣', '🏵', '🏵']

@st.dialog(title="Rogues Gambit")
def RoguesGambit(players):
    #Helper funcs
    def GetDecorator(card):
        d = ""
        if "2" in card:
            d = ".."
        elif "3" in card:
            d = "..."
        elif "4" in card:
            d = "::"
        elif "5" in card:
            d = ":.:"
        elif "6" in card:
            d = ":..:"
        elif "7" in card:
            d = ":...:"
        elif "8" in card:
            d = "::::"
        elif "9" in card:
            d = "::.::"
        elif "10" in card:
            d = ":::::"
        elif "J" in card:
            d = "🐾"
        elif "Q" in card:
            d = "🌺"
        elif "K" in card:
            d = "💠"
        elif "A" in card:
            d = "🔰"
        #joker - can be any value
        if "🏵" in card:
            d = "🏵"
        return d

    def sorthand(hand):
        handindexes = []
        for i in range(len(hand)):
            handindexes.append(DeckOfCards.index(hand[i]))
        handindexes.sort()
        hand.clear()
        for j in range(len(handindexes)):
            hand.append(DeckOfCards[handindexes[j]])
        return hand

    #Main game
    def RenderTable():
        if 'TableEmpty' not in st.session_state.RG:
            TableEmpty = st.empty()
            st.session_state.RG['TableEmpty'] = TableEmpty
        
        with st.session_state.RG['TableEmpty']:
            with st.container():
                LTable, MTable, RTable = st.columns([1, 5, 1])
                with LTable:
                    st.container(border = False, height=150)
                    st.image(players[0]['Image'], caption = players[0]['Name'])
                    TurnMarkerA = st.empty()
                with MTable:
                    _, mid, _ = st.columns([2, 1, 2])
                    with mid:
                        st.image(players[1]['Image'], caption = players[1]['Name'])
                        TurnMarkerB = st.empty()

                    Table = st.container(border = True)
                    with Table:
                        _, mid, _ = st.columns([2, 2, 2])
                        with mid:
                            st.container(border = False, height=10) #v padding
                            
                            CurrentCard = st.empty()
                            CurrentCard.metric(label = '', value = f"{st.session_state.RG['currentCard']}", border = True)
                            st.caption(f"Pot: {st.session_state.RG['pot']}")

                    _, mid, _ = st.columns([2, 2, 2])
                    
                    with mid:
                        st.button("Liar!", type = "primary", key = f'Liar_{uuid.uuid4()}', use_container_width=True)
                with RTable:
                    st.container(border = False, height=150)
                    st.image(players[2]['Image'], caption = players[2]['Name'])
                    TurnMarkerc = st.empty()

        
    
    def DealCards():
        print("dealing cards")
        NumberOfStartingCards = 5
        #create copy of deck
        TheDeck = DeckOfCards.copy()
        #shuffle deck
        random.shuffle(TheDeck)
        #deal cards to players
        for player in players:
            if player not in st.session_state.RG['players']:
                st.session_state.RG['players'].append(player)
            for i in range(NumberOfStartingCards):
                player['hand'].append(TheDeck.pop())

        #deal cards to human
        for i in range(NumberOfStartingCards):
            st.session_state.RG['hand'].append(TheDeck.pop())
        st.session_state.RG['hand'] = sorthand(st.session_state.RG['hand'])
        print("dealt cards")
        print("players: ", st.session_state.RG['players'])
        print("hand: ", st.session_state.RG['hand'])

    def RenderPlayer():
        print("rendering player")
        Pad, H, Pad = st.columns([1, 10, 1])
        with H:
            handcols = st.columns(5)
            for i in range(5):
                with handcols[i]:
                    print("printing hand: ", st.session_state.RG['hand'][i])
                    st.button(f"{st.session_state.RG['hand'][i]}\n\n {GetDecorator(st.session_state.RG['hand'][i])}", key = f"hand{i}_{uuid.uuid4()}", type = "secondary", use_container_width=True)

    
    def AiPlayerTurns():
        print("ai player turns")
        for player in st.session_state.RG['players']:
            with st.spinner(f"{player['Name']} is thinking..."):
                print(f"{player['Name']} is thinking...")
                time.sleep(1)

            player['hand'].remove(random.choice(player['hand']))
            st.session_state.RG['currentCard'] +=1
            RenderTable()
            
            

                
            
    def Play():
        #st.session_state.RG['gameState'] = "Playing"
        print("rendering table")
        RenderTable()
        print("rendered table")
        RenderPlayer()
        AiPlayerTurns()
        #HumanPlayerTurn()
        #CheckForEnd()
        #Play()

        
    def StartGame(players):
        #create new game state
        st.session_state.RG = {
            'gameState': "Start",
            'players': players,
            'table': [],
            'hand': [],
            'pot': 0,
            'currentCard': 2
        }
        DealCards()
        
        

    #if first run    
    if 'RG' not in st.session_state:
        print("--------------------------------first run--------------------------------")
        StartGame(testplayers)
    if st.session_state.RG['gameState'] == "Start":
        Play()



testplayers = [
    {
        "Name": 'Dog',
        "Image": 'Dog.png',
        "hand": []
    },
    {
        "Name": 'Melvin',
        "Image": 'Melvin.png',
        "hand": []
    },
    {
        "Name": 'Mia',
        "Image": 'Mia.png',
        "hand": []
    }
]
if st.button("Start Game",use_container_width=True):
    RoguesGambit(testplayers)

