# Juniper - Copyright © 2025 Federico Santandrea.
# All rights reserved.
#     
# Unauthorized copying, distribution, or use of this software in whole or in part
# is prohibited without the express written permission of the copyright holder.
#
# First: pip install ollama meshtastic
# Then prepare ollama model with: ollama create juniper -f Modelfile.juniper
#

import time
import logging

import ollama

import meshtastic
import meshtastic.serial_interface
from pubsub import pub

#

SIZE = 180
LOGBACK = 4

LOG_FILE = "juniper.log"

logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

histories = {}
interface = meshtastic.serial_interface.SerialInterface()
myID = f"!{interface.getNode("^local").nodeNum:x}"


def onReceive(packet, interface):
    fromId = packet["fromId"]
    toId = packet["toId"]

    text = packet["decoded"]["text"]

    if toId == myID:
        logger.info(f"{fromId} >>> {text}")

        usermsg = {"role": "user", "content": text}

        if text == "/clear":
            del histories[fromId]
            return

        if fromId not in histories:
            histories[fromId] = []

        histories[fromId].append(usermsg)
        histories[fromId] = histories[fromId][-LOGBACK:]

        msg = ollama.chat(
            model='juniper',
            messages=histories[fromId],
            keep_alive=-1
        )["message"]

        histories[fromId].append(msg)

        logger.info(f'{fromId} <<< {msg["content"]}')

        for chunk in split_on_word_boundary(msg["content"].strip(), SIZE):
            interface.sendText(chunk, destinationId=fromId)

def split_on_word_boundary(text, size):
    start = 0
    while start < len(text):
        end = start + size
        if end >= len(text):
            yield text[start:]
            break

        space_index = text.rfind(" ", start, end)
        if space_index == -1 or space_index <= start:
            yield text[start:end]
            start = end
        else:
            yield text[start:space_index]
            start = space_index + 1

logger.info("Juniper server started")

pub.subscribe(onReceive, "meshtastic.receive.text")

while True:
    time.sleep(1)
