import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin, DisplayPlugin#, SequencePlugin
#import math
from math import sin, cos, tan, log, exp, pi

"""
add to midi or osc mapping
use |f: : to bookend your formula

eg

    "control_change 48": {
            "DEFAULT": ["invert|f:sin(x*pi):|set_the_shader_param_0_layer_offset_0_continuous>&print_arguments&&set_variable_A&&print_arguments","set_strobe_amount_continuous"],
            "NAV_DETOUR": ["set_detour_speed_position_continuous"]
    },

example above inverts input, runs sin(x*pi) on it, then uses that value to set the shader param layer 0 and prints the value to console.  it also sets variable A to be the *original* value, and calls print_arguments to print it

           "DEFAULT": ["invert|f:sin(x*pi):|set_the_shader_param_0_layer_offset_0_continuous>&set_variable_B>&print_arguments&&set_variable_A&&print_arguments","set_strobe_amount_continuous"],

this one is similar the above but there's three branches as separated by the &&:-
            invert|
                f:sin(x*pi):|
                    set_the_shader_param_0_layer_offset_0_continuous>&
                    set_variable_B>&
                    print_arguments
            &&
            set_variable_A
            &&
            print_arguments

    "control_change 49": {
            "DEFAULT": ["set_the_shader_param_1_layer_offset_0_continuous&&A>print_arguments","set_shader_speed_layer_0_amount"],
            "NAV_DETOUR": ["set_detour_start_continuous"]
    },

example above outputs value stored in variable A and prints it as well as seting current shader value

TODO: >> ??    invert|set_the_shader_param_0_layer_>>print_arguments>>set_variable_A
     invert input, send to variable and to shader ?

"""

class ManipulatePlugin(ActionsPlugin,DisplayPlugin):
    disabled = False

    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

    @property
    def parserlist(self):
        return [ 
                ( r"(.*)&&(.*)", self.run_multi ),  # split && first since they need to be processed separately
                ( r"^invert\|(.*)$", self.invert ),
                ( r"^f:(.*):\|(.*)$", self.formula ), # formula eg ```f:sin(x):|```
                ( r"^set_variable_([a-zA-Z0-9]+)$", self.set_variable ),
                ( r"^([A-Z0-9]+)>(.*)$", self.recall_variable ), # recall variable and pipe into righthand side eg ```VAR1>invert|set_the_shader_.....```
                ( r"^(.*)>\&(.*)$", self.run_multi ), # pick up piped commands that duplicate a chain of values last
                ( "MANIPULA", None )
        ]

    def show_plugin(self, display, display_mode):
        from tkinter import Text, END
        #super(DisplayPlugin).show_plugin(display, display_mode)
        display.display_text.insert(END, '{} \n'.format(display.body_title))
        display.display_text.insert(END, "test from ManipulatePlugin!\n")

        for key,value in self.variables.items():
            display.display_text.insert(END, "\t" + key + "\t{:03.2f}\n".format(value))


    def get_display_modes(self):
        return ["MANIPULA",None] #"NAV_MANIPULATE"]

    def run_multi(self, action1, action2, value):
        print("multi running %s and %s with value %s" % (action1, action2, value))
        self.pc.actions.call_method_name(action1, value)
        self.pc.actions.call_method_name(action2, value)

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
        print("set_variable     (%s) to %s" % (var_name, value))
        self.variables[var_name] = value

    def recall_variable(self, var_name, action, *args):
        print ("recall_variable (%s) as %s" % (var_name,args))
        self.pc.actions.call_method_name(
                action, self.variables.get(var_name)# + list(args)
        )

    """def pipe2(self, left, right1, separator, right2, tail, value):
        self.pc.actions.call_method_name(
                left + separator + right1, value
        )
        self.pc.actions.call_method_name(
                left + separator + right2, value
        )
        self.pc.actions.call_method_name(
                tail, value
        )"""

    def pipe(self, left, right, value):
        # ??
        print("pipe calling left '%s' and right '%s', both with value '%s'" % (left, right, value))
        self.pc.actions.call_method_name(
                left, value
        )

        self.pc.actions.call_method_name(
                right, value
        )

