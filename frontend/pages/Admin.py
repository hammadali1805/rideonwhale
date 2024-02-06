import streamlit as st
import urllib.request
import io
from PIL import Image
import smtplib
import sqlite3
import pytz
from datetime import datetime, timedelta
IST = pytz.timezone('Asia/Kolkata') 


st.set_page_config(
    page_title="Ride On Whale",
    layout="wide"
)

pageCss = '''
<style>

/* to hide default top bar of streamlit */
.stApp header{
    display: none;
    }

/* to start sidebar from top */
.appview-container{
    position: fixed;
}

/* to lift up sidebar icon */
div[data-testid='collapsedControl'] {
    top: 0px;
    left: 0px;
    }

</style>
'''

st.markdown(pageCss, unsafe_allow_html=True)

fd = urllib.request.urlopen("http://13.232.92.210/logo.png")
image_file = io.BytesIO(fd.read())
im = Image.open(image_file)
st.image(im, width=200)

def adminPage():
    
    connection = sqlite3.connect("database/users.db")
    cursor = connection.cursor()
    
    cursor.execute("SELECT EMAIL FROM USERS;")
    users = [x[0] for x in cursor.fetchall()]

    cursor.execute("SELECT *  FROM SUBSCRIBERS;")
    allSubscribers = cursor.fetchall()

    #filtering out those whose subs ended
    activeSubscribers = [x for x in allSubscribers if x[1] >= datetime.now(IST).strftime("%Y-%m-%d")]

    # not active + never subscribed
    nonSubscribers = [x for x in users if x not in [y[0] for y in activeSubscribers]]

    st.header("List Of Subscribers")
    indexCol, emailCol, subsendCol = st.columns(3)
    for i, subs in enumerate(activeSubscribers):
        indexCol.write(f'{i}')
        emailCol.write(f'{subs[0]}')
        subsendCol.write(f'{subs[1]}')

    with st.form("adminForm", clear_on_submit=True):
        errorPlaceholder = st.empty()
        email  = st.selectbox("Email", nonSubscribers)
        tenure  = st.selectbox("Tenure", [1, 6, 12])
        submitButton = st.form_submit_button("Add Subscriber")

        if submitButton:
            if email:
                current_date = datetime.now(IST)
                # Calculate the date after n months
                subsend_date = current_date + timedelta(days=(tenure * 30))  # Assuming 30 days per month for simplicity
                subsend_date = subsend_date.strftime("%Y-%m-%d")

                if email in [x[0] for x in allSubscribers]:
                    cursor.execute(f"UPDATE SUBSCRIBERS SET SUBSEND = '{subsend_date}' WHERE EMAIL = '{email}';")
                else:
                    cursor.execute(f"INSERT INTO SUBSCRIBERS (EMAIL, SUBSEND) VALUES ('{email}', '{subsend_date}');")
                connection.commit()
                connection.close()
                st.rerun()
            else:
                errorPlaceholder.error("No User To Add!")









if 'loggedIn' in st.session_state:
    if st.session_state.loggedIn and st.session_state.email == 'hammadalipbt18@gmail.com':
        adminPage()
    else:
        st.error("Access Denied!")
else:
    st.error("Access Denied!")