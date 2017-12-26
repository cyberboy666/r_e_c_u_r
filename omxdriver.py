from omxplayer.player import OMXPlayer
from time import sleep

class omx_driver:
    def __init__(self, root, dbus_name):
        self.root = root
        self.path = ''
        self.player = None
        self.status = 'UNASSIGNED'
        self.duration = 0
        self.dbus_name = dbus_name
        self.omx_running = True


    def load(self, location, arguments):
        self.status = 'LOADING'
        self.player = OMXPlayer(location, args=arguments, dbus_name=self.dbus_name)
        self.duration = self.player.duration()
        print('{}: the duration is {}'.format(self.player._dbus_name, self.duration))
        self.pause_at_start()

    def pause_at_start(self):
        position = self.get_position()
        print('{}: the pause_at_start position is {}'.format(self.player._dbus_name, position))
        if(position > -0.05):
            self.status = 'LOADED'
            self.player.pause()
            print('{}: its paused'.format(self.player._dbus_name))
        else:
            self.root.after(5,self.pause_at_start)

    def play(self):
        self.status = 'PLAYING'
        self.player.play()
        self.pause_at_end()

    def pause_at_end(self):
        position = self.get_position()
        print('{}: the pause_at_end position is {}'.format(self.player._dbus_name, position))
        if(position > (self.duration - 0.15 )):
            self.status = 'FINISHED'
            print('time to end is {}'.format(self.duration - position))
            self.player.pause()
            print('its finished')
        elif(self.omx_running):
            self.root.after(5,self.pause_at_end)

    def get_position(self):
        try:
            return self.player.position()
        except:
            return -1

    def toggle_pause(self):
        self.player.play_pause()

        self.status = self.player.playback_status().upper()

    def seek(self, amount):
        self.player.seek(amount)

    def quit(self):
        self.player.quit()
        self.omx_running = False

