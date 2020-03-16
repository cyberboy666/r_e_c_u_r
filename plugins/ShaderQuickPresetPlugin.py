import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin, SequencePlugin, DisplayPlugin
import copy
from plugins.frame_manager import Frame

class ShaderQuickPresetPlugin(ActionsPlugin,DisplayPlugin): #,SequencePlugin):

    MAX_PRESETS = 8
    display_live_on = False

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
            ( r"qksh_toggle_display_live",  self.toggle_display_live ),
            ( r"switch_to_next_preset",     self.switch_to_next_preset ),
            ( r"switch_to_previous_preset", self.switch_to_previous_preset ),
            ( r"switch_to_current_preset",  self.switch_to_current_preset ),
            ( r"select_previous_preset",    self.select_previous_preset ),
            ( r"select_next_preset",    self.select_next_preset ),
        ]

    def toggle_display_live(self):
        self.display_live_on = not self.display_live_on

    # DisplayPlugin methods
    def get_display_modes(self):
        return ['QUIKSHDR',['NAV_QKSH','PLAY_SHADER']]

    def show_plugin(self, display, display_mode):
        from tkinter import Text, END
        #super(DisplayPlugin).show_plugin(display, display_mode)
        display.display_text.insert(END, '{} \n'.format(display.body_title))
        display.display_text.insert(END, "ShaderQuickPresetPlugin")

        status = "Selected: ["
        #for i,preset in enumerate(self.presets):
        for i in range(self.MAX_PRESETS):
            preset = self.presets[i]
            if i == self.selected_preset:
                status += "#"
            elif i == self.last_recalled:
                status += "/"
            elif preset is None or not preset:
                status += "_"
            else:
                status += "="
        display.display_text.insert(END, "" + status + "]\n")

        # display a basic summary of each preset
        """for i,preset in enumerate(self.presets):
            display.display_text.insert(END, "%s\n" % preset.get_active_shader_names())
            #display.display_text.insert(END, "%s: %s %s %s" % """

        if self.display_live_on:
            display.display_text.insert(END, "Showing LIVE preview\n")
        else:
            display.display_text.insert(END, "Showing stored preset slot %s" % self.selected_preset)
            if self.selected_preset==self.last_recalled:
                display.display_text.insert(END, " [last switched]")
            display.display_text.insert(END, "\n")

        ## show a summary of the selected preset
        if self.selected_preset is not None:
            # TODO: switch to display current settings
            #for line in self.pc.fm.get_live_frame().get_frame_summary():
            for line in (self.presets[self.selected_preset] if not self.display_live_on else self.pc.fm.get_live_frame()).get_frame_summary():
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
            self.message_handler.set_message('ERROR',"No quick shader preset in slot %s!" % preset)
            self.selected_preset = preset
            return
        print ("switching to preset %s" % preset)
        self.selected_preset = preset

        self.last_recalled = preset
        preset = self.presets[preset]

        print ("recalled preset %s" % preset)
        self.pc.fm.recall_frame(preset)

    def switch_to_current_preset(self):
        if self.selected_preset is not None:
            self.switch_to_preset(self.selected_preset)

    def switch_to_previous_preset(self):
        self.select_previous_preset()
        self.switch_to_current_preset()

    def switch_to_next_preset(self):
        self.select_next_preset()
        self.switch_to_current_preset()

    def select_next_preset(self):
        if self.selected_preset is None:
            self.selected_preset = 0
            return
        self.selected_preset += 1
        if self.selected_preset>=self.MAX_PRESETS:
            self.selected_preset = 0

    def select_previous_preset(self):
        if self.selected_preset is None:
            self.selected_preset = self.MAX_PRESETS
            return
        self.selected_preset -= 1
        if self.selected_preset<0:
            self.selected_preset = self.MAX_PRESETS-1
        


