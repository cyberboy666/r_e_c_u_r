import subprocess
import data_centre.length_setter as length_setter

class Actions(object):
    def __init__(self, tk, message_handler, data, video_driver, capture, display):
        self.tk = tk
        self.message_handler = message_handler
        self.data = data
        self.video_driver = video_driver
        self.capture = capture
        self.display = display
        

    def move_browser_selection_down(self):
        self.display.browser_menu.navigate_menu_down()

    def move_browser_selection_up(self):
        self.display.browser_menu.navigate_menu_up()

    def enter_on_browser_selection(self):
        self.display.browser_menu.enter_on_browser_selection()

    def move_settings_selection_down(self):
        self.display.settings_menu.navigate_menu_down()

    def move_settings_selection_up(self):
        self.display.settings_menu.navigate_menu_up()

    def enter_on_settings_selection(self):
        is_setting, setting = self.display.settings_menu.enter_on_setting_selection()
        if is_setting:
            if setting['action']:
                if setting['value'] is None:
                    getattr(self, setting['action'])()
                else:
                    getattr(self, setting['action'])(setting['value'])

    def clear_all_slots(self):
        self.data.clear_all_slots()

    def _load_this_slot_into_next_player(self, slot):
        if self.data.update_next_slot_number(slot):
            self.video_driver.reload_next_player()

    def load_slot_0_into_next_player(self):
        self._load_this_slot_into_next_player(0)

    def load_slot_1_into_next_player(self):
        self._load_this_slot_into_next_player(1)

    def load_slot_2_into_next_player(self):
        self._load_this_slot_into_next_player(2)

    def load_slot_3_into_next_player(self):
        self._load_this_slot_into_next_player(3)

    def load_slot_4_into_next_player(self):
        self._load_this_slot_into_next_player(4)

    def load_slot_5_into_next_player(self):
        self._load_this_slot_into_next_player(5)

    def load_slot_6_into_next_player(self):
        self._load_this_slot_into_next_player(6)

    def load_slot_7_into_next_player(self):
        self._load_this_slot_into_next_player(7)

    def load_slot_8_into_next_player(self):
        self._load_this_slot_into_next_player(8)

    def load_slot_9_into_next_player(self):
        self._load_this_slot_into_next_player(9)

    def switch_to_next_player(self):
        self.video_driver.switch_players_and_start_video()

    def cycle_display_mode(self):
        self.display.top_menu_index = 0
        self.display.selected_list_index = self.display.top_menu_index
        if self.data.display_mode == "BROWSER":
            self.data.display_mode = "SETTINGS"
            self.data.control_mode = 'NAV_SETTINGS'
        elif self.data.display_mode == "SAMPLER":
            self.data.display_mode = "BROWSER"
            self.data.control_mode = 'NAV_BROWSER'
        elif self.data.display_mode == "SETTINGS":
            self.data.display_mode = "SAMPLER"
            self.data.control_mode = 'PLAYER'

    def toggle_action_on_player(self):
        play = 'play' in self.data.settings['sampler']['ON_ACTION']['value']
        show = 'show' in self.data.settings['sampler']['ON_ACTION']['value']
        if play:
            self.toggle_play_on_player()
        if show:
            self.toggle_show_on_player()

    def toggle_play_on_player(self):
        if self.data.player_mode == 'now':
            self.video_driver.current_player.toggle_pause()
        elif self.data.player_mode == 'next':
            self.video_driver.next_player.toggle_pause()

    def toggle_show_on_player(self):
        if self.data.player_mode == 'now':
            self.video_driver.current_player.toggle_show()
        elif self.data.player_mode == 'next':
            self.video_driver.next_player.toggle_show()

    def seek_forward_on_player(self):    
        self.video_driver.current_player.seek(30)

    def seek_back_on_player(self):
        self.video_driver.current_player.seek(-30)

    def toggle_function(self):
        self.data.function_on = not self.data.function_on

    def next_bank(self):
        self.data.update_bank_number_by_amount(1)

    def previous_bank(self):
        self.data.update_bank_number_by_amount(-1)
              
    def increase_speed(self):
        new_rate = self.video_driver.current_player.change_rate(0.5)
        current_bank, current_slot = self.data.split_bankslot_number(self.video_driver.current_player.bankslot_number)
        self.data.update_slot_rate_to_this(current_slot, new_rate)
        self._load_this_slot_into_next_player(current_slot)

    def decrease_speed(self):
        new_rate = self.video_driver.current_player.change_rate(-0.5)
        current_bank, current_slot = self.data.split_bankslot_number(self.video_driver.current_player.bankslot_number)
        self.data.update_slot_rate_to_this(current_slot, new_rate)
        self._load_this_slot_into_next_player(current_slot)

    def set_playing_sample_start_to_current_duration(self):
        current_bank, current_slot = self.data.split_bankslot_number(self.video_driver.current_player.bankslot_number)
        current_position = round(self.video_driver.current_player.get_position(),3)
        self.data.update_slot_start_to_this_time(current_slot, current_position)
        self._load_this_slot_into_next_player(current_slot)

    def clear_playing_sample_start_time(self):
        current_bank, current_slot = self.data.split_bankslot_number(self.video_driver.current_player.bankslot_number)
        self.data.update_slot_start_to_this_time(current_slot, -1)
        self._load_this_slot_into_next_player(current_slot)

    def set_playing_sample_end_to_current_duration(self):
        current_bank, current_slot = self.data.split_bankslot_number(self.video_driver.current_player.bankslot_number)
        current_position = round(self.video_driver.current_player.get_position(),0)
        self.data.update_slot_end_to_this_time(current_slot, current_position)
        self._load_this_slot_into_next_player(current_slot)

    def clear_playing_sample_end_time(self):
        current_bank, current_slot = self.data.split_bankslot_number(self.video_driver.current_player.bankslot_number)
        self.data.update_slot_end_to_this_time(current_slot, -1)
        self._load_this_slot_into_next_player(current_slot)

    def toggle_capture_preview(self):
        is_previewing = self.capture.is_previewing
        if is_previewing:
            self.capture.stop_preview()
            if self.video_driver.current_player.status == 'PAUSED':
                self.video_driver.current_player.toggle_pause()
        else:
            is_successful = self.capture.start_preview()
            if is_successful and self.video_driver.current_player.status != 'PAUSED':
                self.video_driver.current_player.toggle_pause()

    def toggle_capture_recording(self):
        is_recording = self.capture.is_recording
        if is_recording:
            self.capture.stop_recording()
        else: 
            self.capture.start_recording()

    def toggle_screen_mirror(self):
        if self.data.update_screen:
            self.data.update_screen = False
            subprocess.call(['sudo', 'systemctl', 'start', 'raspi2fb@1'])
        else:
            self.data.update_screen = True
            subprocess.call(['sudo', 'systemctl', 'stop', 'raspi2fb@1'])

    def toggle_player_mode(self):
        if self.data.player_mode == 'now':
            self.data.player_mode = 'next'
        elif self.data.player_mode == 'next':
            self.data.player_mode = 'now'

    def set_the_camera_colour_u_with_cc(self, amount):
        u_value = self._convert_midi_cc_value(amount, 0, 255)
        self.capture.set_colour(u_value, None)

    def set_the_camera_colour_v_with_cc(self, amount):
        v_value = self._convert_midi_cc_value(amount, 0, 255)
        self.capture.set_colour(None, v_value)

    def set_the_camera_alpha_cc(self, amount):
        alpha_amount = self._convert_midi_cc_value(amount, 0, 255)
        self.capture.set_alpha(alpha_amount)

    @staticmethod
    def _convert_midi_cc_value(cc_value, min_param, max_param):
        output_range = max_param - min_param
        return int(( cc_value / 127 ) * output_range + min_param)

    def update_video_settings(self, setting_value):
        self.video_driver.update_video_settings()

    def update_capture_settings(self, setting_value):
        self.capture.update_capture_settings()

    def change_output_mode(self, setting_value):
        if setting_value == 'hdmi':
                subprocess.call(['tvservice', '-p'])
                self._refresh_frame_buffer()
        elif setting_value == 'composite':
            self.change_composite_setting(setting_value)

    def check_and_set_output_mode_on_boot(self):
        response = str(subprocess.check_output(['tvservice', '-s']))
        if '0x80002' in response or '0x40002' in response:
            self.data.update_setting_value('video', 'OUTPUT', 'composite')
        else:
            self.data.update_setting_value('video', 'OUTPUT', 'hdmi')

    def change_composite_setting(self, setting_value):
        if setting_value == 'composite':
            mode = self.data.settings['video']['COMPOSITE_TYPE']['value']
            aspect = self.data.settings['video']['COMPOSITE_RATIO']['value']
            progressive = ''
            if self.data.settings['video']['COMPOSITE_PROGRESSIVE']['value'] == 'on':
                progressive = 'p'
            subprocess.call(['tvservice --sdtvon="{} {} {}"'.format(mode, aspect, progressive)],shell=True)
            self._refresh_frame_buffer()
            self.persist_composite_setting(mode, progressive, aspect)

    @staticmethod
    def _refresh_frame_buffer():
        subprocess.run(["fbset -depth 16; fbset -depth 32; xrefresh -display :0" ], shell=True)

    def persist_composite_setting(self, mode, progressive, aspect):
        sdtv_mode = ''
        sdtv_aspect = ''
        print('mode {} , prog {} aspect {} '.format(mode, progressive, aspect))
        if mode == 'PAL' and progressive == 'p':
            sdtv_mode = '18'
        elif mode == 'PAL' and progressive == '':
            sdtv_mode = '2'
        elif mode == 'NTSC' and progressive == 'p':
            sdtv_mode = '16'
        elif mode == 'NTSC' and progressive == '':
            sdtv_mode = '0'

        if aspect == '4:3':
            sdtv_aspect = '1'
        elif aspect == '14:9':
            sdtv_aspect = '2'
        elif aspect == '16:9':
            sdtv_aspect = '3'

        self.update_config_settings(sdtv_mode, sdtv_aspect)

    def update_config_settings(self, sdtv_mode, sdtv_aspect):
        self.run_script('set_composite_mode',sdtv_mode, sdtv_aspect)

    def switch_dev_mode(self, state):
        if state == 'on':
            self.run_script('switch_display_to_hdmi')
        elif state == 'off':
            self.run_script('switch_display_to_lcd')

    def switch_display_to_hdmi(self):
        with open('/boot/config', 'r') as config: 
            with open('/usr/share/X11/xorg.conf.d/99-fbturbo.conf') as framebuffer_conf:
                if 'dtoverlay=waveshare35a:rotate=270' in config and 'dev/fb1' in framebuffer_conf:
                    self.run_script('switch_display_to_hdmi')
                else:
                    self.message_handler.set_message('INFO', 'failed to switch display')
        

    def switch_display_to_lcd(self):
        with open('/boot/config', 'r') as config:
            with open('/usr/share/X11/xorg.conf.d/99-fbturbo.conf') as framebuffer_conf:
                if '##no_waveshare_overlay' in config and 'dev/fb0' in framebuffer_conf:
                    self.run_script('switch_display_to_lcd')
                else:
                    self.message_handler.set_message('INFO', 'failed to switch display')

    def run_script(self, script_name, first_argument='', second_argument=''):
        print('first arg is {} , second is {}'.format(first_argument,second_argument))
        subprocess.call(['/home/pi/r_e_c_u_r/dotfiles/{}.sh'.format(script_name),first_argument, second_argument ])
           
    def toggle_x_autorepeat(self):
        if self.data.auto_repeat_on:
            subprocess.call(['xset', 'r', 'off'])
            self.data.auto_repeat_on = False
        else:
            subprocess.call(['xset', 'r', 'on'])
            self.data.auto_repeat_on = True


    def quit_the_program(self):
        self.video_driver.exit_all_players()
        self.toggle_x_autorepeat()
        self.tk.destroy()

    def set_fixed_length(self, value):
        self.data.control_mode = 'LENGTH_SET'
        self.message_handler.set_message('INFO', 'tap: ■ ;   < > : back')
        self.fixed_length_setter = length_setter.FixedLengthSetter(self.data)


    def return_to_default_control_mode(self):
        if self.data.control_mode == 'LENGTH_SET':
            pass
        self.data.control_mode = 'NAV_SETTINGS'

    def record_fixed_length(self):
        if self.fixed_length_setter:
            self.fixed_length_setter.record_input()
        self.display.settings_menu.generate_settings_list()




        
        
