import streamlit as st
import numpy as np
import pandas as pd
import math, datetime

st.write("# Hello, form! :wave:")

today = datetime.date.today()

with st.form('greet_form', clear_on_submit=True):
    first_name = st.text_input('First Name')
    last_name = st.text_input('Last Name')
    state = st.selectbox("Home State", ['', 'AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY'])
    birthday = st.date_input('Birth Date')

    age = math.floor((today - birthday) / pd.timedelta(days=365))

    submitted = st.form_submit_button("Greet!")
    if submitted:
        if first_name == "" or first_name == None:
            st.warning("Please input a first name")
            st.stop()
        if last_name == "" or last_name == None:
            st.warning("Please input a last name")
            st.stop()
        elif state == '':
            st.warning("Please select a state")
            st.stop()
        elif birthday == '' or birthday == None:
            st.warning("Please select a birth date")
            st.stop()
        else:
            st.write(f"Hello, {first_name} {last_name} from {state}. You are {age} years old")
