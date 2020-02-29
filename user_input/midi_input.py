import string
import datetime
import mido
import subprocess

class MidiInput(object):
    def __init__(self, root, message_handler, display, actions, data):
        self.root = root
        self.message_handler = message_handler
        self.display = display
        self.actions = actions
        self.data = data
        self.midi_mappings = data.midi_mappings
        self.midi_device = None
        self.midi_setting = None
        self.port_index = 0
        self.midi_delay = 40
        self.try_open_port()

    def try_open_port(self):
        #self.data.midi_status = 'disconnected'
        self.midi_setting = self.data.settings['user_input']['MIDI_INPUT']['value']
        self.port_index = self.data.midi_port_index
        #print('try open port : midi setting is {}'.format(midi_setting))
        if self.midi_setting == 'usb':
            self.actions.stop_serial_port_process()
            self.open_this_port_and_start_listening('20')
        elif self.midi_setting == 'serial':
            self.actions.create_serial_port_process()
            self.open_this_port_and_start_listening('serial')
        else:
            self.actions.stop_serial_port_process()     
            self.data.midi_status = 'disconnected'
        self.root.after(1000, self.try_open_port)

    def open_this_port_and_start_listening(self, port_phrase):
        midi_ports = mido.get_input_names()
        midi_devices = [s for s in midi_ports if not ('Midi Through' in s)]
        if port_phrase == 'serial':
            midi_devices = [s for s in midi_devices if port_phrase in s]
        if midi_devices:
            if self.data.midi_status == 'disconnected':
                subport_index = self.port_index % len(midi_devices) 
                self.midi_device = mido.open_input(midi_devices[subport_index])
                self.data.midi_status = 'connected'
                self.message_handler.set_message('INFO', 'connected to midi device {}'.format(self.midi_device.name))
                self.poll_midi_input()
        elif self.data.midi_status == 'connected':
            self.data.midi_status = 'disconnected'

    def poll_midi_input(self):
        i = 0
        cc_dict = dict()
        for message in self.midi_device.iter_pending():
            i = i + 1
            message_dict = message.dict()
            midi_channel = midi_setting = self.data.settings['user_input']['MIDI_CHANNEL']['value'] - 1

            if not message_dict.get('channel', None) == midi_channel:
                pass
            ## turning off noisey clock messages for now - may want to use them at some point
            elif message_dict['type'] == 'clock':
                pass
            ## trying to only let through step cc messages to increase response time
            elif message_dict['type'] == 'control_change':
                control_number = message_dict['control']
                print('control number is {} , cc_dict.keys is {}'.format(control_number, cc_dict.keys() ))
                if not control_number in cc_dict.keys():
                    cc_dict[control_number] = message_dict['value']
                    self.on_midi_message(message_dict)
                else:
                    step_size = 3
                    ignore_range = range(cc_dict[control_number] - step_size,cc_dict[control_number] + step_size)
                    #print('value is {} and ignore range is {}'.format(message_dict['value'], ignore_range ))
                    if not message_dict['value'] in ignore_range:
                        cc_dict[control_number] = message_dict['value']
                        #print(message_dict)
                        self.on_midi_message(message_dict)
                    #print(cc_dict)

            else:
                print(message_dict)       
                self.on_midi_message(message_dict)
        if i > 0:
            pass
            #print('the number processed {}'.format(i))
        if self.data.settings['user_input']['MIDI_INPUT']['value'] == self.midi_setting and self.data.midi_port_index == self.port_index:
            self.root.after(self.midi_delay, self.poll_midi_input)
        else:
            self.data.midi_status = 'disconnected'

    def on_midi_message(self, message_dict):
        if message_dict['type'] == 'note_on' and message_dict['velocity'] == 0:
            ## edge case where on note of zero alternative for off note.
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
        if self.data.control_mode in this_mapping:
            mode = self.data.control_mode
        elif 'DEFAULT' in this_mapping:
            mode = 'DEFAULT'

        if self.data.function_on and len(this_mapping[mode]) > 1:
            method_name = this_mapping[mode][1]
            self.data.function_on = False
        else:
            method_name = this_mapping[mode][0]

        print('the action being called is {}'.format(method_name))
        if mapped_message_value is not None:
            norm_message_value = mapped_message_value/127 
            
        else:
            norm_message_value = None
        self.actions.call_method_name(method_name, norm_message_value)
        ## only update screen if not continuous - seeing if cc can respond faster if not refreshing screen on every action
        if 'continuous' not in message_name:
            self.display.refresh_display()

