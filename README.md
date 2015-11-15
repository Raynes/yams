# yams

A Python web service for controlling Yamaha receivers from an Amazon echo device.

## Usage

This is a Python 3 Flask app. Set it up like so:

```
$ pyvenv .env
$ . .env/bin/activate
$ pip install --editable .
$ python -m yams
```

This will run a web server on port 8185 by default, but this can be
changed via a `-p` flag. You can turn on debug mode by passing `-d`.

Getting a self signed SSL certificate and nginx set up to proxy this thing
is an exercise left to the reader and Amazon's excellentish documentation on
the subject.

Intents and utterances are included in `intents.json` and `utterances.txt`,
respectively. All slots are custom types, which I have set as follows on my
own skill:

* `Directions`
  * up
  * down
* `VolumeOptions`
  * a little
  * a bit
  * a lot
  * a bunch
* `ReceiverPowerStates`
  * on
  * off
* `RecieverInputs`
  * Chromecast
  * Playstation

Currently, only volume control is implemented. ReceiverInputs will map
via configuration to actual receiver inputs. On and off is easy, but Erik
needs _something_ to do. <3
