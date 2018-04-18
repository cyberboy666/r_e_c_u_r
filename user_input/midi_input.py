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

    def poll_midi_input(self):
        for message in self.midi_device.iter_pending():
            
            if not message.dict()['type'] == 'clock':
                print(message)
                try:
                    pass#print('{} {} {}'.format(message.dict()['type'],message.dict()['note'],message.dict()['velocity']))
                except:
                    pass                
                self.on_midi_message(message)
        self.root.after(self.midi_delay, self.poll_midi_input)

    def open_port(self):
        print('gonna try open this port!')
        midi_ports = mido.get_input_names()
        midi_device_on_port_20 = [s for s in midi_ports if '20:0' in s]
        if midi_device_on_port_20:
            self.midi_device = mido.open_input(midi_device_on_port_20[0])
            self.message_handler.set_message('INFO', 'listening to midi device {}'.format(self.midi_device.name))
            self.poll_midi_input()

    def on_midi_message(self, message):
        message_dict = message.dict()
        if message_dict['type'] == 'note_on' and message_dict['velocity'] == 0:
            print('!!!!!')
            message_dict['type'] = 'note_off'
        mapped_message_name = message_dict['type']        
        if 'note' in message_dict:
            mapped_message_name = '{} {}'.format(mapped_message_name,message_dict['note'])
        
            #print(mapped_message_name)
        
        if mapped_message_name in self.midi_mappings.keys():
            self.run_action_for_mapped_message(mapped_message_name)
        else:
            pass#print('{} is not in midi map'.format(mapped_message_name))

    def run_action_for_mapped_message(self, message_name):
        this_mapping = self.midi_mappings[message_name]
        if self.display.control_mode in this_mapping:
            mode = self.display.control_mode
        elif 'DEFAULT' in this_mapping:
            mode = 'DEFAULT'

        if self.message_handler.function_on and len(this_mapping[mode]) > 1:
            print('the action being called is {}'.format(this_mapping[mode][1]))
            getattr(self.actions, this_mapping[mode][1])()
        else:
            print('the action being called is {}'.format(this_mapping[mode][0]))
            getattr(self.actions, this_mapping[mode][0])()
      
        self.display.refresh_display()




