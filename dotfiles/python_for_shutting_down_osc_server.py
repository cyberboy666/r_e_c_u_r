import argparse

from pythonosc import udp_client


def setup_osc_client(ip, port):
    client_parser = argparse.ArgumentParser()
    client_parser.add_argument("--ip", default=ip, help="the ip")
    client_parser.add_argument("--port", type=int, default=port, help="the port")

    client_args = client_parser.parse_args()

    return udp_client.SimpleUDPClient(client_args.ip, client_args.port)


client = setup_osc_client('127.0.0.1', 5433)
client.send_message("/shutdown", True)

client = setup_osc_client('127.0.0.1', 9000)
client.send_message("/shutdown", True)
