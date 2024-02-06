import streamlit as st
from PIL import Image
import sqlite3
import urllib.request
import io
import smtplib
import random
from datetime import datetime, timedelta
import pytz


st.set_page_config(
    page_title="Ride On Whale",
    layout="wide"
)

if "loggedIn" not in st.session_state:
    st.session_state.loggedIn=False
    st.session_state.email = ''
    st.session_state.password = ''
    st.session_state.subscribed = False
    st.session_state.otp = None

    
def logInPage():
    IST = pytz.timezone('Asia/Kolkata') #so as to do all cal in IST and doesnt depend on local time of server


    connection = sqlite3.connect("database/users.db")
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS USERS (EMAIL TEXT, PASSWORD TEXT);")
    cursor.execute("CREATE TABLE IF NOT EXISTS SUBSCRIBERS (EMAIL TEXT, SUBSEND TEXT);")
    connection.commit()

    pageCss = '''
    <style>
    
    /* to set background iamge */
    .stApp {
        background-image: url("http://13.232.92.210/background.jpg");
        background-size: cover;
        }

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
    

    /* to give typewriter animation */
    .typewriter {
        display: inline-block;
        overflow: hidden; /* Ensures the content is not revealed until the animation */
        white-space: nowrap; /* Keeps the content on a single line */
        margin: 0 auto; /* Gives that scrolling effect as the typing happens */
        text-align: left;
        animation: typing 7s steps(40) infinite;
    }
    
    /* The typing effect */
    @keyframes typing {
        0% { width: 0 }
        40% { width: 100% }
        50%{ width: 100%}
        90%{width: 0}
        100% { width: 0}
    }
    
    div[data-testid='stForm']{
        background-color: lightgrey;
    }

    </style>
    '''

    st.markdown(pageCss, unsafe_allow_html=True)

    def sendOtp(email):
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login("hammadalipbt18@gmail.com", "YOUR_GMAIL_PASSKEY")
            otp = random.randint(1000, 9999)
            server.sendmail("hammadalipbt18@gmail.com", email, f"Your Otp for Ride On Whale Email Verification is {otp}")
            return str(otp)
        except:
            return None

    def sendPassword(email):
        try:
            cursor.execute(f"SELECT PASSWORD FROM USERS WHERE EMAIL = '{email}';")
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login("hammadalipbt18@gmail.com", "YOUR_GMAIL_PASSKEY")
            password = cursor.fetchone()[0]
            server.sendmail("hammadalipbt18@gmail.com", email, f"Your Password of Ride On Whale Account is {password}")
            return True
        except:
            return False


    def logIn(email: str, password: str, errorPlaceholder):

        email = email.lower().strip()
        password = password.strip()

        if email == '' or password == '':
            errorPlaceholder.error("Please Fill All The Fields !")
        elif email[-10:] != "@gmail.com" or len(email) < 13:
            errorPlaceholder.error("Please Provide Valid Gmail !")
        elif len(password)<8 or  password.isalpha() or password.isdigit() or password.isalnum() or password.islower():
            errorPlaceholder.error("Password Must Contain: Minimum 8 characters, Atlest 1 special Character, Atlest 1 Numeric Character, Atlest 1 Capital Letter")
        else:
            cursor.execute(f"SELECT * FROM USERS WHERE EMAIL = '{email}';")
            if cursor.fetchone() is None:
                errorPlaceholder.error("No User Exists With This Email, SignUp First !")
            else:
                cursor.execute(f"SELECT * FROM USERS WHERE EMAIL = '{email}' AND PASSWORD = '{password}';")
                if cursor.fetchone() is None:
                    errorPlaceholder.error("Incorrect Password ! You can Get Your Password From The DropDown By Choosing Forget Password.")
                else:
                    cursor.execute(f"SELECT SUBSEND FROM SUBSCRIBERS WHERE EMAIL='{email}';")
                    result = cursor.fetchone()
                    if result:
                        if result[0] >= datetime.now(IST).strftime("%Y-%m-%d") :
                            st.session_state.subscribed = True
                    st.session_state.loggedIn = True
                    st.session_state.email = email
                    st.session_state.password = password
                    st.rerun()

    def signUp(email: str, password: str, errorPlaceholder, userOtp=None):

        email = email.lower().strip()
        password = password.strip()

        if email == '' or password == '':
            errorPlaceholder.error("Please Fill All The Fields !")
        elif email[-10:] != "@gmail.com" or len(email) < 13:
            errorPlaceholder.error("Please Provide Valid Gmail !")
        elif len(password)<8 or  password.isalpha() or password.isdigit() or password.isalnum() or password.islower():
            errorPlaceholder.error("Password Must Contain: Minimum 8 characters, Atlest 1 special Character, Atlest 1 Numeric Character, Atlest 1 Capital Letter")
        else:
            cursor.execute(f"SELECT * FROM USERS WHERE EMAIL = '{email}';")
            if cursor.fetchone() is not None:
                errorPlaceholder.error("User Already Exists With This Email !")
            else:
                if not st.session_state.otp:
                    errorPlaceholder.info("Sending OTP...")
                    otp = sendOtp(email)
                    if otp:
                        st.session_state.email = email
                        st.session_state.password = password
                        st.session_state.otp = otp
                        st.rerun()
                    else:
                        errorPlaceholder.error("Error Sending Otp ! Try Again.")
                else:
                    if st.session_state.otp==userOtp:
                        cursor.execute(f"INSERT INTO USERS (EMAIL, PASSWORD) VALUES ('{email}', '{password}');")
                        #adding a 7 days Trial
                        # cursor.execute(f"INSERT INTO SUBSCRIBERS (EMAIL, SUBSEND) VALUES ('{email}', '{(datetime.now(IST) + timedelta(days=7)).strftime('%Y-%m-%d')}');")
                        connection.commit()
                        # st.session_state.subscribed = True
                        st.session_state.loggedIn = True
                        st.session_state.otp = None
                        st.rerun()
                    else:
                        errorPlaceholder.error("Incorrect Otp")

    def forgetPassword(email, errorPlaceholder, userOtp=None):
        email = email.lower().strip()

        if email == '' or email[-10:] != "@gmail.com" or len(email) < 13:
            errorPlaceholder.error("Please Provide Valid Gmail !")
        else:
            cursor.execute(f"SELECT * FROM USERS WHERE EMAIL = '{email}';")
            if cursor.fetchone() is None:
                errorPlaceholder.error("User Does Not Exists!")
            else:
                if not st.session_state.otp:
                    errorPlaceholder.info("Sending OTP...")
                    otp = sendOtp(email)
                    if otp:
                        st.session_state.otp = otp
                        st.session_state.email = email
                        st.rerun()
                    else:
                        errorPlaceholder.error("Error Sending Otp ! Try Again.")
                else:
                    if st.session_state.otp==userOtp:
                        passwordSent = sendPassword(email)
                        if passwordSent:
                            st.session_state.otp = None
                            errorPlaceholder.success("Password Sent At Your Email !")
                        else:
                            errorPlaceholder.error("Error Sending Password ! Try Again.")
                    else:
                        errorPlaceholder.error("Incorrect Otp")           
    


    def displayForm(formToDisplay, form):

        with form:
            errorPlaceholder = st.empty()
            if formToDisplay=="LogIn":
                    email = st.text_input("Email", placeholder="Enter Your Email")
                    password = st.text_input("Password", placeholder="Enter Your Password", type='password')
                    submitButton = st.form_submit_button("LogIn")

                    if submitButton:
                        logIn(email, password, errorPlaceholder)

            elif formToDisplay=="SignUp":
                    if st.session_state.otp:
                        errorPlaceholder.success("OTP sent Successfully ! Check your spam folder too!")
                        userOtp = st.text_input("OTP", placeholder="Enter OTP sent to your email")
                        submitButton = st.form_submit_button("SignUp")
                        if submitButton:
                            signUp(st.session_state.email, st.session_state.password, errorPlaceholder, userOtp=userOtp)


                    else:
                        email = st.text_input("Email", placeholder="Enter Your Email")
                        password = st.text_input("Password", placeholder="Enter Your Password", type='password')
                        submitButton = st.form_submit_button("SignUp")
                        if submitButton:
                            signUp(email, password, errorPlaceholder)

                        

            elif formToDisplay=="ForgetPassword":
                    if st.session_state.otp:
                        errorPlaceholder.success("OTP sent Successfully ! Check your spam folder too!")
                        userOtp = st.text_input("OTP", placeholder="Enter OTP sent to your email")
                        submitButton = st.form_submit_button()
                        if submitButton:
                            forgetPassword(st.session_state.email, errorPlaceholder, userOtp=userOtp)


                    else:
                        email = st.text_input("Email", placeholder="Enter Your Email")
                        submitButton = st.form_submit_button()
                        if submitButton:
                            forgetPassword(email, errorPlaceholder)
            

    textCol, formCol = st.columns([0.7, 0.3], gap="large")


    with textCol:
        fd = urllib.request.urlopen("http://13.232.92.210/logo.png")
        image_file = io.BytesIO(fd.read())
        im = Image.open(image_file)
        st.image(im, width=200)
        st.markdown("# <div class='typewriter'>Unlock Market Secrets</div>", unsafe_allow_html=True)
        st.markdown("## Decode Option Chains", unsafe_allow_html=True)
        st.markdown("""<br>Follow the money and trade alongside the giants - Where they invest, you profit!<br><br>
        Decode the market participants by Option chain in real-time to see where (Institutional investors, Foreign investors, Big players, Big fish) were they putting their money, If you know their move, if you know where their money is going, you can easily drive with them. See it in every 2 minutes what they are doing.""", unsafe_allow_html=True)



    with formCol:
        st.markdown("## <br><br>LogIn/SignUp", unsafe_allow_html=True)
        formToDisplay = st.selectbox(" Select Operation", ["LogIn", "SignUp", "ForgetPassword"])

        form = st.form("loginForm", clear_on_submit=True)

        displayForm(formToDisplay, form)


    st.markdown("# <br><br>Learn To Analyse", unsafe_allow_html=True)
    # st.markdown("""<style>
    #     iframe {
    #     border: none;
    #     border-radius: 10px; /* Set your desired border radius */
    #     }
    #     </style>""", unsafe_allow_html=True)
    
    st.warning("Comming Soon...")
    connection.close()





def homePage():
    pageCss = '''
    <style>
    .stApp header{
    display: none;
    }
    </style>
    '''

    def logOut():
        st.session_state.loggedIn = False
        st.session_state.email = ''
        st.session_state.password = ''
        st.session_state.subscribed = False

    st.markdown(pageCss, unsafe_allow_html=True)
    st.markdown("Home Page")
    st.button("Log Out", on_click=logOut)



if st.session_state.loggedIn:
    homePage()
else:
    logInPage()
