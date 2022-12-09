import streamlit as st
import smtplib, datetime, schedule
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def emailMe():
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = st.secrets['zeal_address']
        msg['To'] = 'jshank@abacustechnologies.com'
        msg['Subject'] = "Hello from streamlit"

        body_html = f"<p>Hello from streamlit. It is currently {datetime.datetime.now().strftime('%I:%M %p')}</p>"
        mimeBody = MIMEText(body_html, 'html')
        msg.attach(mimeBody)

        mail = smtplib.SMTP("smtp.outlook.office365.com", 587, timeout=20)
        mail.starttls()
        
        recipient = ['jshank@abacustechnologies.com']
        
        mail.login(st.secrets['zeal_address'], st.secrets['zeal_pass'])
        mail.sendmail(st.secrets['zeal_address'], recipient, msg.as_string())
        mail.quit()
    except Exception as e:
        st.error(e)

st.write("# Hello, home! :wave:")
st.snow()

st.write("This is the Abacus Technologies test site for creating streamlit apps for Business Intelligence. If you are interested in our services, please [email us](mailto:bizintel@abacustechnologies.com?subject=Streamlit).")

try:
    schedule.every(12).hours.do(emailMe)
except Exception as e:
    st.error(e)