import time

from beowulf.beowulfd import Beowulfd
from beowulfbase import operations
from beowulfbase.transactions import SignedTransaction, fmt_time_from_now_to_epoch, fmt_time_from_now, get_block_params

known_chains = {
    "BWF": {
        "chain_id": "430b37f23cf146d42f15376f341d7f8f5a1ad6f4e63affdeb5dc61d55d8c95a7",
        "prefix": "BEO",
        "beowulf_symbol": "BWF",
        "wd_symbol": "W",
        "vests_symbol": "M",
    }
}

# Variables for Wallet File
creator = "beowulf"
wif = "5JrfnT23TfZSg6xHtBpsc7NRuGNakCiGUZ5WN1tNUJBVkWapYfb"
wallet_file_name = "alice.json"
wallet_file_pwd = "P4ssw0rd"

# Transfer Test-net
bwfd = Beowulfd(nodes=["127.0.0.1:8376/rpc"])
# 5KRmjuQHYPG5qCEz9npXkmpZ63frsb2E1MwoWUbm4JCE7eHG1YE
default_key_auths = [
    ["BEO7qmQizytdxsWMpRFknhG432ucKHTbv4XzR8HVQKBwWJCSuFvML",
     1]
]


# extensions = [
#         0,
#         {
#           "beneficiaries": [
#             {"account": "david", "weight": 500},
#             {"account": "erin", "weight": 500},
#             {"account": "faythe", "weight": 1000},
#             {"account": "frank", "weight": 500}
#           ]
#         }
#     ]


def generate_key_pairs(password):
    from beowulfbase.account import PasswordKey
    owner_key = PasswordKey("default", password, role="owner")
    owner_pubkey = owner_key.get_public_key()
    owner_privkey = owner_key.get_private_key()
    print(owner_pubkey, owner_privkey)
    return owner_pubkey.__str__(), owner_privkey.__str__()


def prepare_properties_for_tx():
    expiration = fmt_time_from_now(360)
    ref_block_num, ref_block_prefix = get_block_params(bwfd)
    created_time = fmt_time_from_now_to_epoch()
    return expiration, ref_block_num, ref_block_prefix, created_time


def create_operation_create_account(
        new_account_name,
        account_auths=[],
        key_auths=default_key_auths,
        weight_threshold=None,
        json_meta=None):
    if weight_threshold is None:
        weight_threshold = 1

    op_create = operations.AccountCreate(
        **{
            "fee": "1.00000 W",
            "creator": creator,
            "new_account_name": new_account_name,
            "owner": {
                "weight_threshold": weight_threshold,
                "account_auths": account_auths,
                "key_auths": key_auths
            },
            "json_metadata": json_meta
        })

    ops = [operations.Operation(op_create)]
    return ops


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

    op_transfer_2 = operations.Transfer(
        **{
            "from": sender,
            "to": receiver,
            "amount": amount,
            "fee": "0.01000 W",
            "memo": memo
        })

    ops = [operations.Operation(op_transfer), operations.Operation(op_transfer_2)]
    return ops


def sign_and_broadcast(wif, ops):
    expiration, ref_block_num, ref_block_prefix, created_time = prepare_properties_for_tx()
    tx = SignedTransaction(
        ref_block_num=ref_block_num,
        ref_block_prefix=ref_block_prefix,
        expiration=expiration,
        operations=ops,
        created_time=created_time)

    tx = tx.sign([wif], chain=known_chains["BWF"])
    print(tx.json())
    start = time.time()
    response = bwfd.broadcast_transaction_synchronous(tx.json())
    end = time.time()

    print(response)
    print('Total time:' + str(end - start))


def sign_and_broadcast_with_extensions(wif, ops, extensions):
    expiration, ref_block_num, ref_block_prefix, created_time = prepare_properties_for_tx()
    tx = SignedTransaction(
        ref_block_num=ref_block_num,
        ref_block_prefix=ref_block_prefix,
        expiration=expiration,
        extensions=extensions,
        operations=ops,
        created_time=created_time)

    tx = tx.sign([wif], chain=known_chains["BWF"])
    print(tx.json())
    start = time.time()
    response = bwfd.broadcast_transaction_synchronous(tx.json())
    end = time.time()

    print(response)
    print('Total time:' + str(end - start))


def sign_and_broadcast_multi(ops, wifs, weight_thres=1):
    expiration, ref_block_num, ref_block_prefix, created_time = prepare_properties_for_tx()
    tx = SignedTransaction(
        ref_block_num=ref_block_num,
        ref_block_prefix=ref_block_prefix,
        expiration=expiration,
        operations=ops,
        created_time=created_time)

    signs = []
    for wif in wifs[:weight_thres]:
        tx = tx.sign([wif], chain=known_chains["BWF"])
        sign = tx.json()["signatures"][0]
        signs.append(sign)

    print(signs)
    final_tx = tx
    from beowulfbase.types import Array
    final_tx.data["signatures"] = Array(signs)
    print(final_tx.json())
    start = time.time()
    response = bwfd.broadcast_transaction_synchronous(tx.json())
    end = time.time()
    print(response)
    print('Total time:' + str(end - start))


def create_account_with_account_auths():
    new_account_name = "tommy4"
    account_auths = [["jayce", 1]]
    ops = create_operation_create_account(new_account_name,
                                          account_auths)
    try:
        sign_and_broadcast(wif, ops)
    except Exception as e:
        raise e
        # Expected: "New owner authority on account tommy3
        # references non-existing account jayce"


def create_account_with_0_weight_thres():
    new_account_name = "tommy1"
    weight_threshold = 0
    ops = create_operation_create_account(new_account_name=new_account_name,
                                          weight_threshold=weight_threshold)
    try:
        sign_and_broadcast(wif, ops)
    except Exception as e:
        raise e


def create_account_with_no_pub():
    new_account_name = "tommy8"
    weight_threshold = 1
    key_auths = []
    ops = create_operation_create_account(new_account_name=new_account_name,
                                          key_auths=key_auths,
                                          weight_threshold=weight_threshold)
    try:
        sign_and_broadcast(wif, ops)
    except Exception as e:
        raise e


def create_account():
    new_account_name = "chautk2"
    #pub1, pri1 = generate_key_pairs("chautk2")
    # pub3, pri3 = generate_key_pairs("password3")

    # key_auths = [[pub1, 1], [pub2, 1]]
    key_auths = [["BEO64ovMhyXhmCArNbUecJpJh2Epvgi9XTry6NZmBC25YpQtwmxDC", 1]]

    # key_auths = [[pub1, 1], [pub2, 1], [pub3, 1]]
    print(key_auths)
    weight_threshold = 1

    ops = create_operation_create_account(new_account_name=new_account_name,
                                          weight_threshold=weight_threshold,
                                          key_auths=key_auths)
    try:
        sign_and_broadcast(wif, ops)
    except Exception as e:
        raise e


def create_account_with_multi_pubs():
    new_account_name = "tommy"
    pub1, pri1 = generate_key_pairs("password1")
    pub2, pri2 = generate_key_pairs("password2")
    # pub3, pri3 = generate_key_pairs("password3")

    # key_auths = [[pub1, 1], [pub2, 1]]
    key_auths = [[pub2, 1], [pub1, 1]]

    # key_auths = [[pub1, 1], [pub2, 1], [pub3, 1]]
    print(key_auths)
    weight_threshold = 1

    ops = create_operation_create_account(new_account_name=new_account_name,
                                          weight_threshold=weight_threshold,
                                          key_auths=key_auths)
    try:
        sign_and_broadcast(wif, ops)
    except Exception as e:
        raise e


def create_account_with_multi_pubs_1():
    weight_threshold = 1
    new_account_name_1 = "mother1"
    pub1, pri1 = generate_key_pairs("mother1")
    key_auths_1 = [[pub1, 1]]
    ops1 = create_operation_create_account(new_account_name=new_account_name_1,
                                           weight_threshold=weight_threshold,
                                           key_auths=key_auths_1)

    new_account_name_2 = "mother2"
    pub2, pri2 = generate_key_pairs("mother2")
    key_auths_2 = [[pub2, 1]]
    ops2 = create_operation_create_account(new_account_name=new_account_name_2,
                                           weight_threshold=weight_threshold,
                                           key_auths=key_auths_2)

    new_account_name_3 = "mother3"
    pub3, pri3 = generate_key_pairs("mother3")
    key_auths_3 = [[pub3, 1]]
    ops3 = create_operation_create_account(new_account_name=new_account_name_3,
                                           weight_threshold=weight_threshold,
                                           key_auths=key_auths_3)

    new_account_name_4 = "mother4"
    pub4, pri4 = generate_key_pairs("mother4")
    key_auths_4 = [[pub4, 1]]
    ops4 = create_operation_create_account(new_account_name=new_account_name_4,
                                           weight_threshold=weight_threshold,
                                           key_auths=key_auths_4)
    try:
        # sign_and_broadcast(wif, ops1)
        # sign_and_broadcast(wif, ops2)
        # sign_and_broadcast(wif, ops3)
        sign_and_broadcast(wif, ops4)
    except Exception as e:
        raise e


def create_account_with_multi_pubs_2():
    weight_threshold = 1
    new_account_name_1 = "mother11"
    pub11, pri11 = generate_key_pairs("mother11")
    pub12, pri12 = generate_key_pairs("mother12")
    pub13, pri13 = generate_key_pairs("mother13")

    key_auths_1 = [[pub11, 1], [pub12, 1], [pub13, 1]]
    ops1 = create_operation_create_account(new_account_name=new_account_name_1,
                                           weight_threshold=weight_threshold,
                                           key_auths=key_auths_1)

    new_account_name_2 = "mother21"
    pub21, pri21 = generate_key_pairs("mother21")
    pub22, pri22 = generate_key_pairs("mother22")
    pub23, pri23 = generate_key_pairs("mother23")

    key_auths_2 = [[pub21, 1], [pub22, 1], [pub23, 1]]
    ops2 = create_operation_create_account(new_account_name=new_account_name_2,
                                           weight_threshold=weight_threshold,
                                           key_auths=key_auths_2)

    new_account_name_3 = "mother31"
    pub31, pri31 = generate_key_pairs("mother31")
    pub32, pri32 = generate_key_pairs("mother32")
    pub33, pri33 = generate_key_pairs("mother33")

    key_auths_3 = [[pub31, 1], [pub32, 1], [pub33, 1]]
    ops3 = create_operation_create_account(new_account_name=new_account_name_3,
                                           weight_threshold=weight_threshold,
                                           key_auths=key_auths_3)

    try:
        # sign_and_broadcast(wif, ops1)
        # sign_and_broadcast(wif, ops2)
        sign_and_broadcast(wif, ops3)
    except Exception as e:
        raise e


def create_account_with_multi_pubs_3():
    weight_threshold = 1
    new_account_name_1 = "mother1111"
    pub_same1, pri_same1 = generate_key_pairs("mothersame1")
    pub_same2, pri_same2 = generate_key_pairs("mothersame2")
    pub_same3, pri_same3 = generate_key_pairs("mothersame3")

    key_auths = [[pub_same1, 1], [pub_same2, 1], [pub_same3, 1]]
    ops1 = create_operation_create_account(new_account_name=new_account_name_1,
                                           weight_threshold=weight_threshold,
                                           key_auths=key_auths)

    new_account_name_2 = "mother2111"
    ops2 = create_operation_create_account(new_account_name=new_account_name_2,
                                           weight_threshold=weight_threshold,
                                           key_auths=key_auths)

    new_account_name_3 = "mother3111"
    ops3 = create_operation_create_account(new_account_name=new_account_name_3,
                                           weight_threshold=weight_threshold,
                                           key_auths=key_auths)

    try:
        sign_and_broadcast(wif, ops1)
        sign_and_broadcast(wif, ops2)
        sign_and_broadcast(wif, ops3)
    except Exception as e:
        raise e


def create_account_with_multi_pubs_4():
    weight_threshold = 2
    new_account_name_1 = "mother41"
    pub11, pri11 = generate_key_pairs("mother41a")
    pub12, pri12 = generate_key_pairs("mother41b")
    pub13, pri13 = generate_key_pairs("mother41c")

    key_auths_1 = [[pub11, 1], [pub12, 1], [pub13, 1]]
    ops1 = create_operation_create_account(new_account_name=new_account_name_1,
                                           weight_threshold=weight_threshold,
                                           key_auths=key_auths_1)

    new_account_name_2 = "mother42"
    pub21, pri21 = generate_key_pairs("mother42a")
    pub22, pri22 = generate_key_pairs("mother42b")
    pub23, pri23 = generate_key_pairs("mother42c")

    key_auths_2 = [[pub21, 1], [pub22, 1], [pub23, 1]]
    ops2 = create_operation_create_account(new_account_name=new_account_name_2,
                                           weight_threshold=weight_threshold,
                                           key_auths=key_auths_2)

    new_account_name_3 = "mother43"
    pub31, pri31 = generate_key_pairs("mother43a")
    pub32, pri32 = generate_key_pairs("mother43b")
    pub33, pri33 = generate_key_pairs("mother43c")

    key_auths_3 = [[pub31, 1], [pub32, 1], [pub33, 1]]
    ops3 = create_operation_create_account(new_account_name=new_account_name_3,
                                           weight_threshold=weight_threshold,
                                           key_auths=key_auths_3)

    try:
        sign_and_broadcast(wif, ops1)
        sign_and_broadcast(wif, ops2)
        sign_and_broadcast(wif, ops3)
    except Exception as e:
        raise e


def create_account_with_multi_account_ath():
    new_account_name = "son"

    account_auths = [["account1", 1], ["account2", 1], ["account3", 2]]
    pub, pri = generate_key_pairs("son1")
    pub2, pri2 = generate_key_pairs("son3")
    pub3, pri3 = generate_key_pairs("son2")

    key_auths = [[pub, 1], [pub2, 1], [pub3, 1]]
    weight_threshold = 3

    ops = create_operation_create_account(new_account_name=new_account_name,
                                          weight_threshold=weight_threshold,
                                          key_auths=key_auths,
                                          account_auths=account_auths)
    try:
        sign_and_broadcast(wif, ops)
    except Exception as e:
        raise e


def create_account_with_multi_account_ath_2level():
    new_account_name = "grandson44"

    account_auths = [["son42", 1]]
    pub, pri = generate_key_pairs("grandson44")
    key_auths = [[pub, 1]]
    weight_threshold = 2

    ops = create_operation_create_account(new_account_name=new_account_name,
                                          weight_threshold=weight_threshold,
                                          key_auths=key_auths,
                                          account_auths=account_auths)
    try:
        sign_and_broadcast(wif, ops)
    except Exception as e:
        raise e


def init_balance():
    sender = creator
    receiver = "tommy"
    amount = "10.00000 BWF"
    fee = "10.00000 W"

    ops_amount = create_operation_transfer(sender=sender,
                                           receiver=receiver,
                                           amount=amount)
    ops_fee = create_operation_transfer(sender=sender,
                                        receiver=receiver,
                                        amount=fee)

    extensions = ""
    try:
        sign_and_broadcast_with_extensions(wif, ops_amount, extensions)
        # sign_and_broadcast(wif, ops_fee)
    except Exception as e:
        raise e


def test_transfer():
    sender = "son1"
    _, pri_son = generate_key_pairs("son5")
    _, pri_mother1 = generate_key_pairs("mother1")
    _, pri_mother2 = generate_key_pairs("mother2")
    _, pri_mother3 = generate_key_pairs("mother3")

    receiver = "alice"
    amount = "0.10000 BWF"
    ops_amount = create_operation_transfer(sender=sender,
                                           receiver=receiver,
                                           amount=amount)
    try:
        print("son:")
        sign_and_broadcast(pri_son, ops_amount)
        print("mother1:")
        sign_and_broadcast(pri_mother1, ops_amount)
        print("mother2:")
        sign_and_broadcast(pri_mother2, ops_amount)
        print("mother3:")
        sign_and_broadcast(pri_mother3, ops_amount)
    except Exception as e:
        raise e


def test_transfer_multi():
    sender = "son16"
    _, pri_son1 = generate_key_pairs("son1")
    _, pri_son2 = generate_key_pairs("son3")
    _, pri_son3 = generate_key_pairs("son2")

    _, pri_mother1 = generate_key_pairs("mother1")
    _, pri_mother2 = generate_key_pairs("mother2")
    _, pri_mother4 = generate_key_pairs("mother4")

    receiver = "alice"
    amount = "0.10000 BWF"

    ops_amount = create_operation_transfer(sender=sender,
                                           receiver=receiver,
                                           amount=amount)
    try:
        sign_and_broadcast_multi(ops_amount, [pri_son3, pri_mother2], 2)
    except Exception as e:
        raise e


def test_transfer_multi_2():
    sender = "son11"
    _, pri_son = generate_key_pairs("son11")
    _, pri11 = generate_key_pairs("mother11")
    _, pri12 = generate_key_pairs("mother12")
    _, pri13 = generate_key_pairs("mother13")
    _, pri21 = generate_key_pairs("mother21")
    _, pri22 = generate_key_pairs("mother22")
    _, pri23 = generate_key_pairs("mother23")
    _, pri31 = generate_key_pairs("mother31")
    _, pri32 = generate_key_pairs("mother32")
    _, pri33 = generate_key_pairs("mother33")

    receiver = "alice"
    amount = "1.00000 BWF"

    ops_amount = create_operation_transfer(sender=sender,
                                           receiver=receiver,
                                           amount=amount)
    try:
        sign_and_broadcast_multi(ops_amount, [pri_son], 1)
    except Exception as e:
        raise e


def test_transfer_multi_3():
    sender = "son1112"
    _, pri_son = generate_key_pairs("son1112")
    _, pri_same1 = generate_key_pairs("mothersame1")
    _, pri_same2 = generate_key_pairs("mothersame2")
    _, pri_same3 = generate_key_pairs("mothersame3")

    receiver = "alice"
    amount = "1.00000 BWF"

    ops_amount = create_operation_transfer(sender=sender,
                                           receiver=receiver,
                                           amount=amount)
    try:
        sign_and_broadcast_multi(ops_amount, [pri_son], 1)
    except Exception as e:
        raise e


def test_transfer_multi_4():
    sender = "son42"
    _, pri_son = generate_key_pairs("son42")
    _, pri11 = generate_key_pairs("mother41a")
    _, pri12 = generate_key_pairs("mother41b")
    _, pri13 = generate_key_pairs("mother41c")
    _, pri21 = generate_key_pairs("mother42a")
    _, pri22 = generate_key_pairs("mother42b")
    _, pri23 = generate_key_pairs("mother42c")
    _, pri31 = generate_key_pairs("mother43a")
    _, pri32 = generate_key_pairs("mother43b")
    _, pri33 = generate_key_pairs("mother43c")

    receiver = "alice"
    amount = "1.00000 BWF"

    ops_amount = create_operation_transfer(sender=sender,
                                           receiver=receiver,
                                           amount=amount)
    try:
        sign_and_broadcast_multi(ops_amount, [pri22, pri21, pri31, pri32], 4)
    except Exception as e:
        raise e


def test_transfer_multi_5():
    sender = "grandson44"
    _, pri_grandson = generate_key_pairs("grandson44")
    _, pri_son = generate_key_pairs("son42")
    _, pri11 = generate_key_pairs("mother41a")
    _, pri12 = generate_key_pairs("mother41b")
    _, pri13 = generate_key_pairs("mother41c")
    _, pri21 = generate_key_pairs("mother42a")
    _, pri22 = generate_key_pairs("mother42b")
    _, pri23 = generate_key_pairs("mother42c")
    _, pri31 = generate_key_pairs("mother43a")
    _, pri32 = generate_key_pairs("mother43b")
    _, pri33 = generate_key_pairs("mother43c")

    receiver = "alice"
    amount = "0.10000 BWF"

    ops_amount = create_operation_transfer(sender=sender,
                                           receiver=receiver,
                                           amount=amount)
    try:
        sign_and_broadcast_multi(ops_amount, [pri21, pri22, pri31, pri33, pri_grandson], 5)
    except Exception as e:
        raise e


def main():
    # generate_key_pairs()
    create_account()
    # create_account_with_multi_pubs()
    # create_account_with_multi_pubs_1()
    # create_account_with_multi_account_ath()
    # test_transfer()
    # test_transfer_multi()
    # test_transfer_multi_2()
    # create_account_with_multi_pubs_2()
    # create_account_with_multi_pubs_3()
    # create_account_with_multi_account_ath()
    # test_transfer_multi_3()
    # create_account_with_multi_pubs_3()
    # create_account_with_multi_account_ath()
    # create_account_with_multi_pubs_4()
    # test_transfer_multi_4()
    # create_account_with_multi_account_ath_2level()
    # init_balance()
    # create_account_with_multi_account_ath_2level()
    # test_transfer_multi_5()
    # create_account_with_multi_account_ath()
    # test_transfer_multi()
    # _, _ = generate_key_pairs("son1")
    # _, _ = generate_key_pairs("son2")
    # _, _ = generate_key_pairs("mother4")


if __name__ == '__main__':
    main()
