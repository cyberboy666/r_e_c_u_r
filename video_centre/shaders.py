import display_centre.menu as menu
import os

class Shaders(object):
    MENU_HEIGHT = 9
    EMPTY_SHADER = dict(name='none',is_shader=True,shad_type='-',param_number=0,path='-',shad_index=0)
    def __init__(self, root, message_handler, data):
        self.root = root
        self.message_handler = message_handler
        self.data = data
        self.shaders_menu = menu.ShadersMenu(self.data, self.message_handler, self.MENU_HEIGHT)
        self.selected_shader = self.EMPTY_SHADER
        self.shaders_menu_list = self.generate_shaders_list()
        print('shader list is {}'.format(self.shaders_menu_list))

        #
        
        self.selected_status = '-'
        self.selected_param_values = [0,0,0,0,0,0,0,0]
        self.load_selected_shader()

    def generate_shaders_list(self):
        shaders_menu_list = []
        raw_list = self.shaders_menu.generate_raw_shaders_list()
        print('raw list is {}: '.format(raw_list))
        for line in raw_list:
            shad_i = 0
            if line['is_shader']:
                has_path, path = self.get_path_for_shader(line['name'])
                shad_type = self.determine_if_shader_file_is_processing(path)
                parameter_number = self.determine_shader_parameter_number(path)
                shaders_menu_list.append(dict(name=line['name'],is_shader=True,shad_type=shad_type,param_number=parameter_number,path=path,shad_index=shad_i))
                shad_i = shad_i +1
            else:
                shaders_menu_list.append(dict(name=line[name],is_shader=False,is_proc=None,param_number=None,path=None))
        return shaders_menu_list


    def get_path_for_shader(self, file_name):
        ######## returns full path for a given file name ########
        for path in self.data.PATHS_TO_SHADERS:    
            for root, dirs, files in os.walk(path):
                if file_name in files:
                    return True, '{}/{}'.format(root, file_name)
        return False, ''

    def determine_if_shader_file_is_processing(self, path):
        pass

    def determine_shader_parameter_number(self, path):
        pass

    def load_selected_shader(self):
        pass

    def enter_on_shaders_selection(self):
        is_file, name = self.shaders_menu.extract_file_type_and_name_from_menu_format(
            self.menu_list[self.selected_list_index]['name'])
        if is_file:
            pass
        else:
            self.shader_menu.update_open_folders(name)
        self.generate_shaders_list()
