import streamlit as st
import streamlit.components.v1 as components
import streamlit as st
from pygame import mixer
import os
import random

if "SoundEngine" not in st.session_state:
    mixer.pre_init()
    mixer.init()
    mixer.set_num_channels(32)
if "volume" not in st.session_state:
    st.session_state.volume = 50
    
def SoundEngine(sound):
    channel = mixer.find_channel()
    if channel:
        channel.set_volume(st.session_state.volume/100)
        PlaySound = mixer.Sound(f"static/sounds/{sound}")
        PlaySoundLength = PlaySound.get_length()*1000
        channel.play(PlaySound)
        channel.fadeout(int(PlaySoundLength))
        
        if PlaySoundLength >= 2000:
            channel.fadeout(int(PlaySoundLength)-2000)



col1, col2, col3 = st.columns(3)

with col1:
    if st.button("playsoundtest"):
        SoundEngine('click.mp3')
    if st.button("playsoundtest2"):
        SoundEngine('click2.mp3')
    if st.button("playsoundtest3"):
        SoundEngine('follow.mp3')
    if st.button("playsoundtest4"):
        SoundEngine('click.mp3')

with col2:
    if st.button("playsoundtest5"):
        SoundEngine('everytime.mp3')
    if st.button("playsoundtest6"):
        SoundEngine('everytime2.mp3')
    if st.button("playsoundtest7"):
        SoundEngine('arriving.mp3')
    if st.button("playsoundtest8"):
        SoundEngine('sendmessage.mp3')

with col3:
    if st.button("playsoundtest9"):
        SoundEngine('UmmNo.mp3')
    if st.button("playsoundtest10"):
        SoundEngine('levelup.mp3')
    if st.button("playsoundtest11"):
        SoundEngine('lostheart.mp3')
    if st.button("playsoundtest12"):
        SoundEngine('/music/music1.mp3')

volume = st.slider("volume", 0, 100, (st.session_state.volume), step=1)
if volume:
    st.session_state.volume = volume
if st.button("stop"):
    mixer.stop()
if st.button("rerun"):
    st.rerun()