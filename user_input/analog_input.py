import Adafruit_MCP3008


class AnalogInput(object):
    def __init__(self, root, message_handler, display, actions, data):
        self.root = root
        self.message_handler = message_handler
        self.display = display
        self.actions = actions
        self.data = data
        self.analog_mappings = data.analog_mappings
        self.analog_delay = 50
        self.last_readings = [0, 0, 0, 0, 0, 0, 0, 0]
        self.analog_input = None
        self.check_if_listening_enabled()

    def check_if_listening_enabled(self):
        if self.data.settings['user_input']['ANALOG_INPUT']['value'] == 'enabled':
            if not self.analog_input:
                try:
                    ## note - using software spi for now although on the same pins as the hardware spi described below because hardware spi wasnt working with lcd display
                    # SPI_PORT   = 1
                    # SPI_DEVICE = 2
                    # self.analog_input = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
                    CLK = 21
                    MISO = 19
                    MOSI = 20
                    CS = 16
                    self.analog_input = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

                except:
                    self.message_handler('INFO', 'analog inputs not connected')
            self.poll_analog_inputs()
        else:
            self.root.after(1000, self.check_if_listening_enabled)

    def poll_analog_inputs(self):
        if self.data.settings['user_input']['ANALOG_INPUT']['value'] == 'enabled':

            for i in range(0, 8):
                if str(i) in self.analog_mappings:
                    this_reading = self.analog_input.read_adc(i)
                    # print(str(this_reading))
                    if abs(this_reading - self.last_readings[i]) > 10:
                        # print('the diff is {}'.format(this_reading - self.last_readings[i]))
                        self.run_action_for_mapped_channel(i, this_reading)
                    self.last_readings[i] = this_reading
            self.root.after(self.analog_delay, self.poll_analog_inputs)
        else:
            self.check_if_listening_enabled()

    def run_action_for_mapped_channel(self, channel, channel_value):
        this_mapping = self.analog_mappings[str(channel)]
        if type(self.data.control_mode) is list:
            mode = 'DEFAULT'
            for cm in self.data.control_mode:
                if cm in this_mapping:
                    mode = cm
                    break
        elif self.data.control_mode in this_mapping:
            mode = self.data.control_mode
        elif 'DEFAULT' in this_mapping:
            mode = 'DEFAULT'

        if self.data.function_on and len(this_mapping[mode]) > 1:
            method_name = this_mapping[mode][1]
            self.data.function_on = False
        else:
            method_name = this_mapping[mode][0]

        if channel_value is not None:
            norm_channel_value = channel_value / 1023
        else:
            norm_channel_value = None

        print('the action being called is {}'.format(method_name))
        self.actions.call_method_name(method_name, norm_channel_value)
        ## not sure whether we want to update the screen in general; here - probably not most of the time ...
        # if 'cc' not in message_name:
        #   self.display.refresh_display()
