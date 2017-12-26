from omxplayer.player import OMXPlayer
from time import sleep

class omx_driver:
	def __init__(self, root):
		self.root = root
		self.path = ''
		self.player = None
        self.status = 'UNASSIGNED'
        self.duration = ''


	def load(self, location, arguments):
        self.status = 'LOADING'
		self.player = OMXPlayer(location, arguments)
        self.duration = self.player.duration()
        print('the duration is {}'.format(self.duration))
		self.pause_at_start()

	def pause_at_start(self):
		position = self.get_position()
		print('the position is {}'.format(position))
		if(position > 0):
            self.status = 'LOADED'
			self.player.pause()
			print('its paused')
		else:
			self.root.after(5,self.pause_at_start)

    def play(self):
        self.status = 'PLAYING'
        self.player.play()
        self.pause_at_end()

    def pause_at_end(self):
        position = self.get_position()
		print('the position is {}'.format(position))
		if(position > (self.duration - 0.05 )):
            self.status = 'FINISHED'
            print('time to end is {}'.format(self.duration - position))
			self.player.pause()
			print('its finished')
		else:
			self.root.after(5,self.pause_at_end)

	def get_position(self):
		return self.player.position()

    def toggle_pause(self):
        self.player.play_pause()
        self.status = self.player.playback_status().upper()

    def seek(self, amount):
        self.player.seek(amount)

	def quit(self):
        self.player.quit()
	
