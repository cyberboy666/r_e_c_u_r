#!/usr/bin/python

import traceback
from tkinter import Tk, Frame
import sys
import tracemalloc

from actions import Actions
from data_centre.data import Data
from display_centre.display import Display
from display_centre.messages import MessageHandler
from user_input.numpad_input import NumpadInput
from user_input.midi_input import MidiInput
from user_input.analog_input import AnalogInput
from video_centre.video_driver import VideoDriver
from video_centre.capture import Capture
import data_centre

# create tk object
tk = Tk()
frame = Frame(tk, width=500, height=400)

# setup message handler

message_handler = MessageHandler()

# setup data

data = Data(message_handler)

# setup the video driver
video_driver = VideoDriver(tk, message_handler, data)
capture = Capture(tk, message_handler, data)

# setup the display
display = Display(tk, video_driver, capture, message_handler, data)

# setup the actions
actions = Actions(tk, message_handler, data, video_driver, capture, display)

numpad_input = NumpadInput(tk, message_handler, display, actions, data)
midi_input = MidiInput(tk, message_handler, display, actions, data)
analog_input = AnalogInput(tk, message_handler, display, actions, data)

actions.check_and_set_output_mode_on_boot()
actions.check_dev_mode()
actions.toggle_x_autorepeat()

frame.pack()
tk.attributes("-fullscreen", True)

def handle_error(exc, val, tb):
    print('traceback for error : {}'.format(traceback.format_exc()))
    message_handler.set_message('ERROR', val, traceback.format_exc())

tk.report_callback_exception = handle_error


tk.mainloop()

