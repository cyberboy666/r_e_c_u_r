import subprocess

class Actions(object):
    def __init__(self, tk, message_handler, data, video_driver, display):
        self.tk = tk
        self.message_handler = message_handler
        self.data = data
        self.video_driver = video_driver
        self.display = display


    def move_browser_selection_down(self):
        self.display.navigate_menu('down', len(self.data.return_browser_list()))

    def move_browser_selection_up(self):
        self.display.navigate_menu('up', len(self.data.return_browser_list()))

    def enter_on_browser_selection(self):
        is_file, name = self.data.browser_data.extract_file_type_and_name_from_browser_format(
            self.data.return_browser_list()[self.display.selected_list_index]['name'])
        if is_file:
            self.data.create_new_slot_mapping_in_first_open(name)
        else:
            self.data.browser_data.update_open_folders(name)
        self.data.rewrite_browser_list()

    def move_settings_selection_down(self):
        self.display.navigate_menu('down', len(self.data.get_settings_data()))

    def move_settings_selection_up(self):
        self.display.navigate_menu('up', len(self.data.get_settings_data()))

    def enter_on_settings_selection(self):
        is_action, action = self.data.check_if_setting_selection_is_action_otherwise_cycle_value(self.display.selected_list_index)
        print('is_action : {}, action : {}'.format(is_action,action))
        if(is_action):
            getattr(self, action)()

    def clear_all_slots(self):
        self.data.clear_all_slots()

    def quit_the_program(self):
        if self.video_driver.has_omx:
            self.video_driver.exit_all_players()
        self.tk.destroy()

    def load_this_slot_into_next_player(self, slot):
        self.data.update_next_slot_number(slot)
        self.video_driver.next_player.reload()

    def load_slot_0_into_next_player(self):
        self.load_this_slot_into_next_player(0)

    def load_slot_1_into_next_player(self):
        self.load_this_slot_into_next_player(1)

    def load_slot_2_into_next_player(self):
        self.load_this_slot_into_next_player(2)

    def load_slot_3_into_next_player(self):
        self.load_this_slot_into_next_player(3)

    def load_slot_4_into_next_player(self):
        self.load_this_slot_into_next_player(4)

    def load_slot_5_into_next_player(self):
        self.load_this_slot_into_next_player(5)

    def load_slot_6_into_next_player(self):
        self.load_this_slot_into_next_player(6)

    def load_slot_7_into_next_player(self):
        self.load_this_slot_into_next_player(7)

    def load_slot_8_into_next_player(self):
        self.load_this_slot_into_next_player(8)

    def load_slot_9_into_next_player(self):
        self.load_this_slot_into_next_player(9)

    def trigger_next_player(self):
        self.video_driver.manual_next = True

    def cycle_display_mode(self):
        self.display.top_menu_index = 0
        self.display.selected_list_index = self.display.top_menu_index
        if self.display.display_mode == "BROWSER":
            self.display.display_mode = "SETTINGS"
        elif self.display.display_mode == "SAMPLER":
            self.display.display_mode = "BROWSER"
        elif self.display.display_mode == "SETTINGS":
            self.display.display_mode = "SAMPLER"

    def toggle_pause_on_player(self):
        self.video_driver.current_player.toggle_pause()

    def seek_forward_on_player(self):    
        self.video_driver.current_player.seek(30)

    def seek_back_on_player(self):
        self.video_driver.current_player.seek(-30)

    def toggle_function(self):
        self.message_handler.function_on = not self.message_handler.function_on

    def set_playing_sample_start_to_current_duration(self):
        current_slot = self.video_driver.current_player.slot_number
        current_position = self.video_driver.current_player.get_position()
        self.data.update_slot_start_to_this_time(current_slot, current_position)
        self.load_this_slot_into_next_player(current_slot)

    def clear_playing_sample_start_time(self):
        current_slot = self.video_driver.current_player.slot_number
        self.data.update_slot_start_to_this_time(current_slot, -1)
        self.load_this_slot_into_next_player(current_slot)

    def set_playing_sample_end_to_current_duration(self):
        current_slot = self.video_driver.current_player.slot_number
        current_position = self.video_driver.current_player.get_position()
        self.data.update_slot_end_to_this_time(current_slot, current_position)
        self.load_this_slot_into_next_player(current_slot)

    def clear_playing_sample_end_time(self):
        current_slot = self.video_driver.current_player.slot_number
        self.data.update_slot_end_to_this_time(current_slot, -1)
        self.load_this_slot_into_next_player(current_slot)

    def switch_display_to_hdmi(self):
        settings = self.data.get_settings_data()
        current_screen_mode = [x['options'][0] for x in settings if x['name'] == 'SCREEN_SIZE']
        if('dev_mode' in current_screen_mode): 
            self.run_script('switch_display_to_hdmi')
        else:
            self.message_handler.set_message('INFO', 'must be in dev_mode to change display')

    def switch_display_to_lcd(self):
        settings = self.data.get_settings_data()
        current_screen_mode = [x['options'][0] for x in settings if x['name'] == 'SCREEN_SIZE']
        if('dev_mode' in current_screen_mode): 
            self.run_script('switch_display_to_lcd')
        else:
            self.message_handler.set_message('INFO', 'must be in dev_mode to change display')

    def run_script(self, script_name):
        try:
            subprocess.call(['/home/pi/r_e_c_u_r/dotfiles/{}.sh'.format(script_name)])
        except exception as e:
            self.message_handler.set_message('ERROR',e.message)
        
