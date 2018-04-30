from omxplayer.player import OMXPlayer

class VideoPlayer:
    def __init__(self, root, message_handler, data, name):
        self.root = root
        self.message_handler = message_handler
        self.data = data
        self.omx_player = None
        self.name = name
        self.omx_running = False
        self.status = 'N/A'
        self.total_length = 0.0
        self.bankslot_number = '*-*'
        self.start = -1.0
        self.end = -1.0
        self.rate = 1
        self.crop_length = 0.0
        self.location = ''
        self.load_attempts = 0

        self.show_toggle_on = True

    def try_load(self, layer ,show):
        load_attempts = 0
        while(load_attempts < 2):
            load_attempts = load_attempts + 1
            if self.load(layer, show):
                print('load success')
                return True
            else:
                print('load failed')
        self.message_handler.set_message('ERROR', 'failed to load')
        self.status = 'ERROR'
        return False
            

    def load(self, layer , show):
        try:
            self.get_context_for_player()
            is_dev_mode, first_screen_arg, second_screen_arg = self.set_screen_size_for_dev_mode()
            arguments = ['--no-osd', '--layer', str(layer), '--adev', 'local', '--alpha', '0', first_screen_arg, second_screen_arg]
            if not is_dev_mode:
                arguments.append('-b')
            self.status = 'LOADING'
            print('the location is {}'.format(self.location))
            self.omx_player = OMXPlayer(self.location, args=arguments, dbus_name=self.name)
            self.omx_running = True
            self.total_length = self.omx_player.duration() # <-- uneeded once self.duration stores float
            if(self.end is -1): 
                self.end = self.total_length
            if(self.start is -1):
                self.start = 0
            self.crop_length = self.end - self.start
            print('{}: the duration is {}'.format(self.name, self.total_length))
            if self.start > 0.9:
                self.set_position(self.start - 0.9)
            self.pause_at_start(show)
            #print('set rate to {}'.format(self.rate))
            #self.omx_player.set_rate(self.rate)
            #self.load_attempts = 0
            return True
        except (ValueError, SystemError):
            #self.message_handler.set_message('ERROR', 'load attempt fail')
            return False

    def pause_at_start(self, show):
        position = self.get_position()
        start_threshold = round(self.start - 0.05,2)
        #print('is playing: {} , position : {} , start_threshold : {}'.format(self.omx_player.is_playing(), position, start_threshold))
        if position > start_threshold:
            self.status = 'LOADED'
            if show:
                self.omx_player.set_alpha(255)
            else:
                self.omx_player.set_alpha(0)
            #self.omx_player.pause()
        elif self.omx_running:
            self.root.after(5, self.pause_at_start, show)

    def play(self, show):
        self.status = 'PLAYING'
        if show:
            self.omx_player.set_alpha(255)
        else:
            self.omx_player.set_alpha(0)
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

    def reload(self, layer, show):
        self.exit()
        self.omx_running = False
        self.try_load(layer, show)

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
        self.bankslot_number = next_context['bankslot_number']
        self.rate = next_context['rate']

    def toggle_pause(self):
        self.omx_player.play_pause()
        self.status = self.omx_player.playback_status().upper()

    def toggle_show(self):
        if self.show_toggle_on:
            self.show_toggle_on = False
            self.omx_player.set_alpha(0)
        else:
            self.show_toggle_on = True
            self.omx_player.set_alpha(255)

    def seek(self, amount):
        position = self.get_position()
        after_seek_position = position + amount
        if after_seek_position > self.start and after_seek_position < self.end:
            self.set_position(after_seek_position)
            #self.player.seek(amount)
        else:
            self.message_handler.set_message('INFO', 'can not seek outside range')

    def change_rate(self, amount):
        new_rate = self.rate + amount
        if (new_rate > self.omx_player.minimum_rate() and new_rate < self.omx_player.maximum_rate()):
            updated_speed = self.omx_player.set_rate(new_rate)
            self.rate = new_rate
            print('max rate {} , min rate {} '.format(self.omx_player.maximum_rate() ,self.omx_player.minimum_rate()))
            return new_rate
        else:
            self.message_handler.set_message('INFO', 'can not set speed outside of range')
            return self.rate

    def set_position(self, position):
        self.omx_player.set_position(position)

    def exit(self):
        try:
            self.omx_player.quit()
            self.status = 'N/A'
            self.omx_running = False
        except:
            pass

    def set_screen_size_for_dev_mode(self):
        ## only dev mode is needed now that auto handles all modes... can be removed probably ...
        if self.data.settings['other']['DEV_MODE_RESET']['value'] == 'on':
            return True, '--win', '50,350,550,750'
        else:
            aspect_mode = self.data.settings['video']['SCREEN_MODE']['value']
            return False, '--aspect-mode', aspect_mode


