import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import requests

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.colors as pc

@st.cache_data
def fetch_info(ticker):
    ticker = yf.Ticker(ticker)
    info = ticker.info
    if "quoteType" in ticker.info:
        return info
    else:
        return None
        #st.warning("Invalid ticker")
        #st.stop()

@st.cache_data
def fetch_history(ticker, period="3mo", interval="1d", start=None):
    ticker = yf.Ticker(ticker)
    if start:
        hist = ticker.history(
            start=start,
            interval=interval
        )
    else:
        hist = ticker.history(
            period=period,
            interval=interval
        )

    return hist

@st.cache_data
def fetch_balance(ticker, tp="Annual"):
    ticker = yf.Ticker(ticker)
    if tp == "Annual":
        bs = ticker.balance_sheet
    else:
        bs = ticker.quarterly_balance_sheet
    return bs.loc[:, bs.isna().mean() < 0.5]

@st.cache_data
def fetch_income(ticker, tp="Annual"):
    ticker = yf.Ticker(ticker)
    if tp == "Annual":
        ins = ticker.income_stmt
    else:
        ins = ticker.quarterly_income_stmt
    return ins.loc[:, ins.isna().mean() < 0.5]

@st.cache_data
def fetch_cash(ticker, tp="Annual"):
    ticker = yf.Ticker(ticker)
    if tp == "Annual":
        cf = ticker.cashflow
    else:
        cf = ticker.quarterly_cashflow
    return cf.loc[:, cf.isna().mean() < 0.5]

@st.cache_data
def fetch_splits(ticker):
    ticker = yf.Ticker(ticker)
    return ticker.splits

@st.cache_data
def fetch_table(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(url, headers=headers)
        df = pd.read_html(response.content)
        return df[0]
    except:
        return None

def format_value(value):
    # Split the string at the first space
    base_value, change = value.split(' ', 1)

    # Determine the color based on the sign of the change
    if change.startswith('+'):
        color = 'green'
    else:
        color = 'red'

    # Create the formatted string
    return f"{base_value}<br><span style='color: {color};'>{change}</span>"

def remove_duplicates(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result

def top_table(df):
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='lightgrey',
                    align='center'),
        cells=dict(values=[df[col] for col in df.columns],
                   fill_color='white',
                   align=['left', 'right']),
        columnwidth=[0.6, 0.4]
    )])

    fig.update_layout(height=270, margin=dict(t=0, b=0, l=0, r=0))

    return fig


def info_table(info):
    data = {}

    TYPE = info['quoteType']

    if TYPE == "EQUITY":

        data['Name'] = info.get('shortName', "")
        data['Country'] = info.get('country', "")
        data['Market Exchange'] = info.get('exchange', "")
        data['Sector'] = info.get('sector', "")
        data['Industry'] = info.get('industry', "")
        data['Market Capitalization'] = str(info.get('marketCap', ""))
        data['Quote currency'] = info.get('currency', "")
        data['Beta'] = str(info.get('beta', ""))
        data['Price'] = info.get('currentPrice', 0)

    elif TYPE == "ETF":

        data['Market Exchange'] = info.get('exchange', "")
        data['Fund Family'] = info.get('fundFamily', "")
        data['Category'] = info.get('category', "")
        data['Total Assets'] = info.get('totalAssets', "")
        data['Quote currency'] = info.get('currency', "")
        data['Beta'] = info.get('beta3Year', "")
        data['Price'] = info.get('navPrice', 0)

    elif TYPE == "FUTURE":
        pass

    elif TYPE == "MUTUALFUND":
        pass

    elif TYPE == "CURRENCY":
        pass

    df = pd.DataFrame([data]).T

    return df


def plot_gauge(df, ticker):
    df = df[df['Ticker'] == ticker]

    initial_price = df['Close'].iloc[0]
    last_price = df['Close'].iloc[-1]
    last_pct = df['Pct_change'].iloc[-1] * 100
    color_pct = 'green' if last_pct > 0 else 'red'

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=last_pct,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': ticker},
        number={'font': {'color': color_pct}},
        gauge={
            'axis': {'range': [-50, 50]},
            'bar': {'thickness': 0},
            'steps': [
                {'range': [0, last_pct], 'color': color_pct, 'thickness': 0.8},
            ],
        },
    ))

    fig.update_layout(height=150, margin=dict(t=50, b=0, l=0, r=0))

    return fig

def plot_candles_stick_bar(df, title=""):

    rows = 1
    row_heights = [7]
    for col_name in df.columns:
        if col_name in ['Volume', 'MACD', 'ATR', 'RSI']:
            rows += 1
            row_heights.append(3)

    fig = make_subplots(rows=rows, cols=1, shared_xaxes=True,
                        vertical_spacing=0.01,
                        subplot_titles=None,
                        row_heights=row_heights
                        )

    fig.update_xaxes(title_text="Date", row=rows, col=1)

    row = 1
    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df['Open'],
                                 high=df['High'],
                                 low=df['Low'],
                                 close=df['Close'],
                                 name="OHVC"
                                 ),
                  row=1, col=1)

    for col_name in df.columns:

        if 'SMA' in col_name or 'EMA' in col_name:
            fig.add_trace(go.Scatter(x=df.index,
                                     y=df[col_name],
                                     mode='lines',
                                     line=dict(
                                         #color='black',
                                         width=2
                                     ),
                                     name=col_name),
                          row=1, col=1)

        elif 'Crossover' in col_name:

            first_period = col_name.split('_')[1].split('/')[0]

            for i, v in df[col_name].items():

                if v == 1.0:  # Buy signal

                    fig.add_annotation(x=df.index[i], y=df[f'SMA_{first_period}'][i],
                                       text="Golden cross",
                                       showarrow=True,
                                       arrowhead=1,
                                       arrowsize=1,
                                       ay=60
                                       )

                if v == -1.0:  # Sell signal

                    fig.add_annotation(x=df.index[i], y=df[f'SMA_{first_period}'][i],
                                       text="Death cross",
                                       showarrow=True,
                                       arrowhead=1,
                                       arrowsize=1,
                                       ay=-60
                                       )

        if col_name == 'Volume':
            row += 1

            volume_colors = ['green' if df['Close'].iloc[i] > df['Open'].iloc[i] else 'red' for i in range(len(df))]

            fig.add_trace(go.Bar(x=df.index,
                                 y=df[col_name],
                                 name=col_name,
                                 marker_color=volume_colors),
                          row=row, col=1)

            fig.update_yaxes(title_text="Volume", row=row, col=1)

        elif col_name == 'MACD':
            row += 1

            fig.add_trace(go.Scatter(x=df.index,
                                     y=df[col_name],
                                     name=col_name,
                                     ),
                          row=row, col=1)

            fig.update_yaxes(title_text="MACD", row=row, col=1)

            if 'Signal' in df.columns:
                fig.add_trace(go.Scatter(x=df.index,
                                         y=df['Signal'],
                                         name='Signal',
                                         ),
                              row=row, col=1)

            if 'MACD_Hist' in df.columns:
                MACD_colors = ['green' if df['MACD_Hist'][i] > 0 else 'red' for i in range(len(df))]

                fig.add_trace(go.Bar(x=df.index,
                                     y=df['MACD_Hist'],
                                     name='MACD_Hist',
                                     marker_color=MACD_colors),
                              row=row, col=1)

        elif col_name == 'ATR':
            row += 1

            fig.add_trace(go.Scatter(x=df.index,
                                     y=df[col_name],
                                     name=col_name,
                                     ),
                          row=row, col=1)

            fig.update_yaxes(title_text="ATR", row=row, col=1)

        elif col_name == 'RSI':
            row += 1

            fig.add_trace(go.Scatter(x=df.index,
                                     y=df[col_name],
                                     name=col_name,
                                     ),
                          row=row, col=1)

            fig.update_yaxes(title_text="RSI", row=row, col=1)

            fig.add_hline(y=70, line_dash="dash", annotation_text='top', row=row, col=1)
            fig.add_hline(y=30, line_dash="dash", annotation_text='bottom', row=row, col=1)
            fig.add_hrect(y0=30, y1=70, fillcolor="blue", opacity=0.25, line_width=0, row=row, col=1)

    fig.update_layout(
        title=title,
        # xaxis_title='Date',
        yaxis_title='Price',
        # xaxis2_title='Date',
        # yaxis2_title='Volume',
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="top",  # Aligns the legend vertically to the top
            y=-0.15,  # Positions the legend below the subplots
            xanchor="center",  # Aligns the legend horizontally to the center
            x=0.5  # Centers the legend horizontally
        ),
        showlegend=True,
        xaxis_rangeslider_visible=False,
        height=800
    )

    return fig


def plot_candles_stick(df, title="", time_span=None):

    fig = go.Figure()


    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df['Open'],
                                 high=df['High'],
                                 low=df['Low'],
                                 close=df['Close'],
                                 name="OHVC")
                  )

    if 'SMA' in df.columns:
        fig.add_trace(go.Scatter(x=df.index,
                                 y=df['SMA'],
                                 mode='lines',
                                 line=dict(color='black', width=2),
                                 name=f'{time_span}SMA')
                      )
    if 'EMA' in df.columns:
        fig.add_trace(go.Scatter(x=df.index,
                                 y=df['EMA'],
                                 mode='lines',
                                 line=dict(color='blue', width=2),
                                 name=f'{time_span}EMA')
                      )

    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Price',
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="top",  # Aligns the legend vertically to the top
            y=-0.3,  # Positions the legend below the subplots
            xanchor="center",  # Aligns the legend horizontally to the center
            x=0.5  # Centers the legend horizontally
        ),
        showlegend=True,
        xaxis_rangeslider_visible=False,
    )

    return fig

def plot_line_multiple(df, title=""):
    fig = go.Figure()

    dfs = df.groupby('Ticker')

    for df_name, df in dfs:
        fig.add_trace(go.Scatter(x=df.index,
                                 y=df['Pct_change'],
                                 mode='lines',
                                 name=f'{df_name}',
                                 meta=df_name,
                                 hovertemplate='%{meta}: %{y:.2f}<br><extra></extra>', )
                      )

    fig.add_hline(y=0, line_dash="dash")

    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Percentage change',
        hovermode='x',
        xaxis=dict(
            showspikes=True,  # Enable vertical spikes
            spikemode='across',  # Draw spikes across the entire plot
            spikesnap='cursor',  # Snap spikes to the cursor position
            showline=True,  # Show axis line
            showgrid=True,  # Show grid lines
            spikecolor='black',  # Custom color for spikes
            spikethickness=1,  # Custom thickness for spikes
            rangeslider=dict(
                visible=True,
                thickness=0.1
            ),
        ),
        yaxis=dict(
            tickformat='.0%',
            showspikes=True,  # Enable horizontal spikes
            spikemode='across',  # Draw spikes across the entire plot
            spikesnap='cursor',  # Snap spikes to the cursor position
            showline=True,  # Show axis line
            showgrid=True,  # Show grid lines
            spikecolor='black',  # Custom color for spikes
            spikethickness=1,  # Custom thickness for spikes
            side='right'  # Move the y-axis ticks to the right side
        ),
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="top",  # Aligns the legend vertically to the top
            y=-0.3,  # Positions the legend below the subplots
            xanchor="center",  # Aligns the legend horizontally to the center
            x=0.5  # Centers the legend horizontally
        ),
        showlegend=True,
        # xaxis_rangeslider_visible=True,
        height=800
    )

    return fig

def plot_balance(df, ticker="", currency=""):
    df.columns = pd.to_datetime(df.columns).strftime('%b %d, %Y')

    components = {
        'Total Assets': {
            'color': 'forestgreen',
            'name': 'Assets',
        },
        'Stockholders Equity': {
            'color': 'CornflowerBlue',  # http://davidbau.com/colors/
            'name': "Stockholder's Equity",
        },
        'Total Liabilities Net Minority Interest': {
            'color': 'tomato',
            'name': "Total Liabilities",
        },
    }
    fig = go.Figure()

    for component in components:
        if component == 'Total Assets':
            fig.add_trace(go.Bar(
                x=[df.columns, ['Assets'] * len(df.columns)],
                y=df.loc[component],
                name=components[component]['name'],
                marker=dict(color=components[component]['color'])
            ))
        else:

            fig.add_trace(go.Bar(
                x=[df.columns, ['L+E'] * len(df.columns)],
                y=df.loc[component],
                name=components[component]['name'],
                marker=dict(color=components[component]['color'])
            ))

    offset = 0.03 * df.loc['Total Assets'].max()

    for i, date in enumerate(df.columns):
        fig.add_annotation(
            x=[date, "Assets"],
            y=df.loc['Total Assets', date]/2,
            text=str(round(df.loc['Total Assets', date] / 1e9, 1)) + 'B',  # Format as text
            showarrow=False,
            font=dict(size=12, color="black"),
            align="center"
        )
        percentage = round((df.loc['Total Liabilities Net Minority Interest', date] / df.loc['Total Assets', date]) * 100, 1)
        fig.add_annotation(
            x=[date, "L+E"],
            y=df.loc['Stockholders Equity', date] + df.loc['Total Liabilities Net Minority Interest', date] / 2,
            text=str(percentage) + '%',  # Format as text
            showarrow=False,
            font=dict(size=12, color="black"),
            align="center"
        )
        if i > 0:
            percentage = round((df.loc['Total Assets'].iloc[i] / df.loc['Total Assets'].iloc[i - 1] - 1) * 100, 1)
            sign = '+' if percentage >= 0 else ''
            fig.add_annotation(
                x=[date, "Assets"],
                y=df.loc['Total Assets', date] + offset,
                text=sign + str(percentage) + '%',  # Format as text
                showarrow=False,
                font=dict(size=12, color="black"),
                align="center"
            )

    fig.update_layout(
        barmode='stack',
        title=f'Accounting Balance: {ticker}',
        xaxis_title='Year',
        yaxis_title=f'Amount (in {currency})',
        legend_title='Balance components',
    )

    return fig

def plot_assets(df, ticker="", currency=""):
    assests = {
        'Current Assets': {
            'Cash Cash Equivalents And Short Term Investments': {},
            'Receivables': {},
            'Prepaid Assets': None,
            'Inventory': {},
            'Hedging Assets Current': None,
            'Other Current Assets': None
        },
        'Total Non Current Assets': {
            'Net PPE': {},
            'Goodwill And Other Intangible Assets': {},
            'Investments And Advances': {},
            'Investment Properties': None,
            'Other Non Current Assets': None
        }
    }

    fig = make_subplots(
        rows=1, cols=2,
        shared_yaxes=True,  # Share x-axis for both subplots
        horizontal_spacing=0.05,  # Adjust the space between the subplots
        subplot_titles=['Current Assets', 'Non-Current Assets']  # Titles for the subplots
    )

    colors = pc.sequential.Blugrn[::-1]
    i = 0

    for component in assests['Current Assets']:
        if component in df.index:
            fig.add_trace(go.Bar(
                x=df.columns,
                y=df.loc[component],
                name=component,
                marker=dict(
                    color=colors[i]  # Assign a color from the green color scale
                ),
                legendgroup='Current Assets',
                showlegend=True
            ), row=1, col=1)
            i += 1

    colors = pc.sequential.Purp[::-1]
    i = 0

    for component in assests['Total Non Current Assets']:
        if component in df.index:
            fig.add_trace(go.Bar(
                x=df.columns,
                y=df.loc[component],
                name=component,
                marker=dict(
                    color=colors[i]  # Assign a color from the green color scale
                ),
                legendgroup='Non-current Assets',
                showlegend=True
            ), row=1, col=2)
            i += 1

    offset = 0.03 * max(df.loc['Current Assets'].max(), df.loc['Total Non Current Assets'].max())

    for i, date in enumerate(df.columns):
        fig.add_annotation(
            x=date,
            y=df.loc['Current Assets', date] + offset,
            text=str(round(df.loc['Current Assets', date] / 1e9, 1)) + 'B',  # Format as text
            showarrow=False,
            font=dict(size=12, color="black"),
            align="center",
            row=1, col=1
        )
        fig.add_annotation(
            x=date,
            y=df.loc['Total Non Current Assets', date] + offset,
            text=str(round(df.loc['Total Non Current Assets', date] / 1e9, 1)) + 'B',  # Format as text
            showarrow=False,
            font=dict(size=12, color="black"),
            align="center",
            row=1, col=2
        )

    # Update layout to stack bars and set titles
    fig.update_layout(
        barmode='stack',
        title=f'Assets: {ticker}',
        #xaxis1_title='Year',
        #xaxis2_title='Year',
        xaxis1=dict(
            title='Date',
            type='date',  # Ensure the x-axis is treated as a date/time axis
            tickvals=df.columns
        ),
        xaxis2=dict(
            title='Date',
            type='date',  # Ensure the x-axis is treated as a date/time axis
            tickvals=df.columns
        ),
        yaxis_title=f'Amount (in {currency})',
        # yaxis2_title=f'Amount (in {currency})',
        legend_title='Asset Components',
        # height=800
    )

    return fig

def plot_liabilities(df, ticker="", currency=""):
    liabilities = {
        'Current Liabilities': {
            'Payables And Accrued Expenses': {},
            'Pensionand Other Post Retirement Benefit Plans Current': None,
            'Current Debt And Capital Lease Obligation': {},
            'Current Deferred Liabilities': {},
            'Other Current Liabilities': {}
        },
        'Total Non Current Liabilities Net Minority Interest': {
            'Long Term Debt And Capital Lease Obligation': {},
            'Non Current Deferred Liabilities': {},
            'Tradeand Other Payables Non Current': None,
            'Other Non Current Liabilities': None
        }
    }

    fig = make_subplots(
        rows=1, cols=2,
        shared_yaxes=True,  # Share x-axis for both subplots
        horizontal_spacing=0.05,  # Adjust the space between the subplots
        subplot_titles=['Current Liabilities', 'Non-Current Liabilities']  # Titles for the subplots
    )

    colors = pc.sequential.Oryel[::-1]
    i = 0

    for component in liabilities['Current Liabilities']:
        if component in df.index:
            fig.add_trace(go.Bar(
                x=df.columns,
                y=df.loc[component],
                name=component,
                marker=dict(
                    color=colors[i]  # Assign a color from the green color scale
                ),
                legendgroup='Current Liabilities',
                showlegend=True
            ), row=1, col=1)
            i += 1

    colors = pc.sequential.Brwnyl[::-1]
    i = 0

    for component in liabilities['Total Non Current Liabilities Net Minority Interest']:
        if component in df.index:
            fig.add_trace(go.Bar(
                x=df.columns,
                y=df.loc[component],
                name=component,
                marker=dict(
                    color=colors[i]  # Assign a color from the green color scale
                ),
                legendgroup='Non-current Liabilities',
                showlegend=True
            ), row=1, col=2)
            i += 1

    offset = 0.03 * max(df.loc['Current Liabilities'].max(),
                        df.loc['Total Non Current Liabilities Net Minority Interest'].max())

    for i, date in enumerate(df.columns):
        fig.add_annotation(
            x=date,
            y=df.loc['Current Liabilities', date] + offset,
            text=str(round(df.loc['Current Liabilities', date] / 1e9, 1)) + 'B',  # Format as text
            showarrow=False,
            font=dict(size=12, color="black"),
            align="center",
            row=1, col=1
        )
        fig.add_annotation(
            x=date,
            y=df.loc['Total Non Current Liabilities Net Minority Interest', date] + offset,
            text=str(round(df.loc['Total Non Current Liabilities Net Minority Interest', date] / 1e9, 1)) + 'B',
            # Format as text
            showarrow=False,
            font=dict(size=12, color="black"),
            align="center",
            row=1, col=2
        )

    # Update layout to stack bars and set titles
    fig.update_layout(
        barmode='stack',
        title=f'Liabilities: {ticker}',
        #xaxis1_title='Year',
        #xaxis2_title='Year',
        xaxis1=dict(
            title='Date',
            type='date',  # Ensure the x-axis is treated as a date/time axis
            tickvals=df.columns
        ),
        xaxis2=dict(
            title='Date',
            type='date',  # Ensure the x-axis is treated as a date/time axis
            tickvals=df.columns
        ),
        yaxis_title=f'Amount (in {currency})',
        # yaxis2_title=f'Amount (in {currency})',
        legend_title='Liability Components',
        # height=800
    )

    return fig

def plot_equity(df, ticker="", currency=""):
    equity = {
        'Stockholders Equity': {
            'Capital Stock': {},
            'Retained Earnings': None,
            'Gains Losses Not Affecting Retained Earnings': {},
        },
    }

    fig = go.Figure()

    colors = pc.sequential.Blues[::-1]
    i = 0

    for component in equity['Stockholders Equity']:
        if component in df.index:
            fig.add_trace(go.Bar(
                x=df.columns,
                y=df.loc[component],
                name=component,
                marker=dict(
                    color=colors[i]  # Assign a color from the green color scale
                ),
            ))
            i += 2

    offset = 0.05 * df.loc['Stockholders Equity'].max()

    for i, date in enumerate(df.columns):
        fig.add_annotation(
            x=date,
            y=df.loc['Stockholders Equity', date] + offset,
            text=str(round(df.loc['Stockholders Equity', date] / 1e9, 1)) + 'B',  # Format as text
            showarrow=False,
            font=dict(size=12, color="black"),
            align="center"
        )

    # Update layout to stack bars and set titles
    fig.update_layout(
        barmode='relative',
        title=f'Equity: {ticker}',
        # xaxis_title='Year',
        xaxis=dict(
            title='Date',
            type='date',  # Ensure the x-axis is treated as a date/time axis
            # tickformat='%Y',
            # dtick='M12'
            tickvals=df.columns
        ),
        yaxis_title=f'Amount (in {currency})',
        legend_title='Equity Components',
    )

    return fig

def plot_income(df, ticker="", currency=""):
    income_st = {
        'Total Revenue': {
            'name': 'Total Revenue',
            'sign': '+',
            'base': None,
            'color': 'rgb(0,68,27)'
        },
        'Cost Of Revenue': {
            'name': 'Cost of Revenue',
            'sign': '-',
            'base': ['Total Revenue'],
            'color': 'rgb(165,15,21)'
        },
        'Gross Profit': {
            'name': 'Gross Profit',
            'sign': '+',
            'base': None,
            'color': 'rgb(35,139,69)'
        },
        'Operating Expense': {
            'name': 'Operating Expense',
            'sign': '-',
            'base': ['Gross Profit'],
            'color': 'rgb(239,59,44)'
        },
        'Operating Income': {
            'name': 'Operating Income',
            'sign': '+',
            'base': None,
            'color': 'rgb(116,196,118)'
        },
        'Net Non Operating Interest Income Expense': {
            'name': 'Net Non Operating I/E',
            'sign': '+',
            'base': ['Operating Income'],
            'color': 'rgb(130, 109, 186)'
        },
        'Other Income Expense': {
            'name': 'Other Income Expense',
            'sign': '+',
            'base': ['Operating Income', 'Net Non Operating Interest Income Expense'],
            'color': 'rgb(185, 152, 221)'
        },
        'Pretax Income': {
            'name': 'Pretax Income',
            'sign': '+',
            'base': None,
            'color': 'rgb(199,233,192)'
        },
        'Tax Provision': {
            'name': 'Tax Provision',
            'sign': '-',
            'base': ['Pretax Income'],
            'color': 'rgb(252,146,114)'
        },
        'Net Income Common Stockholders': {
            'name': 'Net Income',
            'sign': '+',
            'base': None,
            'color': 'rgb(224, 253, 74)'
        }
    }

    # Create traces for stacked data
    traces = list()

    for component in income_st:
        if component in df.index:

            sign = income_st[component]['sign']
            value = df.loc[component] if sign == '+' else -df.loc[component]

            base = income_st[component]['base']
            if base:
                base = 0
                for _ in income_st[component]['base']:
                    base += df.loc[_]

            if component == "Total Revenue" or component == "Net Income Common Stockholders":
                percentages = round(df.loc[component].astype('float64').pct_change(periods=-1) * 100, 1)
                percentages = percentages.apply(
                    lambda x: f"+{x}%" if x > 0 else ("" if pd.isna(x) else f"{x}%")).tolist()
                trace = go.Bar(
                    x=df.columns,
                    y=value,
                    name=income_st[component]['name'],
                    base=base,
                    marker=dict(
                        color=income_st[component]['color']  # Assign a color from the green color scale
                    ),
                    text=percentages,
                    textfont=dict(size=12, color='black', family='Arial', weight='bold'),
                    textposition='outside',
                )
            else:
                trace = go.Bar(
                    x=df.columns,
                    y=value,
                    name=income_st[component]['name'],
                    base=base,
                    marker=dict(
                        color=income_st[component]['color']  # Assign a color from the green color scale
                    )
                )

            traces.append(trace)

    # Create the figure
    fig = go.Figure(data=traces)

    # Update layout to stack bars and set titles
    fig.update_layout(
        barmode='group',
        # barmode = 'overlay',
        title=f'Income Statement: {ticker}',
        # xaxis_title='Year',
        xaxis=dict(
            title='Date',
            type='date',  # Ensure the x-axis is treated as a date/time axis
            tickvals=df.columns
        ),
        yaxis_title=f'Amount (in {currency})',
        legend_title='I/E segregation',
    )

    return fig

def plot_cash(df, ticker="", currency=""):
    cashflow = {
        'Operating Cash Flow': {},
        'Investing Cash Flow': {},
        'Financing Cash Flow': {},
        'End Cash Position': {
            'Changes In Cash': None,
            'Effect Of Exchange Rate Changes': None,
            'Beginning Cash Position': None
        }
    }

    fig = go.Figure()

    colors = pc.sequential.Plotly3[::-1]
    i = 0

    for component in cashflow:
        if component in df.index:
            if component == 'End Cash Position':
                for item in cashflow[component]:
                    if item in df.index:
                        if item == 'Changes In Cash':
                            fig.add_trace(go.Scatter(
                                x=df.columns,
                                y=df.loc[item],
                                mode='lines',
                                line=dict(color='black', width=2, dash='dash'),
                                name=item,
                            ))
                        else:
                            fig.add_trace(go.Bar(
                                x=df.columns,
                                y=df.loc[item],
                                name=item,
                                marker=dict(
                                    color=colors[i]  # Assign a color from the green color scale
                                ),
                            ))
                            i += 2
                fig.add_trace(go.Scatter(
                    x=df.columns,
                    y=df.loc[component],
                    mode='lines+markers',
                    line=dict(color='black', width=3),
                    name=component,
                ))
            else:
                fig.add_trace(go.Bar(
                    x=df.columns,
                    y=df.loc[component],
                    name=component,
                    marker=dict(
                        color=colors[i]  # Assign a color from the green color scale
                    ),
                ))
                i += 2

    offset = 0.08 * (df.loc['Operating Cash Flow']+df.loc['Beginning Cash Position']).max()

    for i, date in enumerate(df.columns):
        fig.add_annotation(
            x=date,
            y=df.loc['End Cash Position', date] + offset,
            text=str(round(df.loc['End Cash Position', date] / 1e9, 1)) + 'B',  # Format as text
            showarrow=False,
            font=dict(size=12, color="black"),
            align="center"
        )

    # Update layout to stack bars and set titles
    fig.update_layout(
        barmode='relative',
        title=f'Cash flow: {ticker}',
        # xaxis_title='Year',
        xaxis=dict(
            title='Date',
            type='date',  # Ensure the x-axis is treated as a date/time axis
            tickvals=df.columns
        ),
        yaxis_title=f'Amount (in {currency})',
        legend_title='Cash Flow Components',
    )

    return fig

# PERFORMANCES
def format_number(val):
    if isinstance(val, float):
        if val >= 0:
            return f"<br><span style='color: green;'>+{val:.2f}%"  # Positive values with a plus sign
        else:
            return f"<br><span style='color: red;'>{val:.2f}%"  # Negative values without a sign
    else:
        return f"<b>{val}</b>"

def performance_table(df, tickers):
    perform = {}

    for ticker in tickers:
        df_t = df[df['Ticker'] == ticker]
        LEN = len(df_t)
        Pct_change_1P = (df_t['Close'].iloc[-1] - df_t['Close'].iloc[0]) / df_t['Close'].iloc[0]
        Pct_change_12P = (df_t['Close'].iloc[-1] - df_t['Close'].iloc[int(LEN / 2)]) / df_t['Close'].iloc[int(LEN / 2)]
        Pct_change_14P = (df_t['Close'].iloc[-1] - df_t['Close'].iloc[int(LEN / 4)]) / df_t['Close'].iloc[int(LEN / 4)]
        Pct_change_last = (df_t['Close'].iloc[-1] - df_t['Close'].iloc[-2]) / df_t['Close'].iloc[-2]

        perform[ticker] = {
            'Last value': Pct_change_last * 100,
            '1/4 Period': Pct_change_14P * 100,
            '1/2 Period': Pct_change_12P * 100,
            '1 Period': Pct_change_1P * 100,
        }

    df_perform = pd.DataFrame(perform).rename_axis("Period").reset_index()

    header = df_perform.columns.tolist()
    # header.insert(0, 'Period')
    values = [df_perform[col] for col in df_perform.columns]
    # values.insert(0, [1, int(LEN / 4), int(LEN / 2), LEN])

    formatted_values = [[format_number(val) for val in row] for row in values]

    # Create the Plotly Table
    fig = go.Figure(data=[go.Table(
        header=dict(values=header,
                    #fill_color='paleturquoise',
                    align='center',
                    font=dict(size=18, weight='bold')
                    ),
        cells=dict(values=formatted_values,
                   align='center',
                   font=dict(size=16),
                   )
    )])

    fig.update_layout(
        title='Price Performance',  # Add your title here
        #title_x=0.5,  # Centers the title horizontally
        title_font=dict(size=20, family='Arial'),  # Customize the title font
        height=250,
        margin=dict(t=70, b=0, l=0, r=0)
    )
    fig.update_layout()

    return fig

def plot_capital(df, ticker="", currency=""):

    try:
        total_debt = df.loc['Total Debt']
    except:
        df.loc['Total Debt'] = df.loc['Total Liabilities Net Minority Interest']

    df1 = pd.concat([df.loc['Ordinary Shares Number'], df.loc['Cash Cash Equivalents And Short Term Investments'],
                     df.loc['Total Debt']], axis=1)

    df1 = df1.iloc[::-1].dropna()

    dates = df1.index
    start = dates[0]

    hist = fetch_history(
        ticker=ticker,
        interval='1d',
        start=start - datetime.timedelta(days=5)
    )
    df2 = hist.copy()

    df2.index = df2.index.tz_localize(None)

    merge = pd.merge_asof(df1, df2, left_index=True, right_index=True, direction='backward')

    merge['Market cap'] = merge['Close'] * merge['Ordinary Shares Number']
    merge['Enterprise Value'] = merge['Market cap'] + merge['Total Debt'] - \
                                merge['Cash Cash Equivalents And Short Term Investments']

    df = merge.copy()

    percentages = round(df['Market cap'].astype('float64').pct_change(periods=1) * 100, 1)
    percentages = percentages.apply(lambda x: f"+{x}%" if x > 0 else ("" if pd.isna(x) else f"{x}%")).tolist()

    # Create the line chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df.index,
        y=df['Market cap'],
        name='Market cap',
        # base=base,
        marker=dict(
            color='green'  # Assign a color from the green color scale
        ),
        text=percentages,
        textfont=dict(size=12, color='black', family='Arial', weight='bold'),
        textposition='outside',
    ))

    fig.add_trace(go.Bar(
        x=df.index,
        y=df['Total Debt'],
        name='Total Debt',
        base=df['Market cap'],
        marker=dict(
            color='orange'  # Assign a color from the green color scale
        )
    ))

    fig.add_trace(go.Bar(
        x=df.index,
        y=-df['Cash Cash Equivalents And Short Term Investments'],
        name='Cash',
        base=df['Market cap'] + df['Total Debt'],
        marker=dict(
            color='red'  # Assign a color from the green color scale
        )
    ))

    fig.add_trace(go.Bar(
        x=df.index,
        y=df['Enterprise Value'],
        name='Enterprise Value',
        # base=base,
        marker=dict(
            color='blue'  # Assign a color from the green color scale
        )
    ))

    # Add titles and labels
    fig.update_layout(
        title=f'Capital structure: {ticker}',
        xaxis_title='Date',
        yaxis_title=f'Amount (in {currency})',
        # template='plotly_dark'  # Optional: use a dark theme
    )

    return fig


def plot_capital_multiple(tickers, tp="Annual"):
    fig = go.Figure()

    for ticker in tickers:
        bs = fetch_balance(ticker, tp=tp)
        df = bs.iloc[:, :4]
        df = df[df.columns[::-1]]
        df.columns = pd.to_datetime(df.columns).strftime('%b %d, %Y')

        df1 = bs.loc['Ordinary Shares Number'].to_frame()

        df1 = df1.iloc[::-1].dropna()

        dates = df1.index
        start = dates[0]

        hist = fetch_history(
            ticker=ticker,
            interval='1d',
            start=start - datetime.timedelta(days=5)
        )

        df2 = hist.copy()

        df2.index = df2.index.tz_localize(None)

        merge = pd.merge_asof(df1, df2, left_index=True, right_index=True, direction='backward')

        merge['Market cap'] = merge['Close'] * merge['Ordinary Shares Number']

        df = merge.copy()

        percentages = round(df['Market cap'].astype('float64').pct_change(periods=1) * 100, 1)
        percentages = percentages.apply(lambda x: f"+{x}%" if x > 0 else ("" if pd.isna(x) else f"{x}%")).tolist()

        df.index = pd.to_datetime(df.index).strftime('%b %d, %Y')

        fig.add_trace(go.Bar(
            x=[[ticker] * len(df.index), df.index],
            y=df['Market cap'],
            name='Market cap',
            # marker=dict(color='green'),
            text=percentages,
            textfont=dict(size=10, color='black', family='Arial', weight='bold'),
            textposition='outside',
            showlegend=False,
        ))

    # Update layout to stack bars and set titles
    fig.update_layout(
        barmode='group',
        title=f'Market Cap: {", ".join(tickers)}',
        # xaxis_title='Date',
        yaxis_title=f'Amount',
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="top",  # Aligns the legend vertically to the top
            y=-0.5,  # Positions the legend below the subplots
            xanchor="center",  # Aligns the legend horizontally to the center
            x=0.5  # Centers the legend horizontally
        ),
        margin=dict(t=70, b=150)
    )
    return fig

def plot_balance_multiple(TICKERS, tp="Annual"):

    fig = go.Figure()

    for ticker in TICKERS:
        bs = fetch_balance(ticker, tp=tp)
        df = bs.iloc[:, :4]
        df = df[df.columns[::-1]]
        df.columns = pd.to_datetime(df.columns).strftime('%b %d, %Y')

        show_legend = ticker == TICKERS[0]

        percentages = round(df.loc['Total Assets'].astype('float64').pct_change(periods=1) * 100, 1)
        percentages = percentages.apply(lambda x: f"+{x}%" if x > 0 else ("" if pd.isna(x) else f"{x}%")).tolist()

        fig.add_trace(go.Bar(
            x=[[ticker] * len(df.columns), df.columns],
            y=df.loc['Total Assets'],
            name='Total Assets',
            marker=dict(color='forestgreen'),
            text=percentages,
            textfont=dict(size=10, color='black', family='Arial', weight='bold'),
            textposition='outside',
            showlegend=show_legend,
        ))

        fig.add_trace(go.Bar(
            x=[[ticker] * len(df.columns), df.columns],
            y=df.loc['Total Liabilities Net Minority Interest'],
            name='Total Liabilities',
            marker=dict(color='tomato'),
            showlegend=show_legend,
        ))

    # Update layout to stack bars and set titles
    fig.update_layout(
        barmode='overlay',
        title=f'Accounting Balance: {", ".join(TICKERS)}',
        #xaxis_title='Date',
        yaxis_title=f'Amount',
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="top",  # Aligns the legend vertically to the top
            y=-0.5,  # Positions the legend below the subplots
            xanchor="center",  # Aligns the legend horizontally to the center
            x=0.5  # Centers the legend horizontally
        ),
        margin=dict(t=70)
    )
    return fig

def plot_income_multiple(TICKERS, tp="Annual"):

    fig = go.Figure()

    for ticker in TICKERS:
        ist = fetch_income(ticker, tp=tp)
        df = ist.iloc[:, :4]
        df = df[df.columns[::-1]]
        df.columns = pd.to_datetime(df.columns).strftime('%b %d, %Y')

        show_legend = ticker == TICKERS[0]

        percentages = round(df.loc['Total Revenue'].astype('float64').pct_change(periods=1) * 100, 1)
        percentages = percentages.apply(lambda x: f"+{x}%" if x > 0 else ("" if pd.isna(x) else f"{x}%")).tolist()

        fig.add_trace(go.Bar(
            x=[[ticker] * len(df.columns), df.columns],
            y=df.loc['Total Revenue'],
            name='Total Revenue',
            marker=dict(color='rgb(0,68,27)'),
            text=percentages,
            textfont=dict(size=10, color='black', family='Arial', weight='bold'),
            textposition='outside',
            showlegend=show_legend,
        ))

        percentages = round(df.loc['Net Income Common Stockholders'].astype('float64').pct_change(periods=1) * 100, 1)
        percentages = percentages.apply(lambda x: f"+{x}%" if x > 0 else ("" if pd.isna(x) else f"{x}%")).tolist()

        fig.add_trace(go.Bar(
            x=[[ticker] * len(df.columns), df.columns],
            y=df.loc['Net Income Common Stockholders'],
            name='Net Income',
            marker=dict(color='rgb(224, 253, 74)'),
            text=percentages,
            textfont=dict(size=10, color='gray', family='Arial', weight='bold'),
            textposition='outside',
            showlegend=show_legend,
        ))

    # Update layout to stack bars and set titles
    fig.update_layout(
        barmode='overlay',
        title=f'Income: {", ".join(TICKERS)}',
        #xaxis_title='Date',
        yaxis_title=f'Amount',
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="top",  # Aligns the legend vertically to the top
            y=-0.5,  # Positions the legend below the subplots
            xanchor="center",  # Aligns the legend horizontally to the center
            x=0.5  # Centers the legend horizontally
        ),
        margin=dict(t=70)
    )
    return fig

def plot_cash_multiple(TICKERS, tp="Annual"):

    fig = go.Figure()

    for ticker in TICKERS:
        cf = fetch_cash(ticker, tp=tp)
        df = cf.iloc[:, :4]
        df = df[df.columns[::-1]]
        df.columns = pd.to_datetime(df.columns).strftime('%b %d, %Y')

        show_legend = ticker == TICKERS[0]

        percentages = round(df.loc['Operating Cash Flow'].astype('float64').pct_change(periods=1) * 100, 1)
        percentages = percentages.apply(lambda x: f"+{x}%" if x > 0 else ("" if pd.isna(x) else f"{x}%")).tolist()

        fig.add_trace(go.Bar(
            x=[[ticker] * len(df.columns), df.columns],
            y=df.loc['Operating Cash Flow'],
            name='Operating Cash Flow',
            marker=dict(color='#fec3fe'),
            text=percentages,
            textfont=dict(size=10, color='black', family='Arial', weight='bold'),
            textposition='outside',
            showlegend=show_legend,
        ))

        fig.add_trace(go.Bar(
            x=[[ticker] * len(df.columns), df.columns],
            y=df.loc['Free Cash Flow'],
            name='Free Cash Flow',
            marker=dict(color='blue'),
            showlegend=show_legend,
        ))

    # Update layout to stack bars and set titles
    fig.update_layout(
        barmode='overlay',
        title=f'Cash flow: {", ".join(TICKERS)}',
        #xaxis_title='Date',
        yaxis_title=f'Amount',
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="top",  # Aligns the legend vertically to the top
            y=-0.5,  # Positions the legend below the subplots
            xanchor="center",  # Aligns the legend horizontally to the center
            x=0.5  # Centers the legend horizontally
        ),
        margin=dict(t=70)
    )
    return fig