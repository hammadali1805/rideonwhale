import multiprocessing
import time
import sqlite3
import pandas as pd
import re
from datetime import datetime
from nsepython import nsefetch
import pytz


def call_api(symbol):
    connection = sqlite3.connect("database/optionChainData.db", check_same_thread=False)
    cursor = connection.cursor()

    if symbol in ["NIFTY", "FINNIFTY", "BANKNIFTY", "MIDCPNIFTY"]:
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
    else:
        url = f"https://www.nseindia.com/api/option-chain-equities?symbol={symbol}"
        symbol = re.sub(r'[^a-zA-Z0-9]', '_', symbol) #to avoid special characters in table names

    try:
        data = nsefetch(url)
        data = data['records']
        print(f'Data Fetched: {symbol}')
    except:
        return False
    

    underlyingValue = data['underlyingValue']
    symbol_underlyingValues = [value[0] for value in cursor.execute("SELECT symbol FROM initialUnderlyingValues;").fetchall()]

    if symbol not in symbol_underlyingValues:
        # Insert data into the table
        cursor.execute('''
        INSERT INTO initialUnderlyingValues (symbol, underlyingValue)
        VALUES (?, ?)
        ''', [symbol, underlyingValue])

        # Commit the changes and close the connection
        connection.commit()
        initialUnderlyingValue = underlyingValue
    else:
        # Execute a SELECT query to retrieve the underlyingValue for the given symbol
        cursor.execute("SELECT underlyingValue FROM initialUnderlyingValues WHERE symbol = ?;", (symbol,))

        # Check if the result is not None and return the underlyingValue
        initialUnderlyingValue = cursor.fetchone()[0]


            
    timestamp = data['timestamp'][-8:]

    relevant_data = data['data']
    extracted_data = []

    for i in relevant_data:
        record = [timestamp, underlyingValue, i['strikePrice']]
        try:
            record.append(i['CE']['changeinOpenInterest'])
        except:
            record.append(0)
        try:
            record.append(i['PE']['changeinOpenInterest'])
        except:
            record.append(0)
        record.append(i['expiryDate'])
        extracted_data.append(record)

    #create df from extracted records with the desired field names
    df = pd.DataFrame(extracted_data, columns = ['Time', 'underlyingValue', 'Strike_Price', 'COI_Calls', 'COI_Puts', 'Expiry_Date'])

    #convert the expiry date fro string to datetime format so as to sort according to the dates. 
    df['Expiry_Date'] = pd.to_datetime(df['Expiry_Date'], format='%d-%b-%Y')

    #sort the data frame first by expiry date and then by strike price
    df = df.sort_values(by=['Expiry_Date', 'Strike_Price'])


    #setting 20 above and below each strike prices of symbol if not set

    # Filter data based on underlyingValue (max 12 above and belo each)
    above_df = df[df['Strike_Price'] > initialUnderlyingValue].groupby('Expiry_Date').head(20)
    below_df = df[df['Strike_Price'] <= initialUnderlyingValue].groupby('Expiry_Date').tail(20)

    # Concatenate the results
    result_df = pd.concat([above_df, below_df], ignore_index=True)

    #sort the filter data 
    result_df = result_df.sort_values(by=['Expiry_Date', 'Strike_Price'])


    try:
        #this will throw error if symbol table  is not in db 
        query = f"SELECT * FROM {symbol};"

        # Use pandas read_sql_query to load the table into a DataFrame
        past_all_df = pd.read_sql_query(query, connection)

        past_all_df['Expiry_Date'] = pd.to_datetime(past_all_df['Expiry_Date'], format='%Y-%m-%d')

        #seprating only the data of last cycle as calc depend on last cycle
        prev_df=past_all_df.tail(len(result_df))

        #sorting the values as the the difrence of corresponding columns is to be calculated
        prev_df = prev_df.sort_values(by=['Expiry_Date', 'Strike_Price'])
        result_df = result_df.sort_values(by=['Expiry_Date', 'Strike_Price'])

        #resetting indexes from 0 as the difrence happens wrt to index
        prev_df.reset_index(drop=True, inplace=True)
        result_df.reset_index(drop=True, inplace=True)

        #performing calc
        result_df['C_Calls'] = result_df['COI_Calls'] - prev_df['COI_Calls']
        result_df['C_Puts'] = result_df['COI_Puts'] - prev_df['COI_Puts']
        result_df['C_Amt_Calls_Cr'] = (result_df['C_Calls']*132000)/10000000
        result_df['C_Amt_Puts_Cr'] = (result_df['C_Puts']*132000)/10000000

    except:
        result_df['C_Calls'] = 0
        result_df['C_Puts'] = 0
        result_df['C_Amt_Calls_Cr'] = 0.0
        result_df['C_Amt_Puts_Cr'] = 0.0


    #convert expiry date from datetime back to sting date to as to maintain a uniformity while reading and combining data from csv while later on.
    result_df['Expiry_Date'] = result_df['Expiry_Date'].dt.strftime('%Y-%m-%d')

    if timestamp < '09:17:00':
        #to delete data of previous day
        result_df.to_sql(name=symbol, con=connection, index=False, if_exists='replace')
    else:
        result_df.to_sql(name=symbol, con=connection, index=False, if_exists='append')

    cursor.close()
    connection.close()

    return True

        
def call_batch(symbols):
        results = []
        for symbol in symbols:
            results.append(call_api(symbol))
        return results


def market_status():
    data=nsefetch('https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY')
    data=data['records']
    timestamp = data['timestamp'][-8:]

    if timestamp[0:6] == '15:30':
        return False
    else:
        return True

        

if __name__ == "__main__":
    IST = pytz.timezone('Asia/Kolkata') 
    while True:
        if not ('09:18:00' <= datetime.now(IST).strftime("%H:%M:%S") <= '15:33:00'):
            continue
        else:
            if market_status():
                while ('09:18:00' <= datetime.now(IST).strftime("%H:%M:%S") <= '15:33:00'):
                            start = time.time()

                            connection = sqlite3.connect("database/optionChainData.db", check_same_thread=False)
                            cursor = connection.cursor()

                            cursor.execute('''
                            CREATE TABLE IF NOT EXISTS initialUnderlyingValues (
                                symbol TEXT,
                                underlyingValue REAL
                            )
                        ''')

                            connection.commit()
                            connection.close()

                            with open("backend/symbols.txt") as f:
                                data = f.readlines()

                            num_cores = multiprocessing.cpu_count()
                            symbols = [i.strip('\n') for i in data]
                            no_of_batches = 3*num_cores
                            avg_elements = len(symbols) // no_of_batches
                            remainder = len(symbols) % no_of_batches

                            symbol_batches = [symbols[i * avg_elements + min(i, remainder):(i + 1) * avg_elements + min(i + 1, remainder)] for i in range(no_of_batches)]       


                            # Use the number of CPU cores as the number of processes
                            with multiprocessing.Pool(processes=no_of_batches) as pool:
                                # Use the pool to map the worker function onto the tasks
                                results = pool.map(call_batch, symbol_batches)

                            flattened_list = [item for sublist in results for item in sublist]

                            print(f"\nPassed: {flattened_list.count(True)}\nFailed: {flattened_list.count(False)}")
                            end = time.time()

                            print(f'{end-start}\n')
                            time.sleep(120-(end-start))
            
            else:
                #to sleep on holiday for the hours in which market remains open
                time.sleep(25200)