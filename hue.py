import json
import time
from idlelib.multicall import r
from typing import List, Tuple

import requests
import os

from rgbxy import Converter

Morse = List[bool]


def base_address(hue = os.environ['hue-ip'], user = os.environ['hue-user'], postfix = ''):
    return 'http://{}/api/{}/{}'.format(hue, user, postfix)


def change_color():
    print(os.environ['user'])


def get_lights():
    request = requests.get(base_address(postfix = 'lights'))
    print(request.content)


def get_groups():
    request = requests.get(base_address(postfix = 'groups'))
    print(request.content)


def get_hex_color_payload(hex_color: str, transitiontime: int = 400):
    return {'xy': Converter().hex_to_xy(hex_color), 'transitiontime': transitiontime}


def change_color(hex_color, lamp_id):
    postfix = 'lights/{}/state/'.format(lamp_id)
    paylod = get_hex_color_payload(hex_color = hex_color)
    request = requests.put(base_address(postfix = postfix), data = json.dumps(paylod))
    print(request.content)

def lamp_is_on(lamp_id) -> bool:
    postfix = 'lights/{}/'.format(lamp_id)
    lamp_response = requests.get(base_address(postfix = postfix)).json()
    return lamp_response['state']['on'] == True


def light_off_on(lamp_id):
    postfix = 'lights/{}/state/'.format(lamp_id)
    request = requests.put(base_address(postfix = postfix), data = json.dumps({"on": not lamp_is_on(lamp_id)}))
    print(request.content)


def morse(code: Morse, lamp_id: int):
    postfix = 'lights/{}/state/'.format(lamp_id)

    short_first = 'ffc003'
    short_second = 'fff069'
    long_first = '0005ff'
    long_second = '7770ff'
    morse_start = 'fc2403'

    start_payload = get_hex_color_payload(morse_start, 0)
    start_payload['on'] = True
    requests.put(base_address(postfix = postfix), data = json.dumps(start_payload))
    time.sleep(1)

    current_short = short_first
    current_long = long_first

    for letter in code:

        if letter:
            time.sleep(0.5)
            payload = get_hex_color_payload(current_long, 0)
            requests.put(base_address(postfix = postfix), data = json.dumps(payload))
            current_long = long_first if current_long == long_second else long_second

        else:
            time.sleep(0.5)
            payload = get_hex_color_payload(current_short, 0)
            payload['on'] = True
            requests.put(base_address(postfix = postfix), data = json.dumps(payload))
            current_short = short_first if current_short == short_second else short_second


