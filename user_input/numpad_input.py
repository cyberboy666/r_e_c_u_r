import string
import datetime

class NumpadInput(object):
    def __init__(self, root, message_handler, display, actions, data):
        self.root = root
        self.message_handler = message_handler
        self.display = display
        self.actions = actions
        self.key_mappings = data.get_keypad_mapping_data()
        self.bind_actions()
        self.last_0_press_time = datetime.datetime.now()
        self.last_0_difference = 2000
        self.number_of_0_represses = 0
        self.is_triple = False

    def bind_actions(self):
        self.display.display_text.bind("<Key>", self.on_key_press)

    def on_key_press(self, event):
        
        numpad = list(string.ascii_lowercase[0:19])
        if event.char is 's':
            self.on_0_press()

        if event.char is '.':
            self.actions.quit_the_program()

        elif event.char in numpad:
            this_mapping = self.key_mappings[event.char]
            if self.display.display_mode in this_mapping:
                mode = self.display.display_mode
            elif 'DEFAULT' in this_mapping:
                mode = 'DEFAULT'

            if self.message_handler.function_on and len(this_mapping[mode]) > 1:
                print('the action being called is {}'.format(this_mapping[mode][1]))
                getattr(self.actions, this_mapping[mode][1])()
            else:
                print('the action being called is {}'.format(this_mapping[mode][0]))
                getattr(self.actions, this_mapping[mode][0])()
          
            self.display.refresh_display()
        else:
            print('{} is not in keypad map'.format(event.char))

    def on_0_press(self):
        this_press_time = datetime.datetime.now()
        print('the last 0 press was at {}'.format(self.last_0_press_time))
        self.last_0_difference = this_press_time - self.last_0_press_time
        print('the difference between last and now is {}'.format(self.last_0_difference))
        print('the total dif in secs is {}.'.format(self.last_0_difference.total_seconds()))
        self.last_0_press_time = this_press_time
        if (self.last_0_difference.total_seconds() < 0.7):
            self.number_of_0_represses = self.number_of_0_represses + 1
        self.last_0_press_time = this_press_time
        self.root.after(1000, self.respond_to_0_press)

    def respond_to_0_press(self):
        print('current represses is {},.'.format(self.number_of_0_represses))
        if(self.number_of_0_represses == 0):
            print('doing single action now')
        elif(self.number_of_0_represses == 1):
            print('waiting for another...')
        elif(self.number_of_0_represses == 2):
            print('doing triple action now')
            self.number_of_0_represses = -10
            self.root.after(1000, self.set_represses_to_0)

    def set_represses_to_0(self):
        print('clearing repress from {}'.format(self.number_of_0_represses))
        self.number_of_0_represses = 0

