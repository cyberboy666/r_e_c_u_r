import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin, SequencePlugin

class MidiActionsTestPlugin(ActionsPlugin,SequencePlugin):
    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

    @property
    def parserlist(self):
        return [ 
                ( r"test_plugin", self.test_plugin ),
                ( r"cycle_shaders", self.cycle_shaders ),
                ( r"run_automation",  self.run_automation ),
                ( r"stop_automation", self.stop_automation ),
                ( r"toggle_pause_automation", self.toggle_pause_automation ),
                ( r"pause_automation", self.pause_automation ),
        ]

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

    duration = 5000
    frequency = 50
    def run_sequence(self, position):
        self.pc.midi_input.call_method_name(
                "set_the_shader_param_0_layer_offset_0_continuous", position
        )

        self.pc.midi_input.call_method_name(
                "set_the_shader_param_1_layer_offset_0_continuous", position
        )

