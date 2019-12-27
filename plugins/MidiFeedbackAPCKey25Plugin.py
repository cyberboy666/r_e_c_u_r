from data_centre import plugin_collection
from data_centre.plugin_collection import MidiFeedbackPlugin
import mido

class MidiFeedbackAPCKey25Plugin(MidiFeedbackPlugin):

    status = {}

    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)
        self.description = 'Outputs feedback to APC Key 25'

    def supports_midi_feedback(self, device_name):
        supported_devices = ['APC Key 25']
        for supported_device in supported_devices:
            if device_name.startswith(supported_device):
                return True

    def set_status(self, command='note_on', note=None, velocity=None):
        self.status[note] = {
                'command': command,
                'note': note,
                'velocity': velocity
        }
        #print("set status to %s: %s" % (note, self.status[note]))

    def send_command(self, command='note_on', note=None, velocity=None):
        #print("send_command(%s, %s)" % (note, velocity))
        self.midi_feedback_device.send(
            mido.Message(command, note=note, velocity=velocity)
        )

    def feedback_shader_feedback(self, on):
        self.set_status(note=85, velocity=int(on))

    def feedback_capture_preview(self, on):
        self.set_status(note=86, velocity=int(on))

    def feedback_shader_on(self, layer, slot, colour=127):
        self.set_status(note=(32-(layer)*8)+slot, velocity=int(colour))

    def feedback_shader_off(self, layer, slot):
        self.set_status(note=(32-(layer)*8)+slot, velocity=self.COLOUR_OFF)

    def feedback_shader_layer_on(self, layer):
        self.set_status(note=82+layer, velocity=127)
        
    def feedback_shader_layer_off(self, layer):
        self.set_status(note=82+layer, velocity=self.COLOUR_OFF)

    def feedback_show_layer(self, layer):
        self.set_status(note=70, velocity=layer)

    def feedback_plugin_status(self):
        from data_centre.plugin_collection import SequencePlugin

        from plugins.MidiActionsTestPlugin import MidiActionsTestPlugin
        from plugins.ShaderLoopRecordPlugin import ShaderLoopRecordPlugin
        for plugin in self.pc.get_plugins(SequencePlugin):
            if isinstance(plugin, ShaderLoopRecordPlugin): #MidiActionsTestPlugin):

                NOTE_PLAY_STATUS = 65
                NOTE_RECORD_STATUS = 66 
                NOTE_OVERDUB_STATUS = 67
                NOTE_CLIP_STATUS_ROW = 8

                colour = self.COLOUR_OFF
                if plugin.is_playing():
                    colour = self.COLOUR_GREEN
                    if plugin.is_paused():
                        colour += self.BLINK
                self.set_status(command='note_on', note=NOTE_PLAY_STATUS, velocity=colour)

                colour = self.COLOUR_OFF
                if plugin.recording:
                    colour = self.COLOUR_GREEN
                    if plugin.is_ignoring():
                       colour += self.BLINK
                self.set_status(command='note_on', note=NOTE_RECORD_STATUS, velocity=colour)

                colour = self.COLOUR_OFF
                if plugin.overdub:
                    colour = self.COLOUR_RED
                    if plugin.is_paused() or plugin.is_ignoring():
                        colour += self.BLINK
                self.set_status(command='note_on', note=NOTE_OVERDUB_STATUS, velocity=colour)

                for i in range(plugin.MAX_CLIPS):
                    if i in plugin.running_clips:
                        if plugin.is_playing() and not plugin.is_paused():
                            colour = self.COLOUR_GREEN
                        else:
                            colour = self.COLOUR_AMBER
                        if plugin.selected_clip==i: #blink if selected
                            colour += self.BLINK
                    elif plugin.selected_clip==i:
                        colour = self.COLOUR_RED_BLINK
                    else:
                        colour = self.COLOUR_OFF
                    self.set_status(command='note_on', note=NOTE_CLIP_STATUS_ROW+i, velocity=colour)
 

        from plugins.ShaderQuickPresetPlugin import ShaderQuickPresetPlugin
        #print ("feedback_plugin_status")
        for plugin in self.pc.get_plugins(ShaderQuickPresetPlugin):
            #print ("for plugin %s" % plugin)
            for pad in range(0,8):
                #print ("checking selected_preset %s vs pad %s" % (plugin.selected_preset, pad))
                colour = self.COLOUR_OFF
                if plugin.presets[pad] is not None:
                    colour = self.COLOUR_AMBER
                    if plugin.last_recalled==pad:
                        colour = self.COLOUR_GREEN
                if plugin.selected_preset==pad:
                    if plugin.presets[pad] is None:
                        colour = self.COLOUR_RED
                    colour += self.BLINK
                self.set_status(command='note_on', note=pad, velocity=colour)

    BLINK = 1
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

        if self.pc.message_handler.actions.display.capture.is_previewing:
            self.feedback_capture_preview(self.COLOUR_GREEN)
        else:
            self.feedback_capture_preview(self.COLOUR_OFF)

        self.feedback_plugin_status()

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

        self.update_device()

        #print("refresh_midi_feedback")

    last_state = None
    def update_device(self):
        from copy import deepcopy
        print("in update device status is %s" % self.status)
        for i,c in self.status.items():
            #'print("comparing\n%s to\n%s" % (c, self.last_state[i]))
            if self.last_state is None or self.last_state[i]!=c:
                print("got command: %s: %s" % (i,c))
                self.send_command(**c)
        self.last_state = deepcopy(self.status)
