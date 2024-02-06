import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts
import sqlite3
from datetime import datetime, timedelta
from PIL import Image 
import pytz
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
st.title("Option Chain Data - RideOnWhale.com")




def optionChainDataPage():
    IST = pytz.timezone('Asia/Kolkata') #so as to do all cal in IST and doesnt depend on local time of server

    def drawLineChart(conn, symbol, expiryDate, strikes):
        # Create a placeholder string with as many placeholders as the length of your value_list
        strikePrices = ', '.join(['?'] * len(strikes))

        query = f"SELECT * FROM {symbol} WHERE Expiry_Date='{expiryDate}'  AND Strike_Price IN ({strikePrices});"

        # Execute the query with the values as parameters
        df = pd.read_sql_query(query, conn, params=strikes)

        df['S_COI_Calls'] = df.groupby('Time')['COI_Calls'].transform('sum')
        df['S_COI_Puts'] = df.groupby('Time')['COI_Puts'].transform('sum')
        df['R_S_COI'] = np.where(df["S_COI_Calls"] != 0, df['S_COI_Puts'] / df["S_COI_Calls"], np.nan)
        graph = px.line(df, x='Time', y='R_S_COI', height=200)
        return graph



    if __name__ == "__main__":
        # to maintain a single connection for sinle session to reduce the load on db 
        if 'connection' not in st.session_state:
            st.session_state.connection = sqlite3.connect("database/optionChainData.db", check_same_thread=False)
            st.session_state.cursor = st.session_state.connection.cursor()


        symbols = ["NIFTY", "FINNIFTY", "BANKNIFTY", "MIDCPNIFTY"]

        with open("backend/symbols.txt") as f:
            data = f.readlines()

        stocks = [i.strip('\n') for i in data if i.strip('\n') not in symbols]
        
        #to display filters side by side
        col1, col2, col3, col4, col5 = st.columns(5)


        # symbol filter to select the symbol to decide which table to fetch data from
        symbol_filter = col1.selectbox("Select the Symbol", symbols)

        stock_filter = col2.selectbox("Select the Stock", stocks, index=None)

        if stock_filter == None:
            table_to_fetch = symbol_filter
        else:
            table_to_fetch = stock_filter


        # Use a SQL query to get unique Distinct Expiry Dates from the tabel so as to display in date filter as epiry dates depends on the symbol
        query = f"SELECT DISTINCT Expiry_Date FROM {table_to_fetch};"
        st.session_state.cursor.execute(query)

        # Fetch all unique values
        unique_values = st.session_state.cursor.fetchall()

        # Extract values from the result
        expiryDates = [value[0] for value in unique_values]



        # exopiraty date filter to decide wich dates data has to be fetch from the table
        date_filter = col3.selectbox("Select the Expiry", expiryDates)


        #no of strike filter so to give an option to the user to decide how many strikes he want to analyse fixing initialy at 12   
        no_of_strikes_filter = col4.selectbox("Select number of Strikes", [10, 12, 14, 16, 18, 20], index=1)

        #possibel time ranges...the data is displayed dividing in time ranges so as to reduce lagg as too much data to dispaly
        time_ranges = ["09:15:00-09:45:00", "09:45:00-10:15:00","10:15:00-10:45:00","10:45:00-11:15:00","11:15:00-11:45:00","11:45:00-12:15:00", "12:15:00-12:45:00", "12:45:00-13:15:00", "13:15:00-13:45:00", "13:45:00-14:15:00", "14:15:00-14:45:00", "14:45:00-15:15:00", "15:15:00-15:30:00"]

        #time filter to give user a choice which time range he want to analyse, setted to none as if nothing is selected live data will be shown of pas half hour
        time_filter  = col5.selectbox("Select Time Range", time_ranges, index=None)



        # creating a single-element container. as we cant initiate a widget in while true so creating a placee holder and than chainging content inside it
        placeholder = st.empty()
        while True:
            
            #so as to check if there is any time filter than show data based on time filter otherwise show past half hour data
            if time_filter:

                start_time_filter, end_time_filter = time_filter.split('-')

                query = f"SELECT * FROM {table_to_fetch} WHERE Expiry_Date='{date_filter}' AND Time >= '{start_time_filter}' AND Time <= '{end_time_filter}';"
                
                # Use pandas read_sql_query to load the table into a DataFrame
                df = pd.read_sql_query(query, st.session_state.connection)

                # this live flac is used to display live banner on the screen if the data is live 
                live = False
            
            else:

                # Get current time
                current_time = datetime.now(IST)

                #so as display half hour data from current time if market open but if market is closed than dislplay last half hour market data
                if ("09:18:00" <= current_time.strftime("%H:%M:%S") <= "15:33:00"):

                    # Calculate half an hour earlier
                    half_hour_earlier = current_time - timedelta(minutes=30)

                    # Format the result as a string
                    formatted_time = half_hour_earlier.strftime('%H:%M:%S')


                    query = f"SELECT * FROM {table_to_fetch} WHERE Expiry_Date='{date_filter}' AND Time >= '{formatted_time}' ;"
                    
                    # Use pandas read_sql_query to load the table into a DataFrame
                    df = pd.read_sql_query(query, st.session_state.connection)

                    live = True

                else:

                    query = f"SELECT * FROM {table_to_fetch} WHERE Expiry_Date='{date_filter}' AND Time >= '15:00:00' ;"
                
                    # Use pandas read_sql_query to load the table into a DataFrame
                    df = pd.read_sql_query(query, st.session_state.connection)

                    # this live flac is used to display live banner on the screen if the data is live 
                    live = False

            #sorting the values in descending by time so to show new data above
            df = df.sort_values(by=['Time', 'Strike_Price'], ascending=[False, True]).reset_index(drop=True)

            with placeholder.container():
                #showing the underlying value and timestamp from the session state and this value changes after every cycle and depends on symbol.
                # if data is live and time is of market open... than show live banner
                if live and ("09:18:00" <= datetime.now(IST).strftime("%H:%M:%S") <= "15:33:00"):
                    st.markdown(":large_green_circle: LIVE")

                #this check is added so that there should be no index error when all tables will be cleared at 00:00:00 midnight
                if len(df)>1:
                    # 0 is used as to show latest values as it in lagrest time so will be on top
                    st.markdown(f"## {df['underlyingValue'][0]}") 
                    st.markdown(f"{df['Time'][0]}")

                #keeping the chart place at the top...not creating it rn as its data will be calculated afterwards
                chart_place = st.empty()

                #splitting the df of every time as the formatting and calc and background gradient will  be done for each time individually
                splitted_dfs = []
                strikes = []  #defining empty list as if there would be no data in df then the loop will not run and there will be no strikes defined and the function to draw chart will throw error that strikes is not defined 
                for i in df["Time"].unique().tolist():


                    st.markdown(i)
                    temp_df = df[df["Time"]==i].reset_index(drop=True)

                    # Specify the number of middle rows you want (replace 'n' with the actual number) it is basically doubel of the no of strike filgter as to analyse for both above and below
                    n = 2*no_of_strikes_filter
                    #this check is done as sometimes there will be less data in df for some dates so then it should display all the values..
                    if len(temp_df) > n :
                        # Calculate the starting index for the middle rows
                        start_index = (len(temp_df) - n) // 2
                        temp_df = temp_df.iloc[start_index:start_index + n].copy().reset_index(drop=True)

                    #seprating strikes so as to build graph
                    strikes = temp_df['Strike_Price'].unique().tolist()

                    #doing this calc for every time as this depends on both time no of strikes symbol expiry date...so doing in lasgt after fetching required dataset....
                    temp_df['S_C_Calls'] = temp_df['C_Calls'].sum()
                    temp_df['S_C_Puts'] = temp_df['C_Puts'].sum()
                    temp_df['S_COI_Calls'] = temp_df['COI_Calls'].sum()
                    temp_df['S_COI_Puts'] = temp_df['COI_Puts'].sum()
                    temp_df['R_S_COI'] = np.where(temp_df["S_COI_Calls"] != 0, temp_df['S_COI_Puts'] / temp_df["S_COI_Calls"], np.nan)



                    #calculating the index at which the underlying value of the time lies as comapard to nearest strike price
                    index_of_current_strikePrice = (temp_df['Strike_Price'] - temp_df['underlyingValue']).abs().idxmin()

                    #this is a calc to decide how much hight should each df use on the screen to display without scrolling
                    height_of_df = ((len(temp_df)+1)*35+3)


                    #dropping further unwanted colms....havent dropped time as when data will be downloaded then there should be time in it.....
                    temp_df = temp_df.drop(columns=['underlyingValue', 'Expiry_Date'])

                    # this step is done as the above calcs result has to be shown in only that row at which underlying value of that time is nearest and replacing ather cells by none not by empty string as the type of np.nan is float
                    temp_df.loc[temp_df.index != index_of_current_strikePrice,['S_C_Calls', 'S_C_Puts', 'S_COI_Calls', 'S_COI_Puts', 'R_S_COI'] ] = np.nan

                    
                    # styling the df to be shown like the row of underlying value yellow....C_Amt_Calls_Cr reddish above the yellow row and c_Amt_Puts_Cr greenish below yellow row
                    #calculaing background gradient for COI calls and puts
                    # NOTE: Syling is done at the last as some functions of pd Dataframe dont run on Styled DataFrame
                    temp_df = temp_df.style.background_gradient(cmap='Blues', subset = ['COI_Calls', 'COI_Puts'])
                    temp_df = temp_df.map(lambda s: 'background-color: yellow; color: black;', subset = pd.IndexSlice[index_of_current_strikePrice, :])
                    temp_df = temp_df.map(lambda s: 'background-color: Tomato;', subset = pd.IndexSlice[0:index_of_current_strikePrice-1, ['C_Amt_Calls_Cr']])
                    temp_df = temp_df.map(lambda s: 'background-color: MediumSeaGreen;', subset = pd.IndexSlice[index_of_current_strikePrice+1:, ['C_Amt_Puts_Cr']])

                    #formatting all the floats to 2 decimal
                    temp_df.format(precision = 2)

                    #setting border so as to show in html do make a table
                    temp_df.set_properties(**{"border": "1px solid black"})

                    splitted_dfs.append(temp_df) 

                    # displaying data of each time....
                    st.dataframe(temp_df, height=height_of_df)

                # the code below concats all the data on the screen to  a concatination is done using for loop as  only 2 styled dfs can be concatinated the concatinated data is converted to html and encoded to utf-8 and then download button is created with all this data
                if len(splitted_dfs) > 0:
                    result_df = splitted_dfs[0]
                    for i in splitted_dfs[1:]:
                        result_df = result_df.concat(i)
                    html = result_df.to_html() # convert the DataFrame to HTML
                    data_to_download = html.encode("utf-8")# encode the HTML string to bytes

                    #the key is so as too keep key unique otherwise it will give error that no too widgets can have same key..as download button is in loop so it will be created agai  and again...
                    st.download_button(key=f"download_{time.time()}",label="Download HTML", data=data_to_download, file_name=f"{datetime.now(IST).strftime('%d-%m-%Y')}_{table_to_fetch}_{date_filter}.html")

                
                #creating the chart of the complete data of the symbol with the given expiry and set of strike prices....
                chart_place.plotly_chart(drawLineChart(st.session_state.connection, table_to_fetch, date_filter, strikes), use_container_width=True)
                #so as to refresh after every 2 mins
                time.sleep(120)




if 'loggedIn' in st.session_state:
    if st.session_state.loggedIn :
        if st.session_state.subscribed:
            optionChainDataPage()
        else:
            st.error("You are not subscribed or your subscription ended!")
    else:
        st.error("You are not Logged In!")
else:
    st.error("You are not Logged In!")