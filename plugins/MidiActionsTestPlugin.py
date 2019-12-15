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
            #self.pc.midi_input.run_action_for_mapped_message(
            self.pc.midi_input.call_method_name(
                "play_shader_%s_%s" % (i, self.cycle_count), None
            )
            self.pc.midi_input.call_method_name(
                "start_shader_layer_%s" % i, None
            )
        self.cycle_count += 1
                
