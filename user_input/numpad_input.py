

class NumpadInput(object):
    def __init__(self, display, actions):
        self.display = display
        self.actions = actions
        self.bind_actions()

    def bind_actions(self):
        self.display.display_text.bind("<Key>", self.on_key_press)
        self.display.display_text.bind("<BackSpace>", self.on_backspace_press)

    def on_key_press(self, event):
        if event.char == '-':
            self.on_minus_press()
        elif event.char == '+':
            self.on_plus_press()
        elif event.char == '\r':
            self.on_enter_press()
        elif event.char == '*':
            self.on_star_press()
        elif event.char == '/':
            self.on_slash_press()
        elif event.char == '.':
            self.on_dot_press()
        if event.char is not '.':        
            self.display.refresh_display()

        # for bank in range(10):
        #     if event.char == str(bank):
        #         self.actions.load_this_bank_into_next_player(bank)

    def on_backspace_press(self, event):
        if self.display.display_mode == 'BROWSER':
            self.actions.enter_on_browser_selection()
        elif self.display.display_mode == 'LOOPER':
            self.actions.toggle_pause_on_player()
        elif self.display.display_mode == 'SETTINGS':
            self.actions.enter_on_settings_selection()
        self.display.refresh_display()

    def on_minus_press(self):
        if self.display.display_mode == 'BROWSER':
            self.actions.move_browser_selection_up()
        elif self.display.display_mode == 'LOOPER':
            self.actions.seek_back_on_player()
        elif self.display.display_mode == 'SETTINGS':
            self.actions.move_settings_selection_up()

    def on_plus_press(self):
        if self.display.display_mode == 'BROWSER':
            self.actions.move_browser_selection_down()
        elif self.display.display_mode == 'LOOPER':
            self.actions.seek_forward_on_player()
        elif self.display.display_mode == 'SETTINGS':
            self.actions.move_settings_selection_down()

    def on_enter_press(self):
        self.actions.trigger_next_player()

    def on_star_press(self):
        self.actions.cycle_display_mode()

    def on_slash_press(self):
        pass

    def on_dot_press(self):
        self.actions.quit_the_program()

