import streamlit as st
import plotly.graph_objects as go
import math
import random
import time

st.set_page_config(page_title="Lockpicking Simulator", layout="wide")
from  streamlit_vertical_slider import vertical_slider 

st.session_state.lastwatched = 0
@st.dialog(title="Lockpicking Simulator")
def lockpicking_simulator():
    st.session_state.watched = random.randint(0,1)
    _, c, _ = st.columns([1,1,1])
    with c:
        with st.empty():
            if st.session_state.watched == 1:
                st.button('', icon = ':material/visibility:', type = 'tertiary', use_container_width = True)
            else:
                st.button('', icon = ':material/unknown_med:', type = 'tertiary', use_container_width = True)
                           
    
    targetpins = [3,3,3]

    keybut, pin1, pin2, pin3 = st.columns(4)
    with pin1:
        a = vertical_slider(
            label = " ",  #Optional
            key = "vert_01" ,
        height = 200, #Optional - Defaults to 300
        thumb_shape = "pill", #Optional - Defaults to "circle"
        step = 1, #Optional - Defaults to 1
        default_value=5 ,#Optional - Defaults to 0
        min_value= 1, # Defaults to 0
        max_value= 5, # Defaults to 10
        
        slider_color = ('darkgrey','darkgrey'), #Optional
        thumb_color= "slategrey", #Optional - Defaults to Streamlit Red
        value_always_visible = True ,#Optional - Defaults to False
        )
        
    with pin2:
        b = vertical_slider(
            label = " ",  #Optional
            key = "vert_02" ,
        height = 200, #Optional - Defaults to 300
        thumb_shape = "pill", #Optional - Defaults to "circle"
        step = 1, #Optional - Defaults to 1
        default_value=5 ,#Optional - Defaults to 0
        min_value= 1, # Defaults to 0
        max_value= 5, # Defaults to 10
        
        slider_color = ('darkgrey','darkgrey'), #Optional
        thumb_color= "slategrey", #Optional - Defaults to Streamlit Red
        value_always_visible = True ,#Optional - Defaults to False
        )
        
        
    with pin3:
        c = vertical_slider(
            label = " ",  #Optional
            key = "vert_03" ,
        height = 200, #Optional - Defaults to 300
        thumb_shape = "pill", #Optional - Defaults to "circle"
        step = 1, #Optional - Defaults to 1
        default_value=5 ,#Optional - Defaults to 0
        min_value= 1, # Defaults to 0
        max_value= 5, # Defaults to 10
        
        slider_color = ('darkgrey','darkgrey'), #Optional
        thumb_color= "slategrey", #Optional - Defaults to Streamlit Red
        value_always_visible = True ,#Optional - Defaults to False
        )
    with keybut:
        st.container(border = False, height = 75)
        lastprog = 0
        if st.button(':material/key:', use_container_width = True, type = 'primary'):
            lastprog = (1 - (abs(targetpins[0]-a) + abs(targetpins[1]-b) + abs(targetpins[2]-c)) / 15) 
            if st.session_state.lastwatched == 1:
                st.session_state.caught = True
                st.rerun()
    

    st.progress(lastprog)
    if lastprog == 1:
        st.success('Success!')
        time.sleep(1.5)
        st.session_state.caught = False
        st.session_state.lockpickSuccess = True
        st.rerun()

    st.session_state.lastwatched = st.session_state.watched

if st.button("Simulate"):
    lockpicking_simulator()