import data_centre.plugin_collection
from data_centre.plugin_collection import MidiActionsPlugin

class MidiActionsTestPlugin(MidiActionsPlugin):
    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

    @property
    def parserlist(self):
        return {
                ( r"test_plugin", self.test_plugin ),
                ( r"cycle_shaders", self.cycle_shaders ),
                ( r"run_automation", self.run_automation )
        }

    def test_plugin(self):
        print ("TEST PLUGIN test_plugin CALLED!!")
        # can now access various parts of recur via self.pc

    cycle_count = 0
    def cycle_shaders(self):
        print ("Cycle shaders!!!")
        if self.cycle_count>9:
            self.cycle_count = 0

        for i,shader in enumerate(self.pc.message_handler.shaders.selected_shader_list):
            self.pc.midi_input.call_method_name(
                "play_shader_%s_%s" % (i, self.cycle_count), None
            )
            self.pc.midi_input.call_method_name(
                "start_shader_layer_%s" % i, None
            )
        self.cycle_count += 1



    automation_start = None
    duration = 2000
    frequency = 100
    def run_automation(self):
        import time
        import math
        if not self.automation_start:
            self.automation_start = time.time()

        passed = time.time() - self.automation_start
        position = passed / self.duration*1000

        #print("%s: position is %s" % (passed,position))

        print("running automation at %s!" % position)

        self.pc.midi_input.call_method_name(
                "set_the_shader_param_0_layer_offset_0_continuous", position
        )

        self.pc.midi_input.call_method_name(
                "set_the_shader_param_1_layer_offset_0_continuous", position
        )

        if time.time() - self.automation_start < self.duration/1000:
            self.pc.midi_input.root.after(self.frequency, self.run_automation)
        else:
            self.automation_start = None
