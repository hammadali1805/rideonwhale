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

st.title("Terms and Conditions - RideOnWhale.com")

## Introduction
st.header("Introduction:")
st.write("By accessing and using RideOnWhale.com ('Website'), users agree to the following terms and conditions and the accompanying Privacy Policy. Continued use implies acceptance of any future modifications to these terms.")

## Registration and Termination
st.header("Registration and Termination:")
st.write("- RideOnWhale reserves the right to deny access or terminate accounts without notice for unauthorized use or violation of terms.")
st.write("- Termination does not waive any rights held by RideOnWhale, and all granted rights revert to RideOnWhale upon termination.")

## License
st.header("License:")
st.write("- Users are granted a non-exclusive, revocable license to view the website for personal use.")
st.write("- No rights are granted for adaptation, editing, republishing, etc., without the prior written permission of RideOnWhale.")

## Data Mining
st.header("Data Mining:")
st.write("- Automated collection of data from the website is strictly prohibited.")
st.write("- Copyright for the website material, including text, images, and multimedia, belongs to RideOnWhale and its licensors.")

## Security
st.header("Security:")
st.write("- Unauthorized use, entry, password misuse, or interference is strictly prohibited.")
st.write("- Users are responsible for securing login information.")
st.write("- RideOnWhale may employ technology for aggregate statistical information but does not monitor individual user behavior.")

## Service Delays
st.header("Service Delays:")
st.write("- RideOnWhale reserves the right, without obligation or notice, to modify, improve, or suspend the website for maintenance.")
st.write("- Services described on the website may be discontinued or changed at RideOnWhale's discretion.")

## Liability
st.header("Liability:")
st.write("- RideOnWhale and its affiliates are not liable for direct, indirect, or incidental damages arising from website use.")
st.write("- Continuous, uninterrupted, or secure access to the website is not guaranteed.")

## Entire Agreement
st.header("Entire Agreement:")
st.write("- This User Agreement constitutes the entire agreement between the parties.")
st.write("- Users assume full responsibility for gains and losses; RideOnWhale does not guarantee accuracy or endorse views.")

## Disclaimer
st.header("Disclaimer:")
st.write("- Information on RideOnWhale.com is for educational purposes only and does not constitute specific recommendations.")
st.write("- Users acknowledge the high risks associated with trading and investing, taking sole responsibility for their activities.")
st.write("- Past performance does not guarantee future results.")
st.write("- Services provided are non-refundable.")

## Contact Information
st.header("Contact Information:")
st.write("For inquiries regarding these terms and conditions, users can contact RideOnWhale's privacy officer at rideonwhale@gmail.com.")
