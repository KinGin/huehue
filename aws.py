import json
import os
from queue import Queue
from typing import Dict, Union, Any, List

from hue import Morse
from morse import MORSE_CODE


def read_morse(sqs, queue: Queue) -> None:

    sqs_queue = sqs.get_queue_by_name(QueueName=os.environ['morse-queue'])
    for message in sqs_queue.receive_messages():
        queue.put(parse_message('morse', message.body))

        # Let the queue know that the message is processed
        message.delete()


def read_color(sqs, queue: Queue) -> None:

    sqs_queue = sqs.get_queue_by_name(QueueName='huehue-color')
    for message in sqs_queue.receive_messages():
        queue.put(parse_message('color', message.body))

        #Let the queue know that the message is processed
        message.delete()


def parse_message(key: str, body) -> Dict[str, Union[str, Any]]:
    d = json.loads(body)
    print(d['mail']['commonHeaders']['subject'])
    if key == 'color':
        return {'key': key, 'value': d['mail']['commonHeaders']['subject']}
    else:
        return {'key': key, 'value': parse_to_morse(d['mail']['commonHeaders']['subject'])}


def parse_to_morse(message: str) -> List[Morse]:
    if message is None:
        return []

    words = message.split()
    result = []
    for word in words:
        morse_word = []
        for character in str.upper(word):
            morse_word.append(MORSE_CODE.get(character))
        result.append(morse_word)
    return result






