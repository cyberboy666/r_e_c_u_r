import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin, SequencePlugin, DisplayPlugin
from plugins.frame_manager import Frame

class LFOModulationPlugin(ActionsPlugin,SequencePlugin,DisplayPlugin):
    disabled = False

    stop_flat = True
    pause_flag = False
    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

        #self.PRESET_FILE_NAME = "ShaderLoopRecordPlugin/frames.json"

        self.pc.shaders.root.after(1000, self.run_automation)

    def get_display_modes(self):
        return ['LFOMODU','NAV_LFO']

    def show_plugin(self, display, display_mode):
        from tkinter import Text, END
        #super(DisplayPlugin).show_plugin(display, display_mode)
        display.display_text.insert(END, '{} \n'.format(display.body_title))
        display.display_text.insert(END, "test from LFOModulationPlugin!\n")

    @property
    def parserlist(self):
        return [ ]
        """( r"run_automation",  self.run_automation ),
                ( r"stop_automation", self.stop_automation ),
                ( r"toggle_pause_automation", self.toggle_pause_automation ),
                ( r"pause_automation", self.pause_automation ),"""

    def run_sequence(self, position):
        import time
        now = time.time()

        if self.pc.data.plugins is None:
            return

        print("run_automation position %s!"%position)

        import math
        self.pc.actions.call_method_name("modulate_param_0_to_amount_continuous", math.sin(position*math.pi)) #(now*100)%300)
        self.pc.actions.call_method_name("modulate_param_1_to_amount_continuous", math.cos(position*math.pi)/math.pi)
        self.pc.actions.call_method_name("modulate_param_2_to_amount_continuous", math.atan(position*math.pi)/math.pi)
        self.pc.actions.call_method_name("modulate_param_3_to_amount_continuous", math.sin(math.sin(position*math.pi)*math.pi))
