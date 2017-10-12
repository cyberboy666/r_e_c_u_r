import logging
import math
import os
import sys
import time
import traceback
from data_centre import *
from Tkinter import *

import video_centre
import data_centre

# logger = data_centre.setup_logging()
tk = Tk()

label1Text = StringVar()
label1Text.set('blah')
# tk.withdraw()
frame = Frame(tk, width=500, height=400)
# data = data_centre.data()
label = Label(tk, textvariable=label1Text)
video_driver = video_centre.video_driver(frame)

label.pack()

def key(event):
    print "pressed", repr(event.char)
    print "video position is :{}".format(video_driver.current_player.get_position())
    if(event.char in ['0','1','2'] ):
        print 'updating next bank'
        data_centre.update_next_bank_number(int(event.char))
        #video_driver.next_player.reload_content()

def update_current_time():
    label1Text.set(convert_int_to_string_for_display(video_driver.current_player.get_position() / 1000000))
    tk.after(500, update_current_time)

frame.bind("<Key>", key)

frame.pack()
frame.focus_set()

tk.after(500, update_current_time)
tk.mainloop()
# try:
# #    video_driver = video_centre.video_driver(canvas)
#     pass

# except Exception as e:
#     # logger.error(str(e))
