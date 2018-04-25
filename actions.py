import subprocess

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
            if setting['value'] is None:
                getattr(self, setting['action'])()
            else:
                getattr(self, setting['action'])(setting['value'])

    def clear_all_slots(self):
        self.data.clear_all_slots()

    def quit_the_program(self):
        self.video_driver.exit_all_players()
        self.tk.destroy()

    def _load_this_slot_into_next_player(self, slot):
        self.data.update_next_slot_number(slot)
        self.video_driver.next_player.reload()

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

    def trigger_next_player(self):
        self.video_driver.switch_players_and_play_video()

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

    def toggle_pause_on_player(self):
        self.video_driver.current_player.toggle_pause()

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
        self.data.update_slot_rate_to_this(current_bank, current_slot, new_rate)
        self._load_this_slot_into_next_player(current_slot)

    def decrease_speed(self):
        new_rate = self.video_driver.current_player.change_rate(-0.5)
        current_bank, current_slot = self.data.split_bankslot_number(self.video_driver.current_player.bankslot_number)
        self.data.update_slot_rate_to_this(current_bank, current_slot, new_rate)
        self._load_this_slot_into_next_player(current_slot)

    def set_playing_sample_start_to_current_duration(self):
        current_bank, current_slot = self.data.split_bankslot_number(self.video_driver.current_player.bankslot_number)
        current_position = round(self.video_driver.current_player.get_position(),3)
        self.data.update_slot_start_to_this_time(current_bank, current_slot, current_position)
        self._load_this_slot_into_next_player(current_slot)

    def clear_playing_sample_start_time(self):
        current_bank, current_slot = self.data.split_bankslot_number(self.video_driver.current_player.bankslot_number)
        self.data.update_slot_start_to_this_time(current_bank, current_slot, -1)
        self._load_this_slot_into_next_player(current_slot)

    def set_playing_sample_end_to_current_duration(self):
        current_bank, current_slot = self.data.split_bankslot_number(self.video_driver.current_player.bankslot_number)
        current_position = round(self.video_driver.current_player.get_position(),0)
        self.data.update_slot_end_to_this_time(current_bank, current_slot, current_position)
        self._load_this_slot_into_next_player(current_slot)

    def clear_playing_sample_end_time(self):
        current_bank, current_slot = self.data.split_bankslot_number(self.video_driver.current_player.bankslot_number)
        self.data.update_slot_end_to_this_time(current_bank, current_slot, -1)
        self._load_this_slot_into_next_player(current_slot)

    def toggle_capture_preview(self):
        is_previewing = self.capture.is_previewing
        if is_previewing:
            self.capture.stop_preview()
            if self.video_driver.current_player.status == 'PAUSED':
                self.toggle_pause_on_player()
        else:
            is_successful = self.capture.start_preview()
            if is_successful and self.video_driver.current_player.status != 'PAUSED':
                self.toggle_pause_on_player()

    def toggle_capture_recording(self):
        is_recording = self.capture.is_recording
        if is_recording:
            self.capture.stop_recording()
        else: 
            self.capture.start_recording()

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

    def switch_display_to_hdmi(self):
        settings = self.data.settings
        current_screen_mode = [x['options'][0] for x in settings if x['name'] == 'SCREEN_SIZE']
        if('dev_mode' in current_screen_mode): 
            self.run_script('switch_display_to_hdmi')
        else:
            self.message_handler.set_message('INFO', 'must be in dev_mode to change display')

    def switch_display_to_lcd(self):
        self.run_script('switch_display_to_lcd')


    def set_composite_to_pal(self):
        self.run_script('set_composite_mode','2')
        self.message_handler.set_message('INFO', 'composite set to pal on next restart')

    def set_composite_to_ntsc(self):
        self.run_script('set_composite_mode','0')
        self.message_handler.set_message('INFO', 'composite set to ntsc on next restart')

    def run_script(self, script_name, script_argument=''):
        try:
            subprocess.call(['/home/pi/r_e_c_u_r/dotfiles/{}.sh'.format(script_name),script_argument])
        except Exception as e:
            if hasattr(e, 'message'):
                error_info = e.message
            else:
                error_info = e
            self.message_handler.set_message('ERROR',error_info)
        
