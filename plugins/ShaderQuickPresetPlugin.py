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

    def store_current_preset(self):
        if self.selected_preset is None: self.selected_preset = 0

        insert_position = self.selected_preset
        self.presets[insert_position] = self.pc.shaders.get_live_frame()
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

        self.pc.shaders.recall_frame(preset)

