import serial
from serial import Serial
import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin, SequencePlugin
import threading

class WJSendPlugin(ActionsPlugin,SequencePlugin):
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


    def open_serial(self, port='/dev/ttyUSB0', baudrate=9600):
        if self.ser is not None:
            self.ser.close()
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
            import traceback
            traceback.print_exc()

    @property
    def parserlist(self):
        return [
                ( r"^open_serial$", self.open_serial ),
                ( r"^wj_send_serial_([0-9a-zA-Z:]*)$", self.send_serial_string ),
                ( r"^wj_set_colour_([A|B|T])_([x|y])$", self.set_colour ),
                ( r"^wj_set_back_colour_([x|y|z])$", self.set_back_colour ),
                ( r"^wj_set_position_([N|L])_([x|y])$", self.set_position ),
                ( r"^wj_set_mix$", self.set_mix ),
                ( r"^wj_send_append_pad_([0-9]*)_(([A-Z:[0-9a-zA-Z])$", self.send_append_pad ),
                ( r"^wj_send_append_([A-Z:[0-9a-zA-Z])$", self.send_append ),
        ]

    def send_serial_string(self, string):
        try:
            print("sending string %s " % string)
            output = b'\2' + string.encode('ascii') + b'\3'
            self.ser.write(output) #.encode())
            print("sent string '%s'" % output) #.encode('ascii'))
            #if 'S' in string:
            #    self.get_device_status()
        except Exception as e:
            print("%s: send_serial_string failed for '%s'" % (e,string.encode()))

    queue = {}
    def refresh(self):
        #print("refresh called!")
        if not self.ser or self.ser is None:
            self.open_serial()

        for queue, command in self.queue.items():
            self.send_buffered(queue, command)
        self.queue.clear()

        if self.ser is not None:
            self.pc.shaders.root.after(self.THROTTLE, self.refresh)

    def send(self, queue, output):
        #self.send_buffered(queue,output)
        self.queue[queue] = output

    last = {}
    def send_buffered(self, queue, output):
        if self.last.get(queue)!=output:
            self.send_serial_string(output)
            self.last[queue] = output

    colour_x = 127
    colour_y = 127
    def set_colour(self, chan, dim, value):
        # chan can be A, B or T (both)
        if dim=='x':
            self.colour_x = int(255*value)
        elif dim=='y':
            self.colour_y = int(255*value)

        output = "VCC:{}{:02X}{:02X}".format(chan, self.colour_x,self.colour_y) #,random.randint(0,255))
        self.send('VCC', output)

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

        output = "VBM:{:02X}{:02X}{:02X}".format(self.back_colour_x,self.back_colour_y,self.back_colour_z) #,random.randint(0,255))
        self.send('VBM', output)

    position_x = 127
    position_y = 127
    def set_position(self, mode, dim, value):
        if dim=='y': # yes, y is really x!
            self.position_x = int(255*value)
        elif dim=='x': # yes, x is really y!
            self.position_y = int(255*value)

        output = "VPS:{}{:02X}{:02X}".format(mode,self.position_x,self.position_y)
        self.send('VPS:{}'.format(mode), output)

    def set_mix(self, value):
        output = "VMM:{:04X}".format(int(255*255*value))
        self.send('VMM', output)


    def send_append(self, command, value):
        # append value to the command as a hex value
        self.send(command.split(':')[0], "{}{:02X}".format(command,int(255*value)))

    def send_append_pad(self, pad, command, value):
        # append value, padded to length
        self.send(command.split(':')[0], ("{}{:0%iX}"%pad).format(command,int(255*value)))
