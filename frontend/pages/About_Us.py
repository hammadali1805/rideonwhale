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

# Page Title
st.title("About Us - RideOnWhale.com")

# Founder's Introduction
st.header("Founder's Introduction")
st.markdown(
    "Hello, I'm Amritesh Chauhan, the founder of RideOnWhale.com. Armed with a degree in civil engineering, "
    "my journey into the dynamic world of finance and options trading may seem unconventional, but it's a testament "
    "to the transformative power of passion and dedication."
)
# st.image("path/to/amritesh_image.jpg", caption="Amritesh Chauhan - Founder", use_column_width=True)

# Professional Journey
st.header("Professional Journey")
st.write(
    "My early professional life was rooted in civil engineering, but my fascination with financial markets, particularly "
    "options trading, led me to embark on a parallel journey. For the past 12 years, I've immersed myself in the dynamic "
    "world of options trading, honing my skills and gaining invaluable insights along the way."
)

# Passion for Trading
st.header("Passion for Trading")
st.write(
    "Driven by a deep-seated passion for option trading, I transitioned from being solely an options trader to a dedicated one. "
    "The intricate dance of numbers, market dynamics, and the thrill of strategic decision-making became my daily pursuit."
)

# RideOnWhale.com Inception
st.header("Inception of RideOnWhale.com")
st.write(
    "The inception of RideOnWhale.com is a result of my desire to share the knowledge and expertise I've acquired over the years. "
    "Despite not having a financial background, I've come to understand the nuances of the stock market, particularly NSE option chains, "
    "and I'm excited to provide a platform that simplifies this information for others."
)

# Our Mission
st.header("Our Mission")
st.write(
    "At RideOnWhale.com, our mission is clear: to empower individuals with the insights and tools needed to navigate the NSE option chain confidently. "
    "We're here to bridge the gap between complex financial concepts and everyday traders, making information accessible and actionable."
)

# Commitment to Transparency
st.header("Commitment to Transparency")
st.write(
    "I want to emphasize that my journey into the financial world started as a passion project, and RideOnWhale.com operates with transparency. "
    "While my educational background may not be in finance, my commitment to providing valuable insights and fostering a community of informed traders is unwavering."
)

# Contact Information
st.header("Contact Information")
st.write("Feel free to reach out to us:")
st.write("- Email: rideonwhale@gmail.com")
st.write("- Phone: +91 123 456 7890")

# Social Links
st.header("Connect with Us:")
st.write("- [Twitter](https://twitter.com/rideonwhale)")
st.write("- [Instagram](https://www.instagram.com/rideonwhale2023)")
st.write("- [Youtube](https://www.youtube.com/@rideonwhale)")

# Disclaimer
st.warning(
    "Disclaimer: The information provided on this website is for educational and informational purposes only. RideOnWhale.com is not a registered entity with SEBI. "
    "Users are encouraged to conduct their research and seek professional advice before making any investment decisions."
)
