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
    DEFAULT_SETTINGS_JSON = 'settings_default.json'
    KEYPAD_MAPPING_JSON = 'keypad_action_mapping.json'
    MIDI_MAPPING_JSON = 'midi_action_mapping.json'
    ANALOG_MAPPING_JSON = 'analog_action_mapping.json'
    EMPTY_SLOT = dict(name='', location='', length=-1, start=-1, end=-1, rate=1)
    PATH_TO_DATA_OBJECTS = '/home/pi/r_e_c_u_r/json_objects/'
    PATH_TO_EXTERNAL_DEVICES = '/media/pi'

    def __init__(self, message_handler):
        self.message_handler = message_handler
        
        #self.EMPTY_BANK = [self.EMPTY_SLOT for i in range(10)]
        self.PATHS_TO_BROWSER = [self.PATH_TO_EXTERNAL_DEVICES, '/home/pi/Videos' ]
        self.PATHS_TO_SHADERS = [self.PATH_TO_EXTERNAL_DEVICES, '/home/pi/Shaders' ]

        ### state data
        self.auto_repeat_on = True
        self.function_on = False
        self.display_mode = "SAMPLER"
        self.control_mode = 'PLAYER'
        self.bank_number = 0
        self.midi_status = 'disconnected'
        self.midi_port_index = 0
        self.update_screen = True
        self.player_mode = 'now'
        
        ### persisted data (use default if doesnt exits):
        self.bank_data = [self.create_empty_bank()]
        if os.path.isfile(self.PATH_TO_DATA_OBJECTS + self.BANK_DATA_JSON):
            self.bank_data = self._read_json(self.BANK_DATA_JSON)

        self.next_bankslot = '0-0'
        if os.path.isfile(self.PATH_TO_DATA_OBJECTS + self.NEXT_BANKSLOT_JSON):
            self.next_bankslot = self._read_json(self.NEXT_BANKSLOT_JSON)

        self.settings = self._read_json(self.DEFAULT_SETTINGS_JSON)
        if os.path.isfile(self.PATH_TO_DATA_OBJECTS + self.SETTINGS_JSON):
            self.settings = self._read_json(self.SETTINGS_JSON)

        self.key_mappings = self._read_json(self.KEYPAD_MAPPING_JSON)
        self.midi_mappings = self._read_json(self.MIDI_MAPPING_JSON)
        self.analog_mappings = self._read_json(self.ANALOG_MAPPING_JSON)
        
    @staticmethod
    def create_empty_bank():
        empty_slot = dict(name='', location='', length=-1, start=-1, end=-1, rate=1)
        return [empty_slot for i in range(10)]
     
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
        self.bank_data[self.bank_number] = self.create_empty_bank()
        self._update_json(self.BANK_DATA_JSON, self.bank_data)

    def update_bank_number_by_amount(self, amount):
        empty_bank = self.create_empty_bank()
        if(self.bank_data[-1] != empty_bank):
            self.bank_data.append(empty_bank)
        elif(len(self.bank_data) > 1):
            if self.bank_data[-2] == empty_bank:
                self.bank_data.pop()
        self._update_json(self.BANK_DATA_JSON, self.bank_data)
        self.bank_number = (self.bank_number+amount)%(len(self.bank_data))
        
    def update_next_slot_number(self,  new_value):
        if self.bank_data[self.bank_number][new_value]['location'] == '':
            self.message_handler.set_message('INFO', 'the slot you pressed is empty')
            return False
        elif self.is_this_path_broken(self.bank_data[self.bank_number][new_value]['location']):
            self.message_handler.set_message('INFO', 'no device found for this slot')
            return False
        else:
            self.next_bankslot =  '{}-{}'.format(self.bank_number,new_value)
            self._update_json(self.NEXT_BANKSLOT_JSON,self.next_bankslot)
            return True

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

        start_value, end_value = self._overwrite_values_with_sampler_settings(start_value, end_value, length)        

        context = dict(location=next_slot_details['location'], name=next_slot_details['name'],
                       length=next_slot_details['length'], rate=next_slot_details['rate'], start=start_value, end=end_value,
                       bankslot_number=self.next_bankslot)

        self._update_next_bankslot_value(slot_num)
        return context

    def _overwrite_values_with_sampler_settings(self, start, end, length):
        use_rand_start = self.settings['sampler']['RAND_START_MODE']['value'] == 'on'
        use_fixed_length = self.settings['sampler']['FIXED_LENGTH_MODE']['value'] == 'on'
        fixed_length_value = self.settings['sampler']['FIXED_LENGTH']['value']
        fixed_length_multiply = self.settings['sampler']['FIXED_LENGTH_MULTIPLY']['value']
        total_fixed_length = fixed_length_value * fixed_length_multiply
        if start == -1:
            start = 0        
        if end == -1:
            end = length        
        new_end = end
        new_start = start

        if use_fixed_length and use_rand_start:
            max_increase = int(max(end - start - max(total_fixed_length, 4),0))
            random_increase = randint(0,max_increase)
            new_start = start + random_increase
            new_end = min(new_start + total_fixed_length, end)
        elif use_fixed_length and not use_rand_start:
            new_end = min(new_start + total_fixed_length, end)
        elif not use_fixed_length and use_rand_start:
            max_increase = int(max(end - start - 4,0))
            random_increase = randint(0,max_increase)
            new_start = start + random_increase

        return new_start, new_end

    def _update_next_bankslot_value(self, slot_num):
        next_setting = self.settings['sampler']['LOAD_NEXT']['value']
        loaded_slots = self._get_list_of_loaded_slots_in_current_bank()
        if loaded_slots:
            if next_setting == 'random':
                next_slot = loaded_slots[randint(0,len(loaded_slots)-1)]
            elif next_setting == 'consecutive':
                next_slot = self.get_next_loaded_slot(slot_num, loaded_slots)
            else:
                next_slot = slot_num

            self.next_bankslot =  '{}-{}'.format(self.bank_number,next_slot)
            self._update_json(self.NEXT_BANKSLOT_JSON,self.next_bankslot)

    def _get_list_of_loaded_slots_in_current_bank(self):
        list_of_loaded_slots = []
        for index, slot in enumerate(self.bank_data[self.bank_number]):
            if slot['location'] != '' and not self.is_this_path_broken(slot['location']):
                list_of_loaded_slots.append(index)
        return list_of_loaded_slots

    @staticmethod
    def get_next_loaded_slot(current_slot, loaded_slots):
        i = ( current_slot + 1 ) % len(loaded_slots)
        while(i not in loaded_slots):
            i = ( i + 1 ) % len(loaded_slots)
        return i

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

    def get_background_colour(self):
        colour_name = self.settings['video']['BACKGROUND_COLOUR']['value']
        colour_argb = (255,0,0,0)
        if colour_name == "black":
            colour_argb = (255,0,0,0)
        elif colour_name == "white":
            colour_argb = (255,255,255,255)
        elif colour_name == "green":
            colour_argb = (255,0,255,0)
        elif colour_name == "blue":
            colour_argb = (255,0,0,255)
        elif colour_name == "pink":
            colour_argb = (255,255,0,255)
        elif colour_name == "none":
            colour_argb = (0,0,0,0)
        colour_hex = '%02x%02x%02x%02x' % colour_argb
        print(colour_hex)
        return colour_hex

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


