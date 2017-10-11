import logging
import math
import os
import sys
import time
import traceback
from Tkinter import *

import video_centre
import data_centre

VIDEO_DISPLAY_TEXT = 'NOW [{}] {}              NEXT [{}] {}'
VIDEO_DISPLAY_BANNER_LIST = [
    '[', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', ']']
VIDEO_DISPLAY_BANNER_TEXT = '{} {} {}'

logger = data_centre.setup_logging()

tk = Tk()
# tk.withdraw()
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()

wid = canvas.winfo_id()
os.system('xterm -into %d -geometry 40x20 -sb &' % wid)

data = data_centre.data()

try:
    video_driver = video_centre.video_driver(canvas)

    while True:
        tk.update()
except Exception as e:
    logger.error(str(e))
