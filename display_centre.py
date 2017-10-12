import logging
import math
import os
import sys
import time
import traceback
from data_centre import *
from Tkinter import *
import tkFont

import video_centre
import data_centre

VIDEO_DISPLAY_TEXT = 'NOW [{}] {}              NEXT [{}] {}'
VIDEO_DISPLAY_BANNER_LIST = ['[','-','-','-','-','-','-','-','-','-','-',']']
VIDEO_DISPLAY_BANNER_TEXT = '{} {} {}'
SELECTOR_WIDTH = 0.35
ROW_OFFSET = 8.0

browser_index = 0

tk = Tk()

#from tkinter.font import Font

bold_font = tkFont.Font( size=12, weight="bold")

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

#terminal_font = Font(family="Terminal", size=12)
#terminal_font_bold = Font(family="Terminal", size=12, weight='bold')
#titles.configure(font=terminal_font_bold)
display_mode = 'BROWSER'

def load_display(display):
    load_title(display)
    load_divider(display)
    load_player(display)
    load_divider(display)
    if display_mode == 'BROWSER':
        load_browser(display)
    elif display_mode == 'SETTINGS':
        load_settings(display)
    else:
        load_looper(display)
    load_divider(display)

    display.pack()


def load_title(display):
    display.insert(END,'======== r_e_c_u_r ======== \n')

def load_divider(display):
    display.insert(END, '---------------- \n')

def load_player(display):
    text, banner = get_text_for_video_display()
    display.insert(END, text + '\n')
    display.insert(END, banner + '\n')

def load_looper(display):
    bank_info = data_centre.get_all_looper_data_for_display()
    display.insert(END, '------ <LOOPER> ------ \n')
    display.insert(END, '{:>10} {:>20} {:>10} {:>10} {:>10} \n'.format('bank no', 'name', 'length', 'start', 'end'))
    for bank in bank_info:
        display.insert(END, '{:>10} {:>20} {:>10} {:>10} {:>10} \n'.format(bank[0], bank[1], bank[2], bank[3], bank[4]))

def get_text_for_video_display():
    now_bank, now_status, next_bank, next_status, duration, video_length = video_driver.get_info_for_video_display()
    banner = create_video_display_banner(duration, video_length)
    time_been = data_centre.convert_int_to_string_for_display(duration)
    time_left = data_centre.convert_int_to_string_for_display(video_length - duration)

    return VIDEO_DISPLAY_BANNER_TEXT.format(time_been, banner, time_left),\
           VIDEO_DISPLAY_TEXT.format(now_bank,now_status,next_bank, next_status)

def create_video_display_banner(duration,video_length):
    banner_list = ['[','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-',']']
    max = len(banner_list) - 1
    if duration <= 0:
        banner_list[0] = '<'
    elif duration >= video_length:
        banner_list[max] = '>'
    else:
        marker = int(math.floor(float(duration)/float(video_length)*(max-1))+1)
        banner_list[marker] = '*'

    return ''.join(banner_list)

def load_browser(self):
    data_object = data_centre.data()
    browser_info = data_object.get_browser_data_for_display()
    display.insert(END, '------ <BROWSER> ------ \n')
    display.insert(END, '{:50} {:20} \n'.format('path', 'bank'))
    for path in browser_info:
        display.insert(END, '{:50} {:20} \n'.format(path[0], path[1]))

def move_browser_selection_up():
    global browser_index
    print "Index at start: " + str(browser_index)
    if browser_index == 0:
        return
    display.tag_remove("SELECT", ROW_OFFSET + browser_index, ROW_OFFSET + SELECTOR_WIDTH + browser_index)
    browser_index = browser_index - 1
    display.tag_add("SELECT", ROW_OFFSET + browser_index, ROW_OFFSET + SELECTOR_WIDTH + browser_index)
    print "Index at end: " + str(browser_index)

def move_browser_selection_down():
    global browser_index
    data_object = data_centre.data()
    browser_info = data_object.get_browser_data_for_display()
    last_index = len(data_object.get_browser_data_for_display()) -1
    print "Index at start: " + str(browser_index)
    if(browser_index == last_index):
        return
    display.tag_remove("SELECT", ROW_OFFSET + browser_index, ROW_OFFSET + SELECTOR_WIDTH + browser_index)
    browser_index = browser_index + 1
    display.tag_add("SELECT", ROW_OFFSET + browser_index, ROW_OFFSET + SELECTOR_WIDTH + browser_index)
    print "Index at end: " + str(browser_index)

display = Text(tk)

display.tag_configure("SELECT", background="black", foreground="white")

load_display(display)

display.tag_add("SELECT", ROW_OFFSET + browser_index, ROW_OFFSET + SELECTOR_WIDTH + browser_index)

def key(event):
    print "pressed", repr(event.char)
    if(event.char in ['0', '1', '2']):
        print 'updating next bank'
        data_centre.update_next_bank_number(int(event.char))
        #video_driver.next_player.reload_content()
    elif(event.char in ['\r']):
        video_driver.manual_next = True

def up_key(event):
    print "pressed up"
    if display_mode == "BROWSER":
        move_browser_selection_up()

def down_key(event):
    print "pressed down"
    if display_mode == "BROWSER":
        move_browser_selection_down()

def update_current_time():
    label_position_value.set('Current Position:' + convert_int_to_string_for_display(video_driver.current_player.get_position() / 1000000))
    label_length_value.set('Video Length: {}'.format(video_driver.current_player.length))
    tk.after(500, update_current_time)

frame.bind("<Key>", key)
frame.bind("<Up>", up_key)
frame.bind("<Down>", down_key)

frame.pack()
frame.focus_set()

tk.after(500, update_current_time)
tk.mainloop()
