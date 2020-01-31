import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin

class MultiActionsPlugin(ActionsPlugin):
    disabled = False

    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

    @property
    def parserlist(self):
        return [
                ( r"(.*)&&(.*)", self.run_multi ),
        ]

    def run_multi(self, action1, action2, value):
        print("multi running %s and %s with value %s" % (action1, action2, value))
        self.pc.actions.call_method_name(action1, value)
        self.pc.actions.call_method_name(action2, value)
