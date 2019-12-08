import display_centre.menu as menu
import os


class Shaders(object):
    MENU_HEIGHT = 10
    EMPTY_SHADER = dict(name='none',is_shader=True,shad_type='-',param_number=4,path='-')
    def __init__(self, root, osc_client, message_handler, data):
        self.root = root
        self.osc_client = osc_client
        self.message_handler = message_handler
        self.data = data
        self.shaders_menu = menu.ShadersMenu(self.data, self.message_handler, self.MENU_HEIGHT )
        self.selected_shader_list = [self.EMPTY_SHADER for i in range(3)]
        self.focused_param = 0
        self.shaders_menu_list = self.generate_shaders_list()
                 
        self.selected_status_list = ['-','-','-'] ## going to try using symbols for this : '-' means empty, '▶' means running, '■' means not running, '!' means error
        self.selected_param_list = [[0.0,0.0,0.0,0.0] for i in range(3)]
        self.selected_speed_list = [1.0, 1.0, 1.0]
        #self.load_selected_shader()

    def generate_shaders_list(self):
        shaders_menu_list = []
        raw_list = self.shaders_menu.generate_raw_shaders_list()
        for line in raw_list:
            if line['is_shader']:
                stripped_name = line['name'].lstrip()
                has_path, path = self.get_path_for_shader(stripped_name)
                shad_type = self.determine_shader_type(path)
                parameter_number = self.determine_shader_parameter_number(path)
        
                shaders_menu_list.append(dict(name=line['name'],is_shader=True,shad_type=shad_type,param_number=parameter_number,path=path))
        
            else:
                shaders_menu_list.append(dict(name=line['name'],is_shader=False,shad_type='',param_number=None,path=None))
        return shaders_menu_list


    def get_path_for_shader(self, file_name):
        ######## returns full path for a given file name ########
        for path in self.data.PATHS_TO_SHADERS:    
            for root, dirs, files in os.walk(path):
                if file_name in files:
                    return True, '{}/{}'.format(root, file_name)
        return False, ''

    def determine_shader_type(self, path):
        with open(path, 'r', errors='ignore') as selected_shader:
                shader_text = selected_shader.read()
                if '//0-input' in shader_text:
                    return '0in'
                elif '//1-input' in shader_text:
                    return '1in'
                elif '//2-input' in shader_text:
                    return '2in'
                else:
                    return '-'


    def determine_shader_parameter_number(self, path):
        max_amount = 4
        if True: # for now always assume 4 params
            return max_amount
        with open(path, 'r') as selected_shader:
            shader_text = selected_shader.read()
            for i in range(max_amount):
                if 'uniform float u_x{}'.format(i) not in shader_text:
                    return i
            return max_amount

    def load_shader_layer(self, layer):
        selected_shader = self.selected_shader_list[layer]
        #self.selected_param_list[self.data.shader_layer] = [0.0,0.0,0.0,0.0]
        print("select shader: ", selected_shader)
        self.osc_client.send_message("/shader/{}/load".format(str(layer)), [selected_shader['path'],selected_shader['shad_type'] == '2in',selected_shader['param_number']])
        if not self.selected_status_list[layer] == '▶':
            self.selected_status_list[layer] = '■'

    def load_selected_shader(self):
        self.load_shader_layer(self.data.shader_layer)

    def start_shader(self, layer):
        self.osc_client.send_message("/shader/{}/is_active".format(str(layer)), True)
        self.selected_status_list[layer] = '▶'

    def stop_shader(self, layer):
        self.osc_client.send_message("/shader/{}/is_active".format(str(layer)), False)
        self.selected_status_list[layer] = '■'

    def start_selected_shader(self):
        self.start_shader(self.data.shader_layer)

    def stop_selected_shader(self):
        self.stop_shader(self.data.shader_layer)

    def map_on_shaders_selection(self):
        index = self.shaders_menu.selected_list_index
        is_file, name = self.shaders_menu.extract_file_type_and_name_from_menu_format(
            self.shaders_menu_list[index]['name'])
        if is_file:
            is_successful = self.data.create_new_shader_mapping_in_first_open(name)
            if not is_successful:
                self.message_handler.set_message('INFO', 'current bank is full')
        else:
            self.message_handler.set_message('INFO', 'can not map folder')

    def enter_on_shaders_selection(self):
        selected_shader = self.selected_shader_list[self.data.shader_layer]
        index = self.shaders_menu.selected_list_index
        is_file, name = self.shaders_menu.extract_file_type_and_name_from_menu_format(
            self.shaders_menu_list[index]['name'])
        is_selected_shader = False
        if is_file and name == selected_shader['name'].lstrip():
            is_selected_shader = True
        elif is_file:
            self.selected_shader_list[self.data.shader_layer] = self.shaders_menu_list[index]
            self.load_selected_shader()
        else:
            self.shaders_menu.update_open_folders(name)
        self.shaders_menu_list = self.generate_shaders_list()
        return is_file, is_selected_shader, selected_shader

    def play_that_shader(self, layer, slot):
        if self.data.shader_bank_data[layer][slot]['path']:
            self.selected_shader_list[layer] = self.data.shader_bank_data[layer][slot]
            self.selected_shader_list[layer]['slot'] = slot
            self.load_shader_layer(layer)
        else:
            self.message_handler.set_message('INFO', "shader slot %s:%s is empty"%(layer,slot))

    def play_this_shader(self, slot):
        print(self.data.shader_bank_data[self.data.shader_layer])
        self.play_that_shader(self.data.shader_layer, slot)

    def increase_this_param(self, amount_change):
        param = self.focused_param
        current_amount = self.selected_param_list[self.data.shader_layer][param]
        amount = self.get_new_param_amount(current_amount,amount_change)
        self.set_param_to_amount(param, amount)

    def decrease_this_param(self, amount_change):
        param = self.focused_param
        current_amount = self.selected_param_list[self.data.shader_layer][param]
        amount = self.get_new_param_amount(current_amount,-amount_change)
        self.set_param_to_amount(param, amount)
    
    def toggle_shader_speed(self):
        if self.selected_speed_list[self.data.shader_layer] > 0.62:
            self.set_speed_to_amount(0.5)
        else:
            self.set_speed_to_amount(0.75)

    @staticmethod
    def get_new_param_amount(current, change):
        if current + change > 1:
            return 1
        elif current + change < 0:
            return 0
        else: 
            return current + change
    
    def set_param_to_amount(self, param, amount, layer_offset=None):
        start_layer = self.data.shader_layer
        if self.data.settings['shader']['FIX_PARAM_OFFSET_LAYER']['value'] == 'enabled':
            start_layer = 0 
        if layer_offset is None:
            start_layer = self.data.shader_layer
            layer_offset = 0
        layer = (start_layer + layer_offset) % 3
        print ("got transposed layer %s" % layer)
        if self.data.settings['shader']['X3_AS_SPEED']['value'] == 'enabled' and param == 3:
            self.set_speed_to_amount(amount, layout_offset=layout_offset)
        else:
            self.osc_client.send_message("/shader/{}/param".format(str(layer)), [param, amount] )
        self.selected_param_list[layer][param] = amount

    def set_speed_to_amount(self, amount, layer_offset=0):
        layer = self.data.shader_layer + layer_offset % 4
        self.osc_client.send_message("/shader/{}/speed".format(str(layer)), amount )
        self.selected_speed_list[layer] = amount
   

