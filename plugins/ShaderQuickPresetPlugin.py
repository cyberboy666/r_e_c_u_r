import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin, SequencePlugin
import copy

class ShaderQuickPresetPlugin(ActionsPlugin): #,SequencePlugin):
    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)
        self.PRESET_FILE_NAME = 'ShaderQuickPresetPlugin/presets.json'

        self.presets = self.load_presets()
        print("loaded presets %s" % self.presets)

        self.selected_preset = None

    def load_presets(self):
        print("trying load presets? %s " % self.PRESET_FILE_NAME)
        return self.pc.read_json(self.PRESET_FILE_NAME) or ([None]*10)

    def save_presets(self):
        self.pc.update_json(self.PRESET_FILE_NAME, self.presets)

    @property
    def parserlist(self):
        return [ 
            ( r"load_presets",              self.load_presets ),
            ( r"save_presets",              self.save_presets ),
            ( r"store_next_preset",         self.store_next_preset ),
            ( r"store_current_preset",      self.store_current_preset ),
            ( r"switch_to_preset_([0-9])",  self.switch_to_preset ),
        ]

    def store_next_preset(self):
        res = [i for i, val in enumerate(self.presets) if val == None]
        if res is None:
            self.selected_preset += 1
            self.selected_preset %= 10
        else:
            self.selected_preset = res[0]

        self.store_current_preset()

    def get_live_frame(self):
        #print("get_live_frame: %s" % self.pc.message_handler.shaders.selected_param_list)
        frame = {
                'selected_shader_slots': [ shader.get('slot',None) for shader in self.pc.message_handler.shaders.selected_shader_list ],
                'shader_params': copy.deepcopy(self.pc.message_handler.shaders.selected_param_list),
                'layer_active_status': copy.deepcopy(self.pc.message_handler.shaders.selected_status_list),
                'feedback_active': self.pc.data.feedback_active,
                'x3_as_speed': self.pc.data.settings['shader']['X3_AS_SPEED']['value']
        }
        #print("built frame: %s" % frame['shader_params'])
        return frame

    def store_current_preset(self):
        if self.selected_preset is None: self.selected_preset = 0

        insert_position = self.selected_preset
        self.presets[insert_position] = self.get_live_frame()
        #print ("stored %s at position %s" % (self.presets[insert_position], insert_position))
        self.selected_preset = insert_position

        self.save_presets()

    def switch_to_preset(self, preset):
        #if preset>len(self.presets):
        if self.presets[preset] is None:
            print ("no quick shader preset in slot %s!" % preset)
            self.selected_preset = preset
            return
        print ("switching to preset %s" % preset)
        self.selected_preset = preset
        #self.pc.message_handler.actions.shaders.selected_shader_list = self.presets[preset].get('selected_shader_list',self.pc.message_handler.actions.shaders.selected_shader_list)
        preset = self.presets[preset]

        print ("recalled preset %s" % preset)

        self.recall_frame(preset)

    def recall_frame_params(self, preset):
        if not preset:
            return
        #print("recall_frame_params got: %s" % preset.get('shader_params'))
        for (layer, param_list) in enumerate(preset.get('shader_params')):
            if param_list:
                for param,value in enumerate(param_list):
                  if value is not None:
                    #print("recalling layer %s param %s: value %s" % (layer,param,value))
                    self.pc.midi_input.call_method_name('set_the_shader_param_%s_layer_%s_continuous' % (param,layer), value)

        if preset.get('feedback_active') is not None:
            self.pc.data.feedback_active = preset.get('feedback_active',self.pc.data.feedback_active)
            if self.pc.data.feedback_active:
                self.pc.midi_input.call_method_name('enable_feedback')
            else:
                self.pc.midi_input.call_method_name('disable_feedback')

    def recall_frame(self, preset):

        self.recall_frame_params(preset)

        self.pc.data.settings['shader']['X3_AS_SPEED']['value'] = preset.get('x3_as_speed')

        for (layer, slot) in enumerate(preset.get('selected_shader_slots',[])):
            if slot is not None:
                #print("setting layer %s to slot %s" % (layer, slot))
                self.pc.midi_input.call_method_name('play_shader_%s_%s' % (layer, slot))

        for (layer, active) in enumerate(preset.get('layer_active_status',[])):
            # print ("got %s layer with status %s " % (layer,active))
            if active=='▶':
                self.pc.midi_input.call_method_name('start_shader_layer_%s' % layer)
            else:
                self.pc.midi_input.call_method_name('stop_shader_layer_%s' % layer)

