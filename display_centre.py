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

tk = Tk()

label_position_value = StringVar()
label_position_value.set('Current Position: --:--')
label_length_value = StringVar()
label_length_value.set('Video Length: --:--')

frame = Frame(tk, width=500, height=400)
label_position = Label(tk, textvariable=label_position_value)
label_length = Label(tk, textvariable=label_length_value)
video_driver = video_centre.video_driver(frame)
label_length.pack()
label_position.pack()

bank_info = data_centre.get_all_looper_data_for_display()
t = Text(tk)
for x in bank_info:
   for y in x:
       t.insert(END, str(y) + ' ')
   t.insert(END, '\n')
t.pack()

def key(event):
    print "pressed", repr(event.char)
    print "video position is :{}".format(video_driver.current_player.get_position())
    if(event.char in ['0', '1', '2']):
        print 'updating next bank'
        data_centre.update_next_bank_number(int(event.char))
        #video_driver.next_player.reload_content()
    elif(event.char in ['\r']):
        video_driver.manual_next = True


def update_current_time():
    label_position_value.set('Current Position:' + convert_int_to_string_for_display(video_driver.current_player.get_position() / 1000000))
    label_length_value.set('Video Length: {}'.format(video_driver.current_player.length))
    tk.after(500, update_current_time)

frame.bind("<Key>", key)

frame.pack()
frame.focus_set()

tk.after(500, update_current_time)
tk.mainloop()
