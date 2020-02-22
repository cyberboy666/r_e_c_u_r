import serial
from serial import Serial
import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin, SequencePlugin, DisplayPlugin, ModulationReceiverPlugin, AutomationSourcePlugin
import threading

class WJSendPlugin(ActionsPlugin, SequencePlugin, DisplayPlugin, ModulationReceiverPlugin, AutomationSourcePlugin):
    disabled = False#True
    DEBUG = False#True
    ser = None
    # from http://depot.univ-nc.nc/sources/boxtream-0.9999/boxtream/switchers/panasonic.py
    """serial.Serial(device, baudrate=9600,
                                          bytesize=serial.SEVENBITS,
                                          parity=serial.PARITY_ODD,
                                          stopbits=serial.STOPBITS_ONE,
                                          xonxoff=False,
                                          rtscts=True, # TODO : test without this one
                                          timeout=timeout)"""

    THROTTLE = 1 # milliseconds to wait between refreshing parameters

    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

        if self.disabled:
            print ("WJSendPlugin is disabled, not opening serial")
            return

        for cmd,struct in self.commands.items():
            self.command_by_queue[struct['queue']] = struct

        self.pc.actions.tk.after(500, self.refresh)

    # methods/vars for AutomationSourcePlugin
    # a lot of the nitty-gritty handled in parent class, these are for interfacing to the plugin
    last_record = {}
    def get_frame_data(self):
        diff = self.last_record.copy()
        #self.last_record = {}
        #print(">>> reporting frame data for rec\n\t%s" % diff)
        return diff

    """def clear_recorded_frame(self):
        self.last_record = {}"""

    def recall_frame_data(self, data):
        if data is None:
            return
        # print(">>>>recall from data:\n\t%s\n" %data)
        for queue, item in data.items():
            if item is not None:
                self.send_buffered(queue, item[0], item[1], record = False)


    # methods for ModulationReceiverPlugin - receives changes to the in-built modulation levels (-1 to +1)
    # experimental & hardcoded !
    # TODO: make this not hardcoded and configurable mapping modulation to parameters, preferably on-the-fly..
    modulation_value = [0.0]*4
    def set_modulation_value(self, param, value):

        self.modulation_value[param] = value    ## invert so that no signal always gives a value ..
        #print("storing modulation slot %s as %s" % (param,value))

        # take modulation value and throw it to local parameter
        if self.DEBUG: print("||||| WJSendPlugin received set_modulation_value for param %s with value %s!" % (param, value))
        #v = (0.5+value)/2
        """mapped = [
                'mix',
                'colour_T',
                #'colour_T',
                'back_colour:x'
        ]"""
        #self.catch_all(*mapped[param].split(":")+[v])
        #self.commands[
        # find which commands are mapped to this modulation, and trigger a send of them 
        # so that they update with the new modulation value
        for queue,cmd in sorted(self.command_by_queue.items()):
            if cmd.get('modulation') is not None:
                #if self.DEBUG: print("\tparam %s, checking modulation %s" % (param, cmd.get('modulation')))
                if len(cmd.get('modulation')[param])>0:
                    if self.DEBUG: print("\tParam %s has modulation! sending update of values? %s" % (param, [x for x in cmd['arguments'].values() ]))
                    self.send_buffered(cmd['queue'], cmd['form'], [x for x in [ cmd['arguments'][y] for y in cmd['arg_names'] ] ], record=False)
                    continue
                
    #methods for DisplayPlugin
    def show_plugin(self, display, display_mode):
        from tkinter import Text, END
        display.display_text.insert(END, '{} \n'.format(display.body_title))
        display.display_text.insert(END, "WJSendPlugin status\n\n")

        for queue, last in sorted(self.last_modulated.items()):
            display.display_text.insert(END, "%s:\t%s\t%s\n" % (queue,self.last.get(queue)[1],self.last_modulated.get(queue)[1]))

    def get_display_modes(self):
        return ["WJMXSEND","NAV_WJMX"]


    # methods for SerialPlugin (TODO: if this needs generalising out!) and serial command queueing
    def open_serial(self, port='/dev/ttyUSB0', baudrate=9600):
        if self.ser is not None:
            self.ser.close()
        if self.disabled:
            return
        try:
            self.ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                bytesize=serial.SEVENBITS,
                parity=serial.PARITY_ODD,
                stopbits=serial.STOPBITS_ONE,
                xonxoff=False,
                rtscts=True, # TODO : test without this one
                timeout=None #timeout
            )

        except Exception as e:
            print ("WJSendPlugin>> open_serial failed: " + str(type(e)))
            self.disabled = True
            import traceback
            traceback.print_exc()

    def send_serial_string(self, string):
        try:
            if self.DEBUG: print("WJSendPlugin>> sending string %s " % string)
            output = b'\2' + string.encode('ascii') + b'\3'
            self.ser.write(output) #.encode())
            if self.DEBUG: print("send_serial_string: sent string '%s'" % output) #.encode('ascii'))
            #if 'S' in string:
            #    self.get_device_status()
        except Exception as e:
            print("\t%s: send_serial_string failed for '%s'" % (e,string)) 

    queue = {}
    # send the queued commands to WJMX
    def refresh(self):
        if not self.ser or self.ser is None:
            self.open_serial()

        try:
            # sorting the commands that are sent seems to fix jerk and lag that is otherwise pretty horrendous
            for queue, command in sorted(self.queue.items()):
                # TODO: modulate the parameters
                self.send_buffered(queue, command[0], command[1])
            #self.queue.clear()
        except Exception:
            print ("WJSendPlugin>>> !!! CAUGHT EXCEPTION running queue %s!!!" % queue)
            import traceback
            print(traceback.format_exc())
        finally:
            self.queue.clear()

        if self.ser is not None:
            self.pc.shaders.root.after(self.THROTTLE, self.refresh)

    def send(self, queue, form, args):
        #self.send_buffered(queue,output)
        self.queue[queue] = (form, args) #output

    last = {}
    last_modulated = {}
    def send_buffered(self, queue, form, args, record = True):
        # only send if new command is different to the last one we sent
        mod_args = self.modulate_arguments(self.command_by_queue.get(queue), args)
        if self.last_modulated.get(queue)!=(form,mod_args):
            #print("WJSendPlugin>> send_buffered attempting to parse queue\t%s with form\t'%s' and args\t%s" % (queue, form, args))
            # TODO: actually output modulated version of args
            output = form.format(*mod_args)
            self.send_serial_string(output)
            self.last[queue] = (form,args)
            self.last_modulated[queue] = (form,mod_args)
            if record:
                self.last_record[queue] = (form,args)
        else:
            pass
            #print("WJSendPlugin>> found no difference between:\n\t%s\n\t%s\n?" % (self.last_modulated.get(queue), (form,mod_args)))

    def send_append(self, command, value):
        # append value to the command as a hex value - for sending commands that aren't preprogrammed
        self.send(command.split(':')[0], "{}{:02X}", [ command, int(255*value) ])

    def send_append_pad(self, pad, command, value):
        # append value, padded to length - for sending commands that aren't preprogrammed
        self.send(command.split(':')[0], "{}{:0%iX}"%pad, [ command, int(255*value) ])


    # methods for ActionPlugin - preprogrammed parameters
    @property
    def parserlist(self):
        return [
                ( r"^open_serial$", self.open_serial ),
                ( r"^wj_send_serial:([0-9a-zA-Z:]*)$", self.send_serial_string ),
                #( r"^wj_set_colour:([A|B|T])_([x|y])$", self.set_colour ),
                #( r"^wj_set_back_colour:([x|y|z])$", self.set_back_colour ),
                #( r"^wj_set_position:([N|L])_([x|y])$", self.set_position ),
                #( r"^wj_set_mix$", self.set_mix ),
                ( r"^wj_send_append_pad:([0-9]*)_([[:0-9a-zA-Z]*)$", self.send_append_pad ),
                ( r"^wj_send_append:([:0-9a-zA-Z]*)$", self.send_append ),
                ( r"^wj_set_([a-zA-Z_]*)[:]?([a-zA-Z_]*)$", self.catch_all )
        ]

    def catch_all(self, param, argument_name, value):
        #print ("got catch-all %s, %s, %s" % (param, argument_name, value))
        #arguments = packed_arguments.split("_") + [ value ]
        #print("commands looks like %s" % self.commands)
        msg = self.commands[param]
        if len(msg['arg_names'])==1: argument_name = msg['arg_names'][0]
        msg['arguments'][argument_name] = int(value*255) # = arguments
        self.send(msg['queue'], msg['form'], [ msg['arguments'][p] for p in msg['arg_names'] ] )

    def modulate_arguments(self, command, args):
        args = args.copy()
        #if self.DEBUG: print("modulate_arguments passed %s and\n\t%s" % (command,args))
        for slot in range(0,4):
            modlevels = command.get('modulation',[{}]*4)[slot]
            #if self.DEBUG: print("\tfor modulate_arguments for slot %s got modlevels: %s" % (slot, modlevels))
            for i,m in enumerate(modlevels.values()):
                if m>0.0:
                    if self.DEBUG: print("\t\tupdating modulation slot %s, arg is %s\n\t with modlevel '%s' * modvalue '%s'" % (i, args[i], m, self.modulation_value[slot]))
                    newvalue = self.pc.shaders.get_modulation_value(
                            args[i]/255.0, 
                            self.modulation_value[slot], 
                            m
                    )
                    if self.DEBUG: print("\t\tnewvalue is %s" %newvalue)
                    args[i] = int(255*newvalue)
        if self.DEBUG: print("modulate_arguments returning:\n\t%s" % args)
        return args

    commands = {
            'colour_gain_T': {
                'name': 'Colour Corrector gain - both',
                'queue': 'VCG',
                'form': 'VCG:T{:02X}',
                'arg_names': [ 'v' ],
                'arguments': { 'v': 127 }
            },
            'colour_T': {
                'name': 'Colour Corrector - both',
                'queue': 'VCC',
                'form': 'VCC:T{:02X}{:02X}',
                'arg_names': [ 'x', 'y' ],
                'arguments': { 'x': 127, 'y': 127 },
                'modulation': [ {}, {}, { 'x': 1.0 }, { 'y': 1.0 } ]
                #'callback': self.set_colour
            },
            'mix': {
                'name': 'Mix/wipe',
                'queue': 'VMM',
                'form': 'VMM:{:02X}0000',
                'arg_names': [ 'v' ],
                'arguments': { 'v': 127 },
                'modulation': [ { 'v':  1.0 }, {}, {}, {} ]
            },
            'back_colour': {
                'name': 'Back colour/matte HSV',
                'queue': 'VBM',
                'form': 'VBM:{:02X}{:02X}{:02X}',
                'arg_names': [ 'h', 's', 'v' ],
                'arguments': { 'h': 127, 's': 127, 'v': 127 },
                'modulation': [ {}, { 'h': 1.0 }, {}, {} ]
            },
            'position_N': {
                'name': 'Positioner joystick',
                'queue': 'VPS',
                'form': 'VPS:N{:02X}{:02X}',
                'arg_names': [ 'y', 'x' ],
                'arguments': { 'y': 127, 'x': 127 }
            },
            'dsk_level': {
                'name': 'Downstream Key level',
                'queue': 'VDL',
                'form': 'VDL:{:02X}',
                'arg_names': [ 'v' ],
                'arguments': { 'v': 127 }
            }
    }
    command_by_queue = {}

