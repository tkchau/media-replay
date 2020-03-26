from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json 
import requests
import urllib.request
import time
import socket

TOKEN = "1114645856:AAEYwY2ld83KrjuZPdybPVwUIDfihqGOtrs"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

if __name__ == '__main__':
  while True:
    #code = (urllib.request.urlopen("https://testnet-bw.beowulfchain.com").getcode())
    #code = (urllib.request.urlopen("http://127.0.0.1:8080", timeout=5).getcode())
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    code  = sock.connect_ex(('127.0.0.1', 8080))
    if code != 0 :
       send_message("hi pls check API of beowulf" , 523300027)
    time.sleep(60)
