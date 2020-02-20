import serial
from serial import Serial
import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin, SequencePlugin, DisplayPlugin, ModulationReceiverPlugin, AutomationSourcePlugin
import threading

class WJSendPlugin(ActionsPlugin, SequencePlugin, DisplayPlugin, ModulationReceiverPlugin, AutomationSourcePlugin):
    disabled = False#True
    ser = None
    # from http://depot.univ-nc.nc/sources/boxtream-0.9999/boxtream/switchers/panasonic.py
    """serial.Serial(device, baudrate=9600,
                                          bytesize=serial.SEVENBITS,
                                          parity=serial.PARITY_ODD,
                                          stopbits=serial.STOPBITS_ONE,
                                          xonxoff=False,
                                          rtscts=True, # TODO : test without this one
                                          timeout=timeout)"""

    """self.commands = {
            'VCG:': {
                'name': 'Colour Corrector Gain',
                'cmd': 'VCG:',
            },
            'VCC:': {
                'name': 'Colour Corrector XY',
                'cmd': 'VCC',
                'callback': self.set_colour
            }
    }"""

    THROTTLE = 1 # milliseconds to wait between refreshing parameters

    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

        if self.disabled:
            print ("WJSendPlugin is disabled, not opening serial")
            return

        #self.open_serial()
        #print ("starting refresh?")
        self.pc.actions.tk.after(500, self.refresh)
        #tk.after(500, self.refresh)

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
    def set_modulation_value(self, param, value):
        # take modulation value and throw it to local parameter
        print("||||| wjsend received set_modulation_value for param %s with value %s!" % (param, value))
        if param==0:
            self.set_mix((0.5+value)/2)
        elif param==1:
            self.set_colour('T', 'x', 0.5+value)
        elif param==2:
            self.set_colour('T', 'y', 0.5+value)
        elif param==3:
            self.set_back_colour('x', 0.5+value)
        else:
            print("unknown param %s!" % param)

    #methods for DisplayPlugin
    def show_plugin(self, display, display_mode):
        from tkinter import Text, END
        #super(DisplayPlugin).show_plugin(display, display_mode)
        #print("show plugin?")
        display.display_text.insert(END, '{} \n'.format(display.body_title))
        display.display_text.insert(END, "test from WJSendPlugin!\n\n")

        for queue, last in self.last.items():
            display.display_text.insert(END, "last %s:\t%s\n" % (queue,self.last.get(queue)))

    def get_display_modes(self):
        return ["WJMXSEND","NAV_WJMX"]

    # methods for SerialPlugin (todo!)
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

            print ("starting refresh?")

            #self.pc.midi_input.root.after(500, self.refresh)
        except Exception as e:
            print ("open_serial failed: " + str(type(e)))
            self.disabled = True
            import traceback
            traceback.print_exc()

    def send_serial_string(self, string):
        try:
            print("sending string %s " % string)
            output = b'\2' + string.encode('ascii') + b'\3'
            self.ser.write(output) #.encode())
            #print("sent string '%s'" % output) #.encode('ascii'))
            #if 'S' in string:
            #    self.get_device_status()
        except Exception as e:
            print("%s: send_serial_string failed for '%s'" % (e,string)) #.encode()

    queue = {}
    def refresh(self):
        #print("refresh called!")
        if not self.ser or self.ser is None:
            self.open_serial()

        try:
            for queue, command in self.queue.items():
                self.send_buffered(queue, command[0], command[1])
            #self.queue.clear()
        except Exception:
            print ("!!! CAUGHT EXCEPTION running queue !!!")
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
    def send_buffered(self, queue, form, args, record = True):
        """# TODO: remove this crap when i'm sure the bug has been fixed
        if output is not None and (type(output) is dict or 'WJSendPlugin' in output):
            print ("\n\n\ncaught fucker?")
            import traceback
            traceback.print_stack()
            quit()"""

        if self.last.get(queue)!=(form,args):
            print("send_buffered attempting to parse queue\t%s with form\t'%s' and args\t%s" % (queue, form, args))
            output = form.format(*args)
            self.send_serial_string(output)
            self.last[queue] = (form,args) #output
            if record:
                print("### send_buffered is setting last_record[%s] to %s" % (queue,output))
                self.last_record[queue] = (form,args)#output

    def send_append(self, command, value):
        # append value to the command as a hex value
        self.send(command.split(':')[0], "{}{:02X}", [ command,int(255*value) ])

    def send_append_pad(self, pad, command, value):
        # append value, padded to length
        self.send(command.split(':')[0], "{}{:0%iX}"%pad, [ command,int(255*value) ])


    # methods for ActionPlugin
    @property
    def parserlist(self):
        return [
                ( r"^open_serial$", self.open_serial ),
                ( r"^wj_send_serial_([0-9a-zA-Z:]*)$", self.send_serial_string ),
                ( r"^wj_set_colour_([A|B|T])_([x|y])$", self.set_colour ),
                ( r"^wj_set_back_colour_([x|y|z])$", self.set_back_colour ),
                ( r"^wj_set_back_wash_colour_([x|y|z])$", self.set_back_wash_colour ),
                ( r"^wj_set_position_([N|L])_([x|y])$", self.set_position ),
                ( r"^wj_set_mix$", self.set_mix ),
                ( r"^wj_send_append_pad_([0-9]*)_([[:0-9a-zA-Z]*)$", self.send_append_pad ),
                ( r"^wj_send_append_([:0-9a-zA-Z]*)$", self.send_append ),
        ]

    # methods for handling some Panasonic control settings
    #   todo: come up with a way to represent this programmatically
    #   todo: add more!

    colour_x = 127
    colour_y = 127
    def set_colour(self, chan, dim, value):
        # chan can be A, B or T (both)
        if dim=='x':
            self.colour_x = int(255*value)
        elif dim=='y':
            self.colour_y = int(255*value)

        #output = "VCC:{}{:02X}{:02X}".format(chan, self.colour_x, self.colour_y) 
        # could store format string + values, then interpolate over those values
        self.send('VCC', "VCC:{}{:02X}{:02X}", [chan, self.colour_x, self.colour_y]) #output)

    # RGB control of matte colour!
    back_colour_x = 127
    back_colour_y = 127
    back_colour_z = 127
    def set_back_colour(self, dim, value):
        # chan can be A, B or T (both)
        if dim=='x':
            self.back_colour_x = int(255*value)
        elif dim=='y':
            self.back_colour_y = int(255*value)
        elif dim=='z':
            self.back_colour_z = int(255*value)

        #output = "VBM:{:02X}{:02X}{:02X}".format(self.back_colour_x,self.back_colour_y,self.back_colour_z)
        self.send('VBM', "VBM:{:02X}{:02X}{:02X}", [ self.back_colour_x,self.back_colour_y,self.back_colour_z ]) 

    # this doesnt seem to work on WJ-MX30 at least, or maybe i dont know how to get it into the right mode?
    # todo: replace with downstream key control
    back_wash_colour_x = 127
    back_wash_colour_y = 127
    back_wash_colour_z = 127
    def set_back_wash_colour(self, dim, value):
        # chan can be A, B or T (both)
        if dim=='x':
            self.back_wash_colour_x = int(255*value)
        elif dim=='y':
            self.back_wash_colour_y = int(255*value)
        elif dim=='z':
            self.back_wash_colour_z = int(255*value)

        #output = "VBW:{:02X}{:02X}{:02X}".format(self.back_wash_colour_x,self.back_wash_colour_y,self.back_wash_colour_z) 
        self.send('VBW', "VBW:{:02X}{:02X}{:02X}", [ self.back_wash_colour_x,self.back_wash_colour_y,self.back_wash_colour_z ] )

    # positioner joystick
    position_x = 127
    position_y = 127
    def set_position(self, mode, dim, value):
        if dim=='y': # yes, y is really x!
            self.position_x = int(255*value)
        elif dim=='x': # yes, x is really y!
            self.position_y = int(255*value)

        #output = "VPS:{}{:02X}{:02X}".format(mode,self.position_x,self.position_y)
        self.send('VPS:{}'.format(mode), "VPS:{}{:02X}{:02X}", [ mode,self.position_x,self.position_y ])#output)

    # wipe / mix level
    def set_mix(self, value):
        #output = "VMM:{:04X}".format(int(255*255*value))
        self.send('VMM', "VMM:{:04X}", [ int(255*255*value) ])#output)

