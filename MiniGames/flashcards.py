import streamlit as st
import random

randomcolours = ["#ffffaf", "#ffafaf", "#afafff", "#ffffaf", "#ffafaf", "#afafff"]

st.session_state.Flashcards = [["Your singing is beautiful!","Dein Gesang ist wunderschön!", 0, randomcolours[0]], ["You did a great job!","Du hast einen tollen Job gemacht!", 0, randomcolours[1]], ["I love your style!","Ich liebe deinen Stil!", 0, randomcolours[2]], ["You're very talented!","Du bist sehr talentiert!", 0, randomcolours[3]]]
st.session_state.Flashcards_index = 0
fontsize = 14

@st.dialog(title=" ")
def flashcards():
    st.title("Flashcards")
    with st.container(border=False, height=250):
        e = st.empty()
        
        e.markdown(f"<p style='text-align: center; color: black; font-size: {fontsize}px; background-color: {st.session_state.Flashcards[st.session_state.Flashcards_index][3]}; border-radius: 5px; height: 225px; padding-top: 60px; margin: 0;'>{st.session_state.Flashcards[st.session_state.Flashcards_index][0]}</p>", unsafe_allow_html=True)

    if st.button("Next"):
        st.session_state.Flashcards_index += 1
        st.session_state.Flashcards_index = st.session_state.Flashcards_index % len(st.session_state.Flashcards)
        e.markdown(f"<p style='text-align: center; color: grey; font-size: {fontsize}px; background-color: {st.session_state.Flashcards[st.session_state.Flashcards_index][3]}; border-radius: 5px; height: 225px; padding-top: 60px; margin: 0;'>{st.session_state.Flashcards[st.session_state.Flashcards_index][0]}</p>", unsafe_allow_html=True)
    if st.button("Back"):
        st.session_state.Flashcards_index -= 1
        st.session_state.Flashcards_index = st.session_state.Flashcards_index % len(st.session_state.Flashcards)
        e.markdown(f"<p style='text-align: center; color: grey; font-size: {fontsize}px; background-color: {st.session_state.Flashcards[st.session_state.Flashcards_index][3]}; border-radius: 5px; height: 225px; padding-top: 60px; margin: 0;'>{st.session_state.Flashcards[st.session_state.Flashcards_index][0]}</p>", unsafe_allow_html=True)
    if st.button("Flip"):
        if st.session_state.Flashcards[st.session_state.Flashcards_index][2] == 0:
            st.session_state.Flashcards[st.session_state.Flashcards_index][2] = 1
            e.markdown(f"<p style='text-align: center; color: grey; font-size: {fontsize}px; background-color: {st.session_state.Flashcards[st.session_state.Flashcards_index][3]}; border-radius: 5px; height: 225px; padding-top: 60px; margin: 0;'>{st.session_state.Flashcards[st.session_state.Flashcards_index][1]}</p>", unsafe_allow_html=True)
        else:
            st.session_state.Flashcards[st.session_state.Flashcards_index][2] = 0
            e.markdown(f"<p style='text-align: center; color: grey; font-size: {fontsize}px; background-color: {st.session_state.Flashcards[st.session_state.Flashcards_index][3]}; border-radius: 5px; height: 225px; padding-top: 60px; margin: 0;'>{st.session_state.Flashcards[st.session_state.Flashcards_index][0]}</p>", unsafe_allow_html=True)

        
                        
# run it like this
# keep, got it buttons
# cycles until all keeps until empty, shows reset button
# functions as a saved list of flashcards you can run through over and over until you got all of them


# Add a button to open the dialog
if st.button("Open Flashcards"):
    flashcards()
