from tkinter import Text, END
import math
import time
import display_centre.menu as menu

class Display(object):
    MENU_HEIGHT = 10
    SELECTOR_WIDTH = 0.47
    ROW_OFFSET = 6.0
    VIDEO_DISPLAY_BANNER_TEXT = ' {} {} {}'

    def __init__(self, tk, video_driver, capture, message_handler, data):
        self.tk = tk
        self.video_driver = video_driver
        self.capture = capture
        self.message_handler = message_handler
        self.data = data
        self.browser_menu = menu.BrowserMenu(self.data, self.MENU_HEIGHT)      
        self.settings_menu = menu.SettingsMenu(self.data, self.MENU_HEIGHT)

        #self.top_menu_index = 0
        #self.selected_list_index = self.top_menu_index
        
        self.display_text = self._create_display_text(self.tk)
        self._add_tags()
        self._update_screen_every_second()

    @staticmethod
    def _create_display_text(tk):
        return Text(tk, bg="black", fg="white", font=('Liberation Mono', 13))

    def _add_tags(self):
        self.display_text.tag_configure("SELECT", background="white", foreground="black")
        self.display_text.tag_configure("TITLE", background="black", foreground="red")
        self.display_text.tag_configure("DISPLAY_MODE", background="black", foreground="magenta")
        self.display_text.tag_configure("ERROR_MESSAGE", background="red", foreground="white")
        self.display_text.tag_configure("INFO_MESSAGE", background="blue", foreground="white")
        self.display_text.tag_configure("PLAYER_INFO", background="black", foreground="yellow")
        self.display_text.tag_configure("COLUMN_NAME", background="black", foreground="cyan")
        self.display_text.tag_configure("FUNCTION", background="cyan", foreground="black")
        self.display_text.tag_configure("BROKEN_PATH", background="black", foreground="gray")

    def _load_display(self):
        self._load_title()
        self._load_player()
        self._load_display_body()
        self._load_message()
        self.display_text.pack()

    def _load_title(self):
        self.display_text.insert(END, '================== r_e_c_u_r ================== \n')
        self.display_text.tag_add("TITLE", 1.19, 1.28)

    def _load_player(self):
        text, banner = self._get_info_for_player()
        end_of_text = float("3." + str(len(text)))
        end_of_banner = float("3." + str(len(banner)))
        self.display_text.insert(END, text + '\n')
        self.display_text.tag_add("PLAYER_INFO", 2.0, end_of_text)
        self.display_text.insert(END, banner + '\n')
        self.display_text.tag_add("PLAYER_INFO", 3.0, end_of_banner)

    def _load_display_body(self):
        if self.data.display_mode == 'BROWSER':
            self._load_browser()
        elif self.data.display_mode == 'SETTINGS':
            self._load_settings()
        else:
            self._load_sampler()
        self.display_text.tag_add("COLUMN_NAME", 5.0, 6.0)
        

    def _load_sampler(self):
        bank_data = self.data.bank_data[self.data.bank_number]
        self.display_text.insert(END, '------------------ <SAMPLER> ------------------ \n')
        self.display_text.tag_add("DISPLAY_MODE", 4.19, 4.29)
        self.display_text.insert(END, '{:^6} {:<16} {:<4} {:<4} {:<4} \n'.format(
            '{}-slot'.format(self.data.bank_number), 'name', 'length', 'start', 'end'))
        for index, slot in enumerate(bank_data):
            name_without_extension =  slot['name'].rsplit('.',1)[0]
            self.display_text.insert(END, '{:^4} {:<18} {:<4} {:<4} {:<4} \n'.format(
                index, name_without_extension[0:22], self.format_time_value(slot['length']),
                self.format_time_value(slot['start']), self.format_time_value(slot['end'])))
            if self.data.is_this_path_broken(slot['location']):
                self.display_text.tag_add("BROKEN_PATH", self.ROW_OFFSET + index,
                                  self.ROW_OFFSET + self.SELECTOR_WIDTH + index)
        current_bank , current_slot = self.data.split_bankslot_number(self.video_driver.current_player.bankslot_number)
        if current_bank is self.data.bank_number:
            self.selected_list_index = current_slot
        else:
            self.selected_list_index = 0

    def _load_browser(self):
        browser_list = self.browser_menu.menu_list
        number_of_lines_displayed = 0
        self.display_text.insert(END, '------------------ <BROWSER> ------------------ \n')
        self.display_text.tag_add("DISPLAY_MODE", 4.19, 4.29)
        self.display_text.insert(END, '{:40} {:5} \n'.format('path', 'slot'))

        number_of_browser_items = len(browser_list)
        for index in range(number_of_browser_items):
            if number_of_lines_displayed >= self.MENU_HEIGHT:
                break
            if index >= self.browser_menu.top_menu_index:
                path = browser_list[index]
                self.display_text.insert(END, '{:40} {:5} \n'.format(path['name'][0:35], path['slot']))
                number_of_lines_displayed = number_of_lines_displayed + 1

        for index in range(self.MENU_HEIGHT - number_of_browser_items):
            self.display_text.insert(END, '\n')

        self._highlight_this_row(self.browser_menu.selected_list_index - self.browser_menu.top_menu_index)

    def _load_settings(self):
        line_count = 0
        settings_list = self.settings_menu.menu_list
        self.display_text.insert(END, '------------------ <SETTINGS> ----------------- \n')
        self.display_text.tag_add("DISPLAY_MODE", 4.19, 4.29)
        self.display_text.insert(END, '{:^23} {:^22} \n'.format('SETTING', 'VALUE'))
        number_of_settings_items = len(settings_list)
        for index in range(number_of_settings_items):
            if line_count >= self.MENU_HEIGHT:
                break
            if index >= self.settings_menu.top_menu_index:
                setting = settings_list[index]
                self.display_text.insert(END, '{:<23} {:<22} \n'.format(setting['name'], setting['value']))
                line_count = line_count + 1

        for index in range(self.MENU_HEIGHT - number_of_settings_items):
            self.display_text.insert(END, '\n')

        self._highlight_this_row(self.settings_menu.selected_list_index - self.settings_menu.top_menu_index)

    def _load_message(self):
        if self.message_handler.current_message[1]:
            self.display_text.insert(END, '{:5} {:38}'.format(
                self.message_handler.current_message[0], self.message_handler.current_message[1][0:38]))
            self.display_text.tag_add('{}_MESSAGE'.format(
                self.message_handler.current_message[0]), 16.0,16.0 + self.SELECTOR_WIDTH)
            if self.message_handler.current_message[2]:
                self.message_handler.current_message[2] = False
                message_length = 4000
                self.tk.after(message_length, self.message_handler.clear_message)
        elif self.data.function_on:
            self.display_text.insert(END, '{:^45}'.format('< FUNCTION KEY ON >'))
            self.display_text.tag_add('FUNCTION', 16.0,16.0 + self.SELECTOR_WIDTH)
        else:
            self.display_text.insert(END, '{:8} {:<10}'.format('CONTROL:', self.data.control_mode))
            self.display_text.tag_add('TITLE', 16.0,16.0 + self.SELECTOR_WIDTH)

    def _highlight_this_row(self, row):
        self.display_text.tag_add("SELECT", self.ROW_OFFSET + row,
                                  self.ROW_OFFSET + self.SELECTOR_WIDTH + row)

    def _unhighlight_this_row(self, row):
        self.display_text.tag_remove("SELECT", self.ROW_OFFSET + row,
                                     self.ROW_OFFSET + self.SELECTOR_WIDTH + row)

    def _get_info_for_player(self):
        now_slot, now_status, next_slot, next_status, position, crop_length, start, end = self.video_driver.get_info_for_player_display()
        banner = self.create_video_display_banner(start, end, crop_length, position)
        time_been = self.format_time_value(position - start)
        time_left = self.format_time_value(end - position)
        capture_status = self._generate_capture_status()        

        now_info = 'NOW [{}] {}'.format(now_slot, now_status)
        next_info = 'NEXT [{}] {}'.format(next_slot, next_status)
        capture_info = '{}'.format(capture_status)

        return self.VIDEO_DISPLAY_BANNER_TEXT.format(time_been, banner, time_left), \
               '{:17} {:10} {:17}'.format(now_info[:17], capture_info[:10], next_info[:18])

    def _generate_capture_status(self):
        is_previewing = self.capture.is_previewing 
        is_recording = self.capture.is_recording
        rec_time = -1
        if is_recording == True:
            rec_time = self.capture.get_recording_time()
        capture_status = ''
        if is_previewing and is_recording == True:
            capture_status = '<{}>'.format('REC'+ self.format_time_value(rec_time))
        elif is_previewing and is_recording == 'saving':
            capture_status = '<{}>'.format('_saving_')
        elif is_previewing:
            capture_status = '<{}>'.format('_preview')
        elif is_recording == True:
            capture_status = '[{}]'.format('REC'+ self.format_time_value(rec_time))
        elif is_recording == 'saving':
            capture_status =  '[{}]'.format('_saving_')
        else:
            capture_status = ''

        return capture_status

    @staticmethod
    def create_video_display_banner(start, end, crop_length, position):
        
        banner_list = ['[', '-', '-', '-', '-', '-', '-', '-', '-',
                       '-', '-', '-', '-', '-', '-', '-', '-', '-',
                       '-', '-', '-', '-', '-', '-', '-', '-', '-',
                       '-', '-', '-', '-', '-',
                       ']']
        max = len(banner_list) - 1
        if position < start:
            banner_list[0] = '<'
        elif position > end:
            banner_list[max] = '>'
        elif crop_length != 0:
            marker = int(math.floor(float(position - start) /
                                    float(crop_length) * (max - 1)) + 1)
            banner_list[marker] = '*'

        return ''.join(banner_list)

    def _update_screen_every_second(self):
        self.refresh_display()
        self.tk.after(500, self._update_screen_every_second)

    def refresh_display(self):
        if self.data.update_screen:
            self.display_text.configure(state='normal')
            self.display_text.delete(1.0, END)
            self._load_display()
            self.display_text.configure(state='disable')
            self.display_text.focus_set()

    def navigate_menu(self, move_direction, number_items_in_list):
        last_list_index = number_items_in_list - 1
        bottom_menu_index = self.top_menu_index + self.MENU_HEIGHT - 1

        ##self._unhighlight_this_row(self.selected_list_index - self.top_menu_index)

        if move_direction == 'down':
            if self.selected_list_index != last_list_index:
                if self.selected_list_index == bottom_menu_index:
                    self.top_menu_index += 1
                self.selected_list_index += 1
            else:
                self.top_menu_index = 0
                self.selected_list_index = self.top_menu_index

        elif move_direction == 'up':
            if self.selected_list_index != 0:
                if self.selected_list_index == self.top_menu_index:
                    self.top_menu_index -= 1
                self.selected_list_index -= 1
            else:
                self.selected_list_index = last_list_index
                self.top_menu_index = last_list_index - (self.MENU_HEIGHT - 1)
                if self.top_menu_index < 0:
                    self.top_menu_index = 0

        ##self._highlight_this_row(self.selected_list_index - self.top_menu_index)

        return

    @staticmethod
    def format_time_value(time_in_seconds):
        if time_in_seconds < 0:
            return ''
        elif time_in_seconds >= 6000:
            return '99:99'
        else:
            return time.strftime("%M:%S", time.gmtime(time_in_seconds))
