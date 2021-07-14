from data_centre.plugin_collection import ActionsPlugin, DisplayPlugin, ModulationReceiverPlugin  # , SequencePlugin

import math ## DO NOT REMOVE -- IS REQUIRED FOR THE 'FORMULA' FUNCTION TO BE ABLE TO ACCESS pi AND random ETC
import random
from math import pi, sin, atan, cos, tan
from random import random as rand

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


class ManipulatePlugin(ActionsPlugin, DisplayPlugin, ModulationReceiverPlugin):
    DEBUG = False

    def __init__(self, plugin_collection):
        globals()['pc'] = plugin_collection
        super().__init__(plugin_collection)

    # ActionsPlugin methods
    @property
    def parserlist(self):
        return [
            (r"(.*)&&(.*)", self.run_multi),  # split && first since they need to be processed separately
            (r"^invert\|(.*)$", self.invert),
            (r"^f:(.*):\|(.*)$", self.formula),  # formula eg ```f:sin(x):|```
            (r"^set_variable_([a-zA-Z0-9]+)$", self.set_variable),
            (r"^([A-Z0-9]+)>(.*)$", self.recall_variable),  # recall variable and pipe into righthand side eg ```VAR1>invert|set_the_shader_.....```
            (r"^(.*)>\&(.*)$", self.run_multi),  # pick up piped commands that duplicate a chain of values last
        ]

    # DisplayPlugin methods
    def show_plugin(self, display, display_mode):
        from tkinter import END
        # super(DisplayPlugin).show_plugin(display, display_mode)
        display.display_text.insert(END, '{} \n'.format(display.body_title))
        display.display_text.insert(END, "test from ManipulatePlugin!\n")

        for key, value in self.variables.items():
            display.display_text.insert(END, "\t" + key + "\t{:03.2f}\n".format(value))

    def get_display_modes(self):
        return ["MANIPULA", "NAV_MANI"]  # "NAV_MANIPULATE"]

    # Actions
    def run_multi(self, action1, action2, value):
        if self.DEBUG:
            print("ManipulatePlugin>> multi-running '%s' and '%s' with value %s" % (action1, action2, value))
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
        if self.DEBUG:
            print("ManipulatePlugin>> evaluating formula `%s` with value `%s`" % (formula, value))
        value = eval(formula, globals(), self.variables)
        if self.DEBUG:
            print("ManipulatePlugin>> got evaluated value `%s`" % value)

        self.pc.actions.call_method_name(
                action, value
        )

    def set_variable(self, var_name, value):
        if self.DEBUG:
            print("ManipulatePlugin>> set_variable     (%s) to %s" % (var_name, value))
        self.variables[var_name] = value

    def get_variable(self, var_name, default):
        if var_name in self.variables:
            return self.variables[var_name]
        else:
            return default

    def recall_variable(self, var_name, action, *args):
        if self.DEBUG:
            print("ManipulatePlugin>> recall_variable (%s) as %s" % (var_name, args))
        self.pc.actions.call_method_name(
                action, self.variables.get(var_name)  # + list(args)
        )

    # ModulationReceiverPlugin methods
    #    methods for ModulationReceiverPlugin - receives changes to the in-built modulation levels (-1 to +1)
    def set_modulation_value(self, param, value):
        # take modulation value and throw it to local parameter
        if self.DEBUG:
            print("||||| ManipulatePlugin received set_modulation_value for param %s with value %s!" % (param, value))
        self.set_variable("MODVALUE%s" % ('ABCD'[param]), value)
