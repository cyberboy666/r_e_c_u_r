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
        self.in_0_event = False
        self.additional_0_in_event = 0

    def bind_actions(self):
        self.display.display_text.bind("<Key>", self.on_key_press)

    def on_key_press(self, event):
        
        numpad = list(string.ascii_lowercase[0:19])


        if event.char is '.':
            self.actions.quit_the_program()
        if event.char is 's':
            event.char = self.on_0_key_press()
        elif event.char in numpad:
            self.run_action_for_mapped_key(event.char)
        else:
            print('{} is not in keypad map'.format(event.char))

    def run_action_for_mapped_key(self, key):
        this_mapping = self.key_mappings[key]
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

    def on_0_key_press(self) :
        if(not self.in_0_event ):
            self.in_0_event  = True
            self.additional_0_in_event = 0
            self.root.after(600, self.check_event_outcome)
        else:
            self.additional_0_in_event = self.additional_0_in_event + 1 

    def check_event_outcome(self):
        if(self.additional_0_in_event == 0 ):
            self.in_0_event  = False
            self.run_action_for_mapped_key('s')
        elif(self.additional_0_in_event > 1):
            self.in_0_event  = False
            self.run_action_for_mapped_key('n')
        elif(self.additional_0_in_event == 1):
            print('this doesnt happen - may not be needed')
            self.root.after(600, self.second_check_event_outcome)

    def second_check_event_outcome(self):
        if(self.additional_0_in_event == 1 ):
            self.in_0_event  = False
            self.run_action_for_mapped_key('s')
        elif(self.additional_0_in_event > 1):
            self.in_0_event  = False
            self.run_action_for_mapped_key('n')

