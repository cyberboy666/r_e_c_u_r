import json
import os
from random import randint
import inspect

from data_centre.browser_data import BrowserData

def get_the_current_dir_path():
    # TODO: investigate weird path formatting differences
    current_file_path = inspect.stack()[0][1]
    return os.path.split(current_file_path)[0]

BANK_DATA_JSON = 'display_data.json'
NEXT_SLOT_JSON = 'next_bank_number.json'
SETTINGS_JSON = 'settings.json'
EMPTY_BANK = dict(name='', location='', length=-1, start=-1, end=-1)
PATH_TO_DATA_OBJECTS = '{}\\json_objects\\'.format(get_the_current_dir_path())

def read_json(file_name):
    with open(PATH_TO_DATA_OBJECTS + file_name) as data_file:
        data = json.load(data_file)
    return data


def update_json(file_name, data):
    with open('{}{}'.format(PATH_TO_DATA_OBJECTS, file_name), 'w') as data_file:
        json.dump(data, data_file)



def get_path_to_browser():
    return read_json('path_to_browser.json')

PATH_TO_BROWSER = get_path_to_browser()


class Data(object):
    def __init__(self, message_handler):
        self.browser_data = BrowserData(PATH_TO_BROWSER)
        self.message_handler = message_handler

        self.has_omx = self._try_import_omx()
        self.DEV_MODE = read_json(SETTINGS_JSON)[6]["value"]



    def create_new_slot_mapping_in_first_open(self, file_name):
        ######## used for mapping current video to next available slot ########
        memory_bank = read_json(BANK_DATA_JSON)
        for index, slot in enumerate(memory_bank):
            if (not slot['name']):
                self.create_new_slot_mapping(index, file_name)
                return True
        return False

    def create_new_slot_mapping(self, slot_number, file_name):
        ######## used for mapping current video to a specific bank ########
        has_location, location = self._get_path_for_file(file_name)
        length = self._get_length_for_file(location)
        new_slot = dict(name=file_name, location=location, length=length, start=-1, end=-1)
        self._update_a_slots_data(slot_number, new_slot)

    @staticmethod
    def clear_all_slots():
        memory_bank = read_json(BANK_DATA_JSON)
        for index, bank in enumerate(memory_bank):
            memory_bank[index] = EMPTY_BANK
        update_json(BANK_DATA_JSON, memory_bank)

    def update_next_slot_number(self, new_value):
        memory_bank = read_json(BANK_DATA_JSON)
        if memory_bank[new_value]['location'] == '':
            print('its empty!')
            self.message_handler.set_message('INFO', 'the slot you pressed is empty')
        else:
            update_json(NEXT_SLOT_JSON, new_value)

    def add_open_folder(self, folder_name):
        self.browser_data.update_open_folders(folder_name)

    def switch_settings(self, setting_index):
        ######## update the value of selected setting by cycling through valid options ########
        settings = read_json(SETTINGS_JSON)

        for index, setting in enumerate(settings):
            if index == setting_index:
                self._cycle_setting_value(setting)

        update_json(SETTINGS_JSON, settings)

    def rewrite_browser_list(self):
        return self.browser_data.generate_browser_list()

    def return_browser_list(self):
        return self.browser_data.browser_list

    @staticmethod
    def get_settings_data():
        return read_json(SETTINGS_JSON)

    @staticmethod
    def get_sampler_data():
        return read_json(BANK_DATA_JSON)

    def get_next_context(self):
        ######## loads the slot details, uses settings to modify them and then set next slot number ########
        next_slot_number = read_json(NEXT_SLOT_JSON)
        memory_bank = read_json(BANK_DATA_JSON)
        next_slot_details = memory_bank[next_slot_number]
        start_value = next_slot_details['start']
        end_value = next_slot_details['end']
        length = next_slot_details['length']

        use_rand_start, use_sync_length, sync_length, playback_mode = self._get_context_options_from_settings()

        if use_rand_start and use_sync_length:
            start_value = randint(0, length - sync_length)
            end_value = start_value + sync_length
        elif use_rand_start and not use_sync_length:
            start_value = randint(0, end_value)
        elif not use_rand_start and use_sync_length:
            end_value = min(length, start_value + sync_length)

        self._set_next_slot_number_from_playback_mode(playback_mode, next_slot_number)

        context = dict(location=next_slot_details['location'], name=next_slot_details['name'],
                       length=next_slot_details['length'], start=start_value, end=end_value,
                       bank_number=next_slot_number)
        return context

    def _get_length_for_file(self, path):
        if self.has_omx:
            temp_player = OMXPlayer(path, args=['--alpha', '0'], dbus_name='t.t')
            duration = temp_player.duration()
            temp_player.quit()
            return duration
        else:
            return -1

    def _get_path_for_file(self, file_name):
        ######## returns full path for a given file name ########
        for root, dirs, files in os.walk(PATH_TO_BROWSER):
            if file_name in files:
                return True, '{}/{}'.format(root, file_name)
        return False, ''

    @staticmethod
    def _update_a_slots_data(bank_number, slot_info):
        ######## overwrite a given banks info with new data ########
        memory_bank = read_json(BANK_DATA_JSON)
        memory_bank[bank_number] = slot_info
        update_json(BANK_DATA_JSON, memory_bank)

    @staticmethod
    def _cycle_setting_value(setting):
        ######## contains the valid setting values for each applicable option ########
        if setting['name'] == 'PLAYBACK_MODE':
            if setting['value'] == 'SAMPLER':
                setting['value'] = 'PLAYLIST'
            elif setting['value'] == 'PLAYLIST':
                setting['value'] = 'RANDOM'
            else:
                setting['value'] = 'SAMPLER'
        elif setting['name'] == 'SYNC_LENGTHS':
            if setting['value'] == 'ON':
                setting['value'] = 'OFF'
            else:
                setting['value'] = 'ON'
        elif setting['name'] == 'RAND_START':
            if setting['value'] == 'ON':
                setting['value'] = 'OFF'
            else:
                setting['value'] = 'ON'
        elif setting['name'] == 'VIDEO_OUTPUT':
            if setting['value'] == 'HDMI':
                setting['value'] = 'COMPOSITE'
            else:
                setting['value'] = 'HDMI'
        elif setting['name'] == 'DEV_MODE':
            if setting['value'] == 'ON':
                setting['value'] = 'OFF'
            else:
                setting['value'] = 'ON'

        return setting

    @staticmethod
    def _get_context_options_from_settings():
        ######## looks up the settings data object and returns states of relevant options ########
        settings = read_json(SETTINGS_JSON)
        use_sync_length = False
        sync_length = 0
        use_rand_start = False
        playback_mode = ''

        for index, setting in enumerate(settings):
            if setting['name'] == 'SYNC_LENGTHS' and setting['value'] == 'ON':
                use_sync_length = True
            elif setting['name'] == 'SYNC_LENGTHS_TO':
                sync_length = setting['value']
            elif setting['name'] == 'RAND_START' and setting['value'] == 'ON':
                use_rand_start = True
            elif setting['name'] == 'PLAYBACK_MODE':
                playback_mode = setting['value']

        return use_rand_start, use_sync_length, sync_length, playback_mode

    @staticmethod
    def _set_next_slot_number_from_playback_mode(playback_mode, current_slot_number):
        ######## sets next slot number by using playback mode logic ########
        next_slot_number = 0
        if playback_mode == 'SAMPLER':
            next_slot_number = current_slot_number
        elif playback_mode == 'RANDOM':
            #TODO: actually find which banks have value and only use those
            next_slot_number = randint(0,14)
        elif playback_mode == 'PLAYLIST':
            #TODO: implement some playlist objects and logic at some point
            next_slot_number = current_slot_number
        update_json('next_bank_number.json',next_slot_number)

    @staticmethod
    def _try_import_omx():
        try:
            from omxplayer.player import OMXPlayer
            return True
        except:
            return False







