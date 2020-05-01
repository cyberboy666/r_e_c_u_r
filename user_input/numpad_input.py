import string


class NumpadInput(object):
    KEY_000_DELAY = 100

    def __init__(self, root, message_handler, display, actions, data):
        self.root = root
        self.message_handler = message_handler
        self.display = display
        self.actions = actions
        self.data = data
        self.key_mappings = data.key_mappings
        self.bind_actions()
        self.in_0_event = False
        self.additional_0_in_event = 0

    def bind_actions(self):
        self.display.display_text.bind("<KeyPress>", self.on_key_press)
        self.display.display_text.bind("<KeyRelease>", self.on_key_release)
        self.display.display_text.bind("<Motion>", self.on_mouse_move)

    def on_key_press(self, event):
        numpad = list(string.ascii_lowercase[0:19])

        if event.char is 'h': # DISP button
            #self.root.after(60, lambda:self.on_key_press_delay(event.char))
            #return
            if self.data.is_display_held:
                return # ignore spurious message if already held"""
            self.data.is_display_held = True
            if self.in_0_event:
                return

        if event.char is '.' or event.char is 'z':
            self.actions.quit_the_program()
        if event.char is 's':
            event.char = self.on_0_key_press()

        if event.char in numpad:
            numbers = "jklmnopqrs"
            if self.data.is_display_held and event.char in numbers:
                self.select_display_mode_index(numbers.index(event.char))
            else:
                self.run_action_for_mapped_key(event.char)
        else:
            print('{} is not in keypad map'.format(event.char))

    def on_key_release(self, event):
            numpad = list(string.ascii_lowercase[0:19])
            if event.char in numpad:
                self.check_key_release_settings(event.char)

            ##print ("--- releasing %s" % event.char)
            # lag for 60ms to check that this is not a 'stream of 000' bullshit job from the keypad
            if event.char is 'h' and not self.in_0_event:
                self.root.after(self.KEY_000_DELAY+5, self.on_key_disp_release_delay)
                #self.data.is_display_held = False

    def on_mouse_move(self, event):
        if self.data.settings['user_input'].setdefault(
                'MOUSE_INPUT',
                self.data.default_settings.get('MOUSE_INPUT',{'value': 'enabled'})).get('value') != 'enabled':
            return
        if event.x > 480 or event.y > 320:
            return
        width = 480
        height = 320 # hard coded since display is fixed , and reading screen is more work

        self.root.after(0, self.run_action_for_mapped_key, 'x_m', event.x / width)
        self.root.after(0, self.run_action_for_mapped_key, 'y_m', event.y / height)
        #self.run_action_for_mapped_key(event.char)

    def select_display_mode_index(self, index):
        if index >= len(self.data.get_display_modes_list()):
            self.message_handler.set_message('ERROR', 'No page %s to display!' % index)
        else:
            self.actions.call_method_name("set_display_mode_%s"%self.data.get_display_modes_list()[index])

    def run_action_for_mapped_key(self, key, value=-1):
        this_mapping = self.key_mappings[key]
        if type(self.data.control_mode) is list:
            mode = 'DEFAULT'
            for cm in self.data.control_mode:
                if cm in this_mapping:
                    mode = cm
                    break
        elif self.data.control_mode in this_mapping:
            mode = self.data.control_mode
        elif 'DEFAULT' in this_mapping:
            mode = 'DEFAULT'

        if self.data.function_on and len(this_mapping[mode]) > 1:
            is_function = 1
        else:
            is_function = 0

        numbers = "jklmnopqrs"
        if self.data.is_display_held and key in numbers:
            self.select_display_mode_index(numbers.index(key))
        else:
            print('the numpad action being called for \'{}\' is {} (mode is {})'.format(key, this_mapping[mode][is_function], mode))
            if value != -1:
                self.actions.call_method_name(this_mapping[mode][is_function],value)
            else:
                self.actions.call_method_name(this_mapping[mode][is_function])

        if is_function and self.data.settings['sampler']['FUNC_GATED']['value'] == 'off':
            self.data.function_on = False

        if not value:
            self.display.refresh_display()



    def check_key_release_settings(self, key):
        
        this_mapping = self.key_mappings[key]
        if self.data.settings['sampler']['ACTION_GATED']['value'] == 'on':
            if self.data.control_mode == 'PLAYER' and 'PLAYER' in this_mapping:
                if this_mapping['PLAYER'][0] == 'toggle_action_on_player' and not self.data.function_on:
                    print('released action key')
                    self.run_action_for_mapped_key(key)
        if self.data.settings['sampler']['FUNC_GATED']['value'] == 'on':
            if 'DEFAULT' in this_mapping:
                if this_mapping['DEFAULT'][0] == 'toggle_function':
                    self.run_action_for_mapped_key(key)

    def on_key_disp_release_delay(self):
        if not self.in_0_event:# and self.additional_0_in_event==0:
            print("releasing !")
            self.data.is_display_held = False
        else:
            print("ignoring release !")

    """def on_key_disp_press_delay(self):
        if not self.in_0_event and self.additional_0_in_event==0:
            print("pressing!")
            self.data.is_display_held = True
        else:
            print("ignoring press!")"""

    def on_0_key_press(self) :
        print ("on_0_key_press!")
        if(not self.in_0_event ):
            print ("    first 0 received!")
            self.in_0_event  = True
            self.additional_0_in_event = 0
            self.root.after(self.KEY_000_DELAY, self.check_event_outcome)
        else:
            print ("    additional 0 received making %s!" % str(self.additional_0_in_event + 1))
            self.additional_0_in_event = self.additional_0_in_event + 1 

    def check_event_outcome(self):
        if(self.additional_0_in_event == 0 ):
            print ("    no additional events, sending s")
            self.in_0_event  = False
            self.run_action_for_mapped_key('s')
        elif(self.additional_0_in_event > 1):
            print ("    %s additional events, sending n"%self.additional_0_in_event)
            self.in_0_event  = False
            self.run_action_for_mapped_key('n')
        elif(self.additional_0_in_event == 1):
            print('this doesnt happen - may not be needed')
            self.root.after(self.KEY_000_DELAY, self.second_check_event_outcome)

    def second_check_event_outcome(self):
        print("not supposed to happen?")
        if(self.additional_0_in_event == 1 ):
            self.in_0_event  = False
            self.run_action_for_mapped_key('s')
        elif(self.additional_0_in_event > 1):
            self.in_0_event  = False
            self.run_action_for_mapped_key('n')

