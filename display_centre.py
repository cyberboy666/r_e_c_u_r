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
video_driver = video_centre.video_driver(canvas)

def key(event):
    print "pressed", repr(event.char)
    print "video position is :{}".format(video_driver.current_player.get_position())
    if(event.char in ['0','1','2'] ):
        print 'updating next bank'
        data_centre.update_next_bank_number(int(event.char))
        video_driver.next_player.reload_content()

canvas.bind("<Key>", key)

canvas.pack()
canvas.focus_set()



tk.mainloop()
# try:
# #    video_driver = video_centre.video_driver(canvas)
#     pass

# except Exception as e:
#     # logger.error(str(e))
