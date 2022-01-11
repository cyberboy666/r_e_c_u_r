import threading
import time

import serial

from data_centre.plugin_collection import ActionsPlugin, AutomationSourcePlugin, DisplayPlugin, ModulationReceiverPlugin, SequencePlugin


class AsyncWriter(threading.Thread):
    queue = []
    quit_flag = False

    def __init__(self, plugin):
        super().__init__()
        self.plugin = plugin

    def write(self, data):
        self.queue.append(data)

    def ready(self):
        return len(self.queue) > 0

    def quit(self):
        self.quit_flag = True

    def run(self):
        while not self.quit_flag:
            # print("AsyncWriter looping..")
            if not self.plugin.active or self.plugin.disabled:
                # print("plugin active or disabled - exiting!")
                return
            if self.plugin.ser is None or not self.plugin.ser:
                # print("no stream - skipping")
                time.sleep(0.5)
                continue
            if not self.ready():
                # print("not ready - skipping")
                time.sleep(0.005)
                continue
            item = self.queue.pop(0)
            if item is not None:
                # print("sending %s" % item)
                self.plugin.ser.write(item)
                time.sleep(len(item) * 0.005)
            else:
                time.sleep(0.01)
            if len(self.queue) > 4:
                self.queue = self.queue[-4:4]


class WJSendPlugin(ActionsPlugin, SequencePlugin, DisplayPlugin, ModulationReceiverPlugin, AutomationSourcePlugin):
    DEBUG = False  # True
    ser = None

    active = True

    asyncwriter = None

    sleep = 0.0

    PRESET_FILE_NAME = "WJSendPlugin/presets.json"
    presets = {}
    # from http://depot.univ-nc.nc/sources/boxtream-0.9999/boxtream/switchers/panasonic.py
    """serial.Serial(device, baudrate=9600,
                                          bytesize=serial.SEVENBITS,
                                          parity=serial.PARITY_ODD,
                                          stopbits=serial.STOPBITS_ONE,
                                          xonxoff=False,
                                          rtscts=True, # TODO : test without this one
                                          timeout=timeout)"""

    THROTTLE = 20  # milliseconds to wait between refreshing parameters

    selected_command_name = None
    selected_argument_index = 0

    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

        """if self.disabled:
            print ("WJSendPlugin is disabled, not opening serial")
            return"""

        self.presets = self.load_presets()
        print("read presets:\n%s\n" % self.presets)
        # load the stored modulation levels into the current config
        for cmd, levels in self.presets['modulation_levels'].items():
            self.commands[cmd]['modulation'] = levels.copy()

        # build a reverse map of friendly name -> command struct for later use
        for cmd, struct in self.commands.items():
            self.command_by_queue[struct['queue']] = struct

        self.pc.actions.tk.after(500, self.start_plugin)

        self.selected_command_name = list(sorted(self.commands.keys()))[0]  # select first command

    def load_presets(self):
        print("trying load presets? %s " % self.PRESET_FILE_NAME)
        return self.pc.read_json(self.PRESET_FILE_NAME) or {'modulation_levels': {}}

    def save_presets(self):
        for cmd, struct in self.commands.items():
            self.presets.setdefault('modulation_levels', {})[cmd] = struct.get('modulation', [{}, {}, {}, {}])
        self.pc.update_json(self.PRESET_FILE_NAME, self.presets)

    def start_plugin(self):
        self.pc.actions.tk.after(0, self.refresh)

    def stop_plugin(self):
        super().stop_plugin()
        if self.asyncwriter is not None:
            self.asyncwriter.quit()
        self.asyncwriter = None
        self.save_presets()

    # methods/vars for AutomationSourcePlugin
    # a lot of the nitty-gritty handled in parent class, these are for interfacing to the plugin
    last_record = {}

    def get_frame_data(self):
        diff = self.last_record.copy()
        # self.last_record = {}
        # print(">>> reporting frame data for rec\n\t%s" % diff)
        return diff

    def recall_frame_data(self, data):
        if data is None:
            return
        # print(">>>>recall from data:\n\t%s\n" %data)
        for queue, item in data.items():
            if item is not None:
                self.send_buffered(queue, item[0], item[1], record=False)

    def get_frame_summary(self, data):
        line = "WJMX: "
        for key, value in data.items():
            line += key + ", "
        print("returning line %s" % line)
        return line

    # methods for ModulationReceiverPlugin - receives changes to the in-built modulation levels (-1 to +1)
    modulation_value = [0.0, 0.0, 0.0, 0.0]

    def set_modulation_value(self, param, value):

        self.modulation_value[param] = value  
        # print("storing modulation slot %s as %s" % (param,value))

        # take modulation value and throw it to local parameter
        if self.DEBUG:
            print("||||| WJSendPlugin received set_modulation_value for param %s with value %s!" % (param, value))
        # v = (0.5+value)/2
        """mapped = [
                'mix',
                'colour_T',
                #'colour_T',
                'back_colour:x'
        ]"""
        # self.catch_all(*mapped[param].split(":")+[v])
        # self.commands[
        # find which commands are mapped to this modulation, and trigger a send of them 
        # so that they update with the new modulation value
        to_send = {}
        for queue, cmd in sorted(self.command_by_queue.items(), reverse=True):
            cmd.setdefault('modulation', [{}, {}, {}, {}])

            if self.DEBUG:
                print("\tparam %s, checking modulation %s" % (param, cmd.get('modulation')))
            if len(cmd['modulation'][param]) > 0:
                if self.DEBUG:
                    print("\tParam %s has modulation! sending update of values? %s" %
                          (param, [cmd['arguments'][y] for y in cmd['arg_names']]))
                # self.send_buffered(cmd['queue'], cmd['form'], [x for x in [ cmd['arguments'][y] for y in cmd['arg_names'] ] ], record=False)
                to_send[cmd['queue']] = cmd
                continue

        for queue, cmd in sorted(to_send.items(), reverse=True):
            self.send_buffered(cmd['queue'], cmd['form'], [x for x in [cmd['arguments'][y] for y in cmd['arg_names']]], record=False)
            # with self.queue_lock:
            # self.send(cmd['queue'], cmd['form'], [x for x in [ cmd['arguments'][y] for y in cmd['arg_names'] ] ])

    # methods for DisplayPlugin
    def show_plugin(self, display, display_mode):
        from tkinter import END
        display.display_text.insert(END, '{} \n'.format(display.body_title))
        display.display_text.insert(END, "WJSendPlugin {}\n\n".format('ACTIVE' if self.active else 'not active'))

        for queue, last in sorted(self.last_modulated.items()):
            is_selected = queue == self.commands[self.selected_command_name].get('queue')
            indicator = " " if not is_selected else "<"
            display.display_text.insert(END, "%s%s:\t%s\t%s" % (indicator, queue, self.last.get(queue)[1], self.last_modulated.get(queue)[1]))
            if is_selected:
                display.display_text.insert(END, ">")  # add indicator of the selected queue for param jobbies
            display.display_text.insert(END, "\n")

        cmd = self.commands[self.selected_command_name]
        output = "\n" + "%s %s : %s\n" % (self.commands[self.selected_command_name].get('queue'), self.selected_command_name, cmd['name'])
        for arg_name in cmd['arg_names']:
            is_selected = cmd['arg_names'].index(arg_name) == self.selected_argument_index
            output += "\t "  # Mod
            indicator = " " if not is_selected else "["
            output += "%s%s: " % (indicator, arg_name)
            for slot, mods in enumerate(cmd.setdefault('modulation', [{}, {}, {}, {}])):
                # if arg_name in mods:
                v = mods.get(arg_name, 0.0)
                g = '%s' % self.pc.display.get_bar(v)
                output += "{}:{}|".format(self.pc.display.get_mod_slot_label(slot), g)
            if is_selected:
                output += "]"
            output += "\n"
        display.display_text.insert(END, output + "\n")

    def get_display_modes(self):
        return ["WJMXSEND", "NAV_WJMX"]

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
                    rtscts=True,  # TODO : test without this one
                    timeout=None  # timeout
            )

        except Exception as e:
            print("WJSendPlugin>> open_serial failed: " + str(type(e)))
            self.pc.data.disable_plugin('WJSendPlugin')
            import traceback
            traceback.print_exc()

    import threading
    serial_lock = threading.Lock()

    def send_serial_string(self, string):
        # TODO: thread this so can implement throttling and reduce bottleneck...
        if not self.active:
            return
        try:
            if self.DEBUG:
                print("WJSendPlugin>> sending string %s " % string)
            output = b'\2' + string.encode('ascii') + b'\3'
            # with self.serial_lock:
            # self.ser.write(b'\2\2\2\2\3\3\3\3')
            if self.asyncwriter is None:
                self.asyncwriter = AsyncWriter(self)
                self.asyncwriter.start()
            self.asyncwriter.write(output)
            # self.ser.write(output) #.encode())
            # TODO: sleeping here seems to help serial response lag problem?
            """self.sleep = 0.2 #self.pc.get_variable('A')
            #print ("got sleep %s" % self.sleep)
            if self.sleep>=0.1:
                #print("using sleep %s" % self.sleep)
                import time
                time.sleep(self.sleep/10.0)"""
            # yield from self.ser.drain()
            if self.DEBUG:
                print("send_serial_string: sent string '%s'" % output)  # .encode('ascii'))
            # if 'S' in string:
            #    self.get_device_status()
        except Exception as e:
            print("\t%s: send_serial_string failed for '%s'" % (e, string))

    queue = {}
    import threading
    queue_lock = threading.Lock()

    # send the queued commands to WJMX
    def refresh(self):
        if not self.ser or self.ser is None:
            self.open_serial()

        try:
            # sorting the commands that are sent seems to fix jerk and lag that is otherwise pretty horrendous
            with self.queue_lock:
                for queue, command in sorted(self.queue.items()):
                    self.send_buffered(queue, command[0], command[1])
                # self.queue.clear()
        except Exception:
            print("WJSendPlugin>>> !!! CAUGHT EXCEPTION running queue %s!!!" % queue)
            import traceback
            print(traceback.format_exc())
        finally:
            with self.queue_lock:
                self.queue.clear()

        if self.ser is not None and not self.disabled:
            self.pc.shaders.root.after(self.THROTTLE, self.refresh)

    def send(self, queue, form, args):
        # self.send_buffered(queue,output)
        with self.queue_lock:
            self.queue[queue] = (form, args)  # output

    last = {}
    last_modulated = {}

    def send_buffered(self, queue, form, args, record=True):
        # only send if new command is different to the last one we sent
        mod_args = self.modulate_arguments(self.command_by_queue.get(queue), args)
        if self.last_modulated.get(queue) != (form, mod_args):
            # print("WJSendPlugin>> send_buffered attempting to parse queue\t%s with form\t'%s' and args\t%s" % (queue, form, args))
            # TODO: actually output modulated version of args
            output = form.format(*mod_args)
            self.send_serial_string(output)
        else:
            if self.DEBUG:
                print("WJSendPlugin>> skipping sending %s %s as it is similar to what was previously sent" % (form, mod_args))

        self.last[queue] = (form, args)
        self.last_modulated[queue] = (form, mod_args)
        if self.last[queue] != (form, args) and record:
            self.last_record[queue] = (form, args)
        else:
            pass
            # print("WJSendPlugin>> found no difference between:\n\t%s\n\t%s\n?" % (self.last_modulated.get(queue), (form,mod_args)))

    def send_append(self, command, value):
        # append value to the command as a hex value - for sending commands that aren't preprogrammed
        self.send(command.split(':')[0], "{}{:02X}", [command, int(255 * value)])

    def send_append_pad(self, pad, command, value):
        # append value, padded to length - for sending commands that aren't preprogrammed
        self.send(command.split(':')[0], "{}{:0%iX}" % pad, [command, int(255 * value)])

    # methods for ActionPlugin - preprogrammed parameters
    @property
    def parserlist(self):
        return [
            (r"^open_serial$", self.open_serial),
            (r"^wj_send_serial:([0-9a-zA-Z:]*)$", self.send_serial_string),
            # ( r"^wj_set_colour:([A|B|T])_([x|y])$", self.set_colour ),
            # ( r"^wj_set_back_colour:([x|y|z])$", self.set_back_colour ),
            # ( r"^wj_set_position:([N|L])_([x|y])$", self.set_position ),
            # ( r"^wj_set_mix$", self.set_mix ),
            (r"^wj_set_modulation_([a-zA-Z_]*)[:]?([a-zA-Z_]*)_slot_([0-3])_level$", self.set_modulation_command_argument_level),
            (r"^wj_set_current_modulation_slot_([0-3])_level$", self.set_current_modulation_level),
            (r"^wj_send_append_pad:([0-9]*)_([[:0-9a-zA-Z]*)$", self.send_append_pad),
            (r"^wj_send_append:([:0-9a-zA-Z]*)$", self.send_append),
            (r"^wj_set_([a-zA-Z_]*)[:]?([a-zA-Z_]*)$", self.catch_all),
            (r"^wj_select_next_command$", self.select_next_command),
            (r"^wj_select_previous_command$", self.select_previous_command),
            (r"^wj_select_next_argument$", self.select_next_argument),
            (r"^wj_select_previous_argument$", self.select_previous_argument),
            (r"^wj_reset_modulation$", self.reset_modulation_levels),
            (r"^wj_toggle_active$", self.toggle_active)
        ]

    def toggle_active(self):
        self.active = not self.active
        if not self.active:
            self.asyncwriter = None

    def reset_modulation_levels(self):
        for cmd, struct in self.commands.items():
            struct['modulation'] = [{}, {}, {}, {}]

    def set_modulation_command_argument_level(self, command_name, argument_name, slot, level):
        if self.DEBUG:
            print("set_modulation_command_argument_level(%s, %s, %s, %s)" % (command_name, argument_name, slot, level))
        if not argument_name:
            self.commands[command_name]['arg_names'][0]  # argument_name = 'v'

        self.commands[command_name].setdefault('modulation', [{}, {}, {}, {}])[slot][argument_name] = level

    def set_current_modulation_level(self, slot, level):
        self.set_modulation_command_argument_level(self.selected_command_name, self.commands[self.selected_command_name]['arg_names'][self.selected_argument_index], slot, level)

    def select_previous_command(self):
        selected_command_index = list(sorted(self.commands.keys())).index(self.selected_command_name) - 1
        if selected_command_index < 0:
            selected_command_index = len(self.commands.keys()) - 1
        self.selected_command_name = sorted(list(self.commands.keys()))[selected_command_index]

        self.selected_argument_index = 0

    def select_next_command(self):
        selected_command_index = list(sorted(self.commands.keys())).index(self.selected_command_name) + 1
        if selected_command_index >= len(self.commands.keys()):
            selected_command_index = 0
        self.selected_command_name = sorted(list(self.commands.keys()))[selected_command_index]

        self.selected_argument_index = 0

    def select_previous_argument(self):
        self.selected_argument_index -= 1
        if self.selected_argument_index < 0:
            self.selected_argument_index = len(self.commands[self.selected_command_name]['arg_names']) - 1

    def select_next_argument(self):
        self.selected_argument_index += 1
        if self.selected_argument_index >= len(self.commands[self.selected_command_name]['arg_names']):
            self.selected_argument_index = 0

    def catch_all(self, param, argument_name, value):
        # print ("got catch-all %s, %s, %s" % (param, argument_name, value))
        # arguments = packed_arguments.split("_") + [ value ]
        # print("commands looks like %s" % self.commands)
        msg = self.commands[param]
        if len(msg['arg_names']) == 1:
            argument_name = msg['arg_names'][0]
        msg['arguments'][argument_name] = int(value * 255)  # = arguments
        self.send(msg['queue'], msg['form'], [msg['arguments'][p] for p in msg['arg_names']])

    def modulate_arguments(self, command, args):
        args = args.copy()
        # if self.DEBUG: print("modulate_arguments passed %s and\n\t%s" % (command,args))
        # TODO: rewrite this so that it combines multiple inputs and averages them
        for slot in range(0, 4):
            modlevels = command.get('modulation', [{}, {}, {}, {}])[slot]
            # if self.DEBUG: print("\tfor modulate_arguments for slot %s got modlevels: %s" % (slot, modlevels))
            # for i,m in enumerate(modlevels.values()):
            for arg_name, m in modlevels.items():
                if m > 0.0:
                    arg_index = command.get('arg_names').index(arg_name)
                    if self.DEBUG:
                        print("\t\tupdating modulation slot %s, arg is %s\n\t with modlevel '%s' * modvalue '%s'" % (arg_index, args[arg_index], m, self.modulation_value[slot]))
                    # amount, value, level
                    newvalue = self.pc.shaders.get_modulation_value(
                            args[arg_index] / 255.0,
                            self.modulation_value[slot],
                            m
                    )
                    if self.DEBUG:
                        print("\t\tnewvalue is %s" % newvalue)
                    args[arg_index] = int(255 * newvalue)
        if self.DEBUG:
            print("modulate_arguments returning:\n\t%s" % args)
        return args

    # panasonic parameters are 8 bit so go 0-255, so 127 is default of centre value
    commands = {
        'colour_gain_T': {
            'name': 'Colour Corrector gain (both)',
            'queue': 'VCG',
            'form': 'VCG:T{:02X}',
            'arg_names': ['v'],
            'arguments': {'v': 127}
        },
        'colour_T': {
            'name': 'Colour Corrector (both)',
            'queue': 'VCC',
            'form': 'VCC:T{:02X}{:02X}',
            'arg_names': ['x', 'y'],
            'arguments': {'x': 127, 'y': 127},
        },
        'mix': {
            'name': 'Mix/wipe',
            'queue': 'VMM',
            'form': 'VMM:{:02X}',
            'arg_names': ['v'],
            'arguments': {'v': 127},
        },
        'back_colour': {
            'name': 'Matte colour HSV',
            'queue': 'VBM',
            'form': 'VBM:{:02X}{:02X}{:02X}',
            'arg_names': ['h', 's', 'v'],
            'arguments': {'h': 127, 's': 127, 'v': 127},
        },
        'position_N': {
            'name': 'Positioner joystick XY',
            'queue': 'VPS',
            'form': 'VPS:N{:02X}{:02X}',
            'arg_names': ['y', 'x'],
            'arguments': {'y': 127, 'x': 127}
        },
        # 'dsk_slice': { ## cant seem to find the right control code for this?!
        #    'name': 'Downstream Key Slice,Slope',
        #    'queue': 'VDS',
        #    'form': 'VDS:{:02X}{:01X}',
        #    'arg_names': [ 'slice','slope' ],
        #    'arguments': { 'slice': 127, 'slope': 8 },
        #    'modulation': [ {}, { 'slice': 1.0 }, {}, {} ]
        # }
    }
    command_by_queue = {}
