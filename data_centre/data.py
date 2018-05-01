import json
import os
from random import randint
import inspect
from itertools import cycle
from omxplayer.player import OMXPlayer




class Data(object):

    BANK_DATA_JSON = 'display_data.json'
    NEXT_BANKSLOT_JSON = 'next_bankslot_number.json'
    SETTINGS_JSON = 'settings.json'
    KEYPAD_MAPPING_JSON = 'keypad_action_mapping.json'
    MIDI_MAPPING_JSON = 'midi_action_mapping.json'
    EMPTY_SLOT = dict(name='', location='', length=-1, start=-1, end=-1, rate=1)
    PATH_TO_DATA_OBJECTS = '/home/pi/r_e_c_u_r/data_centre/json_objects/'
    PATH_TO_EXTERNAL_DEVICES = '/media/pi'

    def __init__(self, message_handler):
        self.message_handler = message_handler
        
        self.EMPTY_BANK = [self.EMPTY_SLOT for i in range(10)]
        self.PATHS_TO_BROWSER = [self.PATH_TO_EXTERNAL_DEVICES, '/home/pi/Videos' ]

        ### state data
        self.function_on = False
        self.display_mode = "SAMPLER"
        self.control_mode = 'PLAYER'
        self.bank_number = 0
        self.midi_status = 'disconnected'
        self.update_screen = True
        
        ### persisted data:
        self.bank_data = self._read_json(self.BANK_DATA_JSON)
        self.next_bankslot = self._read_json(self.NEXT_BANKSLOT_JSON)
        self.settings = self._read_json(self.SETTINGS_JSON)
        self.key_mappings = self._read_json(self.KEYPAD_MAPPING_JSON)
        self.midi_mappings = self._read_json(self.MIDI_MAPPING_JSON)
        
     
    def _read_json(self, file_name):
        with open(self.PATH_TO_DATA_OBJECTS + file_name) as data_file:
            data = json.load(data_file)
        return data

    def _update_json(self, file_name, data):
        with open('{}{}'.format(self.PATH_TO_DATA_OBJECTS, file_name), 'w') as data_file:
            json.dump(data, data_file, indent=4, sort_keys=True)
    
    def get_setting_and_folder_from_name(self, setting_name):
        for folder_key , folder_item in self.settings.items():
            for setting_key, setting_item in folder_item.items():
                if setting_key == setting_name:
                    return folder_key, setting_key, setting_item

    def create_new_slot_mapping_in_first_open(self, file_name):
        ######## used for mapping current video to next available slot ########
        for index, slot in enumerate(self.bank_data[self.bank_number]):
            if (not slot['name']):
                self.create_new_slot_mapping(index, file_name)
                return True
        return False

    def create_new_slot_mapping(self, slot_number, file_name):
        ######## used for mapping current video to a specific slot ########
        has_location, location = self._get_path_for_file(file_name)
        print('file_name:{},has_location:{}, location:{}'.format(file_name,has_location, location))
        length = self._get_length_for_file(location)
        if length:
            new_slot = dict(name=file_name, location=location, length=length, start=-1, end=-1, rate=1)
            self._update_a_slots_data(slot_number, new_slot)

    def clear_all_slots(self):
        self.bank_data[self.bank_number] = self.EMPTY_BANK
        self._update_json(self.BANK_DATA_JSON, self.bank_data)

    def update_bank_number_by_amount(self, amount):
        if(self.bank_data[-1] != self.EMPTY_BANK):
            self.bank_data.append(self.EMPTY_BANK)
        elif(len(self.bank_data) > 1):
            if self.bank_data[-2] == self.EMPTY_BANK:
                self.bank_data.pop()
        self._update_json(self.BANK_DATA_JSON, self.bank_data)
        self.bank_number = (self.bank_number+amount)%(len(self.bank_data))
        
    def update_next_slot_number(self,  new_value):
        if self.bank_data[self.bank_number][new_value]['location'] == '':
            print('its empty!')
            self.message_handler.set_message('INFO', 'the slot you pressed is empty')
        elif self.is_this_path_broken(self.bank_data[self.bank_number][new_value]['location']):
            self.message_handler.set_message('INFO', 'no device found for this slot')
        else:
            self.next_bankslot =  '{}-{}'.format(self.bank_number,new_value)
            self._update_json(self.NEXT_BANKSLOT_JSON,self.next_bankslot)

    def update_setting_value(self, setting_folder, setting_name, setting_value):
        self.settings[setting_folder][setting_name]['value'] = setting_value
        self._update_json(self.SETTINGS_JSON, self.settings)
        return self.settings[setting_folder][setting_name]
      
    @classmethod
    def split_bankslot_number(cls, bankslot_number):
        split = bankslot_number.split('-')
        is_bank_num_int , converted_bank_number = cls.try_convert_string_to_int(split[0])
        is_slot_num_int , converted_slot_number = cls.try_convert_string_to_int(split[1])
        return converted_bank_number, converted_slot_number

    @staticmethod
    def try_convert_string_to_int(string_input):
        try:
            return True , int(string_input)
        except ValueError:
            return False , '*'

    def get_next_context(self):
        ######## loads the slot details, uses settings to modify them and then set next slot number ########
        bank_num , slot_num = self.split_bankslot_number(self.next_bankslot)
        next_slot_details = self.bank_data[bank_num][slot_num]
        start_value = next_slot_details['start']
        end_value = next_slot_details['end']
        length = next_slot_details['length']

        context = dict(location=next_slot_details['location'], name=next_slot_details['name'],
                       length=next_slot_details['length'], rate=next_slot_details['rate'], start=start_value, end=end_value,
                       bankslot_number=self.next_bankslot)
        return context

    def update_slot_start_to_this_time(self, slot_number, position):
        self.bank_data[self.bank_number][slot_number]['start'] = position
        self._update_json(self.BANK_DATA_JSON, self.bank_data)

    def update_slot_end_to_this_time(self, slot_number, position):
        self.bank_data[self.bank_number][slot_number]['end'] = position
        self._update_json(self.BANK_DATA_JSON, self.bank_data)

    def update_slot_rate_to_this(self, slot_number, rate):
        self.bank_data[self.bank_number][slot_number]['rate'] = rate
        self._update_json(self.BANK_DATA_JSON, self.bank_data)

    def _get_length_for_file(self, path):
        try:
            temp_player = OMXPlayer(path, args=['--alpha', '0'], dbus_name='t.t')
            duration = temp_player.duration()
            temp_player.quit()
            return duration
        except Exception as e:
            print (e)
            self.message_handler.set_message('INFO', 'cannot load video')
            return None



    def _get_path_for_file(self, file_name):
        ######## returns full path for a given file name ########
        for path in self.PATHS_TO_BROWSER:    
            for root, dirs, files in os.walk(path):
                if file_name in files:
                    return True, '{}/{}'.format(root, file_name)
        return False, ''

   
    def is_this_path_broken(self, path):
        external_devices = os.listdir(self.PATH_TO_EXTERNAL_DEVICES)
        has_device_in_path = self.PATH_TO_EXTERNAL_DEVICES in path
        has_existing_device_in_path = any([(x in path) for x in external_devices])
         
        if has_device_in_path and  not has_existing_device_in_path:
            return True
        else:
            return False

    @staticmethod
    def _get_mb_free_diskspace(path):
        st = os.statvfs(path)
        return st.f_bavail * st.f_frsize / 1024 / 1024

    def _update_a_slots_data(self, slot_number, slot_info):
        ######## overwrite a given slots info with new data ########
        self.bank_data[self.bank_number][slot_number] = slot_info
        self._update_json(self.BANK_DATA_JSON, self.bank_data)
    
    @staticmethod
    def make_empty_if_none(input):
        if input is None:
            return ''
        else:
            return input
"""
## methods from old BROWSERDATA class

    def update_open_folders(self, folder_name):
        if folder_name not in self.open_folders:
            self.open_folders.append(folder_name)
        else:
            self.open_folders.remove(folder_name)
            
    def update_open_folders_for_settings(self, folder_name):
        if folder_name not in self.settings_open_folders:
            self.settings_open_folders.append(folder_name)
        else:
            self.settings_open_folders.remove(folder_name)

    def generate_browser_list(self):
        ######## starts the recursive process of listing all folders and video files to display ########
        self.browser_list = []
        for path in self.PATHS_TO_BROWSER:
            self._add_folder_to_browser_list(path, 0)
        
        for browser_line in self.browser_list:
            is_file, name = self.extract_file_type_and_name_from_browser_format(browser_line['name'])
            if is_file:
                is_slotted, bankslot_number = self._is_file_in_memory_bank(name)
                if is_slotted:
                    browser_line['slot'] = bankslot_number

    def generate_settings_list(self, open_folders):
        self.settings_list = []
        for sub_setting in self.settings.keys():
            if sub_setting in open_folders:
                self.settings_list.append(dict(name=sub_setting + '/', value=''))
                for setting in self.settings[sub_setting]:
                    setting_value = self.make_empty_if_none(self.settings[sub_setting][setting]['value'])
                    self.settings_list.append(dict(name=' ' + setting, value=setting_value))
            else:   
                self.settings_list.append(dict(name=sub_setting + '|', value=''))



    @staticmethod
    def extract_file_type_and_name_from_browser_format(dir_name):
        # removes whitespace and folder state from display item ########
        if dir_name.endswith('|') or dir_name.endswith('/'):
            return False, dir_name.lstrip()[:-1]
        else:
            return True, dir_name.lstrip()

    def _add_folder_to_browser_list(self, current_path, current_level):
        ######## adds the folders and mp4 files at the current level to the results list. recursively recalls at deeper level if folder is open ########
        # TODO make note of / investigate what happens with multiple folders of same name
        root, dirs, files = next(os.walk(current_path))

        indent = ' ' * 4 * (current_level)
        for folder in dirs:
            is_open, char = self._check_folder_state(folder)
            self.browser_list.append(dict(name='{}{}{}'.format(indent, folder, char), slot='x'))
            if (is_open):
                next_path = '{}/{}'.format(root, folder)
                next_level = current_level + 1
                self._add_folder_to_browser_list(next_path, next_level)

        for f in files:
            split_name = os.path.splitext(f)
            if (split_name[1] in ['.mp4', '.mkv', '.avi', '.mov']):
                self.browser_list.append(dict(name='{}{}'.format(indent, f), slot='-'))

    def _check_folder_state(self, folder_name):
        ######## used for displaying folders as open or closed ########
        if folder_name in self.open_folders:
            return True, '/'
        else:
            return False, '|'

    def _is_file_in_memory_bank(self, file_name):
        ######## used for displaying the mappings in browser view ########
        for bank_index, bank in enumerate(self.bank_data):
            for slot_index, slot in enumerate(bank):
                if file_name == slot['name']:
                    return True, '{}-{}'.format(bank_index,slot_index)
        return False, ''
"""

