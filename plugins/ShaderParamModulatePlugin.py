import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin#, SequencePlugin

class ShaderParamModulatePlugin(ActionsPlugin):#,SequencePlugin):
    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)
        #self.disabled = True

    @property
    def parserlist(self):
        return [
                ( r"set_layer_([0-2])_param_([0-3])_audio_react_volume", self.set_layer_param_audio_react_volume ),
                ( r"modulate_layer_([0-2])_param_([0-3])_continuous", self.modulate_layer_param_continuous )
        ]

    def set_layer_param_audio_react_volume(self, layer, param, value):
        print ("set_layer_param_audio_react_volume layer %s:%s is %s" % (layer, param, value))
        self.pc.actions.call_method_name("modulate_layer_%s_param_%s_continuous"%(layer,param), value)


    def modulate_layer_param_continuous(self,layer,param,value):
        print ("modulate_layer_param_continuous layer %s:%s is %s" % (layer, param, value))
        value = (0.01 * (value-0.5)) + self.pc.shaders.selected_param_list[layer][param]
        print ("got modded value %s" % value)
        self.pc.actions.call_method_name("set_the_shader_param_%s_layer_%s_continuous"%(param,layer), value)
