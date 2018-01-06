

class NumpadInput(object):
    def __init__(self, message_handler, display, actions):
        self.message_handler = message_handler
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
        elif event.char == '0':
            self.on_0_press()
        elif event.char == '1':
            self.on_1_press()
        elif event.char == '2':
            self.on_2_press()
        elif event.char == '3':
            self.on_3_press()
        elif event.char == '4':
            self.on_4_press()
        elif event.char == '5':
            self.on_5_press()
        elif event.char == '6':
            self.on_6_press()
        elif event.char == '7':
            self.on_7_press()
        elif event.char == '8':
            self.on_8_press()
        elif event.char == '9':
            self.on_9_press()
        if event.char is not '.':        
            self.display.refresh_display()

    def on_backspace_press(self, event):
        if self.display.display_mode == 'BROWSER':
            self.actions.enter_on_browser_selection()
        elif self.display.display_mode == 'SAMPLER':
            self.actions.toggle_pause_on_player()
        elif self.display.display_mode == 'SETTINGS':
            self.actions.enter_on_settings_selection()
        self.display.refresh_display()

    def on_minus_press(self):
        if self.display.display_mode == 'BROWSER':
            self.actions.move_browser_selection_up()
        elif self.display.display_mode == 'SAMPLER':
            self.actions.seek_back_on_player()
        elif self.display.display_mode == 'SETTINGS':
            self.actions.move_settings_selection_up()

    def on_plus_press(self):
        if self.display.display_mode == 'BROWSER':
            self.actions.move_browser_selection_down()
        elif self.display.display_mode == 'SAMPLER':
            self.actions.seek_forward_on_player()
        elif self.display.display_mode == 'SETTINGS':
            self.actions.move_settings_selection_down()

    def on_enter_press(self):
        self.actions.trigger_next_player()

    def on_star_press(self):
        self.actions.cycle_display_mode()

    def on_slash_press(self):
        self.actions.toggle_function()

    def on_dot_press(self):
        self.actions.quit_the_program()

    def on_0_press(self):
        if self.message_handler.function_on:
            pass
        else:
            self.actions.load_this_slot_into_next_player(0)

    def on_1_press(self):
        if self.message_handler.function_on:
            self.actions.set_playing_sample_start_to_current_duration()
        else:
            self.actions.load_this_slot_into_next_player(1)

    def on_2_press(self):
        if self.message_handler.function_on:
            self.actions.clear_playing_sample_start_time()
        else:
            self.actions.load_this_slot_into_next_player(2)

    def on_3_press(self):
        if self.message_handler.function_on:
            pass
        else:
            self.actions.load_this_slot_into_next_player(3)

    def on_4_press(self):
        if self.message_handler.function_on:
            pass
        else:
            self.actions.load_this_slot_into_next_player(4)

    def on_5_press(self):
        if self.message_handler.function_on:
            pass
        else:
            self.actions.load_this_slot_into_next_player(5)

    def on_6_press(self):
        if self.message_handler.function_on:
            pass
        else:
            self.actions.load_this_slot_into_next_player(6)

    def on_7_press(self):
        if self.message_handler.function_on:
            pass
        else:
            self.actions.load_this_slot_into_next_player(7)

    def on_8_press(self):
        if self.message_handler.function_on:
            pass
        else:
            self.actions.load_this_slot_into_next_player(8)

    def on_9_press(self):
        if self.message_handler.function_on:
            pass
        else:
            self.actions.load_this_slot_into_next_player(9)

