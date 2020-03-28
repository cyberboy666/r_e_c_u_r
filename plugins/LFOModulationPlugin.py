import math
import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin, SequencePlugin, DisplayPlugin, AutomationSourcePlugin

class LFOModulationPlugin(ActionsPlugin,SequencePlugin,DisplayPlugin, AutomationSourcePlugin):

    MAX_LFOS = 4

    PRESET_FILE_NAME = "LFOModulationPlugin/config.json"
    presets = {}

    # active = True (toggle_lfo_active) to enable sending of modulation
    active = False

    # for keeping track of LFO levels
    level = [0.0]*MAX_LFOS
    speed = 0.5

    # TODO: enable assigning of LFOs to mod slots
    # with combination/averaging...
    # needs UI to control it and [ [ 0.0 ] * 4 ] * 4 to handle the mappings?
    # currently each LFO maps directly to mod slot

    stop_flag = False
    pause_flag = False
    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

        #self.PRESET_FILE_NAME = "ShaderLoopRecordPlugin/frames.json"
        self.presets = self.load_presets()
        self.level = self.presets.get('levels', [0.0]*self.MAX_LFOS).copy()
        self.active = self.presets.get('active', False)
        self.set_lfo_speed_direct(self.presets.get('speed', self.speed))

        self.pc.shaders.root.after(1000, self.start_plugin)
        
    def start_plugin(self):
        super().start_plugin()
        self.pc.shaders.root.after(0, self.run_automation)

    def stop_plugin(self):
        super().stop_plugin()
        self.save_presets()

    def load_presets(self):
        print("trying load presets? %s " % self.PRESET_FILE_NAME)
        return self.pc.read_json(self.PRESET_FILE_NAME) or { 'levels': [0.0]*self.MAX_LFOS, 'active': self.active }

    def save_presets(self):
        #for cmd,struct in self.commands.items():
        #    self.presets.setdefault('modulation_levels',{})[cmd] = struct.get('modulation',[{},{},{},{}])
        self.pc.update_json(self.PRESET_FILE_NAME, { 'levels': self.level.copy(), 'active': self.active, 'speed': self.speed } )

    # DisplayPlugin methods
    def get_display_modes(self):
        return ['LFOMODU','NAV_LFO']

    def show_plugin(self, display, display_mode):
        from tkinter import Text, END
        #super(DisplayPlugin).show_plugin(display, display_mode)
        display.display_text.insert(END, '{} \n'.format(display.body_title))
        display.display_text.insert(END, "LFOModulation is ")

        display.display_text.insert(END, "ACTIVE" if self.active else "not active")

        display.display_text.insert(END, "\tSpeed: {:4.1f}% {}\n\n".format(self.speed*100, display.get_speed_indicator(self.speed/2.0, convert=False)))

        for lfo,value in enumerate(self.level):
            display.display_text.insert(END, "lfo {} level: {:4.2f}% {}\t".format(lfo,value*100,display.get_bar(value)))
            display.display_text.insert(END, "{}\t{}\n".format(self.last_lfo_status[lfo], display.get_bar(self.last_lfo_value[lfo])))
            display.display_text.insert(END, "\tslot %s\t%s\n" % (display.get_mod_slot_label(lfo), self.formula[lfo]))

        display.display_text.insert(END, "\n")

    # AutomationSourcePlugin methods
    # methods/vars for AutomationSourcePlugin
    # a lot of the nitty-gritty handled in parent class, these are for interfacing to the plugin
    def get_frame_data(self):
        diff = { 'levels': self.level.copy(), 'speed': self.speed, 'active': self.active }
        #self.last_record = {}
        #print(">>> reporting frame data for rec\n\t%s" % diff)
        return diff

    def recall_frame_data(self, data):
        if data is None:
            return
        # print(">>>>recall from data:\n\t%s\n" %data)
        if data.get('levels') is not None:
            for slot,level in enumerate(data.get('levels')):
                self.set_lfo_modulation_level(slot, level)
        if data.get('active') is not None:
            self.active = data.get('active')
        if data.get('speed') is not None:
            self.set_lfo_speed_direct(data.get('speed'))

    def get_frame_summary(self, data):
        line = ""
        if data.get('levels') is not None:
            line += "LFO levels ["
            for i in range(4):
                line += self.pc.display.get_bar(data['levels'][i])
            line += "] "
        if data.get('active') is not None:
            line += "active " if data.get('active') else 'inactive '
        if data.get('speed') is not None:
            line += self.pc.display.get_speed_indicator(data.get('speed'))
        #print ("returning %s from %s" %(line, data))
        return line

    # ActionsPlugin methods
    @property
    def parserlist(self):
        return [ 
                ( r"^set_lfo_modulation_([0-3])_level$", self.set_lfo_modulation_level ),
                ( r"^toggle_lfo_active$", self.toggle_lfo_active ),
                ( r"^set_lfo_speed", self.set_lfo_speed )
                # TODO: changing formulas and LFO modes, speed
        ]

    def set_lfo_modulation_level(self, slot, value):
        self.level[slot] = value

    def set_lfo_speed(self, speed):
        self.set_lfo_speed_direct(-4*(0.5-(speed)))

    def set_lfo_speed_direct(self, speed):
        self.speed = speed

    def toggle_lfo_active(self):
        self.active = not self.active
        self.save_presets()

    # Formula handling for generating automation
    # mapping 0-3 to match the LFO 
    # TODO: save & load this to config file, make editable
    formula = [
            "f_sin",
            "f_double_cos",
            "f_invert_sin",
            #"f_invert_double_cos",
            "f_linear"
    ]

    # run the formula for the stored lfo configuration
    last_lfo_status = [None]*MAX_LFOS # for displaying status
    last_lfo_value = [None]*MAX_LFOS
    #lfo_speed = [1.0]*MAX_LFOS
    def getLFO(self, position, lfo):
        lfo_value = getattr(self,self.formula[lfo])(position, self.level[lfo])
        self.last_lfo_value[lfo] = lfo_value
        self.last_lfo_status[lfo] = "sent {:03.1f}%".format(lfo_value*100.0)
        return lfo_value

    # built-in waveshapes
    # outgoing values should be between 0 and 1!!
    # todo: more of the these, and better!
    def f_sin(self, position, level):
        #return level * (( math.sin(position*math.pi)))
        value = math.sin(position * math.pi * 2) / 2
        value *= level
        value += 0.5 # normalise to range 0 - 1

        return value

    def f_invert_sin(self, position, level):
        return 1.0 - self.f_sin(position, level)

    def f_double_cos(self, position, level):
        return self.f_sin(math.cos(position*math.pi), level)

    def f_invert_double_cos(self, position, level):
        return 1.0 - self.f_double_cos(position, level)

    def f_linear(self, position, level):
        return position * level

    # SequencePlugin methods
    def run_sequence(self, position):
        import time
        now = time.time()

        if self.pc.data.plugins is None: # not initialised yet
            return

        if not self.active: # output is disabled
            return

        for lfo in range(0,self.MAX_LFOS):
            # TODO: this is where would use assignable amounts and average across multiple inputs
            if self.level[lfo]>0.0:
                self.pc.actions.call_method_name(
                        "modulate_param_%s_to_amount_continuous"%lfo, 
                        self.getLFO(position, lfo)
                )
