import os
import data_centre.data


class BrowserData(object):
    ######## a data class used mainly for managing the browser list ########
    def __init__(self, initial_path):
        self.initial_path = initial_path
        self.open_folders = []
        self.browser_list = []
        self.memory_bank = []
        self.generate_browser_list()

    def update_open_folders(self, folder_name):
        if folder_name not in self.open_folders:
            self.open_folders.append(folder_name)
        else:
            self.open_folders.remove(folder_name)

    def generate_browser_list(self):
        ######## starts the recursive process of listing all folders and video files to display ########
        self.browser_list = []
        self._add_folder_to_browser_list(self.initial_path, 0)

        self.memory_bank = data_centre.data.read_json(data_centre.data.BANK_DATA_JSON)

        for browser_line in self.browser_list:
            is_file, file_name = self.extract_file_type_and_name_from_browser_format(browser_line['name'])
            if is_file:
                is_slotted, slot_number = self._is_file_in_memory_bank(file_name)
                if is_slotted:
                    browser_line['slot'] = str(slot_number)

        return self.browser_list

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
            if (split_name[1] in ['.mp4', '.mkv']):
                self.browser_list.append(dict(name='{}{}'.format(indent, f), slot='-'))

    def _check_folder_state(self, folder_name):
        ######## used for displaying folders as open or closed ########
        if folder_name in self.open_folders:
            return True, '/'
        else:
            return False, '|'

    def _is_file_in_memory_bank(self, file_name):
        ######## used for displaying the mappings in browser view ########
        if not self.memory_bank:
            self.memory_bank = data_centre.data.read_json(data_centre.data.BANK_DATA_JSON)
        for index, slot in enumerate(self.memory_bank):
            if file_name == slot['name']:
                return True, index
        return False, ''






