import data_centre


class Actions(object):
    def __init__(self, tk, video_driver, display):
        self.tk = tk
        self.video_driver = video_driver
        self.display = display

    def move_browser_selection_down(self):
        self.display.move_browser_down()

    def move_browser_selection_up(self):
        self.display.move_browser_up()

    def enter_on_browser_selection(self):
        self.display.browser_enter()

    def move_settings_selection_down(self):
        self.display.move_settings_down()

    def move_settings_selection_up(self):
        self.display.move_settings_up()

    def enter_on_settings_selection(self):
        self.display.settings_enter()

    @staticmethod
    def clear_all_sampler_banks():
        data_centre.clear_all_banks()

    def quit_the_program(self):
        if self.video_driver.has_omx:
            self.video_driver.exit_all_players()
        self.tk.destroy()

    def load_this_bank_into_next_player(self, bank):
        data_centre.update_next_bank_number(bank)
        self.video_driver.next_player.reload()

    def trigger_next_player(self):
        self.video_driver.manual_next = True

    def cycle_display_mode(self):
        if self.display.display_mode == "BROWSER":
            self.display.display_mode = "LOOPER"
        elif self.display.display_mode == "LOOPER":
            self.display.display_mode = "SETTINGS"
        elif self.display.display_mode == "SETTINGS":
            self.display.display_mode = "BROWSER"

    def toggle_pause_on_player(self):
        self.video_driver.current_player.toggle_pause()

    def seek_forward_on_player(self):    
        self.video_driver.current_player.seek(30)

    def seek_back_on_player(self):
        self.video_driver.current_player.seek(-30)
