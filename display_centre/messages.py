import logging

class MessageHandler(object):
    def __init__(self):
        self.current_message = [None, None, None]
        self.number_of_messages = 0
        self.logger = self.setup_logging()

    def setup_logging(self):
        logger = logging.getLogger('logfile')
        current_dir = '/home/pi/r_e_c_u_r/'
        hdlr = logging.FileHandler(current_dir + 'logfile.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.ERROR)
        return logger

    def set_message(self, message_type, message, stacktrace=''):
        self.current_message = [message_type, message, True]
        self.number_of_messages = self.number_of_messages + 1
        if message_type is 'ERROR':
            self.logger.error('ERROR MESSAGE IS: {} \n STACKTRACE IS: {}'.format(message, stacktrace))

    def clear_message(self):
        self.number_of_messages = self.number_of_messages - 1
        if self.number_of_messages is 0:
            self.current_message = [None, None, None]

