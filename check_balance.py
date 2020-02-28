import threading
import time

from gifto.giftod import Giftod
from gifto.utils import fmt_time_from_now
from giftobase import operations
from giftobase.transactions import get_block_params, fmt_time_from_now_to_epoch, SignedTransaction

bots = [
    'treasurebo39',
    'sparklez22',
    'hunyinglaigift45',
    'cryptodance35',
    'bomulsangja56',
    'gamsa978',
    'geureiteofu55',
    'sunmulmapia56',
    'robinuikeurip17',
    'gasangsunmul33',
    'giftomiracle79',
    'shijiediyixuni84',
    'xunideshijie39',
    'mintypics093',
    'zenyangzuoquku83',
    'xiangshoudaoqu84',
    'qukuailianshen27',
    'shixianqukuail48',
    'gtosanta50',
    'songxuniliwude95'
]

known_chains = {
    "GIF": {
        "chain_id": "f845ee263618f4cbd107bacc8bc69e693537695a773890083afc878c241750e1",
        "prefix": "GIF",
        "beowulf_symbol": "GTO",
        "wd_symbol": "SGTO",
        "vests_symbol": "LGTO",
    }
}

asset_precision = {
    "GTO": 5,
    "SGTO": 5,
    "LGTO": 5,
}


class Amount:
    def __init__(self, d):
        self.amount, self.asset = d.strip().split(" ")
        self.amount = float(self.amount)

        if self.asset in asset_precision:
            self.precision = asset_precision[self.asset]
        else:
            raise Exception("Asset unknown")


# Variables for Wallet File
init_account = "gifto"
wif = "5JEsAzMxv5E1djK7EGzeBCG85EeHf798UJbEYfSKihM1vTVVwQc"

# Transfer Test-net
bwfd = Giftod(nodes=["http://127.0.0.1:8376/rpc"])


def prepare_properties_for_tx():
    expiration = fmt_time_from_now(360)
    ref_block_num, ref_block_prefix = get_block_params(bwfd)
    created_time = fmt_time_from_now_to_epoch()
    return expiration, ref_block_num, ref_block_prefix, created_time


def create_operation_transfer(
        sender,
        receiver,
        amount="10.00000 GTO",
        memo=""):
    op_transfer = operations.Transfer(
        **{
            "from": sender,
            "to": receiver,
            "amount": amount,
            "fee": "0.01000 SGTO",
            "memo": memo
        })

    ops = [operations.Operation(op_transfer)]
    return ops


def sign_and_broadcast(wif, ops):
    expiration, ref_block_num, ref_block_prefix, created_time = prepare_properties_for_tx()
    tx = SignedTransaction(
        ref_block_num=ref_block_num,
        ref_block_prefix=ref_block_prefix,
        expiration=expiration,
        operations=ops,
        created_time=created_time)

    tx = tx.sign([wif], chain=known_chains["GIF"])
    response = bwfd.broadcast_transaction(tx.json())
    print(response)


def init_balance(receiver, type_coin):
    sender = init_account
    amount = "1000.00000 {}".format(type_coin)

    ops_amount = create_operation_transfer(sender=sender,
                                           receiver=receiver,
                                           amount=amount)
    try:
        sign_and_broadcast(wif, ops_amount)
    except Exception as e:
        raise e


def check_empty_balance(receiver):
    account_detail = bwfd.get_account(receiver)
    balance = Amount(account_detail['balance'])
    wbalance = Amount(account_detail['wd_balance'])
    is_empty_balance = False
    is_empty_wbalance = False

    if balance.amount <= 10:
        is_empty_balance = True
    if wbalance.amount <= 60000:
        is_empty_wbalance = True
    return is_empty_balance, is_empty_wbalance


def main():
    while True:
        for account in bots:
            is_empty_balance, is_empty_wbalance = check_empty_balance(account)
            print(account, is_empty_balance, is_empty_wbalance)
            if is_empty_balance:
                t = threading.Thread(target=init_balance, args=(account, "GTO"))
                t.start()
            if is_empty_wbalance:
                t = threading.Thread(target=init_balance, args=(account, "SGTO"))
                t.start()
        try:
            print('Sleep...')
            time.sleep(15)
        except Exception as e:
            continue


if __name__ == '__main__':
    main()
