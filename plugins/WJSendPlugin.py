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

    commands = "GRAEIVXYZ012345Cgraeivxyzc"

    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

        if self.disabled:
            print ("WJSendPlugin is disabled, not opening serial")
            return

        self.open_serial()

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
        except Exception as e:
            print ("open_serial failed: " + str(type(e)))
            import traceback
            traceback.print_exc()

    @property
    def parserlist(self):
        return [
                ( r"^send_serial_macro_([0-9])$", self.send_serial_macro ),
                ( r"^send_serial_string_(.*)$", self.send_serial_string ),
                ( r"^send_random_colour$", self.send_random_settings ),
                ( r"^open_serial$", self.open_serial ),
                ( r"^wj_send_serial_([0-9a-zA-Z:]*)$", self.send_serial_string),
                ( r"^wj_set_colour_x$", self.set_colour_x),
                ( r"^wj_set_colour_y$", self.set_colour_y),
        ]

    def send_serial_macro(self, macro):
        self.send_serial_string(self.macros[macro])

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

    colour_x = 0
    colour_y = 0
    def set_colour_x(self, x):
        self.colour_x = int(x * 255)
        self.set_colour(self.colour_x, self.colour_y)
    def set_colour_y(self, y):
        self.colour_y = int(y * 255)
        self.set_colour(self.colour_x, self.colour_y)

    def set_colour(self, x, y):       
        import random
        #output = "VPS:L{:02x}{:02x}{:02x}".format(x,y,random.randint(0,255))
        output = "VPS:L{:02X}{:02X}".format(x,y) #,random.randint(0,255))
        self.send_serial_string(output)

    def send_random_settings(self):
        import random
        output = ""
        #output += "".join(random.sample(self.commands,5))
        output += "VPS:217%s%s" % (hex(random.randint(0,255)), hex(random.randint(0,255)))
        self.send_serial_string(output)

    def read_serial_string(self): #, what):
        print("starting read?")
        read = self.ser.readline()
        print("read %s" % read)
        self.handle_device_status(reading)

    def get_device_status(self):
        #self.send_serial_string('S')
        #self.read_serial_string(self.handle_device_status)
        print("starting thread to listen?")
        thread = threading.Thread(target=self.read_serial_string)#, args=None)

    def handle_device_status(self, result):
        print("get_device_status got %s" % result)
