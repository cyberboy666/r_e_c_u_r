from tkinter import Text, END
import math
import data_centre


class Display(object):
    MAX_LINES = 5
    SELECTOR_WIDTH = 0.28
    ROW_OFFSET = 6.0
    VIDEO_DISPLAY_TEXT = 'NOW [{}] {}     NEXT [{}] {}'
    VIDEO_DISPLAY_BANNER_TEXT = '{} {} {}'

    def __init__(self, tk, video_driver):
        self.video_driver = video_driver
        self.display_mode = "LOOPER"
        self.tk = tk

        self.browser_data = data_centre.data()
        self.browser_start_index = 0
        self.browser_index = self.browser_start_index
        self.browser_list = self.browser_data.get_browser_data_for_display()
        self.settings_start_index = 0
        self.settings_index = self.settings_start_index
        self.settings_list = data_centre.get_all_settings_data_for_display()

        self.display_text = self.create_display_text(self.tk)
        self.add_tags()
        self.update_screen()

    @staticmethod
    def create_display_text(tk):
        return Text(tk, bg="black", fg="white", font=('courier', 14))

    def add_tags(self):
        self.display_text.tag_configure("SELECT", background="white", foreground="black")
        self.display_text.tag_configure("TITLE", background="black", foreground="red")
        self.display_text.tag_configure("ERROR_MESSAGE", background="red", foreground="black")
        self.display_text.tag_configure("INFO_MESSAGE", background="blue", foreground="black")
        self.display_text.tag_configure("PLAYER_INFO", background="black", foreground="yellow")

    def load_display(self):
        self.load_title()
        self.load_player()
        if self.display_mode == 'BROWSER':
            self.load_browser()
        elif self.display_mode == 'SETTINGS':
            self.load_settings()
        else:
            self.load_looper()
        # load_divider(display)
        if data_centre.current_message:
            print('trying to display')
            self.load_message()
        self.display_text.pack()

    def load_title(self):
        self.display_text.insert(END, '================ r_e_c_u_r ================ \n')
        self.display_text.tag_add("TITLE", 1.17, 1.26)

    def load_player(self):
        text, banner = self.get_text_for_video_display()
        end_of_text = float("3." + str(len(text)))
        end_of_banner = float("3." + str(len(banner)))
        self.display_text.insert(END, text + '\n')
        self.display_text.tag_add("PLAYER_INFO", 2.0, end_of_text)
        self.display_text.insert(END, banner + '\n')
        self.display_text.tag_add("PLAYER_INFO", 3.0, end_of_banner)

    def load_settings(self):
        line_count = 0
        self.display_text.insert(END, '--------------- <SETTINGS> --------------- \n')
        self.display_text.insert(END, '{:>20} {:>20} \n'.format('SETTING', 'VALUE'))
        for index in range(len(self.settings_list)):
            if line_count >= self.MAX_LINES:
                break
            if index >= self.browser_start_index:
                setting = self.settings_list[index]
                self.display_text.insert(END, '{:>20} {:>20} \n'.format(setting[0], setting[1]))
                line_count = line_count + 1

    def load_looper(self):
        bank_info = data_centre.get_all_looper_data_for_display()
        self.display_text.insert(END, '--------------- <LOOPER> --------------- \n')
        self.display_text.insert(END, '{:>4} {:>15} {:>4} {:>4} {:>4} \n'.format(
            'bank', 'name', 'length', 'start', 'end'))
        for bank in bank_info:
            self.display_text.insert(END, '{:>4} {:>15} {:>4} {:>4} {:>4} \n'.format(
                bank[0], bank[1][0:15], bank[2], bank[3], bank[4]))
        self.select_current_playing(self.video_driver.current_player.bank_number)

    def load_message(self):
        self.display_text.insert(END, 'INFO: {}'.format(data_centre.current_message))
        self.display_text.tag_add("ERROR_MESSAGE", 14.0, 15.0)
        self.tk.after(4000, data_centre.clear_message)

    def load_browser(self):
        line_count = 0
        self.display_text.insert(END, '--------------- <BROWSER> --------------- \n')
        self.display_text.insert(END, '{:35} {:5} \n'.format('path', 'bank'))

        for index in range(len(self.browser_list)):
            if line_count >= self.MAX_LINES:
                break
            if index >= self.browser_start_index:
                path = self.browser_list[index]
                self.display_text.insert(END, '{:35} {:5} \n'.format(path[0][0:35], path[1]))
                line_count = line_count + 1

    def highlight_this_row(self, row):
        self.display_text.tag_add("SELECT", self.ROW_OFFSET + row,
                                  self.ROW_OFFSET + self.SELECTOR_WIDTH + row)

    def unhighlight_this_row(self, row):
        self.display_text.tag_remove("SELECT", self.ROW_OFFSET + row,
                                     self.ROW_OFFSET + self.SELECTOR_WIDTH + row)

    def get_text_for_video_display(self):
        now_bank, now_status, next_bank, next_status, duration, video_length = self.video_driver.get_info_for_video_display()
        banner = self.create_video_display_banner(duration, video_length)
        time_been = data_centre.convert_int_to_string_for_display(duration)
        time_left = data_centre.convert_int_to_string_for_display(
            video_length - duration)

        return self.VIDEO_DISPLAY_BANNER_TEXT.format(time_been, banner, time_left), \
               self.VIDEO_DISPLAY_TEXT.format(now_bank, now_status, next_bank, next_status)

    @staticmethod
    def create_video_display_banner(duration, video_length):
        banner_list = ['[', '-', '-', '-', '-', '-', '-', '-', '-',
                       '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
                       ']']
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

    def refresh_display(self):
        self.display_text.configure(state='normal')
        self.display_text.delete(1.0, END)
        self.load_display()
        self.display_text.configure(state='disable')
        if self.display_mode is 'BROWSER':
            self.highlight_this_row(self.browser_index)
        elif self.display_mode is 'SETTINGS':
            self.highlight_this_row(self.settings_index)

    def update_screen(self):
        self.refresh_display()
        self.display_text.focus_set()
        self.tk.after(1000, self.update_screen)

    def select_current_playing(self, bank_number):
        if bank_number != '-':
            self.display_text.tag_add("SELECT", self.ROW_OFFSET + bank_number,
                                      self.ROW_OFFSET + self.SELECTOR_WIDTH + bank_number)

    def move_browser_down(self):
        last_index = len(self.browser_list) - 1
        if self.browser_index + self.browser_start_index >= last_index:
            return
        if self.browser_index >= self.MAX_LINES - 1:
            self.browser_start_index = self.browser_start_index + 1
            return
        self.unhighlight_this_row(self.browser_index)
        self.browser_index = self.browser_index + 1
        self.highlight_this_row(self.browser_index)

    def move_browser_up(self):
        if self.browser_index == 0:
            if self.browser_start_index > 0:
                self.browser_start_index = self.browser_start_index - 1
            return
        self.unhighlight_this_row(self.browser_index)
        self.browser_index = self.browser_index - 1
        self.highlight_this_row(self.browser_index)

    def browser_enter(self):
        is_file, name = data_centre.extract_file_type_and_name_from_browser_format(
            self.browser_list[self.browser_index + self.browser_start_index][0])
        if is_file:
            data_centre.create_new_bank_mapping_in_first_open(name)
        else:
            self.browser_data.update_open_folders(name)
            self.browser_data.rewrite_browser_list()
        self.browser_list = self.browser_data.get_browser_data_for_display()

    def move_settings_down(self):
        last_index = len(self.settings_list) - 1
        if self.settings_index + self.settings_start_index >= last_index:
            return
        if self.settings_index >= self.MAX_LINES - 1:
            self.settings_start_index = self.settings_start_index + 1
            return
        self.unhighlight_this_row(self.settings_index)
        self.settings_index = self.settings_index + 1
        self.highlight_this_row(self.settings_index)

    def move_settings_up(self):
        if self.settings_index == 0:
            if self.settings_start_index > 0:
                self.settings_start_index = self.settings_start_index - 1
            return
        self.unhighlight_this_row(self.settings_index)
        self.settings_index = self.settings_index - 1
        self.highlight_this_row(self.settings_index)

    def settings_enter(self):
        data_centre.switch_settings(self.settings_index + self.settings_start_index)
