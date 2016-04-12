import sys
import json
import argparse
from pathlib import Path
import asyncio

import rxv
import alexandra

# Load input mappings and make sure the keys are lowercase.
input_map = json.load(Path('input_mappings.json').open())
input_map = {k.lower(): v for k, v in input_map.items()}

app = alexandra.Application()
rxv_ip = None


async def _get_receiver(ip=None):
    rec = None
    if rxv_ip:
        rec = rxv.RXV('http://{}:80/YamahaRemoteControl/ctrl'.format(rxv_ip))
    try:
        rec = rxv.find()[0]
    except:
        print("No receiver found!")
        sys.exit(1)
    rec.volume
    return rec


async def try_receiver(ip=None):
    await asyncio.wait_for(_get_receiver(ip), 3.0)


def get_receiver(ip=None):
    """If ip is passed in, test that it's accepting requests or raise an
    exception. If ip is not passed in, fallback to ssdp search.

    """
    loop = asyncio.get_event_loop()
    receiver = loop.run_until_complete(try_receiver(ip))
    loop.close()
    return receiver


def server(port, ip, debug):
    """Run a webserver on 0.0.0.0 with the specified port and debug
    options

    """
    global rxv_ip
    rxv_ip = ip
    app.run('0.0.0.0', port, debug=debug)


@app.intent('SetVolume')
def set_volume(slots, session):
    """Implements the SetVolume intent. Depending on the slot values,
    turns the receiver volume up and down at varying granularities described
    below:


    'turn it [down|up]': tick the volume 5.0 decibels up or down.

    'turn it [down|up] [a little|a bit|a tad]': tick the volume 2.0 decibels
    up or down.

    'turn it [down|up] [a lot|a bunch]': tick the volume 10.0 decibels up or
    down.

    You'll receive a response indicating that it understood exactly whats
    you meant.

    """
    receiver = get_receiver(rxv_ip)
    direction = slots['Direction']
    valid_tweaks = ['a lot', 'a bunch', 'a little', 'a bit', 'a tad']
    tweak = slots.get('VolumeTweak', "")
    if tweak not in valid_tweaks:
        tweak = ''
    current_volume = receiver.volume
    if tweak == "a lot" or tweak == "a bunch":
        vol = 10.0
    elif tweak == "a little" or tweak == "a bit" or tweak == "a tad":
        vol = 2.0
    else:
        vol = 5.0

    if direction == 'up':
        new_volume = current_volume + vol
        if new_volume >= -100:
            receiver.volume = new_volume
            return alexandra.respond("Turning it up {}".format(tweak))
        else:
            return alexandra.respond("Can't turn it up this high")
    else:
        new_volume = current_volume - vol
        if new_volume <= -1:
            receiver.volume = new_volume
            return alexandra.respond("Turning it down {}".format(tweak))
        else:
            return alexandra.respond("Can't turn it down this low")


@app.intent("SetPowerState")
def set_state(slots, session):
    """Implements the SetPowerState intent, allowing you to ask the skill
    to 'turn [on|off]' using phrasing dictated in your utterances.

    """
    receiver = get_receiver(rxv_ip)
    state = slots['State']
    if state in ['on', 'off']:
        receiver.on = state == "on"
        return alexandra.respond("Powering {}".format(state))
    else:
        return alexandra.respond("You need to tell me to power on or off")


@app.intent("WhatsTheYams")
def whats_the_yams():
    """An effective way to determine what the yams is."""
    return alexandra.respond("The yams is the power that be!"
                             " You can smell it when I'm walking down"
                             " the street!")


@app.intent("SetInput")
def set_input(slots, session):
    """Implements the SetInput intent.

    This one expects that you've already mapped your `RecieverInputs` slot
    values in the input_mappings.json file and Amazon Echo Skill config. It
    is a simple mapping of recognizable words to actual Yamaha input names.

    Example usage given my input mappings would be 'switch to chromecast'.

    """
    input = slots['Input'].lower()

    if input in input_map:
        receiver = get_receiver(rxv_ip)
        actual_input = input_map[input]
        receiver.input = actual_input
        return alexandra.respond("Switched input to {}".format(actual_input))
    else:
        return alexandra.respond("Input not recognized")


if __name__ == '__main__':
    description = "Yamaha receiver controller for Amazon Echo devices"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-p', '--port',
                        type=int,
                        default=8185,
                        help="Port to run the server on.")
    parser.add_argument('-r', '--receiver',
                        help="Explicitly pass reciever ip.",
                        default=None)
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    server(args.port, args.receiver, args.debug)
