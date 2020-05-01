import plugins


# from plugins.MidiFeedbackAPCKey25Plugin import MidiFeedbackAPCKey25Plugin

class MidiFeedbackLaunchpadPlugin(plugins.MidiFeedbackAPCKey25Plugin.MidiFeedbackAPCKey25Plugin):
    status = {}

    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)
        self.description = 'Outputs feedback to Novation Launchpad'

    def init_notes(self):
        self.NOTE_PLAY_SHADER = self.get_note('play_shader_0_0', 0)
        self.NOTE_SHADER_FEEDBACK = self.get_note('toggle_feedback', 85)
        self.NOTE_SCENE_LAUNCH_COLUMN = self.get_note('toggle_shader_layer_0', 82)
        self.NOTE_MODULATION_COLUMN = self.get_note('select_shader_modulation_slot_0', self.NOTE_SCENE_LAUNCH_COLUMN)
        self.NOTE_CAPTURE_PREVIEW = self.get_note('toggle_capture_preview', 86)
        self.NOTE_CLIP_STATUS_ROW = self.get_note('toggle_automation_clip_0', 8)
        self.NOTE_SHADER_PRESET_ROW = self.get_note('select_preset_0', 112)
        self.NOTE_SHADER_LAYER_ON = [
            self.get_note('toggle_shader_layer_%i' % i, 8 + (i * 16)) for i in range(0, 3)
        ]

    def supports_midi_feedback(self, device_name):
        supported_devices = ['Launchpad']
        for supported_device in supported_devices:
            if device_name.startswith(supported_device):
                return True

    def feedback_shader_on(self, layer, slot, colour=None):
        if colour is None:
            colour = self.COLOUR_GREEN
        self.set_status(note=(self.NOTE_PLAY_SHADER + (layer) * 16) + slot, velocity=int(colour))

    def feedback_shader_off(self, layer, slot):
        self.set_status(note=(self.NOTE_PLAY_SHADER + (layer) * 16) + slot, velocity=self.COLOUR_OFF)

    # TODO: make these colours correct+sensible
    BLINK = 1
    COLOUR_OFF = 0
    COLOUR_GREEN = 8  # 1
    COLOUR_GREEN_BLINK = 15
    COLOUR_RED = 32
    COLOUR_RED_BLINK = 47
    COLOUR_AMBER = 64
    COLOUR_AMBER_BLINK = 80
