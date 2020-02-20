import copy
import json
from json import JSONEncoder

def _default(self, obj):
    if getattr(obj.__class__,'to_json'):
        #return _default.default(obj.to_json())
        return obj.to_json()
    else:
        return _default.default(obj)

_default.default = JSONEncoder().default
JSONEncoder.default = _default

class Frame:
    f = { 'shader_params': [[None]*4,[None]*4,[None]*4] }
    pc = None

    DEBUG_FRAMES = False#True

    def __init__(self, pc):
        import copy #from copy import deepcopy
        self.pc = pc

    def to_json(self):
        return self.f #{ 'f': self.f }

    def store_live(self):
        frame = {
                'selected_shader_slots': [ shader.get('slot',None) for shader in self.pc.shaders.selected_shader_list ],
                'shader_params': copy.deepcopy(self.pc.shaders.selected_param_list),
                'layer_active_status': copy.deepcopy(self.pc.shaders.selected_status_list),
                'feedback_active': self.pc.shaders.data.feedback_active,
                'x3_as_speed': self.pc.shaders.data.settings['shader']['X3_AS_SPEED']['value'],
                'shader_speeds': copy.deepcopy(self.pc.shaders.selected_speed_list),
                'strobe_amount': self.pc.shaders.data.settings['shader']['STROBE_AMOUNT']['value'] / 10.0
        }
        #print("about to call get_plugin_frame_data")
        frame.update(self.pc.fm.get_plugin_frame_data())
        self.f = frame
        #print("built frame: %s" % self.f)
        return self

    def store_copy(self, f):
        #print("told to store_copy %s" % f)
        if f is not None:
            if f.get('f') is not None: #isinstance(f, Frame):
                f = f.get('f')
                return self.store_copy(f.get('f'))
            self.f = f
        else:
            self.f = {}
        return self

    def recall_frame_params(self):
        #print("recall_frame_params got: %s" % preset.get('shader_params'))
        for (layer, param_list) in enumerate(self.f.get('shader_params',[])):
            if param_list:
                for param,value in enumerate(param_list):
                    #if (ignored is not None and ignored['shader_params'][layer][param] is not None):
                    #    print ("ignoring %s,%s because value is %s" % (layer,param,ignored['shader_params'][layer][param]))
                    #    continue
                    if (value is not None):
                      #print("recalling layer %s param %s: value %s" % (layer,param,value))
                      self.pc.actions.call_method_name('set_the_shader_param_%s_layer_%s_continuous' % (param,layer), value)

        if self.f.get('feedback_active') is not None:
            self.pc.data.feedback_active = self.f.get('feedback_active',self.pc.data.feedback_active)
            if self.pc.data.feedback_active:
                self.pc.actions.call_method_name('enable_feedback')
            else:
                self.pc.actions.call_method_name('disable_feedback')

        if self.f.get('x3_as_speed') is not None:
            self.pc.data.settings['shader']['X3_AS_SPEED']['value'] = self.f.get('x3_as_speed',self.pc.data.settings['shader']['X3_AS_SPEED']['value'])
            """if self.data.settings['shader']['X3_AS_SPEED']['value']:
                self.data.plugins.actions.call_method_name('enable_x3_as_speed')
            else:
                self.data.plugins.actions.call_method_name('disable_x3_as_speed')"""

        for (layer, speed) in enumerate(self.f.get('shader_speeds',[])):
            if speed is not None:
                self.pc.actions.call_method_name('set_shader_speed_layer_%s_amount' % layer, speed)

        if self.f.get('strobe_amount') is not None:
            self.pc.actions.set_strobe_amount_continuous(self.f.get('strobe_amount'))

        from data_centre.plugin_collection import AutomationSourcePlugin
        for plugin in self.pc.get_plugins(AutomationSourcePlugin):
            #print("recalling for plugin %s with data %s" % (plugin, self.f.get(plugin.frame_key)))
            plugin.recall_frame_data(self.f.get(plugin.frame_key))

    def recall_frame(self):
        preset = self

        if preset.f is None:
            return

        self.pc.data.settings['shader']['X3_AS_SPEED']['value'] = preset.f.get('x3_as_speed')

        # x3_as_speed affects preset recall, so do that first
        self.recall_frame_params()

        for (layer, slot) in enumerate(preset.f.get('selected_shader_slots',[])):
            if slot is not None:
                #print("setting layer %s to slot %s" % (layer, slot))
                self.pc.actions.call_method_name('play_shader_%s_%s' % (layer, slot))

        for (layer, active) in enumerate(preset.f.get('layer_active_status',[])):
            # print ("got %s layer with status %s " % (layer,active))
            if active=='▶':
                self.pc.actions.call_method_name('start_shader_layer_%s' % layer)
            else:
                self.pc.actions.call_method_name('stop_shader_layer_%s' % layer)

    def merge(self, frame2):
        from copy import deepcopy
        f = deepcopy(self.f) #frame1.copy()
        #if self.DEBUG_FRAMES:  print("merge_frames: got frame1\t%s" % frame1)
        #if self.DEBUG_FRAMES:  print("merge_frames: got frame2\t%s" % frame2)
        for i,f2 in enumerate(frame2.f.get('shader_params')):
            for i2,p in enumerate(f2):
                if p is not None:
                    if 'shader_params' not in f:
                        f['shader_params'] = [[None]*4,[None]*4,[None]*4]
                    f['shader_params'][i][i2] = p

        if frame2.f.get('feedback_active') is not None:
            f['feedback_active'] = frame2['feedback_active']

        if frame2.f.get('x3_as_speed') is not None:
            f['x3_as_speed'] = frame2.f.get('x3_as_speed')

        if f.get('shader_speeds') is None:
            if 'shader_speeds' in frame2.f:
                f['shader_speeds'] = frame2.f.get('shader_speeds')
        else:
            for i,s in enumerate(frame2.f.get('shader_speeds')):
                if s is not None:
                    f['shader_speeds'][i] = s

        if frame2.f.get('strobe_amount'):
            f['strobe_amount'] = frame2.f.get('strobe_amount')

        from data_centre.plugin_collection import AutomationSourcePlugin
        for plugin in self.pc.get_plugins(AutomationSourcePlugin):
            f[plugin.frame_key] = plugin.merge_data(f.get(plugin.frame_key),frame2.f.get(plugin.frame_key))

        if self.DEBUG_FRAMES:  print("merge_frames: got return\t%s" % f)
        return Frame(self.pc).store_copy(f)
 
    def get_ignored(self, ignored):
        from copy import deepcopy
        f = deepcopy(self.f) #frame1.copy()
        frame = self.f
        ignored = ignored.f
        if self.DEBUG_FRAMES:  print("get_frame_ignored: got frame\t%s" % self.f)
        for i,f2 in enumerate(frame.get('shader_params',[])):
            for i2,p in enumerate(f2):
                if ignored['shader_params'][i][i2] is not None:
                    f['shader_params'][i][i2] = None
        if ignored.get('feedback_active') is not None:
            f['feedback_active'] = None
        if ignored.get('x3_as_speed') is not None:
            f['x3_as_speed'] = None
        if ignored.get('shader_speeds') is not None and frame.get('shader_speeds') is not None:
          for i,s in enumerate(frame.get('shader_speeds')):
            if ignored['shader_speeds'][i] is not None:
                f['shader_speeds'][i] = None
        if ignored.get('strobe_amount') is not None:
            f['strobe_amount'] = None

        from data_centre.plugin_collection import AutomationSourcePlugin
        for plugin in self.pc.get_plugins(AutomationSourcePlugin):
            if ignored.get(plugin.frame_key) is not None:
                #print("ignoring for %s:\n\t%s\n" % (plugin.frame_key, ignored.get(plugin.frame_key)))
                f[plugin.frame_key] = plugin.get_ignored_data(f.get(plugin.frame_key,{}),ignored.get(plugin.frame_key,{}))

        if self.DEBUG_FRAMES:  print("get_frame_ignored: got return\t%s" % f)
        return Frame(self.pc).store_copy(f)

    def is_empty(self):
        #from copy import deepcopy
        #f = deepcopy(frame) #frame1.copy()
        frame = self.f
        if self.DEBUG_FRAMES:  print("is_frame_empty: got frame\t%s" % frame)

        if frame.get('feedback_active') is not None:
            return False
        if frame.get('x3_as_speed') is not None:
            return False
        if frame.get('strobe_amount') is not None:
            return False

        for i,f in enumerate(frame['shader_params']):
            for i2,p in enumerate(f):
                if p is not None: #ignored['shader_params'][i][i2] is not None:
                    return False

        if frame.get('shader_speeds') is not None:
          for i,f in enumerate(frame['shader_speeds']):
            if f is not None:
                return False

        from data_centre.plugin_collection import AutomationSourcePlugin
        for plugin in self.pc.get_plugins(AutomationSourcePlugin):
            if frame.get(plugin.frame_key) is None:
                continue
            if not plugin.is_frame_data_empty(frame.get(plugin.frame_key)):
                return False

        if self.DEBUG_FRAMES:  print("is_frame_empty: got return true")
        return True

    def get_diff(self, current_frame):
        #if not last_frame: return current_frame
        current_frame = current_frame.f
        last_frame = self.f

        if self.DEBUG_FRAMES:
            print(">>>>get_frame_diff>>>>")
            print("last_frame: \t%s" % last_frame['shader_params'])
            print("current_frame: \t%s" % current_frame['shader_params'])

        param_values = [[None]*4,[None]*4,[None]*4]
        for layer,params in enumerate(current_frame.get('shader_params',[[None]*4]*3)):
            #if self.DEBUG_FRAMES:  print("got layer %s params: %s" % (layer, params))
            for param,p in enumerate(params):
                if p is not None and p != last_frame.get('shader_params')[layer][param]:
                    if self.DEBUG_FRAMES: print("setting layer %s param %s to %s" % (layer,param,p))
                    param_values[layer][param] = p

        if current_frame['feedback_active'] is not None and last_frame['feedback_active'] != current_frame['feedback_active']:
            feedback_active = current_frame['feedback_active']
        else:
            feedback_active = None

        if current_frame['x3_as_speed'] is not None and last_frame['x3_as_speed'] != current_frame['x3_as_speed']:
            x3_as_speed = current_frame['x3_as_speed']
        else:
            x3_as_speed = None

        speed_values = [None]*3
        for layer,param in enumerate(current_frame.get('shader_speeds',[None]*3)):
            if param is not None and param != last_frame['shader_speeds'][layer]:
                speed_values[layer] = param

        if current_frame['strobe_amount'] is not None and last_frame['strobe_amount'] != current_frame['strobe_amount']:
            strobe_amount = current_frame['strobe_amount']
        else:
            strobe_amount = None

        if self.DEBUG_FRAMES:
            print("param_values is\t%s" % param_values)
            print("speed_values is\t%s" % speed_values)

        plugin_data = {}
        from data_centre.plugin_collection import AutomationSourcePlugin
        for plugin in self.pc.get_plugins(AutomationSourcePlugin):
            if current_frame.get(plugin.frame_key) is not None:
                plugin_data[plugin.frame_key] = plugin.get_frame_diff(last_frame, current_frame)

        diff = {
                'shader_params': param_values,
                'feedback_active': feedback_active,
                'x3_as_speed': x3_as_speed,
                'shader_speeds': speed_values,
                'strobe_amount': strobe_amount,
        }
        diff.update(plugin_data)
        if self.DEBUG_FRAMES: print("returning\t%s\n^^^^" % diff['shader_params'])

        return Frame(self.pc).store_copy(diff)





class FrameManager:
    pc = None

    def __init__(self, pc):
        self.pc = pc

    def get_live_frame(self):
        return Frame(self.pc).store_live()

    def recall_frame_params(self, preset):
        if preset is None:
            return
        preset.recall_frame_params()

    def recall_frame(self, preset):
        if preset is None:
            return
        preset.recall_frame()

    # overlay frame2 on frame1
    def merge_frames(self, frame1, frame2):
        return frame1.merge(frame2)

    def get_frame_ignored(self, frame, ignored):
        return frame.get_ignored(ignored)

    def is_frame_empty(self, frame):
        return frame.is_empty()

    def get_frame_diff(self, last_frame, current_frame):
        return last_frame.get_diff(current_frame)

    def get_plugin_frame_data(self):
        data = {}
        from data_centre.plugin_collection import AutomationSourcePlugin
        for plugin in self.pc.get_plugins(AutomationSourcePlugin):
            data[plugin.frame_key] = plugin.get_frame_data()
            #plugin.clear_recorded_frame()

        #print("get_plugin_frame_data looks like %s" % data)
        return data

    def interpolate_clip(self, frames):
        # loop over every frame
        #   for each property of each frame
        #       if its empty, 
        #           find distance to next value
        #           interpolate from the last to the next value
        #       else,
        #           store as last value

        print("got pre-interpolated clip: %s" % [ f.f for f in frames if f is not None])

        last = [ [None]*4, [None]*4, [None]*4 ]

        """for findex,frame in enumerate(frames):
            if frame is None:
                continue"""

        reproc_to = 0

        def process(self, findex, frame):
              for layer,params in enumerate(frame.f.get('shader_params',[])):
                for param,value in enumerate(params):
                    if value is None and last[layer][param] is not None:
                        # find distance to when this value changes again
                        gap,future_value = self.get_distance_value_layer_param(frames,findex,layer,param)
                        if gap==0 or future_value==value: # if doesnt change again, do nothing
                            continue
                        newvalue = self.interpolate(last[layer][param], future_value, gap)
                        params[param] = newvalue
                        print("findex %s: updating interpolated value to %s - should be between %s and %s over gap %s" % (findex, newvalue, last[layer][param], future_value, gap))
                        last[layer][param] = newvalue
                    #elif last[layer][param] is None:
                    #    reproc_to = findex
                    elif value is not None:
                        last[layer][param] = value
                    
        for i in range(2):
          for findex,frame in enumerate(frames):
            if frame is None:
                continue

            process(self,findex,frame)

        """for findex in range(reproc_to):
            if frames[findex] is None:
                continue

            process(self,findex,frames[findex])"""

        print("got interpolated clip: %s" % [ f.f for f in frames if f is not None ])

    def get_distance_value_layer_param(self, frames, findex, layer, param):
        for i in range(1,len(frames)):
            search_findex = i + findex
            search_findex %= len(frames)
            if frames[search_findex] is not None and frames[search_findex].f.get('shader_params',[ [None]*4, [None]*4, [None]*4 ])[layer][param] is not None:
                return i, frames[search_findex].f.get('shader_params')[layer][param]
        return 0, None

    def interpolate(self, value1, value2, total_steps):
        diff = max(value1,value2)-min(value1,value2)
        sl = diff / total_steps
        if value1>value2:
            v = value1-sl
        else:
            v = value1+sl

        print("interpolate between\t%s and\t%s over\t%s steps, got sl\t%s and value\t%s" % (value1,value2,total_steps, sl, v))
        return v
