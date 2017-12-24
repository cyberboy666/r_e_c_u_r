from omxplayer.player import OMXPlayer
from time import sleep

class omx_player:
	def __init__(self, root):
		self.root = root
		self.path = '/media/pi/TIM1/samplerloop3s.mp4'
		self.player = None

	def play_video(self):
		self.player = OMXPlayer(self.path, pause=False)
		self.check_pause()
		

	def check_pause(self):
		current_position = self.player.position()
		print('the position is {}'.format(current_position))
		if(current_position > 0):
			self.player.pause()
			print('its paused')
		else:
			self.root.after(5,self.check_pause)

	def pause_video(self):
		self.player.play_pause()

	
	
