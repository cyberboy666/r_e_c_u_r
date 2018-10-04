import display_centre.menu as menu
import os

class Shaders(object):
    MENU_HEIGHT = 10
    EMPTY_SHADER = dict(name='none',is_shader=True,shad_type='-',param_number=0,path='-',shad_index=0)
    def __init__(self, root, osc_client, message_handler, data):
        self.root = root
        self.osc_client = osc_client
        self.message_handler = message_handler
        self.data = data
        self.shaders_menu = menu.ShadersMenu(self.data, self.message_handler, self.MENU_HEIGHT )
        self.selected_shader = self.EMPTY_SHADER
        self.shaders_menu_list = self.generate_shaders_list()
        print(self.shaders_menu_list)
        if self.shaders_menu_list is not None:
            pass
                 
        self.selected_status = '-' ## going to try using symbols for this : '-' means empty, '▶' means running, '■' means not running, '!' means error
        self.selected_param_values = [0,0,0,0]
        #self.load_selected_shader()

    def generate_shaders_list(self):
        shaders_menu_list = []
        raw_list = self.shaders_menu.generate_raw_shaders_list()
        shad_i = 0
        for line in raw_list:
            if line['is_shader']:
                has_path, path = self.get_path_for_shader(line['name'])
                shad_type = self.determine_if_shader_file_is_processing(path)
                parameter_number = self.determine_shader_parameter_number(path)
                #print('shader index is {}'.format(shad_i))
                shaders_menu_list.append(dict(name=line['name'],is_shader=True,shad_type=shad_type,param_number=parameter_number,path=path,shad_index=shad_i))
                shad_i = shad_i +1
            else:
                shaders_menu_list.append(dict(name=line['name'],is_shader=False,shad_type='',param_number=None,path=None,shad_index=None))
        return shaders_menu_list


    def get_path_for_shader(self, file_name):
        ######## returns full path for a given file name ########
        for path in self.data.PATHS_TO_SHADERS:    
            for root, dirs, files in os.walk(path):
                if file_name in files:
                    return True, '{}/{}'.format(root, file_name)
        return False, ''

    def determine_if_shader_file_is_processing(self, path):
        with open(path, 'r') as selected_shader:
                shader_text = selected_shader.read()
                if '//pro-shader' in shader_text:
                    return 'pro'
                elif '//gen-shader' in shader_text:
                    return 'gen'

                else:
                    return '-'

    def determine_shader_parameter_number(self, path):
        max_amount = 4
        with open(path, 'r') as selected_shader:
            shader_text = selected_shader.read()
            for i in range(max_amount):
                if 'uniform float u_x{}'.format(i) not in shader_text:
                    return i
            return max_amount

    def load_selected_shader(self):
        print(self.selected_shader)
        is_pro = self.selected_shader['shad_type'] == 'pro'
        self.osc_client.send_message("/shader/load", [self.selected_shader['path'],is_pro,self.selected_shader['param_number']])
        if not self.selected_status == '▶':
            self.selected_status = '■'

    def start_selected_shader(self):
        self.osc_client.send_message("/shader/start", True)
        self.selected_status = '▶'

    def stop_selected_shader(self):
        self.osc_client.send_message("/shader/stop", True)
        self.selected_status = '■'

    def enter_on_shaders_selection(self):
        index = self.shaders_menu.selected_list_index
        is_file, name = self.shaders_menu.extract_file_type_and_name_from_menu_format(
            self.shaders_menu_list[index]['name'])
        if is_file:
            self.selected_shader = self.shaders_menu_list[index]
            self.load_selected_shader()
        else:
            self.shaders_menu.update_open_folders(name)
        self.shaders_menu_list = self.generate_shaders_list()
        return is_file, self.selected_shader
