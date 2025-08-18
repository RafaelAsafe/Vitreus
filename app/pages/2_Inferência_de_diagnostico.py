from datetime import time

import streamlit as st

from model.make_prediction import make_infer
from src.st_modules import time_input_with_seconds

st.title("Inferência de diagnóstico")

if 'button' not in st.session_state:
    st.session_state['button'] = False


def click_button():
    st.session_state['button'] = not st.session_state['button']


st.button("Exame_amostra", on_click=click_button)


if st.session_state['button']:

    ictal_start = time_input_with_seconds("insira tempo de inicio do período ictal", time(0, 0, 0))
    ictal_end = time_input_with_seconds("insira tempo de fim do período ictal", time(0, 0, 0))

    uploaded_file = st.file_uploader("Choose a file")
    st.session_state.clicked = False

    if uploaded_file is not None:
        try:
            # df_exam = edf_handler(uploaded_file)
            result = make_infer(uploaded_file,ictal_start,ictal_end)
            if result == 1:
                st.write('### Hipótese diagnóstica: Crises Não Epilépticas psicogênicas (PNES)')
                
            elif result == 0:
                st.write('### Hipótese diagnóstica: Epilepsia')
            else:
                st.write('Erro')
        except Exception as e:
            st.error(f"Erro ao ler o arquivo {e}")