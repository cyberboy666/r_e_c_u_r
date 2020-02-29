import string
import sys


from pythonosc import dispatcher
from pythonosc import dispatcher
from pythonosc import osc_server
import threading
import argparse


class OscInput(object):
    def __init__(self, root, message_handler, display, actions, data):
        self.root = root
        self.message_handler = message_handler
        self.display = display
        self.actions = actions
        self.data = data
        self.osc_mappings = data.osc_mappings
        
        self.osc_enabled = False
        self.osc_server = None
        self.poll_settings_for_osc_info()

    def poll_settings_for_osc_info(self):
        self.data.settings['user_input'].setdefault('OSC_INPUT',
                self.data.default_settings['user_input'].get('OSC_INPUT'))
        osc_setting_enabled = self.data.settings['user_input']['OSC_INPUT']['value'] == 'enabled'
        if osc_setting_enabled and not self.osc_enabled:
            self.setup_osc_server()
            self.osc_enabled = True
        elif not osc_setting_enabled and self.osc_enabled:
            self.actions.create_client_and_shutdown_osc_server()
            self.osc_enabled = False
        self.root.after(1000, self.poll_settings_for_osc_info)

    def setup_osc_server(self):
        ip_address = self.data.get_ip_for_osc_client()

        print('%%%%%%%%%%%%%%%%%%%%% setting up external_osc on ', ip_address)
        server_parser = argparse.ArgumentParser()
        server_parser.add_argument("--ip", default=ip_address, help="the ip")
        server_parser.add_argument("--port", type=int, default=8080, help="the port")

        server_args = server_parser.parse_args()

        this_dispatcher = dispatcher.Dispatcher()
        
        this_dispatcher.map("/keyboard/*", self.on_osc_input)
        this_dispatcher.map("/shaderparam0", self.on_param_osc_input)
        this_dispatcher.map("/shaderparam1", self.on_param_osc_input)
        this_dispatcher.map("/shaderparam2", self.on_param_osc_input)
        this_dispatcher.map("/shaderparam3", self.on_param_osc_input)
        this_dispatcher.map("/shutdown", self.exit_osc_server)

        # this is for accepting any old osc message to allow binding of modulation to osc messages
        # TODO: make configurable?
        this_dispatcher.map("/*", self.on_param_osc_input)
        
        osc_server.ThreadingOSCUDPServer.allow_reuse_address = True
        server = osc_server.ThreadingOSCUDPServer((server_args.ip, server_args.port), this_dispatcher)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.start()
        self.osc_server = server

    def exit_osc_server(self, unused_addr, args):
        print('%%%%%%%%%%%%%%%%%%%%% exiting external_osc')
        self.osc_server.shutdown()

    def on_osc_input(self, addr, args):
        args = str(args)
        print("!!!!!!!!!!!!!!!!" + args)
        print("the address", addr)
        key = addr[-1]
        numpad = list(string.ascii_lowercase[0:19])

        if key in numpad:
            self.run_action_for_osc_channel(key)
        else:
            print('{} is not in keypad map'.format(args))

    def on_param_osc_input(self, addr, args):
        print("the address", addr)

        self.run_action_for_osc_channel(addr, param_value=args)
        
    def run_action_for_osc_channel(self, channel, param_value=None):
        this_mapping = self.osc_mappings[channel]
        if self.data.control_mode in this_mapping:
            mode = self.data.control_mode
        elif 'DEFAULT' in this_mapping:
            mode = 'DEFAULT'
            
        if self.data.function_on and len(this_mapping[mode]) > 1:
            method_name = this_mapping[mode][1]
            if self.data.settings['sampler']['FUNC_GATED']['value'] == 'off':
                self.data.function_on = False
        else:
            method_name = this_mapping[mode][0]
            
        self.actions.call_method_name(method_name, param_value)

        if 'continuous' not in method_name:
            self.display.refresh_display()

