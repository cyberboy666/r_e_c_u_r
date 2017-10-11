import logging
import math
import os
import sys
import time
import traceback
from Tkinter import *

import video_centre
import data_centre

# logger = data_centre.setup_logging()
tk = Tk()
# tk.withdraw()
canvas = Frame(tk, width=500, height=400)
# data = data_centre.data()


def key(event):
    print "pressed", repr(event.char)

canvas.bind("<Key>", key)

canvas.pack()
canvas.focus_set()
tk.mainloop()
# try:
# #    video_driver = video_centre.video_driver(canvas)
#     pass

# except Exception as e:
#     # logger.error(str(e))
