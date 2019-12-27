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
        self.osc_server = self.setup_osc_server()

    def setup_osc_server(self):
        server_parser = argparse.ArgumentParser()
        server_parser.add_argument("--ip", default="0.0.0.0", help="the ip")
        server_parser.add_argument("--port", type=int, default=5433, help="the port")

        server_args = server_parser.parse_args()

        this_dispatcher = dispatcher.Dispatcher()
        this_dispatcher.map("/recurOsc", self.on_osc_input)
        this_dispatcher.map("/shutdown", self.exit_osc_server)
        this_dispatcher.map("/*", self.on_osc_message)
        
        server = osc_server.ThreadingOSCUDPServer((server_args.ip, server_args.port), this_dispatcher)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.start()
        return server

    def exit_osc_server(self, unused_addr, args):
        self.osc_server.shutdown()

    def on_osc_message(self, addr, args):
        #print("!!!!!!!!!!!!!!!!%s\t%s" %(addr,args))
        #print ("%s" %self.osc_mappings.keys())
        if addr in self.osc_mappings:
            #'print("got a mapping for %s with value %s" % (addr,args))
            self.actions.call_method_name(self.osc_mappings[addr]['DEFAULT'][0], args)

    def on_osc_input(self, addr, args):
        #print("!!!!!!!!!!!!!!!!" + addr + ", " + args)
        numpad = list(string.ascii_lowercase[0:19])

        if args in numpad:
            self.run_action_for_osc_channel(args)
        else:
            print('{} is not in keypad map'.format(args))

    def run_action_for_osc_channel(self, channel, args = None):
        this_mapping = self.osc_mappings[channel]
        if self.data.control_mode in this_mapping:
            mode = self.data.control_mode
        elif 'DEFAULT' in this_mapping:
            mode = 'DEFAULT'

        if self.data.function_on and len(this_mapping[mode]) > 1:
            print('the action being called is {}'.format(this_mapping[mode][1]))
            #getattr(self.actions, this_mapping[mode][1])()
            self.actions.call_method_name(this_mapping[mode][1], args)
            if self.data.settings['sampler']['FUNC_GATED']['value'] == 'off':
                self.data.function_on = False
        else:
            print('the action being called is {}'.format(this_mapping[mode][0]))
            #getattr(self.actions, this_mapping[mode][0])()
            self.actions.call_method_name(this_mapping[mode][0], args)
      
        self.display.refresh_display()

