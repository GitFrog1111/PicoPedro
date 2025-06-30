import streamlit as st
import random
from typing import List, Dict, Optional
import time

st.set_page_config(layout="wide")

st.title("Horsing Around")

@st.dialog(title = "Horseys")
def GameDialog():
    runners = ['🏇', '🏃', '🏃‍♂️']
    
    st.session_state.running = False
    if st.button('Race'):
        st.session_state.running = True
        st.session_state.horse1prog = 0
        st.session_state.winner = None
    
    
    e = st.empty()
    while st.session_state.running:    
        
        t = e.container(border = True)
        with t:              
            cols = e.columns(20)        
            if st.session_state.horse1prog >= 18:
                st.session_state.winner = 'Horse 1'
                st.session_state.running = False
                st.success(f'{st.session_state.winner} wins!')
            else:
                st.session_state.horse1prog += random.randint(1, 2)            
                cols[st.session_state.horse1prog].button(' ', icon = '🏇', key = f"H{st.session_state.horse1prog}", type = 'secondary')

            time.sleep(0.5)
    
st.session_state.horse1prog = 0
st.session_state.winner = None





if st.button("Open Dialog"):
    GameDialog()



