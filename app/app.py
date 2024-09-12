import streamlit as st
import pandas as pd
from datetime import datetime
from utils import read_edf


# olar

st.title("Vitreus")

st.write("Aplicação com intuito de classificar pacientes com diagnosticos de CNEPs (Crises Não Epilépticas Psicogênicas) e CEs (Crises Epilepsia)")

col1, col2 = st.columns([1, 1])

if 'button' not in st.session_state:
    st.session_state['button'] = False

if 'button2' not in st.session_state:
    st.session_state['button2'] = False


# button PNES:
with col1:

    def click_button():
        st.session_state['button'] = not st.session_state['button']

    st.button("CNEP", on_click=click_button)

    if st.session_state['button']:
        uploaded_file_pnes = st.file_uploader("Choose a file")
        st.session_state.clicked = False

        if uploaded_file_pnes is not None:
            try:
                with open(f".\\data\\exams\\raw\\PNES\{uploaded_file_pnes.name.split('.')[0].replace(' ','')}_{datetime.now().strftime('%Y-%m-%d-%H%M%S')}.edf", 'wb') as f:
                    f.write(uploaded_file_pnes.getvalue())
            except Exception as e:
                st.error(f"Erro ao ler o arquivo {e}")
# button PNES:
with col2:

    def click_button2():
        st.session_state['button2'] = not st.session_state['button2']

    st.button("CEs", on_click=click_button2)

    if st.session_state["button2"]:
        uploaded_file_ce = st.file_uploader("Choose a exam")
        st.session_state.clicked = False

        # restringir apenas para edf files
        if uploaded_file_ce is not None:
            try:
                with open(f".\\data\\exams\\raw\\SE\{uploaded_file_ce.name.split('.')[0]}_{datetime.now().strftime('%Y%m%d')}.edf", 'wb') as f:
                    f.write(uploaded_file_ce.getvalue())
            except Exception as e:
                st.error(f"Erro ao ler o arquivo {e}")
