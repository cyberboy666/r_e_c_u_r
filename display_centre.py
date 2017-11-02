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
VIDEO_DISPLAY_BANNER_LIST = [
    '[', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', ']']
VIDEO_DISPLAY_BANNER_TEXT = '{} {} {}'
SELECTOR_WIDTH = 0.35
ROW_OFFSET = 8.0
MAX_LINES = 5
browser_start_index = 0

browser_index = 0


tk = Tk()

frame = Frame(tk, width=500, height=400)

video_driver = video_centre.video_driver(frame)

# our data store
data_object = data_centre.data()

browser_list = data_object.get_browser_data_for_display()

bank_info = data_centre.get_all_looper_data_for_display()

current_message = None
# terminal_font = Font(family="Terminal", size=12)
# terminal_font_bold = Font(family="Terminal", size=12, weight='bold')
# titles.configure(font=terminal_font_bold)
display_mode = 'BROWSER'


def load_display(display):
    load_title(display)
    load_divider(display)
    load_player(display)
    load_divider(display)
    if display_mode == 'BROWSER':
        load_browser(display)
    elif display_mode == 'SETTINGS':
        pass  # load_settings(display)
    else:
        load_looper(display)
    load_divider(display)
    if current_message:
        load_message(display)

    display.pack()


def load_title(display):
    display.insert(END, '======== r_e_c_u_r ======== \n')
    display.tag_add("TITLE", 1.9, 1.18)



def load_divider(display):
    display.insert(END, '---------------- \n')


def load_player(display):
    text, banner = get_text_for_video_display()
    end_of_text = float("3." + str(len(text)))
    end_of_banner = float("3." + str(len(banner)))
    display.insert(END, text + '\n')
    display.tag_add("PLAYER_INFO", 3.0, end_of_text)
    display.insert(END, banner + '\n')
    display.tag_add("PLAYER_INFO", 4.0, end_of_banner)



def load_looper(display):
    bank_info = data_centre.get_all_looper_data_for_display()
    display.insert(END, '------ <LOOPER> ------ \n')
    display.insert(END, '{:>10} {:>20} {:>10} {:>10} {:>10} \n'.format(
        'bank no', 'name', 'length', 'start', 'end'))
    for bank in bank_info:
        display.insert(END, '{:>10} {:>20} {:>10} {:>10} {:>10} \n'.format(
            bank[0], bank[1], bank[2], bank[3], bank[4]))

def load_message(display):
    display.insert(END, 'INFO: {}'.format(current_message))
    display.tag_add("ERROR_MESSAGE", 14.0, 15.0)
    tk.after(4000,clear_message)

def clear_message():
    global current_message
    current_message = None

def get_text_for_video_display():
    now_bank, now_status, next_bank, next_status, duration, video_length = video_driver.get_info_for_video_display()
    banner = create_video_display_banner(duration, video_length)
    time_been = data_centre.convert_int_to_string_for_display(duration)
    time_left = data_centre.convert_int_to_string_for_display(
        video_length - duration)

    return VIDEO_DISPLAY_BANNER_TEXT.format(time_been, banner, time_left),\
        VIDEO_DISPLAY_TEXT.format(now_bank, now_status, next_bank, next_status)


def create_video_display_banner(duration, video_length):
    banner_list = ['[', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
                   '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', ']']
    max = len(banner_list) - 1
    if duration <= 0:
        banner_list[0] = '<'
    elif duration >= video_length:
        banner_list[max] = '>'
    else:
        marker = int(math.floor(float(duration) /
                                float(video_length) * (max - 1)) + 1)
        banner_list[marker] = '*'

    return ''.join(banner_list)


def load_browser(self):
    global data_object
    global browser_start_index
    global browser_list
    line_count = 0
    display.insert(END, '------ <BROWSER> ------ \n')
    display.insert(END, '{:50} {:20} \n'.format('path', 'bank'))

    for index in range(len(browser_list)):
        if line_count >= MAX_LINES:
            break
        if index >= browser_start_index:
            path = browser_list[index]
            display.insert(END, '{:50} {:20} \n'.format(path[0], path[1]))
            line_count = line_count + 1

    
def move_browser_selection_up():
    global browser_index
    global browser_start_index
    if browser_index == 0:
        if(browser_start_index > 0):
            browser_start_index = browser_start_index - 1
            refresh_display()
        return
    deselect_current_browser_index()
    browser_index = browser_index - 1
    select_current_browser_index()


def move_browser_selection_down():
    global browser_index
    global data_object
    global browser_start_index
    global browser_list
    last_index = len(browser_list) - 1
    if browser_index + browser_start_index >= last_index:
        return
    if browser_index >= MAX_LINES - 1:
        browser_start_index = browser_start_index + 1
        refresh_display()
        return
    deselect_current_browser_index()
    browser_index = browser_index + 1
    select_current_browser_index()


def select_current_browser_index():
    display.tag_add("SELECT", ROW_OFFSET + browser_index,
                    ROW_OFFSET + SELECTOR_WIDTH + browser_index)

def deselect_current_browser_index():
    display.tag_remove("SELECT", ROW_OFFSET + browser_index,
                       ROW_OFFSET + SELECTOR_WIDTH + browser_index)

def refresh_display():
    display.delete(1.0, END)
    load_display(display)
    if display_mode == "BROWSER":
        select_current_browser_index()

display = Text(tk, bg="black", fg="white")
display.tag_configure("SELECT", background="white", foreground="black")
display.tag_configure("TITLE", background="black", foreground="red")
display.tag_configure("ERROR_MESSAGE", background="red", foreground="black")
display.tag_configure("INFO_MESSAGE", background="blue", foreground="black")
display.tag_configure("PLAYER_INFO", background="black", foreground="yellow")

load_display(display)

select_current_browser_index()

def num_lock_key(event):
    global display_mode
    if display_mode == "BROWSER":
        display_mode = "LOOPER"
    else:
        display_mode = "BROWSER"
    refresh_display()

def key(event):
    print event.char
    ## '/' clear all banks
    if event.char == '/':
        print 'it\'s cleared!'
        data_centre.clear_all_banks()
        refresh_display()
    ## '.' quits r_e_c_u_r
    elif event.char == '.':
        if video_centre.has_omx:
            video_driver.exit_all_players()
        tk.destroy()
    ## 'num' sets current selection to bank number num
    elif event.char in ['0', '1', '2', '3', '4', '5', '6', '7']:
        data_centre.update_next_bank_number(int(event.char))
        # video_driver.next_player.reload_content()
    ## 'enter' sets manual next flag
    elif event.char in ['\r']:
        video_driver.manual_next = True
    ## 'm' switches display mode
    elif(event.char in ['m']):
        global display_mode
        if display_mode == "BROWSER":
            display_mode = "LOOPER"
        else:
            display_mode = "BROWSER"
        refresh_display()
    ## 'l' pauses/unpauses the video
    elif(event.char in ['l']):
        video_driver.current_player.toggle_pause()


def up_key(event):
    if display_mode == "BROWSER":
        move_browser_selection_up()
        global browser_index
        global browser_start_index

def down_key(event):
    if display_mode == "BROWSER":
        move_browser_selection_down()
        global browser_index
        global browser_start_index



def backspace_key(event):
    try:
        global browser_index
        global data_object
        global browser_start_index
        global browser_list
        global current_message
        if display_mode == "BROWSER":
            is_file, name = data_centre.extract_file_type_and_name_from_browser_format(
                browser_list[browser_index + browser_start_index][0])
            if is_file:
                data_centre.create_new_bank_mapping_in_first_open(name)
            else:
                data_object.update_open_folders(name)
            data_object.rewrite_browser_list()
            browser_list = data_object.get_browser_data_for_display()
            refresh_display()
    except Exception as e:
        print 'the current message is: {}'.format(e.message)
        current_message = e.message


def update_screen():
    refresh_display()
    tk.after(1000, update_screen)

frame.bind("<Key>", key)
frame.bind("<Up>", up_key)
frame.bind("<Down>", down_key)
frame.bind("<BackSpace>", backspace_key)
frame.bind("<Num_Lock>", num_lock_key)

frame.pack()
frame.focus_set()

tk.after(1000, update_screen)

try:
    tk.mainloop()
except:
    current_message = traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
