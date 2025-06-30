import streamlit as st

@st.dialog(title=" ")
def access_panel():
    # Initialize session state for tracking unscrewed buttons if not exists
    if 'unscrew_count' not in st.session_state:
        st.session_state.unscrew_count = {1: 0, 2: 0, 3: 0, 4: 0}

    st.container(border = False, height=10)
    # Create a container with fixed height
    with st.container(border = True):
        
        # Create 4 columns for the buttons
        TLeft, mid, TRight = st.columns([1, 5, 1])
        with st.container(border = False, height=200):
            st.container(border = False, height=45)
            st.markdown("<b><h5 style='text-align: center; color: lightgrey;'>GreyLockIndustries</h5></b>", unsafe_allow_html=True)
        BLeft, mid, BRight = st.columns([1, 5, 1])
        
        # Place buttons in each corner
        with TLeft:
            count = st.session_state.unscrew_count[1]
            if count < 5:
                icon = ':material/add_circle:' if count % 2 == 0 else ':material/cancel:'
                if st.button("", icon=icon, use_container_width=True, key=1, type='tertiary'):
                    st.session_state.unscrew_count[1] += 1
                    
            else:
                st.button("", icon=':material/fiber_manual_record:', use_container_width=True, key=1, type='tertiary', disabled=True)

        with TRight:
            count = st.session_state.unscrew_count[2]
            if count < 5:
                icon = ':material/add_circle:' if count % 2 == 0 else ':material/cancel:'
                if st.button("", icon=icon, use_container_width=True, key=2, type='tertiary'):
                    st.session_state.unscrew_count[2] += 1
                    
            else:
                st.button("", icon=':material/fiber_manual_record:', use_container_width=True, key=2, type='tertiary', disabled=True)

        with BLeft:
            count = st.session_state.unscrew_count[3]
            if count < 5:
                icon = ':material/add_circle:' if count % 2 == 0 else ':material/cancel:'
                if st.button("", icon=icon, use_container_width=True, key=3, type='tertiary'):
                    st.session_state.unscrew_count[3] += 1
                    
            else:
                st.button("", icon=':material/fiber_manual_record:', use_container_width=True, key=3, type='tertiary', disabled=True)

        with BRight:
            count = st.session_state.unscrew_count[4]
            if count < 5:
                icon = ':material/add_circle:' if count % 2 == 0 else ':material/cancel:'
                if st.button("", icon=icon, use_container_width=True, key=4, type='tertiary'):
                    st.session_state.unscrew_count[4] += 1
                    
            else:
                st.button("", icon=':material/fiber_manual_record:', use_container_width=True, key=4, type='tertiary', disabled=True)

# Add a button to open the dialog
if st.button("Open Access Panel"):
    access_panel()
