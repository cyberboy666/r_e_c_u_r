import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin, SequencePlugin

class ShaderLoopRecordPlugin(ActionsPlugin,SequencePlugin):

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
            self.last_saved_index = None
            self.save_presets()

    def clear_frames(self):
        self.frames = [{}] * (int(self.duration / self.frequency))
        self.reset_ignored()
        if self.DEBUG_FRAMES: print ("clear_frames set to %s" % (int(self.duration / self.frequency)))
        return self.frames

    def reset_ignored(self):
        # print("!!!!resetting ignored")
        self.ignored = { 'shader_params': [[None]*4,[None]*4,[None]*4] }

    duration = 2000
    frequency = 10 #25 
    recording = False
    overdub = True 
    #ignored = None # set in reset_ignored in init - used for tracking what parans have changed since overdub
    last_frame = None # for tracking what's changed between frames when overdubbing
    last_saved_index = None # for backfilling
    DEBUG_FRAMES = False#True
    def run_sequence(self, position):
        current_frame_index = int(position * (int(self.duration / self.frequency)))
        if self.DEBUG_FRAMES: print (">>>>>>>>>>>>>>frame at %i%%: %i" % (position*100, current_frame_index))
        #print("got frame index %s" % current_frame_index)

        current_frame = self.pc.shaders.get_live_frame().copy()
        if self.DEBUG_FRAMES: print("current_frame copy before recall is %s" % current_frame['shader_params'])

        if not self.recording:
            self.recall_frame_index(current_frame_index)
        if self.recording:
            if self.last_frame is None: 
                self.last_frame = current_frame
            if self.DEBUG_FRAMES: print("pre-diff frame is\t%s" % current_frame['shader_params'])
            if self.DEBUG_FRAMES: print("last frame is \t\t%s" % self.last_frame['shader_params'])
            if self.DEBUG_FRAMES: print("current f is  \t\t%s" % current_frame['shader_params'])
            diff = self.pc.shaders.get_frame_diff(self.last_frame,current_frame)
            if self.DEBUG_FRAMES: print("diffed frame is \t%s" % diff['shader_params'])
            if self.overdub and self.frames[current_frame_index]:
                # add the params tweaked this frame to the params to be ignored by recall
                if self.DEBUG_FRAMES: print("saved frame is \t%s" % self.frames[current_frame_index]['shader_params'])
                self.ignored = self.pc.shaders.merge_frames(self.ignored, diff)
                diff = self.pc.shaders.merge_frames(
                        self.pc.shaders.get_frame_ignored(self.frames[current_frame_index], self.ignored),
                        diff
                )
                #diff = self.pc.shaders.merge_frames(self.pc.shaders.get_live_frame(), diff)
                self.pc.shaders.recall_frame(diff)
                if self.DEBUG_FRAMES:  print("after diff2 is:  \t%s" % diff['shader_params'])
            if self.DEBUG_FRAMES: print("||||saving frame \t%s" % (diff['shader_params']))
            self.frames[current_frame_index] = diff #self.get_frame_diff(self.last_frame,current_frame)
            #backfill frames
            if self.last_saved_index is not None:
                if self.DEBUG_FRAMES: print ("last_saved_index is %s, current_frame_index is %s" % (self.last_saved_index, current_frame_index))
                for i in range(current_frame_index - (self.last_saved_index) - 1):
                    if self.DEBUG_FRAMES:print("backfilling frame %s" % ((self.last_saved_index+i+1)%len(self.frames)))
                    self.frames[(self.last_saved_index+i+1)%len(self.frames)] = diff
            self.last_saved_index = current_frame_index
            self.last_frame = self.pc.shaders.get_live_frame() #diff
        if self.DEBUG_FRAMES:  print("<<<<<<<<<<<<<< frame at %s" % current_frame_index)

    def recall_frame_index(self, index):
        self.pc.shaders.recall_frame_params(self.frames[index].copy())

