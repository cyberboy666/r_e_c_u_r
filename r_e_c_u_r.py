import traceback
from tkinter import Tk, Frame
import sys

from user_input.actions import Actions
from display_centre.display import Display
from user_input.numpad_input import NumpadInput
from video_centre.video_driver import VideoDriver
import data_centre

## create tk object
tk = Tk()
frame = Frame(tk, width=500, height=400)

## setup the video driver
video_driver = VideoDriver(frame)

## setup the display
display = Display(tk, video_driver)

## setup the actions
actions = Actions(tk, video_driver, display)

numpad_input = NumpadInput(display, actions)

frame.pack()
tk.attributes("-fullscreen", True)

try:
    tk.mainloop()
except:
    data_centre.set_message(traceback.print_tb(sys.exc_traceback, limit=1, file=sys.stdout))
