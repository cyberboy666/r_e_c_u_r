from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import dispatcher
import argparse

def setup_osc_client():
    client_parser = argparse.ArgumentParser()
    client_parser.add_argument("--ip", default="127.0.0.1", help="the ip")
    client_parser.add_argument("--port", type=int, default=5433, help="the port")

    client_args = client_parser.parse_args()

    return udp_client.SimpleUDPClient(client_args.ip, client_args.port)

client = setup_osc_client()

client.send_message("/shutdown", True)
