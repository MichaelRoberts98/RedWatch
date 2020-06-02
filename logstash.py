# Christopher Fischer
# 6/1/2020
# Last Edit: 6/1/2020 11:40 PM
# snake case naming used for convention
# Python 3

import time

import requests

# For now, we're just going to be using discord and storing the MD5 is source
# This is obviously not ideal. We do something very similar in threathunter.py
# I'll eventually make a python file to handle configuration options and get it
# from there.

discord_webhook = True
discord_username = "DoubleAgent"
discord_webhook_link = ""

groupme_webhook = False
groupme_bot_id = ""

slack_webhook = False
slack_webhook_link = ""


# Discord tested and currently works 6/2/2020 12:05 AM

# This is one of the easiest ways to do this
def __discord_webhook(message):
    return requests.post(discord_webhook_link, json={"username": "DoubleAgent", "content": message})


# this wrapper allows us to retry a few times, with dynamic scaling if we're getting API errors or ratelimits.
def __discord_try_webhook(message, number):
    code = discord_webhook(message)
    if (number == 3):
        return code
    if (code == 429 or code == 502 or (code >= 500 and code <= 599)):
        time.sleep(5 * (number + 1))
        return __discord_try_webhook(message, number + 1)
    return code


# This is the main function to call to send a discord message.
def discord_message(message):
    try:
        code = __discord_try_webhook(message, 0)
    except:
        err_log("discord_message", "Exception in discord_message")
        return


# Groupme, untested

def __groupme_webhook(message):
    return requests.post(discord_webhook_link, data={"text": message, "bot_id": groupme_bot_id})


def __groupme_try_webhook(message, number):
    code = __groupme_webhook(message)
    if (number == 3):
        return code
    if (code != 200):
        time.sleep(5 * (number + 1))
        return __groupme_webhook(message, number + 1)
    return code


def slack_message(message):
    try:
        code = __groupme_try_webhook(message, 0)
    except:
        err_log("groupme", "Exception in groupme_message")
        return


# Slack, untested.

def __slack_webhook(message):
    return requests.post(slack_webhook_link, json={"text": message})


def __slack_try_webhook(message, number):
    code = slack_webhook(message)
    if (number == 3):
        return code
    if (code != 200):
        time.sleep(5 * (number + 1))
        return __slack_try_webhook(message, number + 1)
    return code


def slack_message(message):
    try:
        code = __slack_try_webhook(message, 0)
    except:
        err_log("slack_message", "Exception in slack_message")
        return


# We should call this if something fails
def err_log(failedmethod, message):
    f = open("doubleagenterr.log", "a")
    f.write("[ERROR] Failed at giving " + message + " via " + failedmethod)
    f.close()
    return
