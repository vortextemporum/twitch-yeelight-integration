from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from yeelight import *

from ytconfig import BULB1_IP, BULB2_IP, BULB_PORT

bulb1 = Bulb(BULB1_IP,BULB_PORT)
bulb2 = Bulb(BULB2_IP,BULB_PORT)

transitions = [HSVTransition(hue, 100, duration=50)
               for hue in range(0, 359, 40)]

flow = Flow(
    count=10,
    # action=Flow.actions.off,
    transitions=transitions
)

# bulb1.turn_on()

def print_handler(address, *args):
    print(f"{address}: {args}")


def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")
    bulb1.start_flow(flow)
    bulb2.start_flow(flow)


dispatcher = Dispatcher()
dispatcher.map("/something/*", print_handler)
dispatcher.set_default_handler(default_handler)

ip = "127.0.0.1"
port = 4545

server = BlockingOSCUDPServer((ip, port), dispatcher)
server.serve_forever()  # Blocks forever