import time

try:
    from omxdriver import omx_driver  # <== for deving only
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

        self.current_player.load_content()

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
        self.current_player.play_content()
        # self.last_player.exit()

        self.next_player.load_content()

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
            elif(self.next_player.failed_to_load):
                self.switch_players()
                self.next_player.load_content()
                self.widget.after(self.delay, self.wait_for_next_cycle)
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


class video_player(object):
    def __init__(self, widget, name):
        self.widget = widget
        self.name = name
        self.video_name = ''
        self.status = 'UNASSIGNED'
        self.bank_number = '-'
        self.position = 0
        self.start = ''
        self.end = ''
        self.length = 10
        self.location = ''
        self.failed_to_load = False
        self.omx = omx_driver(self.widget, dbus_name=self.name)

    def is_loaded(self):
        return self.omx.status is 'LOADED'

    def is_finished(self):
        return self.omx.status is 'FINISHED'

    def get_position(self):
        if self.is_loaded():
            return self.omx.get_position()
        else:
            return 0

    def play_content(self):
        
        logger.info('{} is playing now'.format(self.name))
        self.omx.play()

    def load_content(self):
        try:
            self.get_context_for_this_player()
            logger.info('{} is loading now {}'.format(
                self.name,self.location ))
            if self.location == '' :
                data_centre.set_message("failed to load - bank empty")
                print('failed to load')
                self.failed_to_load = True
            else:
                self.omx.load(self.location,
                          ['--no-osd']) #'{}'.format(screen_size), 
        except Exception as e:
            print('load problems, the current message is: {}'.format(e.message))
            data_centre.set_message(e.message)

    def get_context_for_this_player(self):
        next_context = data_centre.get_next_context()
        self.location = next_context['location']
        self.length = next_context['length']
        self.start = next_context['start']
        self.end = next_context['end']
        self.video_name = next_context['name']
        self.bank_number = next_context['bank_number']

    def reload_content(self):
        self.status = 'RELOADING'
        if self.is_loaded():
            self.exit()
        else:
            self.widget.after(50, self.reload_content)
            print("trying to reload")
        self.load_content()

    # layer = layer + 1

    def exit(self):
        try:
            if (self.is_loaded):
                logger.info('{} is exiting omx'.format(self.name))
                self.omx.quit()
                self.omx = omx_driver(self.widget, dbus_name=self.name)
        except Exception as e:
            print('the current message is: {}'.format(e.message))
            data_centre.set_message(e.message)

    def toggle_pause(self):
        self.omx.toggle_pause()

    def jump_video_forward(self):
        self.omx.seek(30)

    def jump_video_back(self):
        self.omx.seek(-30)
            

# tk = Tk()

# canvas = Canvas(tk,width=500,height=400, bd=0, highlightthickness=0)
# canvas.pack()

# driver = video_driver(canvas)

# while True:
#	tk.update()
