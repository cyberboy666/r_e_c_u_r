import serial
from serial import Serial
import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin, SequencePlugin

class MidiActionsTestPlugin(ActionsPlugin,SequencePlugin):
    ser = None

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

    def open_serial(self, port='/dev/ttyUSB0', baudrate=9600):
        if self.ser is not None:
            self.ser.close()
        try:
            self.ser = serial.Serial(
                port=port,
                baudrate=baudrate
            )
        except Exception as e:
            print ("open_serial failed: " + e)

    @property
    def parserlist(self):
        return [
                ( r"send_serial_macro_([0-9])", self.send_serial_macro ),
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

    def read_serial_string(self, what):
        read = self.ser.readline()
        self.handle_device_status(reading)

    def get_device_status(self):
        #self.send_serial_string('S')
        self.read_serial_string(self.handle_device_status)
        thread = threading.Thread(target=self.read_serial_string)#, args=None)

    def handle_device_status(self, result):
        print("get_device_status got %s" % result)
