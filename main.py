from multiprocessing.dummy import current_process
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go

NAME = 'XRP-USD'
INIT_USD = 1000

# Initialize variables
if 'usd' not in st.session_state:
    st.session_state.usd = INIT_USD

if 'xrp' not in st.session_state:
    st.session_state.xrp = 0

# Layout
st.set_page_config(layout='wide')

def get_data():
    return yf.download(tickers=NAME, period='3h', interval='1m')

data = get_data()

col1, col2 = st.columns([3, 1])

with col1:
    if st.button('Refresh'):
        data = get_data()

    current_price = float(data.iloc[-1]['Close'])

    st.header('%s %.5f' % (NAME, current_price))

    fig = go.Figure([go.Scatter(x=data.index, y=data['Close'])])

    fig.update_layout(
        height=1000
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.header('Buy/Sell')

    # Buy
    buy_amount = st.number_input('산다', min_value=0, value=0)

    if st.button('Buy'):
        data = get_data()
        current_price = float(data.iloc[-1]['Close'])

        buy_price = buy_amount * current_price

        # Buy and update the session
        if st.session_state.usd >= buy_price:
            st.session_state.xrp += buy_amount
            st.session_state.usd -= buy_price
        else:
            st.warning('Not enough USD')

    # Sell
    sell_amount = st.number_input('판다', min_value=0, value=0)

    if st.button('Sell'):
        data = get_data()
        current_price = float(data.iloc[-1]['Close'])

        # Sell and update the session
        if st.session_state.xrp >= sell_amount:
            sell_price = sell_amount * current_price

            st.session_state.xrp -= sell_amount
            st.session_state.usd += sell_price
        else:
            st.warning('Not enough XRP')


    st.subheader('나의 USD %.2f' % st.session_state.usd)
    st.subheader('나의 XRP %d' % st.session_state.xrp)

    total_in_usd = st.session_state.usd + st.session_state.xrp * current_price

    st.subheader('손익 %.2f%%' % ((total_in_usd - INIT_USD) / INIT_USD * 100))
