import math
import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin, SequencePlugin, DisplayPlugin

class LFOModulationPlugin(ActionsPlugin,SequencePlugin,DisplayPlugin):
    disabled = False

    MAX_LFOS = 4

    # active = True (toggle_lfo_active) to enable sending of modulation
    active = False

    # for keeping track of LFO levels
    level = [0.0]*MAX_LFOS #, 0.0, 0.0, 0.0]

    stop_flag = False
    pause_flag = False
    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

        #self.PRESET_FILE_NAME = "ShaderLoopRecordPlugin/frames.json"

        self.pc.shaders.root.after(1000, self.run_automation)


    # DisplayPlugin methods
    def get_display_modes(self):
        return ['LFOMODU','NAV_LFO']

    def show_plugin(self, display, display_mode):
        from tkinter import Text, END
        #super(DisplayPlugin).show_plugin(display, display_mode)
        display.display_text.insert(END, '{} \n'.format(display.body_title))
        display.display_text.insert(END, "LFOModulationPlugin ")

        display.display_text.insert(END, "ACTIVE\n\n" if self.active else "not active\n\n")

        for lfo,value in enumerate(self.level):
            display.display_text.insert(END, "lfo {} level: {:03.2f}%\t".format(lfo,value))
            display.display_text.insert(END, "%s\n" %self.last_lfo_status[lfo])
            display.display_text.insert(END, "\t%s\n" % self.formula[lfo])


    # ActionsPlugin methods
    @property
    def parserlist(self):
        return [ 
                ( r"^set_lfo_modulation_([0-3])_level$", self.set_lfo_modulation_level ),
                ( r"^toggle_lfo_active$", self.toggle_lfo_active )
                # TODO: changing formulas and LFO modes, speed
        ]

    def set_lfo_modulation_level(self, slot, value):
        self.level[slot] = value

    def toggle_lfo_active(self):
        self.active = not self.active

    # Formula handling for generating automation
    # mapping 0-3 to match the LFO 
    # TODO: save & load this to config file, make editable
    formula = [
            "f_sin",
            "f_inverted_sin",
            "f_sin",
            "f_inverted_sin"
    ]

    # run the formula for the stored lfo configuration
    last_lfo_status = [None]*MAX_LFOS # for displaying status
    def getLFO(self, position, lfo):
        lfo_value = getattr(self,self.formula[lfo])(position, self.level[lfo])
        self.last_lfo_status[lfo] = " output {:03.2f}\tat T{:03.2f}".format(lfo_value*100.0, position)
        return lfo_value

    # built-in waveshapes
    # todo: more of the these, and better!
    def f_sin(self, position, level):
        return 0.5+(0.5*level * math.sin(position*math.pi))

    def f_inverted_sin(self, position, level):
        return self.f_sin(1.0-position, 1.0-level)

    # SequencePlugin methods
    def run_sequence(self, position):
        import time
        now = time.time()

        if self.pc.data.plugins is None:
            return

        if not self.active:
            return

        for i in range(0,4):
            self.pc.actions.call_method_name("modulate_param_%s_to_amount_continuous"%i, self.getLFO(position, i))
