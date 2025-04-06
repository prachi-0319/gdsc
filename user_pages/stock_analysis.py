import streamlit as st
import yfinance as yf
from prophet import Prophet
import pandas as pd
import plotly.graph_objects as go
import logging
import google.generativeai as genai
import os
import numpy as np
import pandas as pd
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import altair as alt


# # Configure logging for Prophet (optional, reduces verbose output)
logging.getLogger('cmdstanpy').setLevel(logging.WARNING)
logging.getLogger('prophet').setLevel(logging.WARNING)


st.markdown("""
<style>
    .profile-header h1 {
            color: #556b3b;
            font-size: 60px;
        }
</style>
""", unsafe_allow_html=True)

# Function to get common currency symbols (add more as needed)
def get_currency_symbol(currency_code):
    """Returns a common symbol for a given currency code."""
    symbols = {
        "USD": "$",
        "INR": "₹",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "CAD": "$", # Canadian Dollar
        "AUD": "$", # Australian Dollar
        # Add more currencies as needed
    }
    # Default to the code itself if symbol not found
    return symbols.get(currency_code, currency_code)


@st.cache_data(ttl=3600) # Cache exchange rate for 1 hour
def get_exchange_rate(from_currency, to_currency):
    """Fetches the exchange rate between two currencies."""
    if from_currency == to_currency:
        return 1.0
    try:
        ticker_symbol = f"{from_currency}{to_currency}=X"
        ticker = yf.Ticker(ticker_symbol)
        rate_data = ticker.history(period="1d")
        if not rate_data.empty:
            return rate_data['Close'].iloc[-1]
        else:
            # Fallback using info if history is empty
            info = ticker.info
            rate = info.get('regularMarketPreviousClose')
            if rate:
                return rate
            else:
                st.warning(f"Could not fetch {from_currency}/{to_currency} rate via history or info. Ticker: {ticker_symbol}")
                return None
    except Exception as e:
        st.warning(f"Could not fetch {from_currency}/{to_currency} exchange rate: {e}. Ticker: {ticker_symbol}")
        return None



# --- Data Fetching (Cached) ---
@st.cache_data # Cache the data fetching function
def fetch_stock_data(ticker, period="5y"):
    """
    Fetches historical stock data from Yahoo Finance and detects currency.
    Returns a tuple: (DataFrame, currency_code or None)
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)

        # --- Detect Currency ---
        currency = None
        try:
            info = stock.info
            currency = info.get('currency', None)
            if not currency:
                 st.warning(f"Could not automatically detect currency for {ticker} from ticker info. Assuming USD.")
                 currency = "USD" # Fallback assumption
        except Exception as info_e:
             st.warning(f"Could not fetch ticker info for {ticker} to detect currency: {info_e}. Assuming USD.")
             currency = "USD" # Fallback assumption


        if df.empty:
            st.error(f"Could not fetch historical data for ticker '{ticker}'. Please check the ticker symbol.")
            return None, currency # Return currency even if data is empty, might be useful

        df = df.reset_index()[["Date", "Close"]]
        df.columns = ["ds", "y"]

        # Ensure 'ds' is timezone-naive datetime objects
        if pd.api.types.is_datetime64_any_dtype(df['ds']) and df['ds'].dt.tz is not None:
             df['ds'] = df['ds'].dt.tz_localize(None)
        else:
             df['ds'] = pd.to_datetime(df['ds'])

        df['y'] = df['y'].astype(float)
        # Ensure ds is just date (remove time component if present)
        df['ds'] = df['ds'].dt.date
        df['ds'] = pd.to_datetime(df['ds']) # Convert back to datetime after stripping time

        # Prophet requires removing duplicate dates
        df = df.drop_duplicates(subset=['ds'], keep='last')
        return df.sort_values('ds'), currency # Return df and currency
    except Exception as e:
        st.error(f"An error occurred while fetching data for {ticker}: {e}")
        return None, None



# --- Prophet Model Training ---
def train_prophet(df, future_days):
    """Trains a Prophet model and generates a forecast."""
    if df is None or df.empty:
        st.error("Cannot train model: Input data is missing.")
        return None, None
    try:
        # Initialize Prophet
        model = Prophet(daily_seasonality=False, weekly_seasonality=True, yearly_seasonality=True)
        model.fit(df)
        future = model.make_future_dataframe(periods=future_days)
        forecast = model.predict(future)
        return model, forecast
    except Exception as e:
        st.error(f"An error occurred during model training or prediction: {e}")
        return None, None



# --- Plotting ---
def plot_forecast(df, forecast, ticker, currency_code):
    """Plots the actual data, forecast, and confidence intervals."""
    fig = go.Figure()
    display_currency_symbol = get_currency_symbol(currency_code) # Use code if symbol unknown

    # Actual Data
    fig.add_trace(go.Scatter(
        x=df['ds'].dt.date,
        y=df['y'],
        mode='lines',
        name='Actual Price',
        line=dict(color='dodgerblue', width=2)
    ))

    # Forecast Line
    fig.add_trace(go.Scatter(
        x=forecast['ds'].dt.date,
        y=forecast['yhat'],
        mode='lines',
        name='Forecast (yhat)',
        line=dict(color='darkorange', width=2)
    ))

    # Confidence Interval Area
    fig.add_trace(go.Scatter(
        x=forecast['ds'].dt.date,
        y=forecast['yhat_upper'],
        mode='lines', name='Upper Bound',
        line=dict(color='yellow', width=0),
        fill=None
    ))
    fig.add_trace(go.Scatter(
        x=forecast['ds'].dt.date,
        y=forecast['yhat_lower'],
        mode='lines', name='Lower Bound',
        line=dict(width=0),
        fill='tonexty',
        fillcolor='rgba(255, 235, 0, 0.2)'
    ))

    last_actual_date = df['ds'].iloc[-1].date()
    # Find the first forecast date strictly after the last actual date
    forecast_only_df = forecast[forecast['ds'].dt.date > last_actual_date]
    if not forecast_only_df.empty:
        forecast_start_date = forecast_only_df['ds'].iloc[0].date()
        forecast_days = len(forecast_only_df)
    else: # Handle edge case where future_days might be 0 or prediction failed partially
        forecast_start_date = last_actual_date
        forecast_days = 0

    fig.update_layout(
        title=f'{ticker} Stock Price Forecast ({forecast_days} Days) in {currency_code}',
        xaxis_title='Date',
        yaxis_title=f'Closing Price ({display_currency_symbol})', # Use symbol
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_rangeslider_visible=True,
         shapes=[dict(
            type='line',
            x0=forecast_start_date, y0=0,
            x1=forecast_start_date, y1=1, yref='paper',
            line=dict(color='grey', dash='dash')
        )],
        annotations=[dict(
            x=forecast_start_date, y=0.95, yref='paper',
            showarrow=False, xanchor='left', text='Forecast Start'
        )]
    )
    return fig



def plot_prophet_components(model, forecast):
    """Plots the components (trend, seasonality) of the Prophet forecast."""
    try:
        fig_components = model.plot_components(forecast)
        return fig_components
    except Exception as e:
        st.warning(f"Could not generate component plots: {e}")
        return None



# --- Streamlit App UI ---

st.markdown("""
<div class="profile-header">
    <h1 style="text-align:center;">📊 Forecast Insights & Components</h1>
    <p style="text-align:center;">Predict future stock prices using Prophet. Prices are shown in the stock's native currency unless converted.</p>
</div>
""", unsafe_allow_html=True)


st.markdown("")
st.markdown("")
st.markdown("")


col1, col2 = st.columns([1, 1], gap="large")


with col1:
    # st.markdown("### ⚙️ Inputs")

    base_ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, RELIANCE.NS, SIE.DE):", "AAPL").upper()
    exchange = st.selectbox(
        "The exhange",
        options=["NYSE (New York Stock Exchange)", "NSE (National Stock Exchange)", "BSE (Bombay Stock Exchange)", "FSE (Frankfurt Stock Exchange)"],
        index=0
    )
    period = st.selectbox(
        "Select Historical Data Period:",
        options=["1y", "2y", "5y", "10y", "max"],
        index=2
    )

with col2:
    future_days = st.slider("Select Forecast Duration (days):", 7, 730, 90)

    display_currency = st.selectbox(
        "Currency:",
        options=["USD", "INR", "EUR", "GBP"],
        index=0
    )

    st.markdown("")
    run_forecast = st.button("🔮 Run Forecast")


# MAPPING:

exchange_suffix_map = {
        "NSE (National Stock Exchange)": ".NS",
        "BSE (Bombay Stock Exchange)": ".BO",
        "NYSE (New York Stock Exchange)": "",
        "FSE (Frankfurt Stock Exchange)": ".DE",
    }
suffix = exchange_suffix_map[exchange]
ticker = base_ticker + suffix


st.markdown("")
st.markdown("")
st.markdown("")

# --- Main Area ---
if not ticker:
    st.warning("Please enter a stock ticker in the sidebar.")
else:
    # --- Data Loading and Processing ---
    with st.spinner(f"Fetching data for {ticker} ({period})..."):
        df_original, original_currency = fetch_stock_data(ticker, period)


    col1, col2, col3 = st.columns([1,0.1,5])

    with col1:
        if original_currency:
            # st.header("💰 Currency Options")
            # st.markdown("Choose Currency")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            
            st.info(f"Detected Currency: **{original_currency}**")
            target_currency_options = ["Original", "USD", "INR", "EUR", "GBP"] # Add more if needed
            # Remove original currency from target options if it's already there
            if original_currency in target_currency_options:
                target_currency_options.remove(original_currency)

            display_currency = st.selectbox(
                "Display Prices In:",
                options=[original_currency] + target_currency_options,
                index=0 # Default to original
            )
        else:
            display_currency = "USD" # Fallback if original currency detection failed
            st.sidebar.warning("Currency could not be detected. Assuming USD.")


    with col3:
        if df_original is not None and not df_original.empty:
            # --- Currency Conversion (if requested) ---
            conversion_rate = 1.0
            display_df = df_original.copy() # Start with original data
            current_display_currency_code = original_currency

            if display_currency != original_currency:
                with st.spinner(f"Fetching {original_currency} to {display_currency} exchange rate..."):
                    rate = get_exchange_rate(original_currency, display_currency)
                if rate:
                    conversion_rate = rate
                    display_df['y'] = display_df['y'] * conversion_rate
                    current_display_currency_code = display_currency
                    st.sidebar.success(f"Rate ({original_currency}/{display_currency}): {conversion_rate:.4f}")
                else:
                    st.sidebar.error(f"Could not get exchange rate. Displaying in original currency ({original_currency}).")
                    # Revert display currency choice if rate fails
                    display_currency = original_currency
                    # No need to change display_df, it's still the original copy


            st.header(f"Forecasting for {ticker}", divider='rainbow')
            # st.info(f"Displaying prices in: **{current_display_currency_code}**")
            st.info(f"Displaying prices in: **{display_currency}**")

            # --- Model Training and Prediction (Always use original data) ---
            with st.spinner(f"Training model & forecasting {future_days} days ahead (using {original_currency} data)..."):
                # Train on the ORIGINAL data before any conversion
                model, forecast_original = train_prophet(df_original.copy(), future_days)

            if model is not None and forecast_original is not None:
                # --- Apply Conversion to Forecast (if needed) ---
                display_forecast = forecast_original.copy()
                if display_currency != original_currency and conversion_rate != 1.0:
                    # Apply the fetched conversion rate to forecast columns
                    for col in ['yhat', 'yhat_lower', 'yhat_upper', 'trend', 'trend_lower', 'trend_upper']: # Convert trend too
                        if col in display_forecast.columns:
                            display_forecast[col] = display_forecast[col] * conversion_rate


                # --- Display Results ---
                # st.subheader("Forecast Plot")
                st.markdown("")
                fig_forecast = plot_forecast(display_df, display_forecast, ticker, current_display_currency_code)
                st.plotly_chart(fig_forecast, use_container_width=True)

            # --- Key Metrics ---
            st.subheader("Key Metrics")
            currency_symbol = get_currency_symbol(current_display_currency_code)

            last_actual_price = display_df['y'].iloc[-1]
            # Find the last row of the forecast (which corresponds to the latest future date)
            predicted_end_price = display_forecast['yhat'].iloc[-1]
            last_forecast_date = display_forecast['ds'].iloc[-1].strftime('%Y-%m-%d')
            last_actual_date_str = display_df['ds'].iloc[-1].strftime('%Y-%m-%d')


            price_change = predicted_end_price - last_actual_price
            percent_change = (price_change / last_actual_price) * 100 if last_actual_price else 0

            col1, col2, col3 = st.columns(3)
            col1.metric(
                label=f"Last Actual Close ({last_actual_date_str})",
                value=f"{currency_symbol}{last_actual_price:.2f}"
            )
            col2.metric(
                label=f"Predicted Close ({last_forecast_date})",
                value=f"{currency_symbol}{predicted_end_price:.2f}",
                delta=f"{price_change:.2f} ({percent_change:.2f}%)"
            )
            col3.metric(
                label="Forecast Duration (Days)",
                value=f"{future_days} days"
            )

            # --- Insights & Components (Collapsible) ---
            # st.write("### Key Insights:")
            # Trend analysis is best done on the original forecast before conversion scaling
            # Compare first forecast point after history vs last forecast point
            st.markdown("")
            first_forecast_idx = len(df_original) # Index of the first forecast point
            if first_forecast_idx < len(forecast_original):
                trend_start_val = forecast_original['yhat'].iloc[first_forecast_idx]
                trend_end_val = forecast_original['yhat'].iloc[-1]
                trend_direction = "an upward" if trend_end_val > trend_start_val else "a downward"
                st.write(f"- **Trend**: The model predicts {trend_direction} trend ({original_currency}) over the next {future_days} days.")
            else:
                st.write("- **Trend**: Could not determine trend (forecast length might be too short).")


            uncertainty = display_forecast['yhat_upper'].iloc[-1] - display_forecast['yhat_lower'].iloc[-1]
            st.write(f"- **Uncertainty**: The predicted price range widens over time, ending with a spread of approximately {currency_symbol}{uncertainty:.2f} ({current_display_currency_code}).")

        elif df_original is None and original_currency is None:
            # Error message already shown by fetch_stock_data or ticker was invalid
            st.error("Could not fetch data. Please ensure the ticker symbol is valid on Yahoo Finance.")
        else: # df is empty but no error was raised explicitly
            st.warning(f"No historical data found for ticker '{ticker}' for the selected period '{period}'. The ticker might be valid but lacks data for this timeframe.")

# --- Disclaimer ---
st.divider()
st.caption("Disclaimer: Stock price forecasting is inherently uncertain. This tool provides model-based predictions based on historical data and should not be considered financial advice. Currency conversions use recent exchange rates and may introduce slight inaccuracies. Always conduct your own research.")


# with col2:
#     st.markdown("### 🎯 Personalize Your Experience")

#     age = st.number_input(
#         "**Your Age**",
#         min_value=10,
#         max_value=100,
#         value=20,
#         step=1,
#         help="We'll adapt the content complexity based on your age"
#     )
#     st.markdown("")
    



# with st.expander("📊 Forecast Insights & Components"):

#   st.title("📈 Stock Forecasting Assistant")
#   st.caption("Predict future stock prices using Prophet. Prices are shown in the stock's native currency unless converted.")

#   left_col, right_col = st.columns([1, 3])  # 1:3 ratio (inputs narrower)

#   # --- LEFT COLUMN: Inputs ---
#   st.header("⚙️ Inputs")

#   base_ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, RELIANCE.NS, SIE.DE):", "AAPL").upper()
#   exchange = st.selectbox(
#       "The exhange",
#       options=["NYSE (New York Stock Exchange)", "NSE (National Stock Exchange)", "BSE (Bombay Stock Exchange)", "FSE (Frankfurt Stock Exchange)"],
#       index=0
#   )
#   period = st.selectbox(
#       "Select Historical Data Period:",
#       options=["1y", "2y", "5y", "10y", "max"],
#       index=2
#   )

#   future_days = st.slider("Select Forecast Duration (days):", 7, 730, 90)

#   display_currency = st.selectbox(
#       "Currency:",
#       options=["USD", "INR", "EUR", "GBP"],
#       index=0
#   )

#   run_forecast = st.button("🔮 Run Forecast")
    
#   # MAPPING:

#   exchange_suffix_map = {
#           "NSE (National Stock Exchange)": ".NS",
#           "BSE (Bombay Stock Exchange)": ".BO",
#           "NYSE (New York Stock Exchange)": "",
#           "FSE (Frankfurt Stock Exchange)": ".DE",
#       }
#   suffix = exchange_suffix_map[exchange]
#   ticker = base_ticker + suffix

#   # --- Main Area ---
#   if not ticker:
#       st.warning("Please enter a stock ticker in the sidebar.")
#   else:
#       # --- Data Loading and Processing ---
#       with st.spinner(f"Fetching data for {ticker} ({period})..."):
#           df_original, original_currency = fetch_stock_data(ticker, period)

#       if original_currency:
#           st.header("💰 Currency Options")
#           st.info(f"Detected Currency: **{original_currency}**")
#           target_currency_options = ["Original", "USD", "INR", "EUR", "GBP"] # Add more if needed
#           # Remove original currency from target options if it's already there
#           if original_currency in target_currency_options:
#               target_currency_options.remove(original_currency)

#           display_currency = st.selectbox(
#               "Display Prices In:",
#               options=[original_currency] + target_currency_options,
#               index=0 # Default to original
#           )
#       else:
#           display_currency = "USD" # Fallback if original currency detection failed
#           st.sidebar.warning("Currency could not be detected. Assuming USD.")


#       if df_original is not None and not df_original.empty:
#           # --- Currency Conversion (if requested) ---
#           conversion_rate = 1.0
#           display_df = df_original.copy() # Start with original data
#           current_display_currency_code = original_currency

#           if display_currency != original_currency:
#               with st.spinner(f"Fetching {original_currency} to {display_currency} exchange rate..."):
#                   rate = get_exchange_rate(original_currency, display_currency)
#               if rate:
#                   conversion_rate = rate
#                   display_df['y'] = display_df['y'] * conversion_rate
#                   current_display_currency_code = display_currency
#                   st.sidebar.success(f"Rate ({original_currency}/{display_currency}): {conversion_rate:.4f}")
#               else:
#                   st.sidebar.error(f"Could not get exchange rate. Displaying in original currency ({original_currency}).")
#                   # Revert display currency choice if rate fails
#                   display_currency = original_currency
#                   # No need to change display_df, it's still the original copy


#           st.header(f"Forecasting for {ticker}", divider='rainbow')
#           # st.info(f"Displaying prices in: **{current_display_currency_code}**")
#           st.info(f"Displaying prices in: **{display_currency}**")

#           # --- Model Training and Prediction (Always use original data) ---
#           with st.spinner(f"Training model & forecasting {future_days} days ahead (using {original_currency} data)..."):
#               # Train on the ORIGINAL data before any conversion
#               model, forecast_original = train_prophet(df_original.copy(), future_days)

#           if model is not None and forecast_original is not None:
#               # --- Apply Conversion to Forecast (if needed) ---
#               display_forecast = forecast_original.copy()
#               if display_currency != original_currency and conversion_rate != 1.0:
#                   # Apply the fetched conversion rate to forecast columns
#                   for col in ['yhat', 'yhat_lower', 'yhat_upper', 'trend', 'trend_lower', 'trend_upper']: # Convert trend too
#                       if col in display_forecast.columns:
#                           display_forecast[col] = display_forecast[col] * conversion_rate


#               # --- Display Results ---
#               st.subheader("Forecast Plot")
#               fig_forecast = plot_forecast(display_df, display_forecast, ticker, current_display_currency_code)
#               st.plotly_chart(fig_forecast, use_container_width=True)

#               # --- Key Metrics ---
#               st.subheader("Key Metrics")
#               currency_symbol = get_currency_symbol(current_display_currency_code)

#               last_actual_price = display_df['y'].iloc[-1]
#               # Find the last row of the forecast (which corresponds to the latest future date)
#               predicted_end_price = display_forecast['yhat'].iloc[-1]
#               last_forecast_date = display_forecast['ds'].iloc[-1].strftime('%Y-%m-%d')
#               last_actual_date_str = display_df['ds'].iloc[-1].strftime('%Y-%m-%d')


#               price_change = predicted_end_price - last_actual_price
#               percent_change = (price_change / last_actual_price) * 100 if last_actual_price else 0

#               col1, col2, col3 = st.columns(3)
#               col1.metric(
#                   label=f"Last Actual Close ({last_actual_date_str})",
#                   value=f"{currency_symbol}{last_actual_price:.2f}"
#               )
#               col2.metric(
#                   label=f"Predicted Close ({last_forecast_date})",
#                   value=f"{currency_symbol}{predicted_end_price:.2f}",
#                   delta=f"{price_change:.2f} ({percent_change:.2f}%)"
#               )
#               col3.metric(
#                   label="Forecast Duration (Days)",
#                   value=f"{future_days} days"
#               )

#               # --- Insights & Components (Collapsible) ---
#               # st.write("### Key Insights:")
#               # Trend analysis is best done on the original forecast before conversion scaling
#               # Compare first forecast point after history vs last forecast point
#               first_forecast_idx = len(df_original) # Index of the first forecast point
#               if first_forecast_idx < len(forecast_original):
#                   trend_start_val = forecast_original['yhat'].iloc[first_forecast_idx]
#                   trend_end_val = forecast_original['yhat'].iloc[-1]
#                   trend_direction = "an upward" if trend_end_val > trend_start_val else "a downward"
#                   st.write(f"- **Trend**: The model predicts {trend_direction} trend ({original_currency}) over the next {future_days} days.")
#               else:
#                   st.write("- **Trend**: Could not determine trend (forecast length might be too short).")


#               uncertainty = display_forecast['yhat_upper'].iloc[-1] - display_forecast['yhat_lower'].iloc[-1]
#               st.write(f"- **Uncertainty**: The predicted price range widens over time, ending with a spread of approximately {currency_symbol}{uncertainty:.2f} ({current_display_currency_code}).")

#       elif df_original is None and original_currency is None:
#           # Error message already shown by fetch_stock_data or ticker was invalid
#           st.error("Could not fetch data. Please ensure the ticker symbol is valid on Yahoo Finance.")
#       else: # df is empty but no error was raised explicitly
#           st.warning(f"No historical data found for ticker '{ticker}' for the selected period '{period}'. The ticker might be valid but lacks data for this timeframe.")

#   # --- Disclaimer ---
#   st.divider()
#   st.caption("Disclaimer: Stock price forecasting is inherently uncertain. This tool provides model-based predictions based on historical data and should not be considered financial advice. Currency conversions use recent exchange rates and may introduce slight inaccuracies. Always conduct your own research.")
