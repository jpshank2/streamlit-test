import streamlit as st
from snowflake.connector import connect
from automations.ncto.frame import clientTakeOn
from PIL import Image
# import automations.ncto.frame as ncto


@st.cache_resource
def init_connection():
    return connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()

MainHeaderImage = Image.open('C:\Users\imesser\BMSS\Business Intelligence - Documents\Clients\Abacus\Abacus Technologies logo 2022\Full color\Abacus logo 2022_Full-color.png')

#Added a logo to the top of the screen
st.image(MainHeaderImage, use_column_width = True)

st.markdown("# Hello, form! :wave:")
# ncto.clientTakeOn(st, conn)
clientTakeOn(st, conn)
