from data_centre import plugin_collection
from data_centre.plugin_collection import MidiFeedbackPlugin
import mido

class MidiFeedbackAPCKey25Plugin(MidiFeedbackPlugin):

    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)
        self.description = 'Outputs feedback to APC Key 25'

    def supports_midi_feedback(self, device_name):
        supported_devices = ['APC Key 25']
        for supported_device in supported_devices:
            if device_name.startswith(supported_device):
                return True

    def feedback_shader_feedback(self, on):
        self.midi_feedback_device.send(
                mido.Message('note_on', note=85, velocity=int(on))
        )

    def feedback_capture_preview(self, on):
        self.midi_feedback_device.send(
                mido.Message('note_on', note=86, velocity=int(on))
        )

    def feedback_shader_on(self, layer, slot, colour=127):
        self.midi_feedback_device.send(
                mido.Message('note_on', note=(32-(layer)*8)+slot, velocity=int(colour))
        )

    def feedback_shader_off(self, layer, slot):
        self.midi_feedback_device.send(
                mido.Message('note_on', note=(32-(layer)*8)+slot, velocity=self.COLOUR_OFF)
        )

    def feedback_shader_layer_on(self, layer):
        self.midi_feedback_device.send(
                mido.Message('note_on', note=82+layer, velocity=127)
        )
    def feedback_shader_layer_off(self, layer):
        self.midi_feedback_device.send(
                mido.Message('note_on', note=82+layer, velocity=self.COLOUR_OFF)
        )

    def feedback_show_layer(self, layer):
        self.midi_feedback_device.send(
            mido.Message('note_on', note=70, velocity=layer)
        )

    COLOUR_OFF = 0
    COLOUR_GREEN = 1
    COLOUR_GREEN_BLINK = 2
    COLOUR_RED = 3
    COLOUR_RED_BLINK = 4
    COLOUR_AMBER = 5
    COLOUR_AMBER_BLINK = 6

    def refresh_midi_feedback(self):

        # show which layer is selected
        self.feedback_show_layer(self.pc.data.shader_layer)

        # show if internal feedback (the shader layer kind) is enabled
        if self.pc.data.feedback_active and not self.pc.data.function_on:
            self.feedback_shader_feedback(self.COLOUR_GREEN)
        elif self.pc.data.settings['shader']['X3_AS_SPEED']['value'] == 'enabled' and self.pc.data.function_on:
            self.feedback_shader_feedback(self.COLOUR_GREEN_BLINK)
        else:
            self.feedback_shader_feedback(self.COLOUR_OFF)

        if self.pc.message_handler.actions.python_capture.is_previewing:
            self.feedback_capture_preview(self.COLOUR_GREEN)
        else:
            self.feedback_capture_preview(self.COLOUR_OFF)

        for n,shader in enumerate(self.pc.message_handler.shaders.selected_shader_list):
            #print ("%s: in refresh_midi_feedback, got shader: %s" % (n,shader))
            # show if layer is running or not
            if self.pc.message_handler.shaders.selected_status_list[n] == '▶':
                self.feedback_shader_layer_on(n)
            else:
                self.feedback_shader_layer_off(n)
            for x in range(0,8):
                if 'slot' in shader and shader.get('slot',None)==x:
                    if self.pc.message_handler.shaders.selected_status_list[n] == '▶':
                        # show that slot is selected and running
                        self.feedback_shader_on(n, x, self.COLOUR_GREEN)
                    else:
                        # show that slot is selected but not running
                        self.feedback_shader_on(n, x, self.COLOUR_AMBER_BLINK)
                elif self.pc.data.shader_bank_data[n][x]['path']:
                    # show that slot is full but not selected
                    self.feedback_shader_on(n, x, self.COLOUR_AMBER)
                else:
                    # hos that nothing in slot
                    self.feedback_shader_off(n, x)

        #print("refresh_midi_feedback")

        #if self.data.settings['user_input']['MIDI_INPUT']['value'] == self.midi_setting and self.data.midi_port_index == self.port_index:
        #  if self.supports_midi_feedback(self.data.midi_device_name):
        #    self.root.after(self.midi_delay*5, self.refresh_midi_feedback)

