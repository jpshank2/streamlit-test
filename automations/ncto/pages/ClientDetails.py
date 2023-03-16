import utilities.queries as q
import streamlit as st
from PIL import image 

st.header("Client Details Form")

cdimage = image.open('[insert bmss logo]', use_column_width = True)



st.markdown("Please input all required fields to proceed to the next screen")


with st.form("Client_Details"):
   st.markdown("Inside the form")
   slider_val = st.slider("Form slider")
   checkbox_val = st.checkbox("Form checkbox")

   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
       st.write("slider", slider_val, "checkbox", checkbox_val)

# inserting elements out of order
form = st.form("my_form")
form.slider("Inside the form")
st.slider("Outside the form")

# Now add a submit button to the form:
form.form_submit_button("Submit")

st.markdown("Outside the form")

def screen(st, conn):
    partner = q.run_query('SELECT * FROM tblEngagement;', conn)
    manager = q.run_query('SELECT * FROM tblEngagement;', conn)
    name = q.run_query('SELECT * FROM tblEngagement;', conn)
    codes = q.run_query('SELECT * FROM tblEngagement;', conn)
    offices = q.run_query('SELECT * FROM DIM_OFFICES; ', conn)

    st.selectbox('Client Partner', [i for i in partner.CLIENTPARTNER])
    st.selectbox('Client Manager', [i for i in manager.CLIENTMANAGER])
    st.selectbox('Client Name', [i for i in name.CLIENTNAME])
    st.selectbox('Client Code', [i for i in codes.CLIENTCODE])
    st.selectbox('Client Office', [i for i in offices.CLIENTOFFICE])