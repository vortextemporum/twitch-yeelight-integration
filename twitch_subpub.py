from twitchAPI.pubsub import PubSub
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
from pprint import pprint
from uuid import UUID

from pythonosc import osc_message_builder
from pythonosc import udp_client
import socket

from ytconfig import APP_ID, APP_SECRET, TWITCH_CHANNEL_NAME

client = udp_client.SimpleUDPClient('127.0.0.1', 4545)
client._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


def callback_function(uuid: UUID, data: dict) -> None:
    print('got callback for UUID ' + str(uuid))
    client.send_message("/message", "got callback!")
    pprint(data)


app_id = APP_ID

app_secret = APP_SECRET

# setting up Authentication and getting your user id
twitch = Twitch(app_id, app_secret)
twitch.authenticate_app([])

target_scope = [AuthScope.WHISPERS_READ, AuthScope.CHANNEL_READ_REDEMPTIONS, AuthScope.CHANNEL_SUBSCRIPTIONS, AuthScope.BITS_READ]

auth = UserAuthenticator(twitch, target_scope, force_verify=False)
# this will open your default browser and prompt you with the twitch verification website
token, refresh_token = auth.authenticate()

print(token, refresh_token)

# add User authentication

twitch.set_user_authentication(token, target_scope, refresh_token)

# starting up PubSub
pubsub = PubSub(twitch)
pubsub.start()

user_id = twitch.get_users(logins=[TWITCH_CHANNEL_NAME])['data'][0]['id']
pprint(twitch.get_users(logins=[TWITCH_CHANNEL_NAME]))
# you can either start listening before or after you started pubsub.

# uuid1 = pubsub.listen_whispers(user_id, callback_function)
uuid2 = pubsub.listen_channel_points(user_id, callback_function)
uuid3 = pubsub.listen_channel_subscriptions(user_id, callback_function)
uuid4 = pubsub.listen_bits(user_id, callback_function)

# print(uuid2)
input('press ENTER to close...')

# you do not need to unlisten to topics before stopping but you can listen and unlisten at any moment you want

# pubsub.unlisten(uuid1)
pubsub.unlisten(uuid2)
pubsub.unlisten(uuid3)
pubsub.unlisten(uuid4)

pubsub.stop()