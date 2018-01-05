import traceback
from tkinter import Tk, Frame
import sys

from actions import Actions
from data_centre.data import Data
from display_centre.display import Display
from display_centre.messages import MessageHandler
from user_input.numpad_input import NumpadInput
from video_centre.video_driver import VideoDriver
import data_centre

# create tk object
tk = Tk()
frame = Frame(tk, width=500, height=400)

# setup message handler

message_handler = MessageHandler()

# setup data

data = Data(message_handler)

# setup the video driver
video_driver = VideoDriver(frame, message_handler, data)

# setup the display
display = Display(tk, video_driver, message_handler, data)

# setup the actions
actions = Actions(tk, message_handler, data, video_driver, display)

numpad_input = NumpadInput(display, actions)

frame.pack()
tk.attributes("-fullscreen", True)

try:
    tk.mainloop()
except:
    message_handler.set_message(traceback.print_tb(sys.exc_traceback, limit=1, file=sys.stdout))
