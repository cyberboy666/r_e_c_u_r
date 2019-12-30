import serial
from serial import Serial
import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin, SequencePlugin

class MidiActionsTestPlugin(ActionsPlugin,SequencePlugin):
    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)
        self.disabled = False

        self.ser = serial.Serial(
    		port='/dev/ttyUSB0',
		baudrate=9600,
	)

        self.macros = [
                "GRI",
                "griV",
                "VXCAV",
                "vYca"
        ]

    @property
    def parserlist(self):
        return [
                ( r"send_serial_macro_([0-9])", self.send_serial_macro )
        ]

    def send_serial_macro(self, macro):
        self.send_serial_string(self.macros[macro])

    def send_serial_string(self, string):
        self.ser.write(string.encode())
        print("sent string %s" % string.encode())
