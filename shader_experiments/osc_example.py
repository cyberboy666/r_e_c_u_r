from tkinter import *
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
import argparse
import threading
print('starting osc_example')

root = Tk()

def key(event):
    print("key pressed is {}".format(event.char)) 
    
    if event.char == 'q':
        print('quiting program')
        root.destroy()
    elif event.char == 'a':
        print('loading video')
        send_osc_message("/player/a/load", "/home/pi/Videos/internal_storage/480-from-adobe.mp4")
    elif event.char == 's':
        print('playing video')
        send_osc_message("/player/a/play", True)
    elif event.char == 'd':
        print('pausing video')
        send_osc_message("/player/a/play", False)
    elif event.char == 'f':
        print('making video partly transparent')
        send_osc_message("/player/a/alpha", 200)
    elif event.char == 'g':
        print('quiting video')
        send_osc_message("/player/a/quit", True)
    elif event.char == 'h':
        print('seeking video')
        send_osc_message("/player/a/position", 0.5)
    elif event.char == 'j':
        print('requesting video position')
        send_osc_message("/player/a/get_position", True)


def send_osc_message(address, value):
   client.send_message(address, value)

def set_position(unused_addr, args, player_name):
    print("the position of the player {} is {}".format(args, player_name))

def set_status(unused_addr, args, player_name):
    print("the status of the player {} is {}".format(args, player_name))

### setting up the client
client_parser = argparse.ArgumentParser()
client_parser.add_argument("--ip", default="127.0.0.1", help="the ip")
client_parser.add_argument("--port", type=int, default=8000, help="the port")

client_args = client_parser.parse_args()

client = udp_client.SimpleUDPClient(client_args.ip, client_args.port)

### setting up the server
server_parser = argparse.ArgumentParser()
server_parser.add_argument("--ip", default="127.0.0.1", help="the ip")
server_parser.add_argument("--port", type=int, default=7000, help="the port")

server_args = server_parser.parse_args()

dispatcher = dispatcher.Dispatcher()
dispatcher.map("/player/a/position", set_position, "a")
dispatcher.map("/player/b/position", set_position, "b")
dispatcher.map("/player/c/position", set_position, "c")
dispatcher.map("/player/a/status", set_status, "a")
dispatcher.map("/player/b/status", set_status, "b")
dispatcher.map("/player/c/status", set_status, "c")

server = osc_server.ThreadingOSCUDPServer((server_args.ip, server_args.port), dispatcher)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()
### setting up tk etc
frame = Frame(root, width=100, height=100)
frame.bind("<KeyPress>", key)
frame.pack()

frame.focus_set()
root.mainloop()


