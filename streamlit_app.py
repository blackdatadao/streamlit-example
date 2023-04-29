from web3 import Web3
from eth_abi import decode
import time
import pandas as pd 
from web3 import Web3,HTTPProvider
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

"""
# Welcome to Streamlit!lllllll

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

def get_current_price_etharb(
        connection
    ):
    # fb=74711249,tb=74811249
    fb=connection.eth.block_number-100
    tb=connection.eth.block_number
    cAddress="0xc6f780497a95e246eb9449f5e4770916dcd6396a"
    tp=["0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67"]
    start_time=time.time()
    result=connection.eth.get_logs(
        {"address": Web3.to_checksum_address(cAddress), 
    "topics":tp,
    "fromBlock":Web3.to_hex(fb),
    "toBlock":Web3.to_hex(tb)
    })
    print('time cost:',time.time()-start_time)

    if result!=[]:
        temp=Web3.to_json(result)#result is a list of attributeDict type,convert attributeDict to json
        
        df=pd.read_json(temp).tail(1)
        df=pd.read_json(temp)
        timestamp_start=connection.eth.get_block(int(df['blockNumber'][0]))['timestamp']
        timestamp_end=connection.eth.get_block(int(df['blockNumber'].tail(1)))['timestamp']
        print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timestamp_start)))
        print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timestamp_end)))
        
        
        #get the timestamp of each transaction
        # df['timeStamp']=df['blockNumber'].map(lambda x:connection.eth.get_block(x)['timestamp'])
        #calculate time stamp to datetime
        # df['create_time']=df['timeStamp'].map(lambda x:time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(x)))
        #decode the data
        df['data_decoded']=df['data'].map(lambda x:decode(['int256','int256','int256'],bytes.fromhex(x[2:])))
        # df['data_decoded']=df['data_decoded'].map(lambda x:eval(x))
        #split data_decoded to 3 columns
        df['sqrtPrice']=df['data_decoded'].map(lambda x:x[2])
        df['amount0']=abs(df['data_decoded'].map(lambda x:x[0]))
        df['amount1']=abs(df['data_decoded'].map(lambda x:x[1]))

        # df['tick']=df['data_decoded'].map(lambda x:x[3])
        decimals1=18
        decimals0=18 #ETH
        price0 = df['amount1']/10**decimals1/(df['amount0']/10**decimals0)
        # Calculate the price of token0 in terms of token1
        price1 = 1 / price0
        # return the value of price0

        return dict(
           price0=price0.values[0])
    else:
        raise Exception('fetched None')

def get_history_price_etharb(
        connection
    ):
    # fb=74711249,tb=74811249
    minutes=12
    fb=connection.eth.block_number-3*60*minutes
    tb=connection.eth.block_number
    cAddress="0xc6f780497a95e246eb9449f5e4770916dcd6396a"
    tp=["0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67"]
    start_time=time.time()
    result=connection.eth.get_logs(
        {"address": Web3.to_checksum_address(cAddress), 
    "topics":tp,
    "fromBlock":Web3.to_hex(fb),
    "toBlock":Web3.to_hex(tb)
    })
    print('time cost:',time.time()-start_time)

    if result!=[]:
        temp=Web3.to_json(result)#result is a list of attributeDict type,convert attributeDict to json
        
        df=pd.read_json(temp)
        timestamp_start=connection.eth.get_block(int(df['blockNumber'][0]))['timestamp']
        timestamp_end=connection.eth.get_block(int(df['blockNumber'].tail(1)))['timestamp']
        print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timestamp_start)))
        print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timestamp_end)))
        
        
        #get the timestamp of each transaction
        # df['timeStamp']=df['blockNumber'].map(lambda x:connection.eth.get_block(x)['timestamp'])
        #calculate time stamp to datetime
        # df['create_time']=df['timeStamp'].map(lambda x:time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(x)))
        #decode the data
        df['data_decoded']=df['data'].map(lambda x:decode(['int256','int256','int256'],bytes.fromhex(x[2:])))
        # df['data_decoded']=df['data_decoded'].map(lambda x:eval(x))
        #split data_decoded to 3 columns
        df['sqrtPrice']=df['data_decoded'].map(lambda x:x[2])
        df['amount0']=abs(df['data_decoded'].map(lambda x:x[0]))
        df['amount1']=abs(df['data_decoded'].map(lambda x:x[1]))

        # df['tick']=df['data_decoded'].map(lambda x:x[3])
        decimals1=18
        decimals0=18 #ETH
        df['price0'] = df['amount1']/10**decimals1/(df['amount0']/10**decimals0)
        # Calculate the price of token0 in terms of token1
        # price1 = 1 / price0
        # return the value of price0

        return df[['blockNumber','price0']]
    else:
        raise Exception('fetched None')
    
def get_swap_price_ethusdc(
        connection
    ):
    #topic:increase liquidity
    # fb=74711249,tb=74811249
    fb=connection.eth.block_number-10000
    tb=connection.eth.block_number
    cAddress="0xC31E54c7a869B9FcBEcc14363CF510d1c41fa443"
    tp=["0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67"]
    start_time=time.time()
    result=connection.eth.get_logs(
        {"address": Web3.to_checksum_address(cAddress), 
    "topics":tp,
    "fromBlock":Web3.to_hex(fb),
    "toBlock":Web3.to_hex(tb)
    })
    print('time cost:',time.time()-start_time)
    if result!=[]:
        temp=Web3.to_json(result)#result is a list of attributeDict type,convert attributeDict to json
        df=pd.read_json(temp).iloc[-1,0]
        #get the timestamp of each transaction
        df['timeStamp']=df['blockNumber'].map(lambda x:connection.eth.get_block(x)['timestamp'])
        #calculate time stamp to datetime
        df['create_time']=df['timeStamp'].map(lambda x:time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(x)))
        #decode the data
        #{"indexed":false,"internalType":"uint128","name":"liquidity","type":"uint128"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"IncreaseLiquidity","type":"event"}
        df['data_decoded']=df['data'].map(lambda x:decode(['int256','int256','int256'],bytes.fromhex(x[2:])))
        # df['data_decoded']=df['data_decoded'].map(lambda x:eval(x))
        #split data_decoded to 3 columns
        df['sqrtPrice']=df['data_decoded'].map(lambda x:x[2])
        df['amount0']=abs(df['data_decoded'].map(lambda x:x[0]))
        df['amount1']=abs(df['data_decoded'].map(lambda x:x[1]))
        # df['tick']=df['data_decoded'].map(lambda x:x[3])
        decimals1=6
        decimals0=18 #ETH
        price0 = df['amount1']/10**decimals1/(df['amount0']/10**decimals0)
        # Calculate the price of token0 in terms of token1
        # price1 = 1 / price0

        return dict(
        #    price1=price1,
           price0=price0)
    else:
        raise Exception('fetched None')


provider_arb='https://arb1.arbitrum.io/rpc'
provider_arb_2='https://arbitrum-mainnet.infura.io/v3/02040948aa024dc49e8730607e0caece'
w3=Web3(HTTPProvider(provider_arb_2, {'timeout': 20}))



# # Read JSON data and convert to pandas DataFrame
# with open('data.json', 'r') as f:
#     data = json.load(f)
# df = pd.DataFrame(data)


df=get_history_price_etharb(w3)
timestamp_start=w3.eth.get_block(int(df['blockNumber'][0]))['timestamp']
timestamp_end=w3.eth.get_block(int(df['blockNumber'].tail(1)))['timestamp']
tick_values = np.linspace(df["blockNumber"].min(), df["blockNumber"].max(), 4).round()
tick_values_int=[w3.eth.get_block(int(x))['timestamp'] for x in tick_values]
tick_labels = [time.strftime("%d %H:%M",time.localtime(x)) for x in tick_values_int]
y_min = df["price0"].mean() - 5 * df["price0"].std()
y_max = df["price0"].mean() + 5 * df["price0"].std()
price_median = df["price0"].median()
df["price0"] = df["price0"].apply(lambda x: price_median if x < y_min or x > y_max else x)


fig=px.line(df,x='blockNumber',y='price0',title=' end time: '+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timestamp_end)))
fig.update_xaxes(tickmode='array',tickvals=tick_values, ticktext=tick_labels)
# fig.update_yaxes(range=[y_min, y_max])
st.plotly_chart(fig, use_container_width=True
                )
