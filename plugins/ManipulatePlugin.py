import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin#, SequencePlugin
#import math
from math import sin, cos, tan, log, exp, pi

"""
add to midi or osc mapping
use |f: : to bookend your formula

eg

    "control_change 48": {
            "DEFAULT": ["invert|f:sin(x*pi):|set_the_shader_param_0_layer_offset_0_continuous&&set_variable_A&&print_arguments","set_strobe_amount_continuous"],
            "NAV_DETOUR": ["set_detour_speed_position_continuous"]
    },

example above inverts input, runs sin(x*pi) on it, then uses that value to set the shader param layer 0.  it also sets variable A to be the *original* value, and call print_arguments to print it


    "control_change 49": {
            "DEFAULT": ["set_the_shader_param_1_layer_offset_0_continuous&&A>print_arguments","set_shader_speed_layer_0_amount"],
            "NAV_DETOUR": ["set_detour_start_continuous"]
    },

example above outputs value stored in variable A and prints it

TODO: >> ??    invert|set_the_shader_param_0_layer_>>print_arguments>>set_variable_A
	invert input, send to variable and to shader ?

"""

class ManipulatePlugin(ActionsPlugin):
    disabled = False

    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

    @property
    def parserlist(self):
        return [ 
                ( r"^invert\|(.*)$", self.invert ),
                ( r"^f:(.*):\|(.*)$", self.formula ), 
                ( r"^set_variable_([a-zA-Z0-9]+)$", self.set_variable ),
                ( r"^([A-Z0-9]+)>(.*)$", self.recall_variable )
        ]

    variables = {}

    def invert(self, action, value):
        # invert the value
        self.pc.actions.call_method_name(
                action, 1.0 - value
                # if you were calling an action with no argument, use eg:
                # "toggle_automation_pause", None
        )

    def formula(self, formula, action, value):
        self.variables['x'] = value
        print("evaluating formula `%s` with value `%s`" % (formula, value))
        value = eval(formula, globals(), self.variables)
        print("got evaluated value `%s`" % value)

        self.pc.actions.call_method_name(
                action, value
        )

    def set_variable(self, var_name, value):
        self.variables[var_name] = value

    def recall_variable(self, var_name, action, *args):
        print ("recall_variable(%s) got args %s" % (var_name,args))
        self.pc.actions.call_method_name(
                action, self.variables.get(var_name)# + list(args)
        )
