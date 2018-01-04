try:
    from omxplayer.player import OMXPlayer
except:
    pass
import data_centre
if data_centre.DEV_MODE == 'ON':
    screen_size = '50,350,550,750'
else:
    screen_size = '45,15,970,760' #'--blank'

class video_player:
    def __init__(self, root, name):
        self.root = root
        self.player = None
        self.name = name
        self.omx_running = False
        self.status = 'N/A'
        self.duration = 0.0
        self.bank_number = '-'
        self.start = -1.0
        self.end = -1.0
        self.length = 0.0
        self.location = ''
        self.arguments = ['--no-osd', '--win', screen_size, '--alpha', '0'] 

    def load(self):
        self.get_context_for_player()

        self.status = 'LOADING'
        self.player = OMXPlayer(self.location, args=self.arguments, dbus_name=self.name)
        self.omx_running = True
        print('duration is: {}'.format(self.duration))
        self.duration = self.player.duration() # <-- uneeded once self.duration stores float
        print('new duration is: {}'.format(self.duration))
        if(self.end is -1): 
            self.end = self.duration
        if(self.start is -1):
            self.start = 0
        print('{}: the duration is {}'.format(self.name, self.duration))
        if(self.start > 0.5):
            self.set_position(self.start - 0.5)
        self.pause_at_start()

    def pause_at_start(self):
        position = self.get_position()  
        start_threshold = self.start - 0.05
        if(position > start_threshold):
            self.status = 'LOADED'
            self.player.pause()
            self.player.set_alpha(255)       
        elif(self.omx_running):
            self.root.after(5,self.pause_at_start)

    def play(self):
        self.status = 'PLAYING'
        self.player.play()
        self.pause_at_end()

    def pause_at_end(self):
        position = self.get_position()
        end_threshold = self.end - 0.2
        if(position > end_threshold):
            self.status = 'FINISHED'
            self.player.pause()
            print('its paused at end!')
        elif(self.omx_running):
            self.root.after(5,self.pause_at_end)

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
            return self.player.position()
        except:
            print('{}: error get_position'.format(self.name))
            return -1

    def get_context_for_player(self):
        next_context = data_centre.get_next_context()
        self.location = next_context['location']
        self.duration = next_context['length']
        self.start = next_context['start']
        self.end = next_context['end']
        self.length = self.end - self.start
        self.bank_number = next_context['bank_number']

    def toggle_pause(self):
        self.player.play_pause()
        self.status = self.player.playback_status().upper()

    def seek(self, amount):
        position = self.get_position()
        after_seek_position = position + amount
        if after_seek_position > self.start and after_seek_position < self.end:
            self.set_position(after_seek_position)
            #self.player.seek(amount)

    def set_position(self, position):
        self.player.set_position(position)

    def exit(self):
        try:
            self.player.quit()
            self.status = 'N/A'
            self.omx_running = False
        except:
            pass

class fake_video_player:
    def __init__(self):
        self.player = None
        self.name = 'fake'
        self.omx_running = False
        self.status = 'N/A'
        self.duration = 0
        self.bank_number = '-'
        self.start = -1
        self.end = -1
        self.length = 0
        self.location = ''



