import string

class NumpadInput(object):
    def __init__(self, message_handler, display, actions, data):
        self.message_handler = message_handler
        self.display = display
        self.actions = actions
        self.key_mappings = data.get_keypad_mapping_data()
        self.bind_actions()

    def bind_actions(self):
        self.display.display_text.bind("<Key>", self.on_key_press)

    def on_key_press(self, event):
        
        numpad = list(string.ascii_lowercase[0:19])
        if event.char is '.':
            self.actions.quit_the_program()
        elif event.char in numpad:
            print('the event key pressed is {}'.format(event.char))
            print('the corrosponding mapping is {}'.format(self.key_mappings[event.char]))
            this_mapping = self.key_mappings[event.char]
            print('the current display mode is {}'.format(self.display.display_mode))
            if self.display.display_mode in this_mapping:
                mode = self.display.display_mode
            elif 'DEFAULT' in this_mapping:
                mode = 'DEFAULT'
            print('the mode is set to {}'.format(mode))

            if self.message_handler.function_on and len(this_mapping[mode]) > 1:
                print('the action being called is {}'.format(this_mapping[mode][1]))
                getattr(self.actions, this_mapping[mode][1])()
            else:
                print('the action being called is {}'.format(this_mapping[mode][0]))
                getattr(self.actions, this_mapping[mode][0])()
          
            self.display.refresh_display()
        else:
            print('{} is not in keypad map'.format(event.char))



