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
        # self.display.move_browser_up()
        self.display.navigate_menu('up', len(self.data.return_browser_list()))

    def enter_on_browser_selection(self):
        is_file, name = self.data.browser_data.extract_file_type_and_name_from_browser_format(
            self.data.return_browser_list()[self.display.selected_list_index]['name'])
        if is_file:
            self.data.create_new_bank_mapping_in_first_open(name)
        else:
            self.data.browser_data.update_open_folders(name)
        self.data.rewrite_browser_list()

    def move_settings_selection_down(self):
        self.display.navigate_menu('down', len(self.data.get_settings_data()))

    def move_settings_selection_up(self):
        self.display.navigate_menu('up', len(self.data.get_settings_data()))

    def enter_on_settings_selection(self):
        self.data.switch_settings(self.display.selected_list_index)

    def clear_all_sampler_slots(self):
        self.data.clear_all_slots()

    def quit_the_program(self):
        if self.video_driver.has_omx:
            self.video_driver.exit_all_players()
        self.tk.destroy()

    def load_this_slot_into_next_player(self, slot):
        self.data.update_next_slot_number(slot)
        self.video_driver.next_player.reload()

    def trigger_next_player(self):
        self.video_driver.manual_next = True

    def cycle_display_mode(self):
        self.display.topscreen_menu_index = 0
        self.display.current_menu_index = self.display.topscreen_menu_index
        if self.display.display_mode == "BROWSER":
            self.display.display_mode = "SAMPLER"
        elif self.display.display_mode == "SAMPLER":
            self.display.display_mode = "SETTINGS"
        elif self.display.display_mode == "SETTINGS":
            self.display.display_mode = "BROWSER"

    def toggle_pause_on_player(self):
        self.video_driver.current_player.toggle_pause()

    def seek_forward_on_player(self):    
        self.video_driver.current_player.seek(30)

    def seek_back_on_player(self):
        self.video_driver.current_player.seek(-30)
