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

st.title("Refund and Cancellation Policy - RideOnWhale.com")

## Introduction
st.header("Introduction:")
st.write(
    "This Refund and Cancellation Policy outlines the terms and conditions for refunds on payments made on RideOnWhale.com. Users are encouraged to carefully read and understand the policy before making any payments."
)

## Refund Conditions
st.header("Refund Conditions:")
st.write("1. Amount once paid through the payment gateway shall not be refunded, except in the following circumstances:")
st.write("   - Multiple debiting of Customer’s Card/Bank Account due to technical error.")
st.write("   - Customer's account being debited with excess amount in a single transaction due to technical error.")
st.write("2. In case of technical error resulting in payment being charged but subscription unsuccessful, the Customer may be provided with the subscription by RideOnWhale at no extra cost.")
st.write("3. If the Customer wishes to seek a refund in such cases, the amount will be refunded after deduction of Payment Gateway charges or any other charges.")

## Refund Application
st.header("Refund Application:")
st.write("1. The customer must submit an application for a refund along with the transaction number and the original payment receipt (if any).")
st.write("2. The application in the prescribed format should be sent to rideonwhale@gmail.com.")
st.write("3. The application will be processed manually, and after verification, if the claim is found valid, the excess amount will be refunded through electronic mode within 21 calendar days.")
st.write("4. It may take 5–21 days for the money to reflect in the bank account, depending on the bank’s policy.")

## Non-Liability
st.header("Non-Liability:")
st.write("The company assumes no responsibility and shall incur no liability if it is unable to affect any payment instruction(s) under the following circumstances:")
st.write("a. Incomplete, inaccurate, invalid, or delayed payment instruction(s) issued by the user.")
st.write("b. Insufficient funds or limits in the payment account to cover the specified amount.")
st.write("c. Funds available in the payment account are subject to encumbrance or charge.")
st.write("d. Refusal or delay by the user's bank or the NCC in honoring the payment instruction(s).")
st.write("e. Events beyond the company's control, including fire, flood, natural disasters, bank strikes, power outages, and system failures.")

## Termination
st.header("Termination:")
st.write("The company may suspend or terminate a user's account or services, with or without notice, for any reason or no reason. Termination is effective immediately.")
st.write("Upon termination, the user agrees to stop using the services.")

## Dispute Resolution
st.header("Dispute Resolution:")
st.write("The company may resolve disputes through binding arbitration in accordance with the Indian Arbitration & Conciliation Act, 1996. Disputes will be arbitrated on an individual basis.")
