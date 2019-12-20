import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin, SequencePlugin

class ShaderLoopRecordPlugin(ActionsPlugin,SequencePlugin):
    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

        self.PRESET_FILE_NAME = "ShaderLoopRecordPlugin/frames.json"

        self.frames = self.load_presets()

    def load_presets(self):
        #try:
        print("trying load presets? %s " % self.PRESET_FILE_NAME)
        return self.pc.read_json(self.PRESET_FILE_NAME) or self.clear_frames()
        #except:
        #    return self.clear_frames()

    def save_presets(self):
        self.pc.update_json(self.PRESET_FILE_NAME, self.frames)


    @property
    def parserlist(self):
        return [
                ( r"run_automation",  self.run_automation ),
                ( r"stop_automation", self.stop_automation ),
                ( r"toggle_pause_automation", self.toggle_pause_automation ),
                ( r"pause_automation", self.pause_automation ),
                ( r"toggle_loop_automation", self.toggle_loop_automation ),
                ( r"toggle_record_automation", self.toggle_record_automation ),
                ( r"toggle_overdub_automation", self.toggle_overdub_automation ),
        ]

    def toggle_overdub_automation(self):
        self.overdub = not self.overdub

    def toggle_record_automation(self):
        self.recording = not self.recording
        if self.recording and not self.overdub:
            self.clear_frames()
        if not self.recording:
            self.last_frame = None
            self.save_presets()

    def clear_frames(self):
        self.frames = [{}] * (int(self.duration / self.frequency))
        return self.frames

    duration = 5000
    frequency = 25 
    recording = False
    overdub = True
    last_frame = None
    def run_sequence(self, position):
        current_frame_index = int(position * 100)

        current_frame = self.get_live_frame()

        if not self.recording or self.overdub:
            self.recall_frame(current_frame_index)
        if self.recording:
            if not self.last_frame: 
                self.last_frame = current_frame
            diff = self.get_frame_diff(self.last_frame,current_frame)
            if self.overdub and self.frames[current_frame_index]:
                diff = self.merge_frames(self.frames[current_frame_index], diff)
            self.frames[current_frame_index] = diff #self.get_frame_diff(self.last_frame,current_frame)
            self.last_frame = self.get_live_frame()

    # overlay frame2 on frame1
    def merge_frames(self, frame1, frame2):
        from copy import deepcopy
        f = deepcopy(frame1) #frame1.copy()
        """print("got frame1 %s" % frame1)
        print("got frame2 %s" % frame2)
        print("got f %s" % f)"""
        for i,f2 in enumerate(frame2['shader_params']):
            for i2,p in enumerate(f2):
                if p is not None:
                    f['shader_params'][i][i2] = p
        return f

    def get_frame_diff(self, last_frame, current_frame):
        if not last_frame: return current_frame

        values = [[None]*4]*3 # 3 shader layers, 4 params
        #print (current_frame.get('shader_params'))
        for i,n in enumerate(last_frame.get('shader_params')):
            for i2,p in enumerate(n):
                if p != current_frame.get('shader_params')[i][i2]:
                    values[i][i2] = p

        if last_frame['feedback_active'] != current_frame['feedback_active']:
            feedback_active = current_frame['feedback_active']
        else:
            feedback_active = None

        diff = { 'shader_params': values, 'feedback_active': feedback_active }
                    
        return diff


    def get_live_frame(self):
        from plugins.ShaderQuickPresetPlugin import ShaderQuickPresetPlugin
        return self.pc.get_plugins(ShaderQuickPresetPlugin)[0].get_live_frame()

    def recall_frame(self, index):
        from plugins.ShaderQuickPresetPlugin import ShaderQuickPresetPlugin
        self.pc.get_plugins(ShaderQuickPresetPlugin)[0].recall_frame_params(self.frames[index])

