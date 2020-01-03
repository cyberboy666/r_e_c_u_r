import serial
from serial import Serial
import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin, SequencePlugin
import threading

class MidiActionsTestPlugin(ActionsPlugin,SequencePlugin):
    ser = None

    commands = "GRAEIVXYZ012345Cgraeivxyzc"

    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)
        self.disabled = False

        self.open_serial()

        self.macros = [
                "GRI0S",
                "griVS",
                "VXCAS",
                "vYca5S"
        ]

    def open_serial(self, port='/dev/ttyUSB0', baudrate=38400):
        if self.ser is not None:
            self.ser.close()
        try:
            self.ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=None
            )
        except Exception as e:
            print ("open_serial failed: " + str(type(e)))
            import traceback
            traceback.print_exc()

    @property
    def parserlist(self):
        return [
                ( r"send_serial_macro_([0-9])", self.send_serial_macro ),
                ( r"send_random_settings", self.send_random_settings ),
                ( r"open_serial", self.open_serial )
        ]

    def send_serial_macro(self, macro):
        self.send_serial_string(self.macros[macro])

    def send_serial_string(self, string):
        try:
            self.ser.write(string.encode())
            print("sent string %s" % string.encode())
            if 'S' in string:
                self.get_device_status()
        except Exception as e:
            print("%s: send_serial_string failed for '%s'" % (e,string.encode()))

    def send_random_settings(self):
        import random
        output = ""
        output += "".join(random.sample(self.commands,5))
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
