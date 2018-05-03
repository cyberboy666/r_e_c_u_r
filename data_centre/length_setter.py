import datetime

class FixedLengthSetter(object):
    DELTA_NUMBER = 2 

    def __init__(self, data):
        self.data = data

        self.last_time = None
        self.list_of_deltas = []
    
    def record_input(self):
        if self.last_time == None:
            self.last_time = datetime.datetime.now()
        else:
            now_time = datetime.datetime.now()
            self.list_of_deltas.append(now_time - self.last_time)
            self.last_time = now_time
            if len(self.list_of_deltas) > self.DELTA_NUMBER:
                average_delta = sum(self.list_of_deltas[-self.DELTA_NUMBER+1:], datetime.timedelta(0))/float(self.DELTA_NUMBER)
                average_seconds = round(average_delta.total_seconds(), 2)
                self.data.update_setting_value('sampler', 'FIXED_LENGTH', average_seconds)
