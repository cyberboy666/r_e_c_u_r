import logging
import sys
import traceback
from Tkinter import *
import time
import os

import math
from asciimatics.effects import RandomNoise
from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import ResizeScreenError, NextScene
from asciimatics.scene import Scene
from dual_screen import Screen
from asciimatics.widgets import Frame, Layout, Divider, Button, ListBox, Widget, MultiColumnListBox, PopUpDialog, Text, \
    Label

import data_centre
import video_centre

VIDEO_DISPLAY_TEXT = 'NOW [{}] {}              NEXT [{}] {}'
VIDEO_DISPLAY_BANNER_LIST = ['[','-','-','-','-','-','-','-','-','-','-',']']
VIDEO_DISPLAY_BANNER_TEXT = '{} {} {}'

logger = data_centre.setup_logging()

class Display(Frame):
    def __init__(self, switch, screen,driver, on_load=None):
        super(Display, self).__init__(screen,
                                      screen.height,
                                      screen.width,
                                      on_load=on_load,
                                      title="r_e_c_u_r"
                                      )
        self._last_frame = 0
        self.video_driver = driver
        self.my_frame_update_count = 40

        layout_top = Layout([1,1,1])
        self.add_layout(layout_top)

        self.browser_button = Button("BROWSER", self.do_nothing())
        self.browser_button.disabled = True
        if switch[0]:
            self.browser_button.custom_colour = "focus_button"

        self.looper_button = Button("LOOPER", self.do_nothing())
        self.looper_button.disabled = True
        if switch[1]:
            self.looper_button.custom_colour = "focus_button"

        self.settings_button = Button("SETTINGS", self.do_nothing())
        self.settings_button.disabled = True
        if switch[2]:
            self.settings_button.custom_colour = "focus_button"
        layout_top.add_widget(Divider(), 0)
        layout_top.add_widget(Divider(), 1)
        layout_top.add_widget(Divider(), 2)
        layout_top.add_widget(self.browser_button, 0)
        layout_top.add_widget(self.looper_button, 1)
        layout_top.add_widget(self.settings_button, 2)

        layout_body = Layout([100], fill_frame=False)
        self.add_layout(layout_body)

        layout_body.add_widget(Divider())
        video_display_text, video_banner_text = self.get_text_for_video_display()
        self.player_info_label = Label(video_display_text)
        self.player_info_banner = Label(video_banner_text)
        layout_body.add_widget(self.player_info_banner)
        layout_body.add_widget(self.player_info_label)
        layout_body.add_widget(Divider())
        self.fix()

    def do_nothing(self):
        pass

    def get_text_for_video_display(self):
        now_bank, now_status, next_bank, next_status, duration, video_length = self.video_driver.get_info_for_video_display()
        banner = create_video_display_banner(duration,video_length)
        time_been = data_centre.convert_int_to_string_for_display(duration)
        time_left = data_centre.convert_int_to_string_for_display(video_length - duration)
        logger.info(VIDEO_DISPLAY_BANNER_TEXT.format(time_been,banner,time_left))
        return VIDEO_DISPLAY_BANNER_TEXT.format(time_been,banner,time_left),VIDEO_DISPLAY_TEXT.format(now_bank , now_status, next_bank, next_status, duration)

    def _update(self, frame_no):
        if frame_no - self._last_frame >= self.frame_update_count or self._last_frame == 0:
            self._last_frame = frame_no

            video_display_text, video_banner_text = self.get_text_for_video_display()
            self.player_info_label._text = video_display_text
            self.player_info_banner._text = video_banner_text

        super(Display, self)._update(frame_no)

    @property
    def frame_update_count(self):
        # Refresh once every 1 seconds by default.
        return 20

    def get_focus_on_list(self, list):
        return list.options[list.value][0][0]

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord('n'), ord('N')]:
                raise NextScene

        return super(Display, self).process_event(event)


class Browser(Display):
    def __init__(self, screen, data, driver):
        super(Browser, self).__init__([1,0,0],screen,driver, on_load=self._reload_list)

        self._data_object = data
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self._browser_data_view = ScrollingMultiColumnListBox(
            Widget.FILL_FRAME,
            [50,10],
            self._data_object.get_browser_data_for_display(),
            titles=['path','bank']
            )
        layout.add_widget(self._browser_data_view)

        self.fix()

    def process_event(self, event):
         numberMapping = [ord('q'),ord('w'),ord('e'),ord('r'),ord('t'),ord('y'),ord('u'),ord('i'),ord('o'),ord('p') ]

         if isinstance(event, KeyboardEvent):
              if event.key_code in numberMapping:

                 focus = self.get_focus_on_list(self._browser_data_view)
                 is_file, name = data_centre.extract_file_type_and_name_from_browser_format(focus)
                 if(is_file):
                    bank_number = numberMapping.index(event.key_code)
                    data_centre.create_new_bank_mapping(bank_number,name)
                    self._data_object.rewrite_browser_list()
                    self._reload_list(self._browser_data_view.value)

              if event.key_code in [ord('m')]:
                 focus = self.get_focus_on_list(self._browser_data_view)
                 is_file , name = data_centre.extract_file_type_and_name_from_browser_format(focus)
                 if(is_file):
                     data_centre.create_new_bank_mapping_in_first_open(name)
                     self._data_object.rewrite_browser_list()
                     self._reload_list(self._browser_data_view.value)
                 else:
                     self._data_object.update_open_folders(name)
                     self._data_object.rewrite_browser_list()
                     self._reload_list(self._browser_data_view.value)

              if event.key_code in [ord('c')]:
                  data_centre.clear_all_banks()

                  self._data_object.rewrite_browser_list()
                  self._reload_list(self._browser_data_view.value)

         return super(Browser, self).process_event(event)
        # Now pass on to lower levels for normal handling of the event.

    def _update(self, frame_no):
        logger.info('the BROWSER frame number is {}'.format(frame_no))
        super(Browser, self)._update(frame_no)

    def _reload_list(self, new_value=None):
        self._browser_data_view.options = self._data_object.get_browser_data_for_display()
        self._browser_data_view.value = new_value


class Looper(Display):
    def __init__(self, screen, data,driver):
        super(Looper, self).__init__([0, 1, 0],screen,driver,on_load=self._reload_list,)

        self._data_object = data
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self._bank_data_view = MultiColumnListBox(
            Widget.FILL_FRAME,
            [10,35,10,10,10],
            data_centre.get_all_looper_data_for_display(),
        titles=['bank','name','length','start','end'])
        layout.add_widget(self._bank_data_view)

        self.fix()

    def process_event(self, event):
        return super(Looper, self).process_event(event)

    def _reload_list(self, new_value=None):
        self._bank_data_view.options = data_centre.get_all_looper_data_for_display()
        self._bank_data_view.value = new_value


class Settings(Display):
    def __init__(self, screen, data,driver):
        super(Settings, self).__init__([0, 0, 1], screen,driver,on_load=self._reload_list)

        self._data_object = data
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self._settings_data_view = MultiColumnListBox(
            Widget.FILL_FRAME,
            [30, 30],
            data_centre.get_all_settings_data_for_display(),
            titles=['setting', 'value'])
        layout.add_widget(self._settings_data_view)

        self.fix()

    def _reload_list(self,new_value=None):
        self._settings_data_view.options = data_centre.get_all_settings_data_for_display()
        self._settings_data_view.value = new_value

    def process_event(self, event):

        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord('m')]:
                focus = self.get_focus_on_list(self._settings_data_view)
                data_centre.switch_settings(focus)
                self._reload_list(self._settings_data_view.value)

        return super(Settings, self).process_event(event)


class ScrollingMultiColumnListBox(MultiColumnListBox):
    def __init__(self, height, columns, options, titles):
        super(ScrollingMultiColumnListBox, self).__init__(height, columns, options, titles)

    def process_event(self, event):
         if isinstance(event, KeyboardEvent):
             if len(self._options) > 0 and event.key_code == Screen.KEY_UP and self._line == 0:
                self._line = len(self._options)
             elif len(self._options) > 0 and event.key_code == Screen.KEY_DOWN and self._line == len(self._options) - 1:
                self._line = -1

         super(ScrollingMultiColumnListBox,self).process_event(event)

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

def demo(screen, tk):
    scenes = [Scene([Browser(screen, data,video_driver)], -1),
              Scene([Looper(screen, data,video_driver)], -1),
              Scene([Settings(screen, data,video_driver)], -1)]
    screen.play(scenes,tk)

data = data_centre.data()
video_driver = video_centre.video_driver()
last_scene = None

tk = Tk()
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()

while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True, arguments=(tk,))
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
    except Exception as e:
        logger.error(traceback.format_exc())
        logger.error(str(e))


