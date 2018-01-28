try:
    from omxplayer.player import OMXPlayer
except:
    pass


class video_player:
    def __init__(self, root, message_handler, data, name):
        self.root = root
        self.message_handler = message_handler
        self.data = data
        self.omx_player = None
        self.name = name
        self.omx_running = False
        self.status = 'N/A'
        self.total_length = 0.0
        self.slot_number = '-'
        self.start = -1.0
        self.end = -1.0
        self.crop_length = 0.0
        self.location = ''

    def load(self):
        try:
            self.get_context_for_player()
            self.arguments = ['--no-osd', '--win', self.set_screen_size(), '--alpha', '0'] 
            self.status = 'LOADING'
            print('the location is {}'.format(self.location))
            self.omx_player = OMXPlayer(self.location, args=self.arguments, dbus_name=self.name)
            self.omx_running = True
            self.total_length = self.omx_player.duration() # <-- uneeded once self.duration stores float
            if(self.end is -1): 
                self.end = self.total_length
            if(self.start is -1):
                self.start = 0
            self.crop_length = self.end - self.start
            print('{}: the duration is {}'.format(self.name, self.total_length))
            if self.start > 0.5:
                self.set_position(self.start - 0.5)
            self.pause_at_start()
        except:
            self.message_handler.set_message('ERROR', 'first load error')
            self.root.after(100, self.load)

    def pause_at_start(self):
        position = self.get_position()  
        start_threshold = self.start - 0.05
        if position > start_threshold:
            self.status = 'LOADED'
            self.omx_player.pause()
            self.omx_player.set_alpha(255)
        elif self.omx_running:
            self.root.after(5, self.pause_at_start)

    def play(self):
        self.status = 'PLAYING'
        self.omx_player.play()
        self.pause_at_end()

    def pause_at_end(self):
        position = self.get_position()
        end_threshold = self.end - 0.2
        if(position > end_threshold):
            self.status = 'FINISHED'
            self.omx_player.pause()
            print('its paused at end!')
        elif(self.omx_running):
            self.root.after(5, self.pause_at_end)

    def reload(self):
        self.exit()
        self.omx_running = False
        self.load()

    def is_loaded(self):
        return self.status is 'LOADED'

    def is_finished(self):
        return self.status is 'FINISHED'

    def get_position(self):
        try:
            return self.omx_player.position()
        except:
            print('{}: error get_position'.format(self.name))
            return -1

    def get_context_for_player(self):
        next_context = self.data.get_next_context()
        self.location = next_context['location']
        #self.total_length = next_context['length']
        self.start = next_context['start']
        self.end = next_context['end']
        self.slot_number = next_context['slot_number']

    def toggle_pause(self):
        self.omx_player.play_pause()
        self.status = self.omx_player.playback_status().upper()

    def seek(self, amount):
        position = self.get_position()
        after_seek_position = position + amount
        if after_seek_position > self.start and after_seek_position < self.end:
            self.set_position(after_seek_position)
            #self.player.seek(amount)
        else:
            self.message_handler.set_message('INFO', 'can not seek outside range')

    def set_position(self, position):
        self.omx_player.set_position(position)

    def exit(self):
        try:
            self.omx_player.quit()
            self.status = 'N/A'
            self.omx_running = False
        except:
            pass

    def set_screen_size(self):
        if self.data.get_screen_size_setting() == 'dev_mode':
            return '50,350,550,750'
        elif self.data.get_screen_size_setting() == 'composite':
            return '45,15,970,760'
        elif self.data.get_screen_size_setting() == 'XGA':
            return '0,0,1024,768'


class fake_video_player:
    def __init__(self):
        self.player = None
        self.name = 'fake'
        self.omx_running = False
        self.status = 'N/A'
        self.duration = 0
        self.slot_number = '-'
        self.start = -1
        self.end = -1
        self.length = 0
        self.location = ''



