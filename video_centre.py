import time

import data_centre


class video_driver(object):
    def __init__(self):

        self.last_player = video_player()
        self.current_player = video_player()
        self.next_player = video_player()

        self.manual_next = False

        #self.video_driver.begin_playing()

    def begin_playing(self):
        #TODO:von startup set up the intital data_structures with a preloaded intial clip in bank 0
        first_context = data_centre.get_next_context()
        self.current_player.load_content(first_context)

        self.wait_for_first_load()

    def wait_for_first_load(self):
        if self.current_player.is_loaded:
            self.play_video()
        else:
            #need to wait here then
            time.sleep(1)
            self.wait_for_first_load()

    def switch_players(self):
        self.last_player = self.current_player
        self.current_player = self.next_player
        self.next_player.set_to_default()

    def play_video(self):
        self.current_player.play_content()
        self.last_player.exit()

        next_context = data_centre.get_next_context()
        self.next_player.load_content(next_context)

        self.wait_for_next_cycle()


    def wait_for_next_cycle(self):
        if(self.current_player.is_finished or self.manual_next):
            self.manual_next = False
            if self.next_player.is_loaded:
                self.switch_players()
                self.play_video()
            else:
                self.current_player.pause_content()
                self.wait_for_next_load()
        else:
            #need to delay here and then
            time.sleep(1)
            self.wait_for_next_cycle()

    def wait_for_next_load(self):
        if(self.next_player.is_loaded):
            self.switch_players()
            self.play_video()
        else:
            #need to delay here, and then
            time.sleep(1)
            self.widget.after(self.delay, self._status_loop)
            self.wait_for_next_load()

    def get_info_for_video_display(self):
        return self.current_player.bank_number, self.current_player.status, self.next_player.bank_number,\
               self.next_player.status, self.current_player.duration, self.current_player.video_length


class video_player(object):
    def __init__(self):
        self.is_loaded = False
        self.is_finished = False
        self.status = 'UNASSIGNED'
        self.bank_number = '-'
        self.duration = 0
        self.video_length = 10

    def get_fake_duration(self):
        self.duration = self.duration + 1
        return self.duration

    def play_content(self):
        self.status = 'PLAYING'
        time.sleep(1)
        self.duration = 1
        time.sleep(1)
        self.duration = 2
        time.sleep(1)
        self.duration = 3
        time.sleep(1)
        self.duration = 4
        time.sleep(1)
        self.duration = 5
        time.sleep(1)
        self.duration = 6
        time.sleep(1)
        self.duration = 7
        time.sleep(1)
        self.duration = 8
        time.sleep(1)
        self.duration = 9
        self.is_finished = True
        pass

    def load_content(self, context):
        self.status = 'LOADING'
        time.sleep(3)
        self.status = 'LOADED'
        self.is_loaded = True
        #do the loading...
        pass

    def set_to_default(self):
        self.is_finished = False
        self.is_loaded = False

    def exit(self):
        pass

    def pause_content(self):
        self.status = 'PAUSED'
