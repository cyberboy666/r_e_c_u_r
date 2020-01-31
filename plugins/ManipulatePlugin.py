import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin#, SequencePlugin
#import math
from math import sin, cos, tan, log, exp, pi

"""
add to midi or osc mapping
use |f: : to bookend your formula

eg

    "control_change 48": {
            "DEFAULT": ["set_the_shader_param_0_layer_offset_0_continuous|invert|f:sin(x*pi):&&print_arguments","set_strobe_amount_continuous"],
            "NAV_DETOUR": ["set_detour_speed_position_continuous"]
    },
"""

class ManipulatePlugin(ActionsPlugin):
    disabled = False

    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

    @property
    def parserlist(self):
        return [ 
                ( r"^(.*)\|invert$", self.invert ),
                ( r"^(.*)\|f:(.*):$", self.formula ),
                ( r"^set_variable_([a-zA-Z0-9]+)$", self.set_variable )
        ]

    variables = {}

    def invert(self, action, value):
        # invert the value
        self.pc.actions.call_method_name(
                action, 1.0 - value
                # if you were calling an action with no argument, use eg:
                # "toggle_automation_pause", None
        )

    def formula(self, action, formula, value):
        self.variables['x'] = value
        print("evaluating formula `%s` with value `%s`" % (formula, value))
        value = eval(formula, globals(), self.variables)
        print("got evaluated value `%s`" % value)

        self.pc.actions.call_method_name(
                action, value
        )

    def set_variable(self, var_name, value):
        self.variables[var_name] = value
