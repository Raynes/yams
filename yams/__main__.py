import sys
import argparse
import flask
import rxv

app = flask.Flask('yams')


def get_reciever():
    try:
        return rxv.find()[0]
    except:
        print("No reciever founpd!")
        sys.exit(1)

reciever = get_reciever()


def server(port, debug):
    app.run('0.0.0.0', port, debug=debug)


def _format_response(message):
    body = {
        'version': '1.0',
        'sessionAttributes': {},
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': message
            },

            'shouldEndSession': True
        }
    }

    return flask.jsonify(**body)


def set_volume(req):
    slots = req['intent']['slots']
    direction = slots['Direction']['value']
    tweak = slots['VolumeTweak'].get("value", "")
    current_volume = reciever.volume
    if tweak == "a lot" or tweak == "a bunch":
        vol = 10.0
    elif tweak == "a little" or tweak == "a bit" or tweak == "a tad":
        vol = 2.0
    else:
        vol = 5.0

    if direction == 'up':
        new_volume = current_volume + vol
        if new_volume >= -100:
            reciever.volume = new_volume
            return _format_response("Turning it up {}".format(tweak))
        else:
            return _format_response("Can't turn it up this high")
    else:
        new_volume = current_volume - vol
        if new_volume <= -1:
            reciever.volume = new_volume
            return _format_response("Turning it down {}".format(tweak))
        else:
            return _format_response("Can't turn it down this low")


def set_state(req):
    pass


def set_input(req):
    pass


@app.route('/yams', methods=['POST'])
def dispatch_request():
    body = flask.request.get_json()
    req = body['request']

    if req['type'] != 'IntentRequest':
        return 'nope', 400

    intent_handler = {
        'SetVolume': set_volume,
        'SetPowerState': set_state,
        'SetInput': set_input
    }.get(req['intent']['name'])

    if intent_handler:
        return intent_handler(req)

    return 'NO.', 400

if __name__ == '__main__':
    description = "Yamaha reciever controller for Amazon Echo devices"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-p', '--port',
                        type=int,
                        default=8185,
                        help="Port to run the server on.")
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    server(args.port, args.debug)
