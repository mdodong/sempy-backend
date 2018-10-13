import datetime
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

#block explorer utilities
def build_dict(seq, key):
    # return a new dictionary from a list of dictionaries identified by key
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))

def delegates_by_address():
    delegates = get_delegates()['result']
    return build_dict(delegates, key="address")

def process_delegate(delegate):
    delegate["status"] = "Delegate"
    if delegate["validator"]:
        delegate["status"] = "Validator"
    votes = float(delegate["votes"])/1000000000
    delegate["votes"] = votes.is_integer() and int(votes) or votes
    if int(delegate["turnsHit"]) == 0:
        delegate["ratio"] = 0
    else:
        delegate["ratio"] = int(delegate["turnsHit"])/(int(delegate["turnsHit"]) + int(delegate["turnsMissed"])) * 100
    #print(delegate["turnsHit"], delegate["turnsMissed"])
    return delegate

def process_all_delegates(all_delegates):
    theDelegates = []
    for d in range(len(all_delegates)):
        theDelegates.append(process_delegate(all_delegates[d]))
    return theDelegates


def process_address(address):
    delegates = delegates_by_address()
    if address["address"] in delegates:
        address["name"] = delegates.get(address["address"] )["name"]
    available = float(address["available"])/1000000000
    locked = float(address["locked"])/1000000000
    address["available"] = available.is_integer() and int(available) or available
    address["locked"] = locked.is_integer() and int(locked) or locked
    address["totalBalance"] = address["available"] + address["locked"]
    return address

def process_transactions(tx):
    delegates = delegates_by_address()
    value = float(tx["value"])/1000000000
    fee = float(tx["fee"])/1000000000
    date = datetime.datetime.fromtimestamp(int(tx['timestamp'])/1000.0)
    tx["value"] = value.is_integer() and int(value) or value
    tx["fee"] = fee.is_integer() and int(fee) or fee
    tx["timestamp"] = date.strftime('%Y-%m-%d %H:%M:%S')
    if tx["from"] in delegates:
        tx["fromName"] = delegates.get(tx["from"])['name']
    if tx["to"] in delegates:
        tx["toName"] = delegates.get(tx["to"])['name']
    return tx

def process_block(block):
    delegates = delegates_by_address()
    theBlock = block['result']
    validatorName = delegates.get(theBlock['coinbase'])['name']
    theBlock['validatorName'] = validatorName
    txs = len(theBlock['transactions']) - 1
    theBlock['transactionCount'] = txs
    totalFees = 0
    for x in range(txs+1):
        theBlock['transactions'][x] = process_transactions(theBlock['transactions'][x])
        totalFees += theBlock['transactions'][x]["fee"]
    if totalFees == 0 or 0.0:
        theBlock['totalFees'] = 0
    else:
        theBlock['totalFees'] = totalFees
    date = datetime.datetime.fromtimestamp(int(theBlock['timestamp'])/1000.0)
    theBlock['timestamp'] = date.strftime('%Y-%m-%d %H:%M:%S')
    return theBlock

def get_blocks(nBlocks=10):
    delegates = delegates_by_address()
    latestBlockNumber = int(get_latest_block_number()["result"])
    blocks = []
    for block in range(latestBlockNumber,(latestBlockNumber-nBlocks), -1):
        theBlock = process_block(get_block_by_number(block))
        blocks.append(theBlock)
    return blocks
