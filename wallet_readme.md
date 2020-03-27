Start in: build/programs/cli_wallet

./cli_wallet -s ws://<IP-Node>:<Port-RPC>

Ex:
./cli_wallet -s ws://34.80.107.9:9876

# SET PASS AND UNLOCK WALLET

set_password <Password>

Ex:
set_password SUPER_SAFE_PASSWORD

unlock SUPER_SAFE_PASSWORD

---------------------------------------------------------------
-- account "initminer"
initminer:

import_key 5JLMze1sUVPhUBwTVjZyQhFMGfbN5KB7nqHfKjXuN5GUTYTbYFy
---------------------------------------------------------------

*Require: Need Unlock before using wallet client

# CREATE NEW KEY: 
unlocked >>> suggest_brain_key

- private key for setting up node: wif_priv_key
- block signing key: pub_key

Ex:
unlocked >>> suggest_brain_key
{
  "brain_priv_key": "PAWN INSIST ORARY SIMMON THIRST NONIC CHOROGI CASSON DESSERT YACHAN ERICAL QUAFFER OXLIKE RIBBAND LOOPLET TEANAL",
  "wif_priv_key": "5JPTEc5fuzWrt3rZbk2qtAJc2Xt98vEkP6owgXKvUjHRRSLJf8X",
  "pub_key": "KNO8eNn2BJnSceLPBkvQa5PgQimghaR3METb2ZDuwb8hQsRhYCjfr"
}

1. Get owner key:
get_private_key_from_password <name account> owner <wif_priv_key>

Ex:
get_private_key_from_password alice owner 5JPTEc5fuzWrt3rZbk2qtAJc2Xt98vEkP6owgXKvUjHRRSLJf8X
[
  "KNO6TFjgmHqyHzFUerTeS7FQpc9bymnNTe5M2CLDtkxo43YT7qjEp",
  "5HpMd7XSKtfX7esYHjVJHShBKyBZ5RBu5UBZAnD1Xdq4bmnxUz6"
]

2. Get other keys:
get_private_key_from_password <name account> active/posting/memo <wif_priv_key>

Ex:
get_private_key_from_password alice active 5JPTEc5fuzWrt3rZbk2qtAJc2Xt98vEkP6owgXKvUjHRRSLJf8X
[
  "KNO8VCwLEyMxGfwhS5YzftdGgBJ5bTM1o2HD2DMFJPGxMgfXofiEE",
  "5KHkrYsNigUNdYhgDVgtDwCprKWLz2R9xt5mAn9sMr7JMkMGg6X"
]
import_key 5KHkrYsNigUNdYhgDVgtDwCprKWLz2R9xt5mAn9sMr7JMkMGg6X

get_private_key_from_password alice posting 5JPTEc5fuzWrt3rZbk2qtAJc2Xt98vEkP6owgXKvUjHRRSLJf8X
[
  "KNO84MewS3fZ7McHknwurNjYctFxQT8mJbZ7L5S5yJaiuySADv8NE",
  "5Hurc4eopwYCptutKH9FxaaSZAng1tWyCGvBT35QGLF7yCyKRmU"
]
import_key 5Hurc4eopwYCptutKH9FxaaSZAng1tWyCGvBT35QGLF7yCyKRmU

get_private_key_from_password alice memo 5JPTEc5fuzWrt3rZbk2qtAJc2Xt98vEkP6owgXKvUjHRRSLJf8X
[
  "KNO6HrtDs32ic4P2azHeTfnZorxHan5pSx3xoELXviMHFimoJTTm1",
  "5JbRCzMSrRRByDGvWmtqX6BmFy2KLRybyt8GY21wNLmSsgr9bHB"
]


# CREATE ACCOUNT WITH KEY

* Require: Wif_pri_key of Creator

create_account_with_keys initminer alice "" KNO6TFjgmHqyHzFUerTeS7FQpc9bymnNTe5M2CLDtkxo43YT7qjEp KNO8VCwLEyMxGfwhS5YzftdGgBJ5bTM1o2HD2DMFJPGxMgfXofiEE KNO84MewS3fZ7McHknwurNjYctFxQT8mJbZ7L5S5yJaiuySADv8NE KNO6HrtDs32ic4P2azHeTfnZorxHan5pSx3xoELXviMHFimoJTTm1 true

# IMPORT ACCOUNT TO WALLET (wallet.json)

Import 4 keys (owner/active/posting/memo)

Ex:
alice:
import_key 5HpMd7XSKtfX7esYHjVJHShBKyBZ5RBu5UBZAnD1Xdq4bmnxUz6
import_key 5KHkrYsNigUNdYhgDVgtDwCprKWLz2R9xt5mAn9sMr7JMkMGg6X 
import_key 5Hurc4eopwYCptutKH9FxaaSZAng1tWyCGvBT35QGLF7yCyKRmU
import_key 5JbRCzMSrRRByDGvWmtqX6BmFy2KLRybyt8GY21wNLmSsgr9bHB


# CREATE ACCOUNT BY ANOTHER ACCOUNT

*Require: Client has account/4 private keys of creator

create_account <creator> <new_account_name> <json_meta> <bool broadcast>

Ex:
create_account initminer alice "" true
create_account alice jack "" true

TODO: Can not get block signing key and super private key

# TRANSFER TOKEN

transfer <from> <to> <asset amount> <fee amount> <memo> <bool broadcast>

Ex:
transfer "initminer" "alice" "100000.000 KNOW" "0.005 EUR" "Transfer from cli wallet" true


# PUBLISH PRICE FEED

*Require: Account has been a witness

publish_feed <witness> <price exchange_rate> <bool broadcast>

Ex:
publish_feed initminer {"base":"5.000 EUR","quote":"1.000 KNOW"} true


# HOW TO BECOME A WITNESS

1. Create new account

2. Broadcast your intent to become a witness

*Require: Account need Token amount to become a witness

update_witness <your-witness-name> <your-witness-post> <your-public-brain-key> <const chain_properties & props> <bool broadcast>

Ex: 
update_witness alice "http://192.168.1.111/@alice" KNO8eNn2BJnSceLPBkvQa5PgQimghaR3METb2ZDuwb8hQsRhYCjfr {"account_creation_fee":"0.100 KNOW", "maximum_block_size":131072,"sbd_interest_rate":0} true

3. Get votes

Account votes for witness

vote_for_witness <account_to_vote_with> <witness_to_vote_for> <bool approve> <bool broadcast>

Ex:
vote_for_witness initminer jayce true true

Refs:
- https://steemit.com/steemhelp/@hannixx42/cliwallet-commands-v0
