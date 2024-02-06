import streamlit as st
import urllib.request
import io
from PIL import Image
import smtplib

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

def subscribePage():

    def sendTransactionId(id):
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login("hammadalipbt18@gmail.com", "cdyysxzrjellwrba")
            server.sendmail("hammadalipbt18@gmail.com", "rideonwhale@gmail.com" , f"{st.session_state.email} subscribed with transaction id {id}")
            return True
        except:
            return False

    # Page Title
    st.title("Subscribe - RideOnWhale.com")

    st.markdown("## <br><br>Packages", unsafe_allow_html=True)

    tenure = [1, 6, 12]
    monthlyPrice = [999, 899, 799]
    packageColumns = st.columns(3)
    for i, col in enumerate(packageColumns):
        col.markdown(f"### {tenure[i]} Month Package")
        col.markdown(f"### :red[Save {int((monthlyPrice[0]-monthlyPrice[i])/monthlyPrice[1]*100)}%]")
        col.markdown(f"### :blue[{monthlyPrice[i]}/- Rs./Month]")
        col.markdown(f"### Total: :green[{tenure[i]*monthlyPrice[i]}/- Rs.]")
        col.divider()

    st.markdown("## <br><br>Proceed To Payment", unsafe_allow_html=True)

    qrCol, formCol = st.columns(2)
    with qrCol:
        fd = urllib.request.urlopen("http://13.232.92.210/payment_qr.jpeg")
        image_file = io.BytesIO(fd.read())
        im = Image.open(image_file)
        st.image(im, width=400)

    with formCol:
        st.header("Provide Transaction ID")
        st.warning("It will take few hours to verify your transaction, You can call us for any other queries!")
        errorPlaceholder = st.empty()
        with st.form('paymentForm', clear_on_submit=True):
            transactionId = st.text_input("Transaction Id")
            submitButton = st.form_submit_button()

            if submitButton:
                if transactionId.strip(" ") == '':
                    errorPlaceholder.error('Please enter a valid transaction id!')
                else:
                    if sendTransactionId(transactionId):
                        errorPlaceholder.success("Submitted Successfully!")
                    else:
                        errorPlaceholder.error("Error in Submitting, Try Again!")


if 'loggedIn' in st.session_state:
    if st.session_state.loggedIn :
        if st.session_state.subscribed:
            st.success("Already A Subscriber!")
        else:
            subscribePage()
    else:
        st.error("You are not Logged In!")
else:
    st.error("You are not Logged In!")