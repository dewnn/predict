import json
import requests
import time

TOKEN = "insert_token"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def check_connection(url):
    try:
        _ = requests.get(url, timeout=5)
        return True
    except requests.ConnectionError:
        print("No connection")
    return False


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = URL + "getUpdates"
    js = get_json(url)
    return js


def get_users(updates):
    # We get the id's of every user to send them messages
    num_updates = len(updates["result"])
    id_list = list(set([updates["result"][i]["message"]["chat"]["id"] for i in range(num_updates)]))
    return id_list


def broadcast(id_list, message):
    # Send the message
    for user_id in id_list:
        url = URL + "sendMessage?text={}&chat_id={}".format(message, user_id)
        get_url(url)


def send_message(user_id, message):
    url = URL + "sendMessage?text={}&chat_id={}".format(message, user_id)
    get_url(url)


def show_bets(updates, text):
    last_text = updates["result"][-1]["message"]["text"]
    user_id = updates["result"][-1]["message"]["chat"]["id"]
    if last_text == "/kupon" and len(updates["result"]) > 0:
        send_message(user_id, text)
    time.sleep(15)