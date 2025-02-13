import streamlit as st
import pandas as pd
from datetime import datetime
from model.make_prediction import make_infer
# from utils import edf_handler


st.title("Inferência de diagnostico")

st.write("envie seu exame!")


if 'button' not in st.session_state:
    st.session_state['button'] = False


def click_button():
    st.session_state['button'] = not st.session_state['button']


st.button("Exame_amostra", on_click=click_button)


if st.session_state['button']:
    uploaded_file = st.file_uploader("Choose a file")
    st.session_state.clicked = False

    if uploaded_file is not None:
        try:
            # df_exam = edf_handler(uploaded_file)
            result = make_infer(uploaded_file)
            if result == 1:
                st.write('### A hipótese diagnóstica é: CNEP (crises não epilépticas psicogênicas)')
                
            elif result == 0:
                st.write('### A hipótese diagnóstica é: Epilepsia')
            else:
                st.write('Erro')
        except Exception as e:
            st.error(f"Erro ao ler o arquivo {e}")