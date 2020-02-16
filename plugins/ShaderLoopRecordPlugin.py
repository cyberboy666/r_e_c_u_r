import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin, SequencePlugin, DisplayPlugin
from plugins.frame_manager import Frame

class ShaderLoopRecordPlugin(ActionsPlugin,SequencePlugin,DisplayPlugin):
    disabled = False
    MAX_CLIPS = 8
    frames = [] 

    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

        self.PRESET_FILE_NAME = "ShaderLoopRecordPlugin/frames.json"

        for clip in self.load_presets():
            c = []
            for frame in clip:
                c.append(Frame(self.pc).store_copy(frame))
            self.frames.append(c)

        self.reset_ignored()

    def load_presets(self):
        #try:
        print("trying load presets? %s " % self.PRESET_FILE_NAME)
        p = self.pc.read_json(self.PRESET_FILE_NAME)
        if p:
            while len(p)<self.MAX_CLIPS:
                print ("adding clip ")
                p += self.get_empty_clip(self.duration) #[ [None] ] #*((int(self.duration / self.frequency))-len(p)) ]
            for i in p:
                print("got automation clip of duration %s" % len(i))
                if i and len(i)<(int(self.duration / self.frequency)):
                    print("adding more slots due to size change")
                    i += [None]*((int(self.duration / self.frequency))-len(i))
                    print("len is now %s" % len(i))
            return p
        elif p:
            return p
        else:
            return self.get_factory_reset()
        #except:
        #    return self.clear_frames()

    def save_presets(self):
        self.pc.update_json(self.PRESET_FILE_NAME, self.frames)

    def get_display_modes(self):
        return ['LOOPREC','NAV_LPRC']

    def show_plugin(self, display, display_mode):
        from tkinter import Text, END
        #super(DisplayPlugin).show_plugin(display, display_mode)
        display.display_text.insert(END, '{} \n'.format(display.body_title))
        display.display_text.insert(END, "test from ShaderLoopRecordPlugin!\n")
        status = ""
        status+="playing" if self.is_playing() else "stopped"
        status+="\t"
        status+="paused" if self.is_paused() else "unpaused"
        status+="\t"
        status+="REC" if self.recording else "---"
        status+="*" if self.is_ignoring() else " "
        status+="\t"
        status+="Overdub" if self.overdub else "-------"
        status+="\t"
        status+="Looping" if self.looping else "Once"
        status+="\n"

        display.display_text.insert(END, status)
        display.display_text.insert(END, ("Position:\t{:03.2f}%\t[{:15s}]".format(self.position,("#"*int(self.position*15)))))
        display.display_text.insert(END, (" Speed: {:03.2f}%\n".format(self.speed*100)))
        if self.speed==0.0:
            display.display_text.insert(END, ("Duration:\tinfinity!\n"))
        else:
            display.display_text.insert(END, ("Duration:\t{:03.2f}s\n".format(((self.duration/1000)/self.speed)/4)))
        #distance s = d/t    d = s*t   t = d/s

        status = "\nEnabled clips:\t"
        for i in range(0,self.MAX_CLIPS):
            status+="#" if i==self.selected_clip and i in self.running_clips else\
                    "/" if i==self.selected_clip and i not in self.running_clips else\
                    "=" if i in self.running_clips else\
                    '_'
        status += "\n"
        display.display_text.insert(END, status)
 
        """for key,value in self.variables.items():
            display.display_text.insert(END, "\t" + key + "\t{:03.2f}\n".format(value))"""



    @property
    def parserlist(self):
        return [
                ( r"run_automation",  self.run_automation ),
                ( r"stop_automation", self.stop_automation ),
                ( r"toggle_pause_automation", self.toggle_pause_automation ),
                ( r"pause_automation", self.pause_automation ),
                ( r"toggle_loop_automation", self.toggle_loop_automation ),
                ( r"set_automation_speed", self.set_speed ),
                ( r"toggle_record_automation", self.toggle_record_automation ),
                ( r"toggle_overdub_automation", self.toggle_overdub_automation ),
                ( r"clear_automation", self.clear_clip ),
                ( r"select_automation_clip_([0-7])", self.select_clip ),
                ( r"toggle_automation_clip_([0-7])", self.toggle_clip )
        ]

    def toggle_overdub_automation(self):
        self.overdub = not self.overdub
        if not self.overdub:
            self.reset_ignored()

    def toggle_record_automation(self):
        self.recording = not self.recording
        if self.recording and not self.overdub:
            self.clear_clip()
        if not self.recording:
            self.reset_ignored()
            self.last_frame = None
            self.last_saved_index = None
            self.save_presets()

    def get_empty_clip(self, duration = 4000):
        return [None] * (int(duration / self.frequency))

    def get_factory_reset(self):
        return [ self.get_empty_clip(self.duration) for i in range(self.MAX_CLIPS) ]

    def clear_clip(self,clip = None):
        if clip is None:
            clip = self.selected_clip
        self.frames[clip] = self.get_empty_clip(self.duration) * self.MAX_CLIPS
        self.reset_ignored()
        if self.DEBUG_FRAMES: print ("clear_frames set to %s" % (int(self.duration / self.frequency)))
        return self.frames

    def toggle_clip(self,clip = None):
        if clip is None:
            clip = self.selected_clip
        else:
            self.selected_clip = clip

        #self.running_clips[clip] = not self.running_clips[clip]
        if clip in self.running_clips:
            self.running_clips.remove(clip)
        else:
            self.running_clips.append(clip)
        print("running clips looks like %s" %self.running_clips)

    def reset_ignored(self):
        # print("!!!!resetting ignored")
        self.ignored = Frame(self.pc).store_copy({ 'shader_params': [[None]*4,[None]*4,[None]*4] })

    def is_ignoring(self):
        return not self.pc.fm.is_frame_empty(self.ignored)

    def select_clip(self, clip):
        self.selected_clip = clip

    selected_clip = 0
    running_clips = [ ] #False ] * self.MAX_CLIPS

    duration = 4000
    frequency = 10 #25 
    recording = False
    overdub = True 
    #ignored = None # set in reset_ignored in init - used for tracking what parans have changed since overdub
    last_frame = None # for tracking what's changed between frames when overdubbing
    last_saved_index = None # for backfilling
    DEBUG_FRAMES = False#True
    def run_sequence(self, position):
        current_frame_index = int(position * (int(self.duration / self.frequency)))
        if current_frame_index<0:
            current_frame_index = (self.duration/self.frequency) - current_frame_index
        if current_frame_index >= self.duration: # self.duration/self.frequency:
            current_frame_index = "(self.duration/self.frequency) +""" (current_frame_index%self.duration)

        if self.DEBUG_FRAMES: print (">>>>>>>>>>>>>>frame at %i%%: %i" % (position*100, current_frame_index))
        #print("got frame index %s" % current_frame_index)

        if self.recording:
            current_frame = self.pc.fm.get_live_frame() #.copy()

        selected_clip = self.selected_clip
        if self.DEBUG_FRAMES: print("current_frame copy before recall is %s" % current_frame['shader_params'])
        #print ("%s clips, looks like %s" % (len(self.frames),self.frames))

        #print("selected_clip is %s "%selected_clip)
        #clip = self.frames[selected_clip]
        if self.is_playing() and self.recording and self.selected_clip not in self.running_clips:
            self.running_clips += [ self.selected_clip ]
        if self.recording:
            current_frame = self.pc.fm.get_live_frame() #.copy()
        if self.DEBUG_FRAMES: print("current_frame copy before recall is %s" % current_frame['shader_params'])

        for selected_clip in self.running_clips:
          saved_frame = self.frames[selected_clip][current_frame_index]
          if not self.recording or (selected_clip!=self.selected_clip):
              self.pc.fm.recall_frame(saved_frame)
          if self.recording and selected_clip==self.selected_clip:
            if self.last_frame is None: 
                self.last_frame = current_frame
            if self.DEBUG_FRAMES: print("last frame is \t\t%s" % self.last_frame['shader_params'])
            if self.DEBUG_FRAMES: print("current f is  \t\t%s" % current_frame['shader_params'])
            diff = self.pc.fm.get_frame_diff(self.last_frame,current_frame)
            if self.DEBUG_FRAMES: print("diffed frame is \t%s" % diff['shader_params'])

            if self.overdub and saved_frame:
                # add the params tweaked this frame to the params to be ignored by recall
                if self.DEBUG_FRAMES: print("saved frame is \t%s" % saved_frame['shader_params'])
                self.ignored = self.pc.fm.merge_frames(self.ignored, diff)
                if self.DEBUG_FRAMES: print("about to call get_ignored_frames with %s\n and\n %s" % (saved_frame.f, self.ignored.f))
                """print("got self.ignored:\n\t%s\n" % self.ignored.f)
                print("diff is currently:\n\t%s\n" % diff.f)
                print("saved_frame is currently:\n\t%s\n" % saved_frame.f)"""
                diff = self.pc.fm.merge_frames(
                        self.pc.fm.get_frame_ignored(saved_frame, self.ignored),
                        diff
                )
                #print("got merged:\n\t%s\n" % diff.f)
                #diff = self.pc.shaders.merge_frames(self.pc.shaders.get_live_frame(), diff)
                self.pc.fm.recall_frame(diff)
                if self.DEBUG_FRAMES:  print("after diff2 is:  \t%s" % diff['shader_params'])
            if self.DEBUG_FRAMES: print("||||saving frame \t%s" % (diff['shader_params']))
            self.frames[selected_clip][current_frame_index] = diff #self.get_frame_diff(self.last_frame,current_frame)
            #backfill frames
            if self.last_saved_index is not None:
                if self.DEBUG_FRAMES: print ("last_saved_index is %s, current_frame_index is %s" % (self.last_saved_index, current_frame_index))
                for i in range(current_frame_index - (self.last_saved_index) ):
                    if self.DEBUG_FRAMES: print("backfilling frame %s" % ((self.last_saved_index+i+1)%len(self.frames[selected_clip])))
                    self.frames[selected_clip][(self.last_saved_index+i+1)%len(self.frames[selected_clip])] = diff
            self.last_saved_index = current_frame_index
            self.last_frame = self.pc.fm.get_live_frame() #diff
        if self.DEBUG_FRAMES:  print("<<<<<<<<<<<<<< frame at %s" % current_frame_index)

    """def recall_frame_index(self, index):
        self.pc.shaders.recall_frame_params(self.frames[index].copy())"""

