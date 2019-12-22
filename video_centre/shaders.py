import display_centre.menu as menu
import os


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
            self.set_speed_to_amount(amount, layer_offset=layer-self.data.shader_layer)
        else:
            self.osc_client.send_message("/shader/{}/param".format(str(layer)), [param, amount] )
        self.selected_param_list[layer][param] = amount

    def set_speed_to_amount(self, amount, layer_offset=0):
        layer = (self.data.shader_layer + layer_offset) % 3
        self.osc_client.send_message("/shader/{}/speed".format(str(layer)), amount )
        self.selected_speed_list[layer] = amount
   
    # methods for helping dealing with storing and recalling shader parameter frame states
    def get_live_frame(self):
        #print("get_live_frame: %s" % self.pc.message_handler.shaders.selected_param_list)
        import copy #from copy import deepcopy
        frame = {
                'selected_shader_slots': [ shader.get('slot',None) for shader in self.selected_shader_list ],
                'shader_params': copy.deepcopy(self.selected_param_list),
                'layer_active_status': copy.deepcopy(self.selected_status_list),
                'feedback_active': self.data.feedback_active,
                'x3_as_speed': self.data.settings['shader']['X3_AS_SPEED']['value']
        }
        #print("built frame: %s" % frame['shader_params'])
        return frame

    def recall_frame_params(self, preset):
        if preset is None:
            return
        #print("recall_frame_params got: %s" % preset.get('shader_params'))
        for (layer, param_list) in enumerate(preset.get('shader_params',[])):
            if param_list:
                for param,value in enumerate(param_list):
                    #if (ignored is not None and ignored['shader_params'][layer][param] is not None):
                    #    print ("ignoring %s,%s because value is %s" % (layer,param,ignored['shader_params'][layer][param]))
                    #    continue
                    if (value is not None):
                      #print("recalling layer %s param %s: value %s" % (layer,param,value))
                      self.data.plugins.midi_input.call_method_name('set_the_shader_param_%s_layer_%s_continuous' % (param,layer), value)

        if preset.get('feedback_active') is not None:
            self.data.feedback_active = preset.get('feedback_active',self.data.feedback_active)
            if self.data.feedback_active:
                self.data.plugins.midi_input.call_method_name('enable_feedback')
            else:
                self.data.plugins.midi_input.call_method_name('disable_feedback')

    def recall_frame(self, preset):

        self.data.settings['shader']['X3_AS_SPEED']['value'] = preset.get('x3_as_speed')

        # x3_as_speed affects preset recall, so do that first
        self.recall_frame_params(preset)

        for (layer, slot) in enumerate(preset.get('selected_shader_slots',[])):
            if slot is not None:
                #print("setting layer %s to slot %s" % (layer, slot))
                self.data.plugins.midi_input.call_method_name('play_shader_%s_%s' % (layer, slot))

        for (layer, active) in enumerate(preset.get('layer_active_status',[])):
            # print ("got %s layer with status %s " % (layer,active))
            if active=='▶':
                self.data.plugins.midi_input.call_method_name('start_shader_layer_%s' % layer)
            else:
                self.data.plugins.midi_input.call_method_name('stop_shader_layer_%s' % layer)

    DEBUG_FRAMES = False

    # overlay frame2 on frame1
    def merge_frames(self, frame1, frame2):
        from copy import deepcopy
        f = deepcopy(frame1) #frame1.copy()
        if self.DEBUG_FRAMES:  print("merge_frames: got frame1\t%s" % frame1)
        if self.DEBUG_FRAMES:  print("merge_frames: got frame2\t%s" % frame2)
        for i,f2 in enumerate(frame2['shader_params']):
            for i2,p in enumerate(f2):
                if p is not None:
                    f['shader_params'][i][i2] = p
        if frame2['feedback_active'] is not None:
            f['feedback_active'] = frame2['feedback_active']
        if self.DEBUG_FRAMES:  print("merge_frames: got return\t%s" % f)
        return f

    def get_frame_ignored(self, frame, ignored):
        from copy import deepcopy
        f = deepcopy(frame) #frame1.copy()
        if self.DEBUG_FRAMES:  print("get_frame_ignored: got frame\t%s" % frame)
        for i,f2 in enumerate(frame['shader_params']):
            for i2,p in enumerate(f2):
                if ignored['shader_params'][i][i2] is not None:
                    f['shader_params'][i][i2] = None
        if ignored.get('feedback_active') is not None:
            f['feedback_active'] = None
        if self.DEBUG_FRAMES:  print("get_frame_ignored: got return\t%s" % f)
        return f

    def is_frame_empty(self, frame):
        #from copy import deepcopy
        #f = deepcopy(frame) #frame1.copy()
        if self.DEBUG_FRAMES:  print("is_frame_empty: got frame\t%s" % frame)
        for i,f in enumerate(frame['shader_params']):
            for i2,p in enumerate(f):
                if p is not None: #ignored['shader_params'][i][i2] is not None:
                    return False
        if frame.get('feedback_active') is not None:
            return False
        if self.DEBUG_FRAMES:  print("is_frame_empty: got return true" % f)
        return True


    def get_frame_diff(self, last_frame, current_frame):
        if not last_frame: return current_frame

        if self.DEBUG_FRAMES:
            print(">>>>get_frame_diff>>>>")
            print("last_frame: \t%s" % last_frame['shader_params'])
            print("current_frame: \t%s" % current_frame['shader_params'])

        #values = [[None]*4]*3 # 3 shader layers, 4 params
        values = [[None]*4,[None]*4,[None]*4]
        #print (current_frame.get('shader_params'))
        for layer,params in enumerate(current_frame.get('shader_params',[[None]*4]*3)):
            #if self.DEBUG_FRAMES:  print("got layer %s params: %s" % (layer, params))
            for param,p in enumerate(params):
                if p is not None and p != last_frame.get('shader_params')[layer][param]:
                    if self.DEBUG_FRAMES: print("setting layer %s param %s to %s" % (layer,param,p))
                    values[layer][param] = p

        if current_frame['feedback_active'] is not None and last_frame['feedback_active'] != current_frame['feedback_active']:
            feedback_active = current_frame['feedback_active']
        else:
            feedback_active = None

        if self.DEBUG_FRAMES: print("values is\t%s" % values)

        diff = { 'shader_params': values, 'feedback_active': feedback_active }
        if self.DEBUG_FRAMES: print("returning\t%s\n^^^^" % diff['shader_params'])

        return diff


