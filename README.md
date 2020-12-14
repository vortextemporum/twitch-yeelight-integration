## WHAT DOES THIS REPO DO?

This repo gets events of a Twitch channel, such as new subscriptions, bits, channel point claims, and flashes the Yeelight bulbs. That's all.

## USAGE

Install these libraries:

```

pip install yeelight

pip install twitchAPI

pip install python-osc

```

Change the name of _ytconfig.py to ytconfig.py and add the necessary variables, which are:

* Twitch channel name, app id and secret
* Bulb ip addresses and port

Give run permission for script:

` chmod +x ./run_yee_twitch.sh `

Run the script:

` ./run_yee_twitch.sh `
