# -*- coding: utf-8 -*

from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import dataset
import logging
import dotenv
import signal
import sys
import os

class SlackHandler(logging.Handler):

    def __init__(self, token, channel, username):
        super().__init__()
        self.setLevel(logging.ERROR)

        self.client = WebClient(token=token)
        self.channel = channel
        self.username = username

    def emit(self, record):
        try:
            message = self.format(record)

            response = self.client.chat_postMessage(
                channel=self.channel, 
                username=self.username,
                text=message
            )

            logging.debug(response)

        except  SlackApiError as ex:
            print(ex)

dotenv_path = os.path.join(os.getcwd(), ".env")
dotenv.load_dotenv( dotenv_path )

LOG_LEVEL = os.getenv("LOG_LEVEL") or 'INFO'

if LOG_LEVEL.lower() == "DEBUG":
    logging.basicConfig(
        format='%(asctime)s.%(msecs).03d [%(pathname)s:%(lineno)d] %(levelname)s - %(message)s',  
        level=logging.DEBUG
    )    
else:
    logging.basicConfig(
        format='%(asctime)s.%(msecs).03d %(levelname)s - %(message)s', 
        level=logging.INFO
    )

SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL')
SLACK_USERNAME = os.getenv('SLACK_USERNAME')

if SLACK_BOT_TOKEN and SLACK_CHANNEL and SLACK_USERNAME:
    logging.getLogger("").addHandler( SlackHandler(SLACK_BOT_TOKEN, SLACK_CHANNEL, SLACK_USERNAME) )

def handle_sigint(signum, frame):
    logging.info("sigint received (%d)", signum)
    sys.exit(0)

def handle_sigterm(signum, frame):
    logging.warning("sigterm received (%d)", signum)
    sys.exit(0)

signal.signal(signal.SIGINT,  handle_sigint)
signal.signal(signal.SIGTERM, handle_sigterm)

CONFIG_URL = os.getenv('CONFIG_URL') or "sqlite:///mydatabase.db"

db = dataset.connect(CONFIG_URL)
table = db['config']

##
#

def get(name, default=None, type=None):
    res = table.find_one(name=name)
    
    if res is None:
        return default
    
    value = res['value']
    
    if type is datetime:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
    
    return value

##
#

def set(name, value):
    data = dict(name=name, value=str(value))
    table.upsert(data, ['name'])
 
