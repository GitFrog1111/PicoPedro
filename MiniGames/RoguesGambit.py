import streamlit as st
import random
from typing import List, Dict, Optional
import time

st.set_page_config(layout="wide")

st.title("Rogues Gambit")
st.session_state.currentCard = 5
DeckOfCards = ['2 ♠', '2 ♥', '2 ♦', '2 ♣', '3 ♠', '3 ♥', '3 ♦', '3 ♣', '4 ♠', '4 ♥', '4 ♦', '4 ♣', '5 ♠', '5 ♥', '5 ♦', '5 ♣', '6 ♠', '6 ♥', '6 ♦', '6 ♣', '7 ♠', '7 ♥', '7 ♦', '7 ♣', '8 ♠', '8 ♥', '8 ♦', '8 ♣', '9 ♠', '9 ♥', '9 ♦', '9 ♣', '10 ♠', '10 ♥', '10 ♦', '10 ♣', 'J ♠', 'J ♥', 'J ♦', 'J ♣', 'Q ♠', 'Q ♥', 'Q ♦', 'Q ♣', 'K ♠', 'K ♥', 'K ♦', 'K ♣', 'A ♠', 'A ♥', 'A ♦', 'A ♣', '🏵', '🏵']

@st.dialog(title="Rogues Gambit")
def RoguesGambit():
    LTable, MTable, RTable = st.columns([1, 5, 1])
    with LTable:
        st.container(border = False, height=150)
        st.image("Dog.png", caption = "Dog")
    with MTable:
        _, mid, _ = st.columns([2, 1, 2])
        with mid:
            st.image("Melvin.png", caption = "Melvin")

        Table = st.container(border = True)
        with Table:
            _, mid, _ = st.columns([2, 2, 2])
            with mid:
                st.container(border = False, height=10) #v padding
                
                CurrentCard = st.empty()
                CurrentCard.metric(label = '', value = f"{st.session_state.currentCard}", border = True)
                st.caption("Pot: 0")

        _, mid, _ = st.columns([2, 2, 2])
        
        with mid:
            st.button("Liar!", type = "primary", use_container_width=True)
    with RTable:
        st.button(" ", key = 'Info', icon = ":material/help:", type = "tertiary", use_container_width=True, help = """Objective
Outwit and outbluff your opponents by playing your cards in an ascending order—real or fake. Build the pot, survive accusations, and walk away with the gold.

Setup
Deck: Standard 52-card deck.

Hands: Each player is dealt 10 cards.

Pot: Each player antes (e.g. 5–10 gold) into the pot to begin the round.

Starting Card: Always begins with 5 as the “first claimed rank.”

Turn Rules
Player Action:

On your turn, play 1 card face-down and declare it as the next value up in the sequence.

Example: Starting with 5, next player declares “6,” then “7,” etc.

You may lie.

Rank Progression:

Claimed values go up: 5 → 6 → 7 → … → Ace → back to 2.

Wraps after Ace (A → 2 → 3 → ... 5, etc.)

Calling “Liar”:

Any player may call “Liar!” immediately after a card is played.

If the card matches the declared rank: The caller was wrong.
→ The pot is split among all other players.

If the card does not match the declared rank: The liar is caught.
→ The caller takes the entire pot.

Round resets after a Liar call (everyone re-antes).

End-of-Round Reset:

If the claimed rank reaches Ace and no Liar was called, the pot is split evenly among all players.

If any player runs out of cards, round ends.
→ Pot is split evenly among remaining players.

New round begins with another ante and reset starting claim (5).""")
        st.container(border = False, height=150-50)
        st.image("Mia.png", caption = "Mia")

    
    NumberOfStartingCards = 10
    
    st.session_state.hand = [random.choice(DeckOfCards) for _ in range(NumberOfStartingCards)]
    st.session_state.hand = sorthand(st.session_state.hand)
    
    Pad, H, Pad = st.columns([1, 10, 1])
    with H:
        Hand = st.empty()
        with Hand:
            handcols = st.columns(5)
        for i in range(5):
            with handcols[i]:
                st.button(f"{st.session_state.hand[i]}\n\n {GetDecorator(st.session_state.hand[i])}", key = f"hand{i}", type = "secondary", use_container_width=True)
                st.button(f"{st.session_state.hand[i+5]}\n\n {GetDecorator(st.session_state.hand[i+5])}", key = f"hand{i+5}", type = "secondary", use_container_width=True)
                i+=1
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

if st.button("Open Dialog"):
    RoguesGambit()


t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _= st.columns(19)
with t:
    st.button('🏵\n\n🏵', type = "secondary")
