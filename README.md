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
# Note that it's best to assign a static DHCP ip to the receiver so the ip is
# always the same, then pass that it in with the -r option.
$ python -m yams # Optionally with --debug or --port.
```

This will run a web server on port 8185 by default, but this can be
changed via a `-p` flag. You can turn on debug mode by passing `-d`.

### Alexa Skill

Note this project is aimed towards developers. It's a complicated process to
set up an Amazon Echo skill, and this project has to run somewhere on the
same network as the receiver it is meant to control, otherwise you'd have
to open up access to the receiver to the internet. For example, I run Yams
on a Raspberry Pi 2. One of the more complicated aspects of setting up an
unpublished Echo Skill is that it is required that the web server has a valid
SSL certificate. Fortunately, a self-signed certificate will work for
unpublished skills and
[alexandra](https://github.com/erik/alexandra#setting-up-a-web-server), the
framework used to develop this skill, has some documentation on it and a
script to help with generating the files you need.

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

`ReceiverInputs` is the only one you'd configure differently when setting up
your own skill. You set the mappings from these slot values in the
`input_mappings.json` file.

### Activation Word

I recommend 'receiver' as the activation word for this skill. 'yams' will
work, but I had spotty luck with the Echo often thinking I was asking it to
turn itself up or down.

### Functionality

Yams can turn your receiver on and off (if network standby is enabled), turn
the volume up and down at various levels of granularity, and switch inputs
for you. Most common remote functionality is covered.

When you get bored of listening to yourself ask it "what's the yams?". If you
don't get it, you don't listen to enough Kendrick Lamar.
