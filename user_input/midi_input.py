import string
import datetime
import mido

class MidiInput(object):
    def __init__(self, root, message_handler, display, actions, data):
        self.root = root
        self.message_handler = message_handler
        self.display = display
        self.actions = actions
        self.midi_mappings = data.get_midi_mapping_data()
        self.midi_device = None
        self.midi_delay = 1
        #self.midi_mappings = data.get_midi_mapping_data()
        self.open_port()

    def open_port(self):
        midi_ports = mido.get_input_names()
        midi_device_on_port_20 = [s for s in midi_ports if '20:0' in s]
        if midi_device_on_port_20:
            self.midi_device = mido.open_input(midi_device_on_port_20[0])
            self.message_handler.set_message('INFO', 'listening to midi device {}'.format(self.midi_device.name))
            self.poll_midi_input()

    def poll_midi_input(self):
        i = 0
        for message in self.midi_device.iter_pending():
            print(message)
            i = i + 1
            if not message.dict()['type'] == 'clock':        
                self.on_midi_message(message)

        self.root.after(self.midi_delay, self.poll_midi_input)


    def on_midi_message(self, message):
        message_dict = message.dict()
        if message_dict['type'] == 'note_on' and message_dict['velocity'] == 0:
            print('!!!!!')
            message_dict['type'] = 'note_off'
        mapped_message_name = message_dict['type']
        mapped_message_value = None
        if 'note' in message_dict:
            mapped_message_name = '{} {}'.format(mapped_message_name,message_dict['note'])
        if 'control' in message_dict:
            mapped_message_name = '{} {}'.format(mapped_message_name,message_dict['control'])
            mapped_message_value = message_dict['value']
        
        if mapped_message_name in self.midi_mappings.keys():
            self.run_action_for_mapped_message(mapped_message_name, mapped_message_value)
        else:
            print('{} is not in midi map'.format(mapped_message_name))

    def run_action_for_mapped_message(self, message_name, mapped_message_value):
        this_mapping = self.midi_mappings[message_name]
        if self.display.control_mode in this_mapping:
            mode = self.display.control_mode
        elif 'DEFAULT' in this_mapping:
            mode = 'DEFAULT'

        if self.message_handler.function_on and len(this_mapping[mode]) > 1:
            method_name = this_mapping[mode][1]
            self.message_handler.function_on = False
        else:
            method_name = this_mapping[mode][0]

        print('the action being called is {}'.format(method_name))
        self.call_method_name(method_name, mapped_message_value)
        self.display.refresh_display()

    def call_method_name(self, method_name, argument=None):
        if argument is not None:
           # try:
            getattr(self.actions, method_name)(argument)
            #except TypeError as e:
             #   print(e)
             #   self.message_handler.set_message('INFO', 'bad midi cc mapping')
        else:
            getattr(self.actions, method_name)()







