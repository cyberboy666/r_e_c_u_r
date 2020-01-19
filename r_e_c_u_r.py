#!/usr/bin/python

import traceback
from tkinter import Tk, Frame
import sys
import tracemalloc
import argparse
from pythonosc import udp_client

from actions import Actions
from data_centre.data import Data
from display_centre.display import Display
from display_centre.messages import MessageHandler
from user_input.numpad_input import NumpadInput
from user_input.osc_input import OscInput
from user_input.midi_input import MidiInput
from user_input.analog_input import AnalogInput
from video_centre.video_driver import VideoDriver
#from video_centre.capture import Capture
from video_centre.shaders import Shaders
import data_centre

# create tk object
tk = Tk()
frame = Frame(tk, width=500, height=400)

# setup message handler

message_handler = MessageHandler()

# setup data

data = Data(message_handler)

def setup_osc_client():
    client_parser = argparse.ArgumentParser()
    client_parser.add_argument("--ip", default="127.0.0.1", help="the ip")
    client_parser.add_argument("--port", type=int, default=8000, help="the port")

    client_args = client_parser.parse_args()

    return udp_client.SimpleUDPClient(client_args.ip, client_args.port)

osc_client = setup_osc_client()
# setup the video driver
video_driver = VideoDriver(tk, osc_client, message_handler, data)
#capture = Capture(tk, osc_client, message_handler, data)
shaders = Shaders(tk, osc_client, message_handler, data)

# setup the display
display = Display(tk, video_driver, shaders, message_handler, data)

# setup the actions
actions = Actions(tk, message_handler, data, video_driver, shaders, display, osc_client)
message_handler.actions = actions

numpad_input = NumpadInput(tk, message_handler, display, actions, data)
osc_input = OscInput(tk, message_handler, display, actions, data)
midi_input = MidiInput(tk, message_handler, display, actions, data)

analog_input = AnalogInput(tk, message_handler, display, actions, data)

actions.check_and_set_output_mode_on_boot()
actions.check_dev_mode()
actions.check_if_should_start_openframeworks()
actions.toggle_x_autorepeat()

frame.pack()
tk.attributes("-fullscreen", True)

def handle_error(exc, val, tb):
    print('traceback for error : {}'.format(traceback.format_exc()))
    message_handler.set_message('ERROR', val, traceback.format_exc())



tk.report_callback_exception = handle_error


tk.mainloop()

