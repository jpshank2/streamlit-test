import streamlit as st
from snowflake.connector import connect
from automations.ncto.frame import clientTakeOn
from PIL import Image
from requests import get
from io import BytesIO
# import automations.ncto.frame as ncto


@st.cache_resource
def init_connection():
    return connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()

MainHeaderImage = Image.open(BytesIO(get('https://i.imgur.com/DcFwdrQ.png').content))

#Added a logo to the top of the screen
st.image(MainHeaderImage, use_column_width = True)

st.markdown("# Hello, form! :wave:")
# ncto.clientTakeOn(st, conn)
clientTakeOn(st, conn)
