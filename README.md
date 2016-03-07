# yams

A Python web service for controlling Yamaha receivers from an Amazon echo
device.

## Usage

Yams is super easy to run. Just get Python 3.5.1 (I highly recommend
[pyenv](https://github.com/yyuu/pyenv)) and do the following inside this
directory.

```shell
$ pyvenv env
$ . env/bin/activate
$ pip install .
$ python -m yams # Optionally with --debug or --port.
```

This will run a web server on port 8185 by default, but this can be
changed via a `-p` flag. You can turn on debug mode by passing `-d`.

Getting a self signed SSL certificate and nginx set up to proxy this guy is
not an entirely trivial process, but
[alexandra](https://github.com/erik/alexandra#setting-up-a-web-server) has
some documentation on it and a script to help with generating the files you
need. The `alexandra` project is the framework used to develop this app.

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
  * chromecast
  * playstation
  * play station

Note all `RecieverInputs` should be lowercase.
