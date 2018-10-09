import requests
import config

CLIENT = requests.Session()
CLIENT.auth = (config.API_USERNAME, config.API_PASSWORD)
HOST = config.API_HOST

def api(command=None, params_=None, method='GET', host=None, client=None):
    if command is None:
        cm = ''
    else:
        cm = command
    if host is None:
        url = HOST + cm
    else:
        url = host + cm

    if client is None:
        cl = CLIENT
    else:
        cl = client

    if method=='GET':
        return cl.get(url, params=params_).json()
    else:
        return  cl.post(url, params=params_).json()

def get_root():
    info = api('/info')
    info["result"]["coinbase"] = "hidden"
    return info

def get_info():
    return get_root()

def get_pending_tx():
    return api('/pending-transactions')

def get_latest_block_number():
    return api('/latest-block-number')

def get_latest_block():
    return api('/latest-block')

def get_block_by_number(number):
    params = {'number' : number}
    return api('/block-by-number', params)

def get_block_by_hash(hash):
    params = {'hash' : hash}
    return api('/block-by-hash', params)

def get_delegates():
    return api('/delegates')

def get_validators():
    return api('/validators')

def get_votes(delegate):
    params = {'delegate' : delegate}
    return api('/votes', params)

def get_account(address):
    params = {'address' : address}
    return api('/account', params)

def get_account_transactions(address, start, end):
    params = {'address' : address, 'from': start, 'to':end}
    return api('/account/transactions', params)

def get_account_votes(address):
    params = {'address' : address}
    return api('/account/votes', params)

def broadcast_rawtx(raw):
    params = {'raw' : raw}
    return api('/transaction/raw', params, 'POST')

def get_vote(delegate, voter):
    params = {'delegate' : delegate, 'voter': voter}
    return api('/vote', params)

def get_latest_block_number():
    return api('/latest-block-number')

def get_transaction(hash):
    params = {'hash' : hash}
    return api('/transaction', params)
