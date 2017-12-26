import time

try:
    from video_player import video_player  # <== for deving only
    has_omx = True
except ImportError:
    has_omx = False
from tkinter import Tk, Canvas
import data_centre
logger = data_centre.setup_logging()
if data_centre.DEV_MODE == "ON":
    screen_size = "--win 250,350,800,800"
else:
    screen_size = '--win 45,15,970,760' #'--blank'

# layer = 0


class video_driver(object):
    def __init__(self, widget=None):
        print('has omx :{}'.format(has_omx))
        self.widget = widget
        self.delay = 5
        logger.info('the has_omx flag is {}'.format(has_omx))
        if has_omx:
            self.last_player = video_player(self.widget, 'a.a')
            self.current_player = video_player(self.widget, 'b.b')
            self.next_player = video_player(self.widget, 'c.c')
            self.manual_next = False

            self.widget.after(self.delay, self.begin_playing)

    def begin_playing(self):
        # TODO: the first clip will be a demo
        # first_context = '/home/pi/pp_home/media/01_trashpalaceintro.mp4'

        self.current_player.load()

        self.wait_for_first_load()

    def wait_for_first_load(self):
        if self.current_player.is_loaded():
            self.play_video()
        else:
            # load player states
            self.widget.after(self.delay, self.wait_for_first_load)

    def switch_players(self):
        self.temp_player = self.last_player
        self.last_player = self.current_player
        logger.info('switch: last_player is {}'.format(self.last_player.name))
        self.current_player = self.next_player
        logger.info('switch: current_player is {}'.format(
            self.current_player.name))
        self.next_player = self.temp_player
        logger.info('switch: next_player is {}'.format(self.next_player.name))
        self.last_player.exit()

    def play_video(self):
        logger.info('{} is about to play'.format(self.current_player.name))
        self.current_player.play()
        # self.last_player.exit()

        self.next_player.load()

        self.wait_for_next_cycle()

    def wait_for_next_cycle(self):

        if (self.current_player.is_finished() or self.manual_next):
            logger.info('{} is finished'.format(self.current_player.name))
            self.manual_next = False
            if (self.next_player.is_loaded()):
                logger.info('{} is loaded on switchover'.format(
                    self.next_player.name))
                self.switch_players()
                self.play_video()
            else:
                logger.info('{} is not loaded yet!'.format(
                    self.next_player.name))
                self.current_player.toggle_pause()
                self.wait_for_next_load()
        else:
            self.widget.after(self.delay, self.wait_for_next_cycle)

    def wait_for_next_load(self):
        if (self.next_player.is_loaded()):
            self.switch_players()
            self.play_video()
        else:
            self.widget.after(self.delay, self.wait_for_next_load)

    def get_info_for_video_display(self):
        if has_omx:
            return self.current_player.bank_number, self.current_player.status, self.next_player.bank_number, \
                self.next_player.status, self.current_player.get_position(), self.current_player.length
        else:
            return 0, 'test', 1, 'test', 0, 10

    def exit_all_players(self):
        self.next_player.exit()
        self.current_player.exit()

