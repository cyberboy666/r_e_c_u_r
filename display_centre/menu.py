import os

class Menu(object):
    def __init__(self, data, message_handler, menu_height):
        self.data = data
        self.message_handler = message_handler        
        self.open_folders = []
        self.menu_list = []
        self.menu_height = menu_height
        self.top_menu_index = 0

        self.selected_list_index = 0
    
    def navigate_menu_up(self):
        if self.selected_list_index != 0:
            if self.selected_list_index == self.top_menu_index:
                self.top_menu_index -= 1
            self.selected_list_index -= 1
        else:
            last_list_index = len(self.menu_list) - 1
            self.selected_list_index = last_list_index
            self.top_menu_index = last_list_index - (self.menu_height - 1)
            if self.top_menu_index < 0:
                self.top_menu_index = 0

    def navigate_menu_down(self):
        last_list_index = len(self.menu_list) - 1
        if self.selected_list_index != last_list_index:
            bot_menu_index = self.top_menu_index + self.menu_height - 1
            if self.selected_list_index == bot_menu_index:
                self.top_menu_index += 1
            self.selected_list_index += 1
        else:
            self.top_menu_index = 0
            self.selected_list_index = self.top_menu_index
        
    def update_open_folders(self, folder_name):
        if folder_name not in self.open_folders:
            self.open_folders.append(folder_name)
        else:
            self.open_folders.remove(folder_name)
    
    def _check_folder_state(self, folder_name):
        ######## used for displaying folders as open or closed ########
        if folder_name in self.open_folders:
            return True, '/'
        else:
            return False, '|'
 
    @staticmethod
    def extract_file_type_and_name_from_menu_format(dir_name):
        # removes whitespace and folder state from display item ########
        if dir_name.endswith('|') or dir_name.endswith('/'):
            return False, dir_name.lstrip()[:-1]
        else:
            return True, dir_name.lstrip()

class BrowserMenu(Menu):    
    def __init__(self, data, message_handler, menu_height):
        Menu.__init__(self, data, message_handler, menu_height)
        self.generate_browser_list()

    def generate_browser_list(self):
        ######## starts the recursive process of listing all folders and video files to display ########
        self.menu_list = []
        for path in self.data.PATHS_TO_BROWSER:
            self._add_folder_to_browser_list(path, 0)
        
        for browser_line in self.menu_list:
            is_file, name = self.extract_file_type_and_name_from_menu_format(browser_line['name'])
            if is_file:
                is_slotted, bankslot_number = self._is_file_in_bank_data(name)
                if is_slotted:
                    browser_line['slot'] = bankslot_number

    def _add_folder_to_browser_list(self, current_path, current_level):
        ######## adds the folders and mp4 files at the current level to the results list. recursively recalls at deeper level if folder is open ########
        # TODO make note of / investigate what happens with multiple folders of same name
        root, dirs, files = next(os.walk(current_path))

        indent = ' ' * 4 * (current_level)
        for folder in sorted(dirs):
            is_open, char = self._check_folder_state(folder)
            self.menu_list.append(dict(name='{}{}{}'.format(indent, folder, char), slot='x'))
            if (is_open):
                next_path = '{}/{}'.format(root, folder)
                next_level = current_level + 1
                self._add_folder_to_browser_list(next_path, next_level)

        files.sort()
        for f in files:
            split_name = os.path.splitext(f)
            if (split_name[1].lower() in ['.mp4', '.mkv', '.avi', '.mov']):
                self.menu_list.append(dict(name='{}{}'.format(indent, f), slot='-'))

    def _is_file_in_bank_data(self, file_name):
        ######## used for displaying the mappings in browser view ########
        for bank_index, bank in enumerate(self.data.bank_data):
            for slot_index, slot in enumerate(bank):
                if file_name == slot['name']:
                    return True, '{}-{}'.format(bank_index,slot_index)
        return False, ''
        

    def enter_on_browser_selection(self):
        is_file, name = self.extract_file_type_and_name_from_menu_format(
            self.menu_list[self.selected_list_index]['name'])
        if is_file:
            is_successful = self.data.create_new_slot_mapping_in_first_open(name)
            if not is_successful:
                self.message_handler.set_message('INFO', 'current bank is full')
        else:
            self.update_open_folders(name)
        self.generate_browser_list()


class SettingsMenu(Menu):

    FOLDER_ORDER = ['video', 'sampler', 'user_input', 'capture', 'shader', 'detour', 'system' ]
    SAMPLER_ORDER = ['LOOP_TYPE', 'LOAD_NEXT', 'RAND_START_MODE', 'RESET_PLAYERS', 'FIXED_LENGTH_MODE', 'FIXED_LENGTH', 'FIXED_LENGTH_MULTIPLY' ]
    VIDEO_ORDER = ['VIDEOPLAYER_BACKEND']
    USER_INPUT_ORDER = ['MIDI_INPUT', 'MIDI_STATUS', 'CYCLE_MIDI_PORT']
    CAPTURE_ORDER = ['DEVICE', 'TYPE']
    SHADER_ORDER = ['USER_SHADER']
    DETOUR_ORDER = ['TRY_DEMO']
    SYSTEM_ORDER = []

    SETTINGS_TO_HIDE = ['OUTPUT' ]

    def __init__(self, data, message_handler, menu_height):

        Menu.__init__(self, data, message_handler, menu_height)
        self.generate_settings_list()

    def generate_settings_list(self):
        self.check_for_settings_to_hide()

        self.menu_list = []
        ordered_folders = self.order_keys_from_list(self.data.settings, self.FOLDER_ORDER)
        for (setting_folder_key, setting_folder_item) in ordered_folders:
            if setting_folder_key in self.open_folders:
                self.menu_list.append(dict(name='{}/'.format(setting_folder_key), value=''))
                order_list_name = '{}_ORDER'.format(setting_folder_key.upper())
                ordered_value = self.order_keys_from_list(setting_folder_item, getattr(self,order_list_name))
                for (setting_details_key, setting_details_item) in ordered_value:
                    if not setting_details_key in self.SETTINGS_TO_HIDE:
                        self.menu_list.append(dict(name='   {}'.format(setting_details_key), value=self.data.make_empty_if_none(setting_details_item['value'])))
            else:   
                self.menu_list.append(dict(name='{}|'.format(setting_folder_key), value=''))

    def enter_on_setting_selection(self):
        is_file, name = self.extract_file_type_and_name_from_menu_format(
            self.menu_list[self.selected_list_index]['name'])
        if is_file:
            folder, setting_name, setting_details = self.data.get_setting_and_folder_from_name(name)
            if setting_details['value'] in setting_details['options']:
                current_value_index = setting_details['options'].index(setting_details['value'])
                new_value_index = (current_value_index + 1) % len(setting_details['options'])
                setting_details = self.data.update_setting_value(folder, setting_name, setting_details['options'][new_value_index])
            self.generate_settings_list()
            return True, setting_details
        else:
            self.update_open_folders(name)
            self.generate_settings_list()
            return False, ''

    def check_for_settings_to_hide(self):
        self.SETTINGS_TO_HIDE = ['OUTPUT']
        if self.data.settings['video']['VIDEOPLAYER_BACKEND']['value'] != 'omxplayer':
            self.SETTINGS_TO_HIDE = self.SETTINGS_TO_HIDE + ['SCREEN_MODE', 'BACKGROUND_COLOUR', 'FRAMERATE', 'IMAGE_EFFECT', 'RESOLUTION', 'SHUTTER']
        else:
            self.SETTINGS_TO_HIDE = self.SETTINGS_TO_HIDE + ['LOOP_TYPE']

    @staticmethod
    def order_keys_from_list(dictionary, order_list):
        ordered_tuple_list = []
        for order_key in order_list:
            if order_key in dictionary:
                ordered_tuple_list.append((order_key, dictionary[order_key]))
        for  other_key in sorted(dictionary):
            if other_key not in [i[0] for i in ordered_tuple_list]:
                ordered_tuple_list.append((other_key, dictionary[other_key]))
        return ordered_tuple_list

class ShadersMenu(Menu):

    def __init__(self, data, message_handler, menu_height):
        Menu.__init__(self, data, message_handler, menu_height)
        #self.top_menu_index = 1
        #self.selected_list_index = 1

    def generate_raw_shaders_list(self):
        ######## starts the recursive process of listing all folders and shader files to display ########
        self.menu_list = []
        for path in self.data.PATHS_TO_SHADERS:
            self._add_folder_to_shaders_list(path, 0)
        return self.menu_list
   

    def _add_folder_to_shaders_list(self, current_path, current_level):
        ######## adds the folders and shader files at the current level to the results list. recursively recalls at deeper level if folder is open ########
        
        root, dirs, files = next(os.walk(current_path))

        indent = ' ' * 4 * (current_level)
        for folder in sorted(dirs):
            is_open, char = self._check_folder_state(folder)
            self.menu_list.append(dict(name='{}{}{}'.format(indent, folder, char), is_shader=False))
            if (is_open):
                next_path = '{}/{}'.format(root, folder)
                next_level = current_level + 1
                self._add_folder_to_shaders_list(next_path, next_level)

        files.sort()
        for f in files:
            split_name = os.path.splitext(f)
            if (split_name[1].lower() in ['.frag', '.shader', '.glsl', '.glslf', '.fsh']):
                self.menu_list.append(dict(name='{}{}'.format(indent, f), is_shader=True))





