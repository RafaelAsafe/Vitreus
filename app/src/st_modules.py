import streamlit as st
from datetime import time

def time_input_with_seconds(label, value=time(0, 0, 0)):
    st.write(label)
    cols = st.columns([1,1,1,2])
    with cols[0]: 
        h = st.number_input("H", min_value=0, max_value=23, value=value.hour, key=f"{label}_h")
    with cols[1]: 
        m = st.number_input("M", min_value=0, max_value=59, value=value.minute, key=f"{label}_m")
    with cols[2]:
        s = st.number_input("S", min_value=0, max_value=59, value=value.second, key=f"{label}_s")
    return time(h, m, s)

