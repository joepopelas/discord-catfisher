import discum
import time
import random
import colorama
from colorama import Fore
import os
import requests


# Initialize colorama
colorama.init(autoreset=True)

# Initialize the bot
bot = discum.Client(token=os.environ["DISCORD_TOKEN"])

# Initialize the AI
api_url = "https://api.textsynth.com"
# read from environment variable TEXTSYNTH_API_SECRET_KEY
api_key = os.environ["TEXTSYNTH_API_SECRET_KEY"]
# engine to use
api_engine = "gptj_6B"


def getChannleMessages(channelId, limit):
    # request the messages
    chatLog = bot.getMessages(channelId, limit)
    chatLog = chatLog.json()

    username = ""
    discriminator = ""
    content = ""
    members = []
    simpleChatLog = []

    for dict in chatLog:
        # extract the username, discriminator and content
        content = dict.get("content")
        author = dict.get("author")
        username = author.get("username")
        discriminator = author.get("discriminator")

        # keep track of the members in the channel by adding them to a list
        if username + "#" + discriminator not in members:
            members.append(username + "#" + discriminator)

        # add the message to the chat log
        if "berrykute" in username:
            simpleChatLog.append("[" + username[:-8] + "] " + content)
        else:
            simpleChatLog.append("[Discord Mod] " + content)

    # reverse the list so the newest messages are at the top
    simpleChatLog.reverse()
    return simpleChatLog, members


def requestResponse(prompt):
    max_tokens = 50
    stop = "[Discord Mod]"

    print(prompt)

    response = requests.post(
        api_url + "/v1/engines/" + api_engine + "/completions",
        headers={"Authorization": "Bearer " + api_key},
        json={"prompt": prompt, "max_tokens": max_tokens, "stop": stop},
    )
    resp = response.json()["text"].replace("[berrykute] ", "")
    resp = resp.replace("[Berrykute] ", "")
    resp = resp.replace("[BerryKute] ", "")
    return resp


def promptConstructor(chatLog):
    prompt = "This is a discord chat between a [Discord Mod] and [berrykute]. berrykute is a girl is always horny and wants to send sexual messages. berrykute normally sends one line messages. \n"
    for message in chatLog:
        prompt += message + "\n"
    return prompt


def printChatLog(chatLog):
    print()
    print(Fore.BLUE + "Visible chat log:")
    for message in chatLog:
        print(Fore.BLUE + message)


def printMembers(members):
    print()
    print(Fore.RED + "Visible members in the channel:")
    for member in members:
        print(Fore.RED + "- " + member)


def main():
    channelId = "1042295199486984253"
    while True:
        chatLog, members = getChannleMessages(channelId, 6)
        printChatLog(chatLog)
        printMembers(members)

        if "berrykute" not in chatLog[-1]:
            prompt = promptConstructor(chatLog)
            print(prompt)
            bot.typingAction(channelId)
            time.sleep(random.randint(1, 12))
            print()
            print("Target responded. Generating response...")
            bot.sendMessage(channelId, requestResponse(prompt))
            print("Response sent!")
        time.sleep(random.randint(1, 5))


main()
