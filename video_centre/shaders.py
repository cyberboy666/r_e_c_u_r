import display_centre.menu as menu
import os
from statistics import mean
from data_centre.plugin_collection import ModulationReceiverPlugin

class Shaders(object):
    MENU_HEIGHT = 10
    EMPTY_SHADER = dict(name='none',is_shader=True,shad_type='-',param_number=4,path='-')
    def __init__(self, root, osc_client, message_handler, data):
        self.root = root
        self.osc_client = osc_client
        self.message_handler = message_handler
        self.message_handler.shaders = self
        self.data = data
        self.shaders_menu = menu.ShadersMenu(self.data, self.message_handler, self.MENU_HEIGHT )
        self.selected_shader_list = [self.EMPTY_SHADER for i in range(3)]
        self.focused_param = 0
        self.shaders_menu_list = self.generate_shaders_list()

        self.selected_modulation_slot = 0
                 
        self.selected_status_list = ['-','-','-'] ## going to try using symbols for this : '-' means empty, '▶' means running, '■' means not running, '!' means error
        self.selected_param_list = [[0.0,0.0,0.0,0.0] for i in range(3)]
        self.selected_speed_list = [1.0, 1.0, 1.0]

        self.selected_modulation_slot = 0
        self.selected_modulation_level = [[[0.0,0.0,0.0,0.0] for i in range(4)] for i in range(3)]
        self.modulation_value = [0.0,0.0,0.0,0.0]

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
        if self.selected_status_list[layer] != '-':
            self.selected_status_list[layer] = '▶'

    def stop_shader(self, layer):
        self.osc_client.send_message("/shader/{}/is_active".format(str(layer)), False)
        if self.selected_status_list[layer] != '-':
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
            if self.selected_shader_list[layer].get('slot') is None or self.selected_shader_list[layer]['slot'] != slot:
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

    def set_x3_as_speed(self, status):
        self.data.settings['shader']['X3_AS_SPEED']['value'] = 'enabled' if status else 'disabled'

    def select_shader_modulation_slot(self, slot):
        self.selected_modulation_slot = slot

    def reset_modulation(self, slot):
        for layer in self.selected_modulation_level:
            for layer,levels in enumerate(layer):
                levels[slot] = 0.0

    def reset_selected_modulation(self):
        self.reset_modulation(self.selected_modulation_slot)

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

        self.set_param_layer_to_amount(param, layer, amount)

    def set_param_layer_to_amount(self, param, layer, amount):
        if self.data.settings['shader']['X3_AS_SPEED']['value'] == 'enabled' and param == 3:
            self.set_speed_to_amount(amount, layer) #layer_offset=layer-self.data.shader_layer)
        else: 
            self.selected_param_list[layer][param] = amount
            self.update_param_layer(param,layer)

    def get_modulation_value_list(self, amount, values, levels):
        l = []
        for i,v in enumerate(values):
            l.append(self.get_modulation_value(amount, v, levels[i]))

        #print ("got mean %s from amount %s with %s*%s" % (mean(l), amount, values, levels))
        return mean(l)

    def get_modulation_value(self, amount, value, level):
        if level==0:
            return amount

        # TODO: read from list of input formulas, from plugins etc to modulate the value
        temp_amount = amount + (value * level)
        #print("from amount %s, modulation is %s, temp_amount is %s" % (amount, modulation, temp_amount))
        if temp_amount <  0: temp_amount = 0 # input range is 0-1 so convert back
        if temp_amount >  1: temp_amount = 1 # modulation however is -1 to +1

        return temp_amount

    def send_param_layer_amount_message(self, param, layer, amount):
        self.osc_client.send_message("/shader/{}/param".format(str(layer)), [param, amount] )

    def modulate_param_to_amount(self, param, value):
        self.modulation_value[param] = (value-0.5)*2
        for plugin in self.data.plugins.get_plugins(ModulationReceiverPlugin):
            plugin.set_modulation_value(param, self.modulation_value[param])
        for layer,params in enumerate(self.selected_param_list):
          for ip,p in enumerate(params):
              for p2,v in enumerate(self.selected_modulation_level[layer][ip]):
                  if v!=0:
                      self.update_param_layer(ip,layer)
                      break

    def set_param_layer_offset_modulation_level(self, param, layer, level):
        layer = (self.data.shader_layer + layer) % 3
        self.set_param_layer_modulation_level(param, layer, level)

    def set_param_layer_modulation_level(self, param, layer, level):
        self.selected_modulation_level[layer][param][self.selected_modulation_slot] = level
        self.update_param_layer(param, layer)

    def update_param_layer(self, param, layer):
        # merge all applicable layers

        self.send_param_layer_amount_message(param, layer,
                self.get_modulation_value_list(
                    self.selected_param_list[layer][param],
                    self.modulation_value,#[0], #param],
                    self.selected_modulation_level[layer][param]
                )
        )

    def set_speed_offset_to_amount(self, layer_offset, amount):
        self.set_speed_to_amount(amount, layer_offset)

    def set_speed_to_amount(self, amount, layer_offset=0):
        layer = (self.data.shader_layer + layer_offset) % 3
        self.set_speed_to_amount_layer(layer)
   
    def set_speed_layer_to_amount(self, layer, amount):
        self.osc_client.send_message("/shader/{}/speed".format(str(layer)), amount )
        self.selected_speed_list[layer] = amount
   
