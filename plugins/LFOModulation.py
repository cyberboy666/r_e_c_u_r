import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin, SequencePlugin, DisplayPlugin
from plugins.frame_manager import Frame

class LFOModulationPlugin(ActionsPlugin,SequencePlugin,DisplayPlugin):
    disabled = False

    active = False

    level = [0.0, 0.0, 0.0, 0.0]

    stop_flag = False
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

        display.display_text.insert(END, "\tACTIVE\n" if self.active else "not active\n")

        for i,value in enumerate(self.level):
            display.display_text.insert(END, "{} level: {:03.2f}%\n".format(i,value))

    @property
    def parserlist(self):
        return [ 
                ( r"^set_lfo_modulation_([0-3])_level$", self.set_lfo_modulation_level ),
                ( r"^toggle_lfo_active$", self.toggle_lfo_active )
        ]

    def set_lfo_modulation_level(self, slot, value):
        self.level[slot] = value

    def toggle_lfo_active(self):
        self.active = not self.active

    def run_sequence(self, position):
        import time
        now = time.time()

        if self.pc.data.plugins is None:
            return

        if not self.active:
            return
        #print("run_automation position %s!"%position)

        import math
        self.pc.actions.call_method_name("modulate_param_0_to_amount_continuous", 0.5+(0.5*self.level[0] * math.sin(position*math.pi))) #(now*100)%300)
        self.pc.actions.call_method_name("modulate_param_1_to_amount_continuous", 0.5+(0.5*self.level[1] * math.cos(position*math.pi)/math.pi))
        self.pc.actions.call_method_name("modulate_param_2_to_amount_continuous", 0.5+(0.5*self.level[2] * math.atan(position*math.pi)/math.pi))
        self.pc.actions.call_method_name("modulate_param_3_to_amount_continuous", 0.5+(0.5*self.level[3] * math.sin(math.sin(position*math.pi)*math.pi)))
