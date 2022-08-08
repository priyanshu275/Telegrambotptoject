# first we will import modules that are required
import requests
import time
import pandas as pd

# BASE URLFOR USING TELEGRAM API

# BASE URL HAS UNIQUE TOKEN WHICH IS USED TO ACCESS YOUR BOT

base_url = "https://api.telegram.org/bot5543652418:AAEuFr4RZMHJCtdZp4T6FVj0VeQSvBd-728"

# URL HAS TSV (tab seperated value) file where question and answer asked by users are written,this file is located in github

url = "https://raw.githubusercontent.com/priyanshu275/bot/master/quest.tsv"

# it is used to read file which is present in github with help of pandas datareader module

df = pd.read_csv(url, sep="\t")


# this function is used to read message given by user

def read_message(offset):
    parameters = {
        "offset": offset
    }

    resp = requests.get(base_url + '/getUpdates', data=parameters)

    data = resp.json()

    print(data)

    for result in data["result"]:
        send_message(result["message"]["text"])

    if data["result"]:
        return data["result"][-1]["update_id"] + 1
    # this function is used to answer the question automatically


def auto_answer(message):
    answer = df.loc[df['Question'].str.lower() == message.lower()]

    if not answer.empty:
        answer = answer.iloc[0]['Answer']
        return answer
    else:
        return "Sorry,I could not understand iam learning"


# this function is used to send the message with the help of auto_answer function

def send_message(message):
    answer = auto_answer(message)

    parameters = {
        "chat_id": 5423913500,
        "text": answer
    }

    resp = requests.get(base_url + '/sendMessage', data=parameters)

    print(resp.text)


# our main function used for the bot

# intro lines
l = ["hello ", "welcome to our group",
     "first of all there are some rules that have you have to follow while being a member of this group",
     "1.donot use abusive language", "2.only topic related chats no useless talks",
     "3. no message after 9 pm", "we are happy to have you in this group"]

for intro in l:
    time.sleep(1)
    parameters = {
        "chat_id": 5423913500,
        "text": intro
    }
    resp = requests.get(base_url + '/sendMessage', data=parameters)
    print(resp.text)

offset = 0
while True:  # infinite loop
    offset = read_message(offset)
