import copy
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
        self.pc = pc

    def to_json(self):
        return self.f #{ 'f': self.f }

    def get(self, key, default=None):
        return self.f.get(key,default)
    def has(self, key):
        return self.get(key) is not None

    def store_live(self):
        frame = {
                #'selected_shader_slots': [ shader.get('slot',None) for shader in self.pc.shaders.selected_shader_list ],
                'selected_shader': copy.deepcopy(self.pc.shaders.selected_shader_list),
                'shader_params': copy.deepcopy(self.pc.shaders.selected_param_list),
                'layer_active_status': copy.deepcopy(self.pc.shaders.selected_status_list),
                'feedback_active': self.pc.shaders.data.feedback_active,
                'x3_as_speed': self.pc.shaders.data.settings['shader']['X3_AS_SPEED']['value'],
                'shader_speeds': copy.deepcopy(self.pc.shaders.selected_speed_list),
                'strobe_amount': self.pc.shaders.data.settings['shader']['STROBE_AMOUNT']['value'] / 10.0,
                'shader_modulation_levels': copy.deepcopy(self.pc.shaders.modulation_level)
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

    def get_active_shader_names(self):
        s = ""
        if self.has('selected_shader_slots'):
            return ['-']*3
        if self.has('selected_shader'):
            return [ shader['name'].strip() for shader in self.get('selected_shader') ]
        return [ self.pc.data.shader_bank_data[layer][x].get('name').strip() if x is not None else '-'\
                 for layer,x in enumerate(self.get('selected_shader_slots',[None]*3)) 
               ]

    def get_frame_summary(self):
        summary = []
        not_shown = {}

        # list the recorded shader info in compact format
        names = self.get_active_shader_names()
        for layer in range(0,3): # number of shader layers
            s = self.get_shader_layer_summary(layer)
            summary.append(s)
            
        # handle summarising the rest of the recorded shader info, two-to-a-line where possible
        count = 0
        line = ""
        for key,d in sorted(self.f.items()):
            #print ("get_frame_summary: checking %s value %s" % (key,d))
            if type(d) is dict and len(d)==0: # skip empty dicts
                continue
            if key in ["selected_shader","layer_active_status","shader_params","shader_speeds","selected_shader_slots"]:
                # skip these as dealt with below
                pass
            elif key in ['shader_modulation_levels']:
                for layer in range(3):
                  o = ""
                  for slot in range(4):
                    sl = self.pc.display.get_mod_slot_label(slot)
                    o+= sl + "["
                    for param in range(4):
                        o += self.pc.display.get_bar(d[layer][param][slot])
                    o+= "] "
                  summary.append("Shader layer %s: %s"%(layer,o))
            elif self.pc.get_plugin_for_class_name(key) is not None:
                summary.append(self.pc.get_plugin_for_class_name(key).get_frame_summary(d))
                """elif key in ["WJSendPlugin"]:
                # for things that tend to be heavy so dont show
                not_shown[key] = d"""
            else:
                line += "%s: %s" % (key, d)
                count += 1
                if count%2==1:
                    line += "\t"
                elif count>0 and count%2==0:
                    summary.append(line)
                    line = ""
        if line != "":
            summary.append(line)

        # add 'not shown' items
        if len(not_shown)>0:
            summary.append(','.join(not_shown.keys()))

        return summary

    def get_shader_layer_summary(self, layer):
            s = "%s%s" % (layer, " " if layer != self.pc.data.shader_layer else ">")
            s += "["
            s += self.pc.display.get_compact_indicators([\
                    (i==self.get('selected_shader_slots',[-1]*3)[layer]) or\
                    (self.has('selected_shader') and self.pc.data.shader_bank_data[layer][i]['name'] == self.get('selected_shader')[layer]['name'])\
                    for i in range(10)\
                ])
            s += "]"

            if self.has('layer_active_status'):
                s += " %s " % (self.get('layer_active_status',['-']*3)[layer])

            if self.get('selected_shader'):
                s += "{:14.14}".format(self.get('selected_shader')[layer].get('name').replace('.frag','').strip())

            s += " " + self.get_shader_param_summary(layer) + " "

            if self.has('shader_speeds'):
                s += self.pc.display.get_speed_indicator(self.get('shader_speeds',[0.0]*3)[layer])

            return s



    def get_shader_param_summary(self, layer):
        if self.get('shader_params') is None:
            return ""
        s = ""
        for i in range(4):
            s += self.pc.display.get_bar(self.get('shader_params')[layer][i])
        return s

    def recall_frame(self):
        preset = self

        if preset.f is None:
            return

        self.pc.data.settings['shader']['X3_AS_SPEED']['value'] = preset.get('x3_as_speed')

        # x3_as_speed affects preset recall, so do that first
        self.recall_frame_params()

        for layer in range(3):
            if preset.has('selected_shader_slots'): # deprecated/compatibility
                self.pc.actions.call_method_name('play_shader_%s_%s' % (layer, preset.get('selected_shader_slots')[layer]))
            elif preset.has('selected_shader') and preset.get('selected_shader')[layer] is not None:
                # match selected shader to a slot and call that back if it exists
                found = False
                for slot,shader in enumerate(self.pc.data.shader_bank_data[layer]):
                    if shader['name'] == preset.get('selected_shader')[layer]['name']:
                        self.pc.actions.call_method_name('play_shader_%s_%s' % (layer, slot))
                        found = True
                        break
                if not found: # otherwise fall back to loading it separately
                    self.pc.shaders.selected_shader_list[self.pc.data.shader_layer] = preset.get('selected_shader')[layer].copy()
                    self.pc.shaders.load_selected_shader()

        if preset.has('shader_modulation_levels'):
            for layer in range(3):
                for param in range(4):
                    for slot in range(4):
                        level = preset.get('shader_modulation_levels')[layer][param][slot]
                        self.pc.shaders.set_param_layer_slot_modulation_level(param, layer, slot, level)

        for (layer, active) in enumerate(preset.get('layer_active_status',[])):
            # print ("got %s layer with status %s " % (layer,active))
            if active=='▶':
                self.pc.actions.call_method_name('start_shader_layer_%s' % layer)
            else:
                self.pc.actions.call_method_name('stop_shader_layer_%s' % layer)

    def recall_frame_params(self):
        #print("recall_frame_params got: %s" % preset.get('shader_params'))
        for (layer, param_list) in enumerate(self.get('shader_params',[])):
            if param_list:
                for param,value in enumerate(param_list):
                    #if (ignored is not None and ignored['shader_params'][layer][param] is not None):
                    #    print ("ignoring %s,%s because value is %s" % (layer,param,ignored['shader_params'][layer][param]))
                    #    continue
                    if (value is not None):
                      #print("recalling layer %s param %s: value %s" % (layer,param,value))
                      self.pc.actions.call_method_name('set_the_shader_param_%s_layer_%s_continuous' % (param,layer), value)

        if self.has('feedback_active'):
            self.pc.data.feedback_active = self.get('feedback_active',self.pc.data.feedback_active)
            if self.pc.data.feedback_active:
                self.pc.actions.call_method_name('enable_feedback')
            else:
                self.pc.actions.call_method_name('disable_feedback')

        if self.has('x3_as_speed'):
            self.pc.data.settings['shader']['X3_AS_SPEED']['value'] = self.get('x3_as_speed',self.pc.data.settings['shader']['X3_AS_SPEED']['value'])
            """if self.data.settings['shader']['X3_AS_SPEED']['value']:
                self.data.plugins.actions.call_method_name('enable_x3_as_speed')
            else:
                self.data.plugins.actions.call_method_name('disable_x3_as_speed')"""

        for (layer, speed) in enumerate(self.get('shader_speeds',[])):
            if speed is not None:
                self.pc.actions.call_method_name('set_shader_speed_layer_%s_amount' % layer, speed)

        if self.has('strobe_amount'):
            self.pc.actions.set_strobe_amount_continuous(self.get('strobe_amount'))

        from data_centre.plugin_collection import AutomationSourcePlugin
        for plugin in self.pc.get_plugins(AutomationSourcePlugin):
            #print("recalling for plugin %s with data %s" % (plugin, self.get(plugin.frame_key)))
            plugin.recall_frame_data(self.get(plugin.frame_key))

    def merge(self, frame2):
        from copy import deepcopy
        f = deepcopy(self.f) #frame1.copy()
        #if self.DEBUG_FRAMES:  print("merge_frames: got frame1\t%s" % frame1)
        #if self.DEBUG_FRAMES:  print("merge_frames: got frame2\t%s" % frame2)
        for i,f2 in enumerate(frame2.get('shader_params')):
            for i2,p in enumerate(f2):
                if p is not None:
                    if 'shader_params' not in f:
                        f['shader_params'] = [[None]*4,[None]*4,[None]*4]
                    f['shader_params'][i][i2] = p

        if frame2.has('feedback_active'):
            f['feedback_active'] = frame2['feedback_active']

        if frame2.has('x3_as_speed'):
            f['x3_as_speed'] = frame2.get('x3_as_speed')

        if f.get('shader_speeds') is None:
            if 'shader_speeds' in frame2.f:
                f['shader_speeds'] = frame2.get('shader_speeds')
        else:
            for i,s in enumerate(frame2.get('shader_speeds')):
                if s is not None:
                    f['shader_speeds'][i] = s

        if frame2.get('strobe_amount'):
            f['strobe_amount'] = frame2.get('strobe_amount')

        from data_centre.plugin_collection import AutomationSourcePlugin
        for plugin in self.pc.get_plugins(AutomationSourcePlugin):
            f[plugin.frame_key] = plugin.merge_data(f.get(plugin.frame_key),frame2.get(plugin.frame_key))

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
        if 'feedback_active' in ignored:
            f['feedback_active'] = None
        if 'x3_as_speed' in ignored:
            f['x3_as_speed'] = None
        if 'shader_speeds' in ignored and 'shader_speeds' in frame:
          for i,s in enumerate(frame.get('shader_speeds')):
            if ignored['shader_speeds'][i] is not None:
                f['shader_speeds'][i] = None
        if 'strobe_amount' in ignored:
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

        if self.has('feedback_active'):
            return False
        if self.has('x3_as_speed'):
            return False
        if self.has('strobe_amount'):
            return False

        for i,f in enumerate(frame['shader_params']):
            for i2,p in enumerate(f):
                if p is not None: #ignored['shader_params'][i][i2] is not None:
                    return False

        if self.has('shader_speeds'):
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
            for layer,params in enumerate(frame.get('shader_params',[])):
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

        from data_centre.plugin_collection import AutomationSourcePlugin
        for plugin in self.pc.get_plugins(AutomationSourcePlugin):
            plugin.process_interpolate_clip(frames)
                    
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
            if frames[search_findex] is not None and frames[search_findex].get('shader_params',[ [None]*4, [None]*4, [None]*4 ])[layer][param] is not None:
                return i, frames[search_findex].get('shader_params')[layer][param]
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
