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
    macros = []

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
                ( r"^send_serial_macro_([0-9])$", self.send_serial_macro ),
                ( r"^send_serial_string_(.*)$", self.send_serial_string ),
                #( r"^send_random_colour$", self.send_random_settings ),
                ( r"^open_serial$", self.open_serial ),
                ( r"^wj_send_serial_([0-9a-zA-Z:]*)$", self.send_serial_string ),
                ( r"^wj_set_colour_([A|B|T])_([x|y])$", self.set_colour ),
                ( r"^wj_set_position_([N|L])_([x|y])$", self.set_position )
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

    queue = {}
    def refresh(self):
        #print("refresh called!")
        if not self.ser or self.ser is None:
            self.open_serial()

        for queue, command in self.queue.items():
            self.send_buffered(queue, command)
        self.queue.clear()

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
        if dim=='x':
            self.colour_x = int(255*value)
        elif dim=='y':
            self.colour_y = int(255*value)

        output = "VCC:{}{:02X}{:02X}".format(chan, self.colour_x,self.colour_y) #,random.randint(0,255))
        self.send('VCC', output)

    position_x = 127
    position_y = 127
    def set_position(self, mode, dim, value):
        if dim=='y': # yes, y is really x!
            self.position_x = int(255*value)
        elif dim=='x': # yes, x is really y!
            self.position_y = int(255*value)

        output = "VPS:{}{:02X}{:02X}".format(mode,self.position_x,self.position_y)
        self.send('VPS:{}'.format(mode), output)

    """
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
    """
