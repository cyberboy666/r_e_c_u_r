import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin, SequencePlugin, DisplayPlugin
import copy
from plugins.frame_manager import Frame

class ShaderQuickPresetPlugin(ActionsPlugin,DisplayPlugin): #,SequencePlugin):

    MAX_PRESETS = 8

    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)
        self.PRESET_FILE_NAME = 'ShaderQuickPresetPlugin/presets.json'

        self.presets = self.load_presets()
        print("loaded presets %s" % self.presets)

        self.selected_preset = None
        self.last_recalled = None

    def load_presets(self):
        print("trying load presets? %s " % self.PRESET_FILE_NAME)
        return [ Frame(self.pc).store_copy(x) for x in (self.pc.read_json(self.PRESET_FILE_NAME) or ([None]*self.MAX_PRESETS)) ]

    def save_presets(self):
        self.pc.update_json(self.PRESET_FILE_NAME, self.presets)

    def stop_plugin(self):
        super().stop_plugin()
        self.save_presets()

    @property
    def parserlist(self):
        return [ 
            ( r"load_presets",              self.load_presets ),
            ( r"save_presets",              self.save_presets ),
            ( r"store_next_preset",         self.store_next_preset ),
            ( r"store_current_preset",      self.store_current_preset ),
            ( r"switch_to_preset_([0-%i])"%self.MAX_PRESETS,  self.switch_to_preset ),
            ( r"select_preset_([0-%i])"%self.MAX_PRESETS, self.select_preset ),
            ( r"clear_current_preset", self.clear_current_preset ),
        ]

    # DisplayPlugin methods
    def get_display_modes(self):
        return ['QUIKSHDR','NAV_QKSH']

    def show_plugin(self, display, display_mode):
        from tkinter import Text, END
        #super(DisplayPlugin).show_plugin(display, display_mode)
        display.display_text.insert(END, '{} \n'.format(display.body_title))
        display.display_text.insert(END, "ShaderQuickPresetPlugin!")

        #display.display_text.insert(END, "
        status = "\t Selected:"
        for i,preset in enumerate(self.presets):
            if i == self.selected_preset:
                status += "#"
            elif i == self.last_recalled:
                status += "/"
            elif preset is None or not preset:
                status += "_"
            else:
                status += "="
        display.display_text.insert(END, "\t[" + status + "]\n\n")

        # display a basic summary of each preset
        """for i,preset in enumerate(self.presets):
            display.display_text.insert(END, "%s\n" % preset.get_active_shader_names())
            #display.display_text.insert(END, "%s: %s %s %s" % """

        ## show a summary of the selected preset
        if self.selected_preset is not None:
            for line in self.presets[self.selected_preset].get_frame_summary():
                display.display_text.insert(END, "%s\n" % line)

    def store_next_preset(self):
        # find an empty slot
        res = [i for i, val in enumerate(self.presets) if val == None]
        if res is None or not res:
            # didnt find an empty slot, save to current
            self.store_current_preset()
            self.selected_preset += 1
            self.selected_preset %= self.MAX_PRESETS 
        else:
            # found an empty slot, save to it
            self.selected_preset = res[0]
            self.store_current_preset()

    def clear_current_preset(self):
        if self.selected_preset is None:
            return
        self.presets[self.selected_preset] = None

        self.save_presets()

    def store_current_preset(self):
        if self.selected_preset is None: self.selected_preset = 0

        insert_position = self.selected_preset
        self.presets[insert_position] = self.pc.fm.get_live_frame()
        #print ("stored %s at position %s" % (self.presets[insert_position], insert_position))
        self.selected_preset = insert_position
        self.last_recalled = insert_position

        self.save_presets()

    def select_preset(self, preset):
        self.selected_preset = preset

    def switch_to_preset(self, preset):
        #if preset>len(self.presets):
        if self.presets[preset] is None:
            print ("no quick shader preset in slot %s!" % preset)
            self.selected_preset = preset
            return
        print ("switching to preset %s" % preset)
        self.selected_preset = preset

        self.last_recalled = preset
        preset = self.presets[preset]

        print ("recalled preset %s" % preset)
        self.pc.fm.recall_frame(preset)

