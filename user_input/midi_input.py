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
        midi_channel = self.data.settings['user_input']['MIDI_CHANNEL']['value'] - 1

        current_message_buffer = [i.dict() for i in self.midi_device.iter_pending()]

        refined_buffer = []
        #refine buffer from lastest messages first
        current_message_buffer.reverse()
        for message in current_message_buffer:
            # discard notes from wrong channel
            if message.get('channel') != midi_channel:
                pass
            # process all note messages (in order)
            if 'note' in message['type']:
                refined_buffer.append(message)
            # only take the latest cc message per cc_channel
            elif message['type'] == 'control_change':
                if not message['control'] in [i.get('control') for i in refined_buffer]:
                    refined_buffer.append(message)
        # process buffer from oldest messages first
        refined_buffer.reverse()

        for message in refined_buffer:
            self.on_midi_message(message)

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
        try:
            self.actions.call_method_name(method_name, norm_message_value)
        except TypeError:
            ## to support using cc-0 as button presses
            if norm_message_value == 0:
                self.actions.call_method_name(method_name, None)
        ## only update screen if not continuous - seeing if cc can respond faster if not refreshing screen on every action
        if 'continuous' not in message_name:
            self.display.refresh_display()

