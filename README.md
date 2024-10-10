# RideOnWhale: Stock Market Analysis Platform

RideOnWhale is a comprehensive platform designed to track and analyze stock market trends using the NSE (National Stock Exchange) of India's option chain data. It provides real-time monitoring of changes in open interest (COI) for call and put options, allowing users to gain insights into market dynamics. The platform is built with Python for backend data handling and a Streamlit-based frontend for user interaction.

## Features

- **Real-time Option Chain Analysis**: Fetch and process NSE option chain data for indices like NIFTY, BANKNIFTY, FINNIFTY, and individual stocks.
- **Change in Open Interest (COI)**: Analyze the change in open interest for both call and put options across different strike prices.
- **Automated Data Updates**: Fetches updated option chain data at regular intervals during market hours (9:18 AM to 3:33 PM IST).
- **User Authentication**: Secure login system for users, including OTP verification and subscription options.
- **Market Holidays**: Automatically halts data fetching when the market is closed.
- **Backend Storage**: Uses SQLite for storing historical data and user credentials.

## Installation

### Prerequisites

- Python 3.7+
- SQLite

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/rideonwhale.git
   ```

3. **Run the Backend**:
   The backend script (`main.py`) continuously fetches option chain data during market hours.
   ```bash
   python Backend/main.py
   ```

4. **Run the Streamlit App**:
   The frontend app is built using Streamlit for a user-friendly interface.
   ```bash
   streamlit run Frontend/Home.py
   ```

## Usage

### Backend (main.py)

- The backend fetches option chain data for the stock symbols listed in the `symbols.txt` file.
- Data is fetched every 2 minutes during market hours and stored in an SQLite database for further analysis.
- The backend calculates the difference in open interest for both calls and puts, allowing users to identify key market trends.

### Frontend (Home.py)

- A login page ensures only authorized users can access the application.
- Users can subscribe to notifications and receive updates about stock movements.
- The platform provides visualizations and tabular data for the option chain, helping users analyze the market.

## Technologies Used

- **Python**: Backend logic and data processing.
- **Streamlit**: Frontend web interface.
- **SQLite**: Database to store user credentials and stock data.
- **NSEPython**: API integration for fetching NSE option chain data.
- **Pandas**: Data manipulation and analysis.
- **Multiprocessing**: To speed up data fetching for multiple stock symbols.
- **SMTP**: For sending email OTPs for user authentication.

## Contributing

We welcome contributions from the community. Feel free to fork the project, create a branch, and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

## Contact

For any questions or suggestions, please reach out to us at [hammadalipbt18@gmail.com].
