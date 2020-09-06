import os
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
import app2
from slack.errors import SlackApiError

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(os.environ["SLACK_SIGNING_SECRET"], "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

def send_direct_message(firstId, secondId):
    return slack_web_client.conversations_open(
        users=[firstId, secondId])

def send_message(channel, text):
    try:
        response = slack_web_client.chat_postMessage(
            channel=channel,
            text=text
  )
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'


if __name__ == '__main__':

    response = slack_web_client.conversations_list()
    conversations = response["channels"]
    conv_ids = list(map(lambda u: u["id"], conversations))
    print(conv_ids)
    for conv in conv_ids:
        print(conv)
        response = slack_web_client.conversations_members(channel=conv)
        user_ids = response["members"]
        print(user_ids)

    send_message(conv, "Hi guys, how you doing")


    app2.main()
