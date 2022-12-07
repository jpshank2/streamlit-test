import streamlit as st
import numpy as np
import pandas as pd

def displayInfo(fname, lname, state):
    st.write(f"Hello, {fname} {lname} from {state}")

st.write("# Hello, form! :wave:")

first_name = st.text_input('First Name')
last_name = st.text_input('Last Name')

state = st.selectbox("State", ['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY'])

clicked = st.button("Greetings!", on_click=displayInfo, args=(first_name, last_name, state))