import time
#from omxdriver import OMXDriver <== for deving only
from Tkinter import Tk, Canvas
import data_centre

class video_driver(object):
    def __init__(self, widget = None):

        self.widget = widget
        self.delay = 50
        self.last_player = video_player(self.widget,'a')
        self.current_player = video_player(self.widget,'b')
        self.next_player = video_player(self.widget,'c')

        self.manual_next = False

        self.begin_playing()

    def begin_playing(self):
        #TODO: the first clip will be a demo
        first_context = data_centre.get_next_context()
        #first_context = '/home/pi/pp_home/media/samplerloop3s.mp4'
        self.current_player.load_content(first_context)

        self.wait_for_first_load()

    def wait_for_first_load(self):
        if self.current_player.is_loaded():
            self.play_video()
        else:
            #load player states
            self.widget.after(self.delay, self.wait_for_first_load)

    def switch_players(self):
        self.temp_player = self.last_player
        self.last_player = self.current_player
        print('switch: last_player is {}'.format(self.last_player.name))
        self.current_player = self.next_player
        print('switch: current_player is {}'.format(self.current_player.name))
        self.next_player = self.temp_player
        print('switch: next_player is {}'.format(self.next_player.name))
        self.last_player.exit()

    def play_video(self):
        print('{} is about to play'.format(self.current_player.name))
        self.current_player.play_content()
        #self.last_player.exit()

        next_context = data_centre.get_next_context()
        #next_context = '/home/pi/pp_home/media/samplerloop3s.mp4'
        self.next_player.load_content(next_context)

        self.wait_for_next_cycle()


    def wait_for_next_cycle(self):

        if(self.current_player.is_finished() or self.manual_next):
            print('{} is finished'.format(self.current_player.name))
            self.manual_next = False
            if self.next_player.is_loaded():
                print('{} is loaded on switchover'.format(self.next_player.name))
                self.switch_players()
                self.play_video()
            else:
                print('{} is not loaded yet!'.format(self.next_player.name))
                self.current_player.pause_content()
                self.wait_for_next_load()
        else:
            self.widget.after(self.delay, self.wait_for_next_cycle)

    def wait_for_next_load(self):
        if(self.next_player.is_loaded()):
            self.switch_players()
            self.play_video()
        else:
            self.widget.after(self.delay, self.wait_for_next_load)


    def get_info_for_video_display(self):
        return self.current_player.bank_number, self.current_player.status, self.next_player.bank_number,\
               self.next_player.status, self.current_player.duration, self.current_player.video_length


class video_player(object):
    def __init__(self, widget, name):
        self.widget = widget
        self.name = name
        self.status = 'UNASSIGNED'
        self.bank_number = '-'
        self.duration = 0
        self.video_length = 10

        self.omx = OMXDriver(self.widget,'')

    def is_loaded(self):
        return self.omx.start_play_signal

    def is_finished(self):
        return self.omx.end_play_signal

    def get_fake_duration(self):
        self.duration = self.duration + 1
        return self.duration

    def play_content(self):
        self.status = 'PLAYING'
        print('{} is playing now'.format(self.name))
        self.omx.pause_before_play_required = 'no'
        self.omx.show(True,0)

    def load_content(self, context):
        self.status = 'LOADING'
        print('{} is loading now {}'.format(self.name,context))
        self.omx.load(context,'after-first-frame','','')

    def set_to_default(self):
        self.omx.kill()
        self.omx = OMXDriver(self.widget,'')

    def exit(self):
        if(self.omx.omx_loaded is not None):
            print('{} is exiting omx'.format(self.name))
            self.omx.stop()
            self.omx = OMXDriver(self.widget,'')

    def pause_content(self):
        self.status = 'PAUSED'

# tk = Tk()
#
# canvas = Canvas(tk,width=500,height=400, bd=0, highlightthickness=0)
# canvas.pack()
#
# driver = video_driver(canvas)
#
# while True:
#     tk.update()
