import math
import time
from tkinter import END, Text

import display_centre.menu as menu


class Display(object):
    MENU_HEIGHT = 10
    SELECTOR_WIDTH = 0.47
    ROW_OFFSET = 6.0
    TITLES = ['{0} r_e_c_u_r {0}'.format('=' * 18), '{0} c_o_n_j_u_r {1}'.format('=' * 18, '=' * 16), '{0} d_e_t_o_u_r {1}'.format('=' * 18, '=' * 16)]

    def __init__(self, tk, video_driver, shaders, message_handler, data):
        self.tk = tk
        self.video_driver = video_driver
        self.capture = None
        self.shaders = shaders
        self.message_handler = message_handler
        self.data = data
        self.browser_menu = menu.BrowserMenu(self.data, self.message_handler, self.MENU_HEIGHT)
        self.settings_menu = menu.SettingsMenu(self.data, self.message_handler, self.MENU_HEIGHT)
        self.plugins_menu = menu.PluginsMenu(self.data, self.message_handler, self.MENU_HEIGHT)
        self.shaders_menu = self.shaders.shaders_menu

        self.body_title = ''
        self.display_text = self._create_display_text(self.tk)
        self._add_tags()
        self._update_screen_every_second()

    @staticmethod
    def _create_display_text(tk):
        return Text(tk, bg="black", fg="white", font=('Liberation Mono', 13), undo=False)

    def _add_tags(self):
        self.display_text.tag_configure("SELECT", background="white", foreground="black")
        self.display_text.tag_configure("TITLE", background="black", foreground="red")
        self.display_text.tag_configure("DISPLAY_MODE", background="black", foreground="magenta")
        self.display_text.tag_configure("ERROR_MESSAGE", background="red", foreground="white")
        self.display_text.tag_configure("INFO_MESSAGE", background="blue", foreground="white")
        self.display_text.tag_configure("NOW_PLAYER_INFO", background="black", foreground="yellow")
        self.display_text.tag_configure("NEXT_PLAYER_INFO", background="black", foreground="cyan")
        self.display_text.tag_configure("COLUMN_NAME", background="black", foreground="VioletRed1")
        self.display_text.tag_configure("SHADER_PARAM", background="VioletRed1", foreground="black")
        self.display_text.tag_configure("FUNCTION", background="yellow", foreground="black")
        self.display_text.tag_configure("BROKEN_PATH", background="black", foreground="gray")
        self.display_text.tag_configure("ZEBRA_STRIPE", background="black", foreground="khaki")

    def _load_display(self):
        self._load_title()
        self._load_player()
        self._load_display_body()
        self._load_message()
        # print('the number of tags are {}'.format(len(self.display_text.tag_names())))
        self.display_text.pack()

    def _load_title(self):
        if self.data.display_mode == 'SHADERS' or self.data.display_mode == 'SHDR_BNK':
            self.display_text.insert(END, self.TITLES[1] + ' \n')
            self.display_text.tag_add("TITLE", 1.19, 1.31)
        elif self.data.display_mode == 'FRAMES':
            self.display_text.insert(END, self.TITLES[2] + ' \n')
            self.display_text.tag_add("TITLE", 1.19, 1.31)
        else:
            self.display_text.insert(END, self.TITLES[0] + ' \n')
            self.display_text.tag_add("TITLE", 1.19, 1.28)

    def _load_player(self):
        if self.data.player_mode == 'now':
            now_banner = self._get_banner_for_player('now')
            self.display_text.insert(END, now_banner + '\n')
            self.display_text.tag_add("NOW_PLAYER_INFO", 2.0, 2.0 + self.SELECTOR_WIDTH)
        elif self.data.player_mode == 'next':
            next_banner = self._get_banner_for_player('next')
            self.display_text.insert(END, next_banner + '\n')
            self.display_text.tag_add("NEXT_PLAYER_INFO", 2.0, 2.0 + self.SELECTOR_WIDTH)

        status = self._get_status_for_player()
        self.display_text.insert(END, status + '\n')
        self.display_text.tag_add("NOW_ALPHA", 3.0, 3.17)
        self.display_text.tag_add("CAPTURE_ALPHA", 3.18, 3.29)
        self.display_text.tag_add("NEXT_ALPHA", 3.29, 3.47)

    def _load_display_body(self):
        self.body_title = self._generate_body_title()
        if self.data.display_mode == 'BROWSER':
            self._load_browser()
        elif self.data.display_mode == 'SETTINGS':
            self._load_settings()
        elif self.data.display_mode == 'SAMPLER':
            self._load_sampler()
        elif self.data.display_mode == 'SHADERS':
            self._load_shaders()
        elif self.data.display_mode == 'SHDR_BNK':
            self._load_shader_bank()
        elif self.data.display_mode == 'SHDR_MOD':
            self._load_modulation_bank()
        elif self.data.display_mode == 'FRAMES':
            self._load_detour()
        elif self.data.display_mode == 'PLUGINS':
            self._load_plugins()
        else:
            from data_centre.plugin_collection import DisplayPlugin
            for plugin in self.data.plugins.get_plugins(DisplayPlugin):
                if plugin.is_handled(self.data.display_mode):
                    self._load_plugin_page(self.data.display_mode, plugin)
        self.display_text.tag_add("DISPLAY_MODE", 4.19, 4.29)
        self.display_text.tag_add("COLUMN_NAME", 5.0, 6.0)

    def _load_plugin_page(self, display_mode, plugin):
        plugin.show_plugin(self, display_mode)

    def _load_sampler(self):
        bank_data = self.data.bank_data[self.data.bank_number]

        self.display_text.insert(END, '{} \n'.format(self.body_title))

        self.display_text.insert(END, '{:>6} {:<17} {:>5} {:<5} {:<5} \n'.format(
                '{}-slot'.format(self.data.bank_number), 'name', 'length', 'start', 'end'))
        for index, slot in enumerate(bank_data):
            name_without_extension = slot['name'].rsplit('.', 1)[0]
            self.display_text.insert(END, '{:^6} {:<17} {:^5} {:>5} {:<5} \n'.format(
                    index, name_without_extension[0:17], self.format_time_value(slot['length']),
                    self.format_time_value(slot['start']), self.format_time_value(slot['end'])))
            if index % 2:
                self.display_text.tag_add("ZEBRA_STRIPE", self.ROW_OFFSET + index,
                                          self.ROW_OFFSET + self.SELECTOR_WIDTH + index)
            if self.data.is_this_path_broken(slot['location']):
                self.display_text.tag_add("BROKEN_PATH", self.ROW_OFFSET + index,
                                          self.ROW_OFFSET + self.SELECTOR_WIDTH + index)
        # highlight the slot of the selected player
        if self.data.player_mode == 'next':
            bank_slot = self.video_driver.next_player.bankslot_number
        else:
            bank_slot = self.video_driver.current_player.bankslot_number
        current_bank, current_slot = self.data.split_bankslot_number(bank_slot)
        if current_bank is self.data.bank_number:
            self._highlight_this_row(current_slot)

    def _load_browser(self):
        browser_list = self.browser_menu.menu_list
        number_of_lines_displayed = 0
        self.display_text.insert(END, '{} \n'.format(self.body_title))

        self.display_text.insert(END, '{:40} {:5} \n'.format('path', 'slot'))

        number_of_browser_items = len(browser_list)
        for index in range(number_of_browser_items):
            if number_of_lines_displayed >= self.MENU_HEIGHT:
                break
            if index >= self.browser_menu.top_menu_index:
                path = browser_list[index]
                self.display_text.insert(END, '{:40} {:5} \n'.format(path['name'][0:38], path['slot']))
                number_of_lines_displayed = number_of_lines_displayed + 1

        for index in range(self.browser_menu.top_menu_index + self.browser_menu.menu_height - number_of_browser_items):
            self.display_text.insert(END, '\n')

        self._highlight_this_row(self.browser_menu.selected_list_index - self.browser_menu.top_menu_index)

    def _load_settings(self):
        line_count = 0
        settings_list = self.settings_menu.menu_list
        self.display_text.insert(END, '{} \n'.format(self.body_title))

        self.display_text.insert(END, '{:^23} {:^22} \n'.format('SETTING', 'VALUE'))
        number_of_settings_items = len(settings_list)
        for index in range(number_of_settings_items):
            if line_count >= self.MENU_HEIGHT:
                break
            if index >= self.settings_menu.top_menu_index:
                setting = settings_list[index]
                self.display_text.insert(END, '{:<23} {:<22} \n'.format(setting['name'][0:22], setting['value']))
                line_count = line_count + 1

        for index in range(self.settings_menu.top_menu_index + self.settings_menu.menu_height - number_of_settings_items):
            self.display_text.insert(END, '\n')

        self._highlight_this_row(self.settings_menu.selected_list_index - self.settings_menu.top_menu_index)

    def _load_plugins(self):
        line_count = 0
        self.display_text.insert(END, '{} \n'.format(self.body_title))
        self.display_text.insert(END, '{:<35} {:<8} \n'.format('plugin', 'status'))
        ## showing list of plugins:
        plugins_list = sorted([
            (type(plugin).__name__, type(plugin).__name__ in self.data.get_enabled_plugin_class_names()) \
            for plugin in self.data.plugins.get_plugins(include_disabled=True)
        ])
        self.plugins_menu.menu_list = plugins_list

        number_of_plugins = len(plugins_list)
        for index in range(number_of_plugins):
            if line_count >= self.MENU_HEIGHT:
                break
            if index >= self.plugins_menu.top_menu_index:
                plugin_line = plugins_list[index]
                self.display_text.insert(END, '{:<35} {:<8} \n'.format(plugin_line[0], 'Enabled' if plugin_line[1] else 'Disabled'))
                line_count = line_count + 1

        for index in range(self.plugins_menu.top_menu_index + self.plugins_menu.menu_height - number_of_plugins):
            self.display_text.insert(END, '\n')

        self._highlight_this_row(self.plugins_menu.selected_list_index - self.plugins_menu.top_menu_index)

    def _load_shaders(self):
        line_count = 0
        self.display_text.insert(END, '{} \n'.format(self.body_title))

        ## showing current shader info:
        shader = self.shaders.selected_shader_list[self.data.shader_layer]
        self.display_text.insert(END, '{:<1}{}{:<1}:{:<2} {:<16} '.format \
            (self.data.shader_layer,
             self.get_speed_indicator(self.shaders.selected_speed_list[self.data.shader_layer]),
             self.shaders.selected_status_list[self.data.shader_layer], shader['shad_type'][0],
             shader['name'].lstrip()[0:16]))
        for i in range(min(4, shader['param_number'])):
            display_param = self.format_param_value(self.shaders.selected_param_list[self.data.shader_layer][i])
            if display_param == 100:
                display_param == 99
            self.display_text.insert(END, 'x{}:{:02d}'.format(i, display_param))
        self.display_text.insert(END, '\n')
        self.display_text.tag_add("COLUMN_NAME", 5.0, 6.0)
        ## showing list of other shaders:
        shaders_list = self.shaders.shaders_menu_list
        number_of_shader_items = len(shaders_list)
        for index in range(number_of_shader_items):
            if line_count >= self.MENU_HEIGHT:
                break
            if index >= self.shaders.shaders_menu.top_menu_index:
                shader_line = shaders_list[index]
                self.display_text.insert(END, '{:<40} {:<5} \n'.format(shader_line['name'][0:30], shader_line['shad_type']))
                line_count = line_count + 1

        for index in range(self.shaders.shaders_menu.top_menu_index + self.shaders.shaders_menu.menu_height - number_of_shader_items):
            self.display_text.insert(END, '\n')

        self._highlight_this_row(self.shaders.shaders_menu.selected_list_index - self.shaders.shaders_menu.top_menu_index)
        if self.data.control_mode == "SHADER_PARAM":
            self._highlight_this_param(self.shaders.focused_param)

    def _load_shader_bank(self):
        shader_bank_data = self.data.shader_bank_data[self.data.shader_layer]

        self.display_text.insert(END, '{} \n'.format(self.body_title))

        self.display_text.insert(END, '{:>6} {:<11} {:<5} '.format(
                '{} {}'.format(self.data.shader_layer, self.get_speed_indicator(self.shaders.selected_speed_list[self.data.shader_layer])),
                'name', 'type'))

        shader = self.shaders.selected_shader_list[self.data.shader_layer]

        for i in range(min(4, shader['param_number'])):
            display_param = self.format_param_value(self.shaders.selected_param_list[self.data.shader_layer][i])
            if display_param == 100:
                display_param == 99
            self.display_text.insert(END, 'x{}:{:02d}'.format(i, display_param))
        self.display_text.insert(END, '\n')

        for index, slot in enumerate(shader_bank_data):
            name_without_extension = slot['name'].rsplit('.', 1)[0]
            self.display_text.insert(END, '{:^6} {:<17} {:<5} \n'.format(index, name_without_extension[0:17], slot['shad_type']))
            if index % 2:
                self.display_text.tag_add("ZEBRA_STRIPE", self.ROW_OFFSET + index,
                                          self.ROW_OFFSET + self.SELECTOR_WIDTH + index)
        # highlight the slot of the selected player
        current_slot = self.shaders.selected_shader_list[self.data.shader_layer].get('slot', None)
        not_playing_tag = self.shaders.selected_status_list[self.data.shader_layer] != '▶'
        if current_slot is not None:
            self._highlight_this_row(current_slot, gray=not_playing_tag)

        self._highlight_this_param(self.shaders.focused_param)

    def _load_modulation_bank(self):
        shader_bank_data = self.data.shader_bank_data[self.data.shader_layer]

        self.display_text.insert(END, '{} \n'.format(self.body_title))

        self.display_text.insert(END, '{:>6} {:<11} {:<5} '.format(
                '{} {}'.format(self.data.shader_layer, self.get_speed_indicator(self.shaders.selected_speed_list[self.data.shader_layer])),
                'name', 'type'))

        shader = self.shaders.selected_shader_list[self.data.shader_layer]

        """for i in range(min(4,shader['param_number'])):
            display_param = self.format_param_value(self.shaders.selected_param_list[self.data.shader_layer][i])
            if display_param == 100:
                display_param == 99
            self.display_text.insert(END, 'x{}:{:02d}'.format(i, display_param))"""
        self.display_text.insert(END, '\n')

        """for index, slot in enumerate(shader_bank_data):
            name_without_extension =  slot['name'].rsplit('.',1)[0]
            #self.display_text.insert(END, '{:^6} {:<17} {:<5} '.format(index, name_without_extension[0:17], slot['shad_type']))
            self.display_text.insert(END, '{:^2} {:<14} {:<3} '.format(index, name_without_extension[0:14], slot['shad_type']))
                #self.display_text.insert(END, '\t')
            if (index) % 2:
                self.display_text.tag_add("ZEBRA_STRIPE", self.ROW_OFFSET + index,
                                  self.ROW_OFFSET + self.SELECTOR_WIDTH + index)
                self.display_text.insert(END, '\n')
            else:
                self.display_text.insert(END, ' | ')

        self.display_text.insert(END, '\n')

        # highlight the slot of the selected player
        current_slot = self.shaders.selected_shader_list[self.data.shader_layer].get('slot', None)
        not_playing_tag = self.shaders.selected_status_list[self.data.shader_layer] != '▶'
        if current_slot is not None:
            self._highlight_this_row(current_slot, gray=not_playing_tag)

        self._highlight_this_param(self.shaders.focused_param) """

        # show info about the modulation configuration
        # self.display_text.insert(END, "Lyr|1a b c d|2a b c d|3a b c d|4a b c d\n")
        # self.display_text.insert(END, "Lyr")
        """for i in range(4):
            self.display_text.insert(END, "|%s"%i)
            for i in range(4):
                a = 'abcd'[i]
                if i==self.shaders.selected_modulation_slot:
                    a = a.upper()
                self.display_text.insert(END, "%s "%a)"""
        # self.display_text.insert(END,  "\n")
        """for layer, modulations in enumerate(self.shaders.modulation_level):
            if (layer==self.data.shader_layer):
                self.display_text.insert(END, '*')
            else:
                self.display_text.insert(END, ' ')
            self.display_text.insert(END, '%s:' % layer)
            for param, levels in enumerate(modulations):
                self.display_text.insert(END, '|')
                for slot,level in enumerate(levels):
                    self.display_text.insert(END, ' %s'%self.get_bar(level))
                self.display_text.insert(END, ' ')
            self.display_text.insert(END, '\n')"""

        for layer in range(3):
            o = ""
            o += self.data.plugins.fm.get_live_frame().get_shader_layer_summary(layer)
            o += "\n  Modmatrix:\t"

            name = self.shaders.selected_shader_list[layer].get('name').strip()
            # o = ""
            for slot in range(4):
                sl = self.get_mod_slot_label(slot)
                o += sl + ("[" if sl.isupper() else "-")
                for param in range(4):
                    o += self.get_bar(self.shaders.modulation_level[layer][param][slot])
                o += ("]" if sl.isupper() else "-") + " "
            self.display_text.insert(END, "%s %s:\t%s\n\n" % (">" if layer == self.data.shader_layer else " ", layer, o))
        self.display_text.insert(END, '\n')
        # todo: this doesnt work but would be a better way to highlight the selected modulation slot/layer
        """self._highlight_this_param(
                self.shaders.selected_modulation_slot, 
                param_row = 10+self.data.shader_layer, 
                param_length = 0.05, 
                column_offset = 0.1
            )"""

    def _load_detour(self):
        line_count = 0
        self.display_text.insert(END, '{} \n'.format(self.body_title))

        ## showing current detour info:
        self.display_text.insert(END, '{:^23} {:^22} \n'.format('SETTING', 'VALUE'))
        self.display_text.insert(END, '{:>23} {:<22} \n'.format("DETOUR_ACTIVE", self.data.detour_active))
        for index, (key, value) in enumerate(self.data.detour_settings.items()):
            if index < 8:
                self.display_text.insert(END, '{:>23} {:<22} \n'.format(key, value))
        detour_banner = self.create_detour_display_banner(self.data.detour_settings['detour_size'], self.data.detour_settings['detour_position'], self.data.detour_settings['detour_start'], self.data.detour_settings['detour_end'])
        self.display_text.insert(END, '{} \n'.format(detour_banner))
        self._set_colour_from_mix(self.data.detour_settings['detour_mix'])
        self.display_text.tag_add("DETOUR_BAR", 15.0, 15.0 + self.SELECTOR_WIDTH)

    def _load_message(self):
        if self.message_handler.current_message[1]:
            self.display_text.insert(END, '{:5} {:42} \n'.format(
                    self.message_handler.current_message[0], self.message_handler.current_message[1][0:38]))
            self.display_text.tag_add('{}_MESSAGE'.format(
                    self.message_handler.current_message[0]), 16.0, 16.0 + self.SELECTOR_WIDTH)
            if self.message_handler.current_message[2]:
                self.message_handler.current_message[2] = False
                message_length = 4000
                self.tk.after(message_length, self.message_handler.clear_message)
        elif self.data.function_on:
            self.display_text.insert(END, '{:^47} \n'.format('< FUNCTION KEY ON >'))
            self.display_text.tag_add('FUNCTION', 16.0, 16.0 + self.SELECTOR_WIDTH)
        else:
            feedback = ''
            if self.data.feedback_active:
                feedback = 'FDBCK'

            self.display_text.insert(END, '{:8} {:<28} {:>5} \n'.format('CONTROL:', str(self.data.control_mode), feedback))
            self.display_text.tag_add('TITLE', 16.0, 16.0 + self.SELECTOR_WIDTH)

    def _highlight_this_row(self, row, gray=False):
        highlight_tag = "SELECT"
        if gray:
            highlight_tag = "BROKEN_PATH"
        self.display_text.tag_remove("ZEBRA_STRIPE", self.ROW_OFFSET + row,
                                     self.ROW_OFFSET + self.SELECTOR_WIDTH + row)
        self.display_text.tag_add(highlight_tag, self.ROW_OFFSET + row,
                                  self.ROW_OFFSET + self.SELECTOR_WIDTH + row)

    def _unhighlight_this_row(self, row):
        self.display_text.tag_remove("SELECT", self.ROW_OFFSET + row,
                                     self.ROW_OFFSET + self.SELECTOR_WIDTH + row)

    def _highlight_this_param(self, param_num, column_offset=0.26, param_length=0.05, param_row=None):
        if param_row is None:
            param_row = self.ROW_OFFSET - 1
        self.display_text.tag_add("SHADER_PARAM",
                                  round(param_row + column_offset + param_num * param_length, 2),
                                  round(param_row + column_offset + (param_num + 1) * param_length, 2)
                                  )

    def _get_status_for_player(self):
        now_slot, now_status, now_alpha, next_slot, next_status, next_alpha = self.video_driver.get_player_info_for_status()

        if self.capture is not None:
            capture_status = self._generate_capture_status()
            preview_alpha = self.capture.get_preview_alpha()
        else:
            capture_status = ''
            preview_alpha = 0

        if preview_alpha == None:
            preview_alpha = 0
        # print('capture alpha is {}'.format(preview_alpha))

        self._set_colour_from_alpha(now_alpha, preview_alpha, next_alpha)

        now_info = 'NOW [{}] {}'.format(now_slot, now_status)
        next_info = 'NEXT [{}] {}'.format(next_slot, next_status)
        capture_info = '{}'.format(capture_status)
        return '{:17} {:10} {:17}'.format(now_info[:17], capture_info[:10], next_info[:18])

    def _get_banner_for_player(self, player):
        start, end, position = self.video_driver.get_player_info_for_banner(player)
        banner = self.create_video_display_banner(start, end, position)
        time_been = self.format_time_value(position - start)
        time_left = self.format_time_value(end - position)
        return ' {:5} {} {:5}'.format(time_been, banner, time_left)

    def _generate_capture_status(self):
        is_previewing = self.capture.is_previewing
        is_recording = self.capture.is_recording
        rec_time = -1
        if is_recording == True:
            rec_time = self.capture.get_recording_time()
        capture_status = ''
        if is_previewing and is_recording == True:
            capture_status = '<{}>'.format('REC' + self.format_time_value(rec_time))
        elif is_previewing and is_recording == 'saving':
            capture_status = '<{}>'.format('_saving_')
        elif is_previewing:
            capture_status = '<{}>'.format('_preview')
        elif is_recording == True:
            capture_status = '[{}]'.format('REC' + self.format_time_value(rec_time))
        elif is_recording == 'saving':
            capture_status = '[{}]'.format('_saving_')
        else:
            capture_status = ''

        return capture_status

    def get_bar(self, value, max_value=1.0):
        if value is None:
            return " "
        value = abs(value / max_value)  # abs() so negative values make some sense
        if value > 1.0:
            value = 1.0
        elif value < 0.0:
            value = 0.0
        bar = u"_\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588"
        g = '%s' % bar[int(value * (len(bar) - 1))]
        return g

    def get_mod_slot_label(self, slot):
        sl = 'ABCD'[slot]
        if slot != self.shaders.selected_modulation_slot:
            sl = sl.lower()
        return sl

    def get_speed_indicator(self, value, convert=True):
        if convert:
            value = (value * 2.0) - 1.0  # convert 0 to 1 to -1 to +1
        output = u""
        if value == 0.0 or (value >= -0.02 and value <= 0.02):
            output += u"\u23f9"  # stopped
        elif value <= -0.5:
            output += u"\u00AB"  # fast reverse
        elif value < 0.0:
            output += u"\u2039"  # reverse
        elif value >= 0.5:
            output += u"\u00BB"  # fast forward
        elif value > 0.0:
            output += u"\u203A"  # forward

        # output += " {:03f}".format(value)
        output += self.get_bar(value)

        return output

    def get_compact_indicators(self, inp):
        step = 2
        s = ""
        for i in range(0, len(inp), step):  # number of shader slots per layer
            selected1 = inp[i]
            if i + 1 > len(inp):  # catch if odd number of elements passed to us?
                selected2 = False
            else:
                selected2 = inp[i + 1]

            if selected1 and selected2:
                # full block
                s += u"\u2588"
            elif selected1 and not selected2:
                # left block
                s += u"\u258C"
            elif selected2 and not selected1:
                # right block
                s += u"\u2590"
            else:
                # empty
                s += "_"

            # s += "#" if selected else "-"
        return s

    @staticmethod
    def create_video_display_banner(start, end, position):
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
        elif end - start != 0 and not math.isnan(position):
            # print('start value is {}, end value is {}, position is {}'.format(start, end, position))
            marker = int(math.floor(float(position - start) /
                                    float(end - start) * (max - 1)) + 1)
            banner_list[marker] = '*'

        return ''.join(banner_list)

    @staticmethod
    def create_detour_display_banner(size, position, start, end):
        banner_list = ['|', '-', '-', '-', '-', '-', '-', '-', '-',
                       '-', '-', '-', '-', '-', '-', '-', '-', '-',
                       '-', '-', '-', '-', '-', '-', '-', '-', '-',
                       '-', '-', '-', '-', '-', '-', '-', '-', '-',
                       '-', '-', '-', '-', '-', '-', '-', '-', '-',
                       '|']
        max = len(banner_list) - 1
        if size == 0:
            size = max
        # print('start value is {}, end value is {}, position is {}'.format(start, end, position))
        if start > 0:
            start = int(math.floor(float(start) /
                                   float(size) * (max - 1)) + 1)
            banner_list[start] = '['
        if end > 0:
            end = int(math.floor(float(end) /
                                 float(size) * (max - 1)) + 1)
            banner_list[end] = ']'
        position = int(math.floor(float(position) /
                                  float(size) * (max - 1)) + 1)
        if 0 <= position and position < len(banner_list):
            banner_list[position] = '*'

        return ''.join(banner_list)

    def _set_colour_from_mix(self, mix):
        hex_colour = self.hex_from_rgb(255, 255 - int(255 * mix), int(255 * mix))
        self.display_text.tag_configure("DETOUR_BAR", background="black", foreground=hex_colour)

    def _set_colour_from_alpha(self, now_alpha, preview_alpha, next_alpha):
        upper_bound = 150
        if self.capture is not None:
            is_recording = self.capture.is_recording == True
        else:
            is_recording = False
        ### scale values
        scaled_now = int((now_alpha / 255) * (255 - upper_bound) + upper_bound)
        scaled_preview = int((preview_alpha / 255) * (255 - upper_bound) + upper_bound)
        scaled_next = int((next_alpha / 255) * (255 - upper_bound) + upper_bound)

        ### convert to hex
        now_colour = self.hex_from_rgb(scaled_now, scaled_now, 0)
        capture_colour = self.hex_from_rgb(255 * is_recording, 100, scaled_preview)
        next_colour = self.hex_from_rgb(0, scaled_next, scaled_next)
        ### update the colours
        self.display_text.tag_configure("NOW_ALPHA", background="black", foreground=now_colour)
        self.display_text.tag_configure("CAPTURE_ALPHA", background="black", foreground=capture_colour)
        self.display_text.tag_configure("NEXT_ALPHA", background="black", foreground=next_colour)

    def _generate_body_title(self):
        display_modes = self.data.get_display_modes_list()
        current_mode = self.data.display_mode
        selected_list = []
        for index, v in enumerate(display_modes):
            if v == current_mode:
                while len(v) < 8:
                    v = v + '_'
                selected_list.append('[{}]'.format(v))
                selected_list_index = index
            else:
                selected_list.append('<{}>'.format(v[:2].lower()))
                # 18 char to PURPLE : 18 - 29 ,18 after
        if selected_list_index > 4:
            selected_list = selected_list[selected_list_index - 4:len(selected_list)]
            selected_list = ['--'] + selected_list
        selected_string = ''.join(selected_list)
        # if len(selected_string)<19:
        #    selected_string += '-'*(21-len(selected_string))
        # selected_string = selected_string[:30]
        # wid = 19 #int(2+((len(display_modes)/2)*4))
        output = ('-' * ((19) - (selected_list_index * 4))) + \
                 selected_string + \
                 ('-' * (18 - ((len(display_modes) - selected_list_index - 1) * 4)))
        output = output[0:46]
        return output

    @staticmethod
    def hex_from_rgb(r, g, b):
        return '#%02x%02x%02x' % (r, g, b)

    def _update_screen_every_second(self):
        self.refresh_display()
        self.tk.after(50, self._update_screen_every_second)

    last_refreshed = 0
    REFRESH_LIMIT = 100

    def refresh_display(self):
        if self.data.update_screen:
            if time.time() * 1000 - self.last_refreshed < self.REFRESH_LIMIT:
                return
            self.last_refreshed = time.time() * 1000
            self.display_text.configure(state='normal')
            self.display_text.delete(1.0, END)
            self._load_display()
            self.display_text.configure(state='disable')
            self.display_text.focus_set()

    @staticmethod
    def format_time_value(time_in_seconds):
        if time_in_seconds < 0:
            return ''
        elif time_in_seconds >= 6000:
            return '99:99'
        else:
            return time.strftime("%M:%S", time.gmtime(time_in_seconds))

    @staticmethod
    def format_speed_value(value):
        if value == 1:
            return ''
        else:
            return value

    @staticmethod
    def format_param_value(value):
        display_param = int(100 * value)
        if display_param == 100:
            display_param = 99
        return display_param
