import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin, SequencePlugin

class ShaderLoopRecordPlugin(ActionsPlugin,SequencePlugin):
    DEBUG_FRAMES = False
    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

        self.PRESET_FILE_NAME = "ShaderLoopRecordPlugin/frames.json"

        self.frames = self.load_presets()
        self.reset_ignored()

    def load_presets(self):
        #try:
        print("trying load presets? %s " % self.PRESET_FILE_NAME)
        p = self.pc.read_json(self.PRESET_FILE_NAME)
        if p and len(p)<(int(self.duration / self.frequency)):
            print("adding more slots due to size change")
            p += [None]*((int(self.duration / self.frequency))-len(p))
            print("len is now %s" % len(p))
            return p
        elif p:
            return p
        else:
            return self.clear_frames()
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
                ( r"clear_automation", self.clear_frames ),
        ]

    def toggle_overdub_automation(self):
        self.overdub = not self.overdub
        if not self.overdub:
            self.reset_ignored()

    def toggle_record_automation(self):
        self.recording = not self.recording
        if self.recording and not self.overdub:
            self.clear_frames()
        if not self.recording:
            self.reset_ignored()
            self.last_frame = None
            self.save_presets()

    def clear_frames(self):
        self.frames = [{}] * (int(self.duration / self.frequency))
        if self.DEBUG_FRAMES: print ("clear_frames set to %s" % (int(self.duration / self.frequency)))
        return self.frames

    def reset_ignored(self):
        self.ignored = { 'shader_params': [[None]*4,[None]*4,[None]*4] }

    duration = 2000
    frequency = 25 
    recording = False
    overdub = True
    last_frame = None
    def run_sequence(self, position):
        if self.DEBUG_FRAMES: print (">>>>>>>>>>>>>>frame at %s" % position)
        current_frame_index = int(position * (int(self.duration / self.frequency)))
        #print("got frame index %s" % current_frame_index)

        current_frame = self.pc.shaders.get_live_frame().copy()
        if self.DEBUG_FRAMES: print("current_frame copy before recall is %s" % current_frame['shader_params'])

        if not self.recording:
            #pass
            self.recall_frame_index(current_frame_index)
        #if self.overdub:
        #    self.recall_frame(current_frame_index,ignored = self.last_frame
        if self.recording:
            if not self.last_frame: 
                self.last_frame = current_frame
            if self.DEBUG_FRAMES: print("pre-diff frame is %s" % current_frame['shader_params'])
            diff = self.get_frame_diff(self.last_frame,current_frame)
            if self.DEBUG_FRAMES: print("diffed frame is %s" % diff['shader_params'])
            if self.overdub and self.frames[current_frame_index]:
                self.ignored = self.merge_frames(self.ignored, diff)
                self.recall_frame_index(current_frame_index, ignored = self.ignored)
                #self.ignored = self.merge_frames(self.ignored, diff)
                diff = self.merge_frames(self.frames[current_frame_index], diff)
                if self.DEBUG_FRAMES:  print("after diff2 is: %s" % diff['shader_params'])
            self.frames[current_frame_index] = diff #self.get_frame_diff(self.last_frame,current_frame)
            self.last_frame = self.pc.shaders.get_live_frame()
        if self.DEBUG_FRAMES:  print("<<<<<<<<<<<<<< frame at %s" % position)

    # overlay frame2 on frame1
    def merge_frames(self, frame1, frame2):
        from copy import deepcopy
        f = deepcopy(frame1) #frame1.copy()
        if self.DEBUG_FRAMES:  print("merge_frames: got frame1 %s" % frame1)
        if self.DEBUG_FRAMES:  print("merge_frames: got frame2 %s" % frame2)
        for i,f2 in enumerate(frame2['shader_params']):
            for i2,p in enumerate(f2):
                if p is not None:
                    f['shader_params'][i][i2] = p
        if self.DEBUG_FRAMES:  print("merge_frames: got f %s" % f)
        return f

    def get_frame_diff(self, last_frame, current_frame):
        if not last_frame: return current_frame

        if self.DEBUG_FRAMES:
            print("get_frame_diff>>>>")
            print("last_frame: \t%s" % last_frame['shader_params'])
            print("current_frame: \t%s" % current_frame['shader_params'])

        #values = [[None]*4]*3 # 3 shader layers, 4 params
        values = [[None]*4,[None]*4,[None]*4]
        #print (current_frame.get('shader_params'))
        for layer,params in enumerate(last_frame.get('shader_params',[[None]*4]*3)):
            if self.DEBUG_FRAMES:  print("got layer %s params: %s" % (layer, params))
            for param,p in enumerate(params):
                if p is not None and p != current_frame.get('shader_params')[layer][param]:
                    if self.DEBUG_FRAMES: print("setting layer %s param %s to %s" % (layer,param,p))
                    values[layer][param] = p

        if last_frame['feedback_active'] != current_frame['feedback_active']:
            feedback_active = current_frame['feedback_active']
        else:
            feedback_active = None

        if self.DEBUG_FRAMES: print("values is\t%s " % values)

        diff = { 'shader_params': values, 'feedback_active': feedback_active }
        if self.DEBUG_FRAMES:  print("returning %s\n^^^^" % diff['shader_params'])
                    
        return diff


    def recall_frame_index(self, index, ignored = None):
        #from plugins.ShaderQuickPresetPlugin import ShaderQuickPresetPlugin
        if ignored is not None:
            f = self.frames[index].copy()
            for ix,x in enumerate(ignored['shader_params']):
               for ip,p in enumerate(x):
                  if p is not None:
                      print("ignoring %ix,%ip" % (ix,ip))
                      f['shader_params'][ix][ip] = None  
            #self.pc.get_plugins(ShaderQuickPresetPlugin)[0].recall_frame_params(f)
            self.pc.shaders.recall_frame_params(f)
        else:
            if self.DEBUG_FRAMES:  print("recall_frame about to recall %s" % self.frames[index])
            #self.pc.get_plugins(ShaderQuickPresetPlugin)[0].recalL_frame_params(self.frames[index])
            self.pc.shaders.recall_frame_params(self.frames[index])
        #print("recalling \t%s\nwith ignored\t%s" % (self.frames[index].copy(),ignored))
        self.pc.shaders.recall_frame_params(self.frames[index].copy(), ignored)

