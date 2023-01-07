import os
from celery import Celery
from web3 import Web3
from eth_defi.event_reader.fast_json_rpc import patch_web3
from eth_defi.event_reader.conversion import decode_data, convert_int256_bytes_to_int
from django.core.cache import cache
import pandas
import pandas as pd
import requests
import json

# web3
contractAddress = '0x09757DabaC779e8420b40df0315962Bbc9833C73'
binance_testnet_rpc_url = "https://ethereum-goerli-rpc.allthatnode.com"
w3 = Web3(Web3.HTTPProvider(binance_testnet_rpc_url,
          request_kwargs={'timeout': 60}))

# ключ etherscan
ETHERSCAN_API_KEY = '2YP969R63AA4198CSD7JVAA1QDH6HDBWIX'
#ETHERSCAN_API_KEY = ''

# ускорение работы
patch_web3(w3)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'token_monitor.settings')

# Создаем объект(экземпляр класса) celery и даем ему имя
app = Celery('token_monitor')

# Загружаем config с настройками для объекта celery.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Функция выполняемая после запуска celery


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # получаем данные начиная с блока 8057223
    get_history_data(8057223)
    # добавляем периодическую задачу, для обновления данных
    sender.add_periodic_task(60.0, update_data.s(),
                             name='update transaction logs')

# функция обновления данных


@app.task
def update_data():
    # получаем данные из кэша, находим самый новый блок и начиная с него ищём логи,объеденяем данные и возваращаем в кэш
    data = cache.get('txnx')
    cache_df = pd.DataFrame.from_dict(data)
    index = len(cache_df)-1
    last_block = int(cache_df.loc[[index], 'Block'])
    update_df = get_history_data(last_block)
    update_df = pandas.concat([cache_df, update_df])
    update_df = update_df.drop_duplicates()
    update_df = update_df.sort_values('Block', ascending=False)[:100]
    update_item = update_df.to_dict('records')
    cache.set('txnx', update_item, timeout=360)

# функция получения данных


@app.task
def get_history_data(fromBlock):
    # собираем логи
    block_filter = w3.eth.filter(
        {'fromBlock': fromBlock, 'address': contractAddress})
    df = pd.DataFrame({
        'Hash': ['-'],
        'Amount': [0],
        'Method': ['-'],
        'Block': [int(0)]
    })
    # разбираем логи и собираем нужную информацию
    for event in block_filter.get_all_entries():
        hash_txn = event['transactionHash'].hex()
        block_num = event['blockNumber']
        data = event['data']
        amount = convert_int256_bytes_to_int(
            decode_data(data)[0])
        amount = w3.fromWei(amount, 'ether')
        tx = w3.eth.get_transaction(hash_txn)
        # строка запроса abi смарт контракта с которым взаимодействие в транзакции
        abi_endpoint = f"https://api-goerli.etherscan.io/api?module=contract&action=getabi&address={tx['to']}&apikey=2YP969R63AA4198CSD7JVAA1QDH6HDBWIX"
        # подключаемся и выгружаем abi
        get_status = False
        while not get_status:
            response = requests.get(abi_endpoint)
            if response.status_code == 200:
                try:
                    abi = json.loads(response.text)
                    get_status = True
                except ValueError:
                    print(response.status_code)
        # Если abi выгрузился без ошибок, то получааем метод и количество с помощью него
        if abi['message'] != 'NOTOK':
            contract = w3.eth.contract(address=tx["to"], abi=abi["result"])
            func_obj, func_params = contract.decode_function_input(tx["input"])
            method_id = func_obj.function_identifier
            try:
                amount = w3.fromWei(func_params['amount'], 'ether')
            except KeyError:
                amount = '-'
        # Если abi недоступен, то разбираем метод вручную или просто записываем в том виде, котором получили
        else:
            method_id = tx['input'][:10]
            if method_id == '0x672cc9c7':
                method_id = 'Stake'
        # вносим данные в dataframe
        df = pd.concat([df, pd.DataFrame.from_records(
            [{'Hash': hash_txn, 'Amount': amount, 'Method': method_id, 'Block': block_num}])], ignore_index=True)

    # обрабатываем датафрейм для получения последних 100 действий
    df = df.drop_duplicates()
    df = df.sort_values('Block', ascending=False)[:100]
    item = df.to_dict('records')
    cache.set('txnx', item, timeout=360)
    return df
