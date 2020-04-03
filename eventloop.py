import threading
import time
from queue import Queue

import boto3

from aws import read_morse, read_color
from hue import morse, change_color


class EventLoop:

    def __init__(self):
        self.sqs = boto3.resource('sqs')
        self.queue = Queue(maxsize = 0)
        self.poller_thread = threading.Thread(target=self.poll_messages, args=(self.sqs, self.queue,), daemon=True)

    def start(self):

        self.poller_thread.start()
        while True:
            if not self.queue.empty():
                message = self.queue.get()
                if message['key'] == 'morse':
                    for morse_word in message['value']:
                        for word_contents in morse_word:
                            morse(word_contents)
                elif message['key'] == 'color':
                    change_color(message['value'])


    @staticmethod
    def poll_messages(sqs, queue):
        while True:
            read_morse(sqs, queue)
            read_color(sqs, queue)
            time.sleep(1)

