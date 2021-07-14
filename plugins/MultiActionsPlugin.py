from data_centre.plugin_collection import ActionsPlugin


class MultiActionsPlugin(ActionsPlugin):
    disabled = False  # this is only a demo of very basic multi-actions plugin -- superceded by ManipulatePlugin

    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)
        try:
            from plugins import ManipulatePlugin
            self.disabled = True  # if we've found ManipulatePlugin then disable this one
        except:
            # if it fails, we're good to go (so long as not disabled explictly above)
            pass

    @property
    def parserlist(self):
        return [
            (r"(.*)&&(.*)", self.run_multi),
        ]

    def run_multi(self, action1, action2, value):
        print("multi running %s and %s with value %s" % (action1, action2, value))
        self.pc.actions.call_method_name(action1, value)
        self.pc.actions.call_method_name(action2, value)
