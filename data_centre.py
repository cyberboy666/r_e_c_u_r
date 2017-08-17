import json

import logging
from collections import OrderedDict

import os
from random import randint

#TODO : standise the paths to things, use constants for file names, standise the naming convention of files
import time

PATH_TO_BROWSER = 'C:/TestFolderStucture'

PATH_TO_DATA_OBJECTS = 'C:/Users/Tim/PycharmProjects/videoLooper/'

EMPTY_BANK = dict(name='',location='',length=-1,start=-1,end=-1)

logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('C:/Users/Tim/PycharmProjects/videoLooper/myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

class data(object):
    def __init__(self):

        self._open_folders = []
        self._browser_list = []

    def rewrite_browser_list(self):
        self._browser_list = generate_browser_list(PATH_TO_BROWSER, 0, self._open_folders)

    def get_browser_data_for_display(self):
        if not self._browser_list:
            self.rewrite_browser_list()

        browser_list_for_display = []
        for index , dir in enumerate(self._browser_list):
            browser_list_for_display.append(([dir['name'],dir['bank']],index))
        #logger.info(browser_list_for_display)
        return browser_list_for_display

    def update_open_folders(self, folder_name):
        if folder_name not in self._open_folders:
            self._open_folders.append(folder_name)
        else:
            self._open_folders.remove(folder_name)


def get_all_looper_data_for_display():

    memory_bank = read_json('DisplayData.json')
    loop_data = []
    for index, bank in enumerate(memory_bank):
        length = convert_int_to_string_for_display(bank["length"])
        start = convert_int_to_string_for_display(bank["start"])
        end = convert_int_to_string_for_display(bank["end"])
        loop_data.append(([str(index),bank["name"],length,start,end],index))

    return loop_data

def is_file_in_memory_bank(file_name, memory_bank=[]):
    if not memory_bank:
        memory_bank = read_json('DisplayData.json')
    for index, bank in enumerate(memory_bank):
        if(file_name == bank['name']):
            return True , index
    return False, ''

def generate_browser_list(current_path, current_level, open_folder_list):

    global results
    results = []

    add_folder_to_browser_list(current_path, current_level,open_folder_list)

    memory_bank = read_json('DisplayData.json')

    for browser_line in results:
        is_file, file_name = extract_file_type_and_name_from_browser_format(browser_line['name'])
        if is_file:
            is_banked, bank_number = is_file_in_memory_bank(file_name, memory_bank)
            if is_banked:
                browser_line['bank'] = str(bank_number)

    return results

def add_folder_to_browser_list(current_path, current_level,open_folder_list):
    root, dirs, files = next(os.walk(current_path))

    indent = ' ' * 4 * (current_level)
    for folder in dirs:
        is_open, char = check_folder_state(folder,open_folder_list)
        #print('{}{}{}'.format(indent, folder, char))
        results.append(dict(name='{}{}{}'.format(indent, folder, char), bank='x'))
        if (is_open):
            next_path = '{}/{}'.format(root, folder)
            next_level = current_level + 1
            add_folder_to_browser_list(next_path, next_level,open_folder_list)

    for f in files:
        if (os.path.splitext(f)[1] in ['.mp4']):
            #print('{}{}'.format(indent, f))
            results.append(dict(name='{}{}'.format(indent, f), bank='-'))

def check_folder_state(folder_name,open_folder_list):
    if (folder_name in open_folder_list):
        return True, '/'
    else:
        return False, '|'

def extract_file_type_and_name_from_browser_format(dir_name):
    #logger.info('the name we got was {}'.format(dir_name))
    if(dir_name.endswith('|') or dir_name.endswith('/')):
        return False , dir_name.lstrip()[:-1]
    else:
        return True , dir_name.lstrip()

def get_length_for_file(location):
    #TODO: will have omx.player get length of file probs..
    pass

def create_new_bank_mapping_in_first_open(file_name):
    memory_bank = read_json('DisplayData.json')
    for index , bank in enumerate(memory_bank):
        if(not bank['name']):
            create_new_bank_mapping(index,file_name,memory_bank)
            return True
    return False

def create_new_bank_mapping(bank_number,file_name,memory_bank=[]):
    has_location , location = get_path_for_file(file_name)
    length = get_length_for_file(location)
    new_bank = dict(name=file_name, location=location, length=-1, start=-1, end=-1)
    update_a_banks_data(bank_number, new_bank, memory_bank)

def get_path_for_file(file_name):
    for root, dirs, files in os.walk(PATH_TO_BROWSER):
        if file_name in files:
            print root
            return True, '{}/{}'.format(root,file_name)
        else:
            return False, ''

def update_a_banks_data(bank_number, bank_info, memory_bank=[]):
    if not memory_bank:
        memory_bank = read_json('DisplayData.json')
    memory_bank[bank_number] = bank_info
    update_json('DisplayData.json', memory_bank)

def clear_all_banks():
    memory_bank = read_json('DisplayData.json')
    for index , bank in enumerate(memory_bank):
        memory_bank[index] = EMPTY_BANK
    update_json('DisplayData.json', memory_bank)

def read_json(file_name):

    with open(PATH_TO_DATA_OBJECTS + file_name) as data_file:
        data = json.load(data_file)

    return data

def update_json(file_name,data):

    with open('{}{}'.format(PATH_TO_DATA_OBJECTS, file_name), 'w') as data_file:
        json.dump(data, data_file)

def get_all_settings_data_for_display():
    settings = read_json('Settings.json')
    display_settings = []
    for index, setting in enumerate(settings):
        display_settings.append(([setting['name'],setting['value']],index))
    return display_settings

def get_a_banks_data(bank_number):
    memory_bank = read_json('DisplayData.json')
    return memory_bank[bank_number]

def switch_settings(setting_name):
    settings = read_json('Settings.json')

    for index, setting in enumerate(settings):
        if setting['name'] == setting_name:
            setting = cycle_setting_value(setting)

    update_json('Settings.json',settings)

def cycle_setting_value(setting):
    if setting['name'] == 'PLAYBACK_MODE':
        if setting['value'] == 'LOOPER':
            setting['value'] = 'PLAYLIST'
        elif setting['value'] == 'PLAYLIST':
            setting['value'] = 'RANDOM'
        else:
            setting['value'] = 'LOOPER'
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

    return setting


def get_next_context():
    next_bank_number = read_json('next_bank_number.json')
    memory_bank = read_json('DisplayData.json')
    next_bank_details = memory_bank[next_bank_number]
    start_value = next_bank_details['start']
    end_value = next_bank_details['end']
    length = next_bank_details['length']

    use_rand_start, use_sync_length, sync_length, playback_mode = get_context_options_from_settings()
    set_next_bank_number_from_playback_mode(playback_mode,next_bank_number)

    if use_rand_start and use_sync_length:
        start_value = randint(0, length - sync_length)
        end_value = start_value + sync_length
    elif use_rand_start and not use_sync_length:
        start_value = randint(0, end_value)
    elif not use_rand_start and use_sync_length:
        end_value = min(length, start_value + sync_length)

    context = dict(location=next_bank_details['location'],start=start_value,end=end_value, bank_number=next_bank_number)

def get_context_options_from_settings():
    settings = read_json('Settings.json')
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

    return use_rand_start , use_sync_length , sync_length , playback_mode

def set_next_bank_number_from_playback_mode(playback_mode, current_bank_number):
    next_bank_number = 0
    if playback_mode == 'LOOPER':
        next_bank_number = current_bank_number
    elif playback_mode == 'RANDOM':
        #TODO: actually find which banks have value and only use those
        next_bank_number = randint(0,14)
    elif playback_mode == 'PLAYLIST':
        #TODO: implement some playlist objects and logic at some point
        next_bank_number = current_bank_number
    update_json('next_bank_number.json',next_bank_number)

def convert_int_to_string_for_display(time_in_seconds):
    if time_in_seconds < 0:
        return ''
    elif time_in_seconds >= 6000:
        return '99:99'
    else:
        return time.strftime("%M:%S", time.gmtime(time_in_seconds))
