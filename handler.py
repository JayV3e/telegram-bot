import json
import os
import requests
from datetime import date

# Settings to specify the group chat to answer to
TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)
CHAT_ID = -368126466

# The main function when someone sends a message to botler
def router(event, context):
    # The try just means that if something goes wrong while processing, it will go to the except part and logs an error without crashing. 
    # Otherwise, all sorts of weird stuff can happen and since this is an AWS lambda function, I am not sure how this would be handled.
    try:
        # Read data from the message sent on telegram to botler
        data = json.loads(event["body"])

        # Read the actual message sent to botler
        message = str(data["message"]["text"])


        # Here are the (keyword <--> function) mapping
        # Define any new keyword here
        # Example :
        # if 'the_keyword' in message:
        # reponse = 'whatever_you_want_botler_to_respond'    // This can be a direct answer or you can use any variable that returns a string.

        if "hi botler" in message.lower():
            response = say_hi(data["message"]["from"]["first_name"])

        # message.lower() just means that the whole message will be lowercase. So if someone writes Chores, it will be converted to chores. Therefore, chore will be found in chores.
        if "chore" in message.lower():
            response =  delegate_chores()


        # This is the API call to telegram so botler can answer. 
        data = {"text": response.encode("utf8"), "chat_id": CHAT_ID}
        url = BASE_URL + "/sendMessage"
        requests.post(url, data)

    except Exception as e:
        print(e)

    # Tells AWS lambda that all is fine. HTTP status code means 'OK', while 404 means 'page not found' ;)

    return {"statusCode": 200}


def say_hi(first_name):
    return "Hello {}".format(first_name)

def delegate_chores():
    chores = ['Cuisine / Kitchen', 'Toilette / Toilet', 'Salon / Living Room', 'Escalier / Stairs']
    roomates = ['Jerome', 'Megan', 'Miwako', 'Andrew']

    # This just means that the 4 items in chores will swap place n times, n being the week of the year we are in out of 52. 
    # First week of the year, they will swap once, so kitchen goes last, toilet becomes first ... 
    [chores.append(chores.pop(chores.index(chores[0]))) for i in range(date.today().isocalendar()[1])]
    
    # Since chores are already swapped, I only print the names and the chores in sequential order.
    return "This week chores are : \n" + ''.join([roomate + " : " + chores.pop(0) + "\n" for roomate in roomates])


# The daily messages. They are triggered in the serverless.yml file and give the actual message to the send_basic_message function
def monday(event, context):
    delegate_chores()
    send_basic_message("\n 🍌🍌 Today is compost day 🍌🍌")

def wednesday(event, context):
    send_basic_message("\n ♻️♻️ Today is recycling day ♻️♻️")

def thursday(event, context):
    delegate_chores()
    send_basic_message("\n 🚮🚮 Today is garbage day 🚮🚮. \n \n Also don't forget to place your order for Lufa Farms.")

# This function only prevents from rewriting the configuration in every daily message function. 
def send_basic_message(message):
    url = BASE_URL + "/sendMessage"
    data = {"text": message.encode("utf8"), "chat_id": CHAT_ID}
    requests.post(url, data)
    return {"statusCode": 200}

# Monthly message that includes a photo so it can't use the send_basic_message function
def monthly(event, context):
    url = BASE_URL + "/sendPhoto"
    data = {
        "text": response.encode("utf8"), 
        "chat_id": CHAT_ID,
        "caption": "Today is rent day !!",
        "photo": "http://3.bp.blogspot.com/_vj2e1m7Hlgw/SwGAMlTZwtI/AAAAAAAAbOU/h_p1cFZzwjk/s1600/monopoly.jpg"
    }
    requests.post(url, data)
    return {"statusCode": 200}

