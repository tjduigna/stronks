import datetime as dt

import numpy as np
import pandas as pd
import altair as alt

import streamlit as st
import yfinance as yf


def fetch_ticker_data(ticker, start, end, interval):
    data = yf.download(ticker, start=start, end=end, interval=interval)
    print("data downloaded", data.shape)
    if len(ticker.split()) == 1:
        data['Ticker'] = ticker
        data['Spread'] = (data['Open'] + data['Close']) / 2
        return data.reset_index().rename(columns={'Date': 'Datetime'})
    attribs, tickers = data.columns.levels
    index, indexes = 0, {}
    for attr in attribs:
        for ticker in tickers:
            indexes.setdefault(ticker, [])
            indexes[ticker].append(index)
            index += 1
    grouped = []
    for ticker in tickers:
        tuples = [data.columns[i] for i in indexes[ticker]]
        grouped.append(data[tuples].copy())
        grouped[-1].columns = attribs
        grouped[-1]['Ticker'] = ticker
        grouped[-1]['Spread'] = (grouped[-1]['Open'] + grouped[-1]['Close']) / 2
    return pd.concat(grouped).reset_index().rename(columns={'Date': 'Datetime'})


def make_chart(data):

    # green-red condition check
    open_close_color = alt.condition(
        "datum.Open <= datum.Close",
        alt.value("#06982d"),
        alt.value("#ae1325")
    )

    # interactive axes
    scales = alt.selection_interval(bind='scales')

    # base chart with X-axis defined
    axis = alt.Axis(format='%m/%d/%y', labelAngle=-45, title='Datetime')
    xaxis = alt.X('Datetime:T', axis=axis)
    base = alt.Chart(data).encode(xaxis, color=open_close_color)

    # candlestick lifted from examples
    candle = base.mark_bar().encode(alt.Y('Open:Q'), alt.Y2('Close:Q'))
    yaxis = alt.Y('Low:Q', title='Price', scale=alt.Scale(zero=False))
    stick = base.mark_rule().encode(yaxis, alt.Y2('High:Q'))

    # lines of average between open and close 
    # TODO : better colors, toggle view/hide individual tickers
    spread = (base.mark_line(interpolate='basis')
                  .encode(y='Spread:Q', color='Ticker:N')
                  .add_selection(scales))


    return alt.layer(candle, stick, spread).properties(width=600, height=600)


_END = dt.datetime.today()
_START = _END - dt.timedelta(days=90)

def main():

    intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m',
                 '1d', '5d', '1wk', '1mo', '3mo']

    st.sidebar.markdown("# StonkVieu")
    ticker = st.sidebar.text_input("Tickers (space separated)", value="SPY")
    interval = st.sidebar.selectbox("Interval", intervals, index=7)

    start = st.sidebar.date_input("Start Date", value=_START)
    end = st.sidebar.date_input("End Date", value=_END)
    check = st.sidebar.checkbox("Party", value=False)

    if interval.endswith('m'):
        days = (end - start).total_seconds() // 86400
        limit = 7 if interval == '1m' else 59
        if days > 59:
            start = end - dt.timedelta(days=limit)

    if check:
        st.balloons()

    data = fetch_ticker_data(ticker, start, end, interval)
    chart = make_chart(data)
    st.write(chart)



if __name__ == '__main__':
    main()

