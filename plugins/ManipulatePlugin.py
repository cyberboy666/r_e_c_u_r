import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin#, SequencePlugin

class ManipulatePlugin(ActionsPlugin):
    disabled = False

    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

    @property
    def parserlist(self):
        return [ 
                ( r"(.*)\|invert$", self.invert ),
        ]

    def invert(self, action, value):
        # invert the value
        self.pc.actions.call_method_name(
                action, 1.0 - value
                # if you were calling an action with no argument, use eg:
                # "toggle_automation_pause", None
        )
