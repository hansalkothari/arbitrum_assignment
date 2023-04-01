import websocket
import json
from web3 import Web3
import logging
import sys
from io import StringIO
from web3.middleware import geth_poa_middleware

#setting up logging
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s', handlers = [
    logging.FileHandler('transactions.log'),
    logging.StreamHandler(sys.stdout)
]
)

def on_open(ws):
    subs_req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_subscribe",
        "params": ["newHeads"]
    }
    ws.send(json.dumps(subs_req))

def handle_msg(message):
    print(message)
    messageIO = StringIO(message)
    message = json.load(messageIO)

    # print(message.get('type'))
    # if message.get('type') == 'tx':
    data = message['params']['result']
    logging.info(f"new txn: { data }")

def on_message(ws,message):
    handle_msg(message)

def WebsocketSubscription():
    websocket_url = "wss://arb-goerli.g.alchemy.com/v2/h9QpNlfSPIG5Rvu5NOPatlG16Ihvi3Un"
    ws = websocket.WebSocketApp(websocket_url, on_open=on_open, on_message=on_message)
    ws.run_forever()


if __name__ == '__main__':
    #connection of web3 with alchemy api
    alchemy_url = "https://arb-goerli.g.alchemy.com/v2/h9QpNlfSPIG5Rvu5NOPatlG16Ihvi3Un"
    w3 = Web3(Web3.HTTPProvider(alchemy_url))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    print(w3.is_connected())
    WebsocketSubscription()

