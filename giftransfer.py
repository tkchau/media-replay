import threading
import time

from beowulf.beowulfd import Beowulfd
from beowulf.utils import fmt_time_from_now
from beowulfbase import operations
from beowulfbase.transactions import get_block_params, fmt_time_from_now_to_epoch, SignedTransaction

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
    "BEO": {
        "chain_id": "430b37f23cf146d42f15376f341d7f8f5a1ad6f4e63affdeb5dc61d55d8c95a7",
        "prefix": "BEO",
        "gifto_symbol": "BWF",
        "wd_symbol": "W",
        "vests_symbol": "M",
    }
}

asset_precision = {
    "BWF": 5,
    "W": 5,
    "M": 5,
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
init_account = "chautk1"
wif = "5KXj6EsHizm7f7sLPWBMcoUuyy7Jxci2exvkCo3Pb9YqMzhqbLE"
nhan = "chautk2"
loai1 = "BWF"
# Transfer Test-net
bwfd = Beowulfd(nodes=["http://35.247.136.41:8376/rpc"])


def prepare_properties_for_tx():
    expiration = fmt_time_from_now(360)
    ref_block_num, ref_block_prefix = get_block_params(bwfd)
    created_time = fmt_time_from_now_to_epoch()
    return expiration, ref_block_num, ref_block_prefix, created_time


def create_operation_transfer(
        sender,
        receiver,
        amount="10.00000 BWF",
        memo=""):
    op_transfer = operations.Transfer(
        **{
            "from": sender,
            "to": receiver,
            "amount": amount,
            "fee": "0.01000 W",
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

    tx = tx.sign([wif], chain=known_chains["BEO"])
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
    wbalance = Amount(account_detail['sg_balance'])
    is_empty_balance = False
    is_empty_wbalance = False

    if balance.amount <= 10:
        is_empty_balance = True
    if wbalance.amount <= 10:
        is_empty_wbalance = True
    return is_empty_balance, is_empty_wbalance


def main():
     init_balance(nhan , loai1)

if __name__ == '__main__':
    main()
