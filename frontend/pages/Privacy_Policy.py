import streamlit as st
import urllib.request
import io
from PIL import Image


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

st.title("Privacy Policy - RideOnWhale.com")

## Introduction
st.header("Introduction:")
st.write(
    "RideOnWhale respects your privacy. This Privacy Policy explains how your information is handled on RideOnWhale.com and other community channels, such as Telegram, Whatsapp, Twitter, Facebook, Google+, and Quora ('Site(s) and the Service'). By accessing or using our Site(s), you agree to be bound by the terms and conditions of this Privacy Policy."
)

## Policy Changes
st.header("Policy Changes:")
st.write(
    "We reserve the right to change this Privacy Policy at any time. Changes will be effective immediately upon notice, given through means like emails to registered users or posting the revised Policy on this page. It is your responsibility to review and be aware of any modifications."
)

## Consent and Processing
st.header("Consent and Processing:")
st.write(
    "By using our Site(s) and the Service, you consent to the processing of your information as outlined in this Privacy Policy. Processing includes activities like using cookies and information collection, storage, and disclosure, all conducted in India."
)

## Location of Data Processing
st.write(
    "We and our service providers may be located in India. If you reside outside India, your personally identifiable information will be transferred to and processed in India. By using the Site(s) and/or the Service, you consent to such transfer and processing."
)

## Contact Information
st.header("Contact Information:")
st.write(
    "For questions or comments about this Privacy Policy or the use of your personally identifiable information, contact our privacy officer at rideonwhale@gmail.com."
)

## Why do we gather information?
st.header("Why do we gather information?")
st.write(
    "We gather, use, and disclose information to provide and administer requested products/services, understand user preferences, communicate with users, and manage user accounts. Information is used for marketing communications, newsletters, and updates about our company."
)

## Information Collected and Its Use
st.header("Information Collected and Its Use:")
st.subheader("Consumer Information:")
st.write(
    "The contact information collected includes first and last name, email address, telephone/mobile number, and physical address. Information may also be collected through cookies, as described below."
)

st.subheader("Cookies and Log Data:")
st.write(
    "Cookies are used to personalize information, record visits, and improve user experience. Log Data, including IP address, browser type, and web pages visited, is automatically recorded. This data is used for monitoring site usage and technical administration."
)

## Sharing Information
st.header("Sharing Information:")
st.write(
    "We do not sell, license, lease, or disclose personal information to third parties except as noted. Information may be shared with agents, contractors, and other marketers to improve marketing efforts. Google Analytics is used for web analysis, and you can opt-out."
)

## Policy Changes
st.header("Policy Changes:")
st.write(
    "If our information practices change, you will be notified through the Site(s). We may use customer information for new, unanticipated uses, and any changes will be disclosed in the updated privacy policy."
)

## Personal Privacy
st.header("Personal Privacy:")
st.write("We take utmost care of personal information at RideOnWhale to ensure no sharing with others.")

## Notification of Changes
st.header("Notification of Changes:")
st.write(
    "If changes occur in this privacy policy, they will be promptly posted on our Site(s), and notice may be given through the RideOnWhale channels. You agree to accept electronic posting as notice."
)

