import traceback
from tkinter import Tk, Frame
import sys

from actions import Actions
from data_centre.data import Data
from display_centre.display import Display
from display_centre.messages import MessageHandler
from user_input.numpad_input import NumpadInput
from user_input.midi_input import MidiInput
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
display = Display(tk, video_driver, message_handler, data)

# setup the actions
actions = Actions(tk, message_handler, data, video_driver, capture, display)

numpad_input = NumpadInput(tk, message_handler, display, actions, data)
midi_input = MidiInput(tk, message_handler, display, actions, data)

frame.pack()
tk.attributes("-fullscreen", True)

try:
    tk.mainloop()
except:
    message_handler.set_message(traceback.print_tb(sys.exc_traceback, limit=1, file=sys.stdout))
