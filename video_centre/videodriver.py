try:
    from video_centre.video_player import video_player  # <== for deving only
    has_omx = True
except ImportError:
    has_omx = False
    from video_centre.video_player import fake_video_player


class VideoDriver(object):
    def __init__(self, root=None):
        print('has omx :{}'.format(has_omx))
        self.root = root
        self.delay = 5
        self.has_omx = has_omx
        if self.has_omx:
            self.last_player = video_player(self.root, 'a.a')
            self.current_player = video_player(self.root, 'b.b')
            self.next_player = video_player(self.root, 'c.c')
            self.manual_next = False
            self.print_status()
            self.root.after(self.delay, self.begin_playing)
        else:
            self.last_player = fake_video_player()
            self.current_player = fake_video_player()
            self.next_player = fake_video_player()


    def print_status(self):
        print('l({}):{}, c({}):{}, n({}):{}'.format(self.last_player.name, self.last_player.status, self.current_player.name, self.current_player.status, self.next_player.name, self.next_player.status,))
        self.root.after(1000,self.print_status)

    def begin_playing(self):
        # TODO: the first clip will be a demo
        self.current_player.load()
        self.wait_for_first_load()

    def wait_for_first_load(self):
        if self.current_player.is_loaded():
            self.play_video()
        else:
            self.root.after(self.delay, self.wait_for_first_load)

    def switch_players(self):
        temp_player = self.last_player
        self.last_player = self.current_player
        self.current_player = self.next_player
        self.next_player = temp_player
        self.last_player.exit()

    def play_video(self):
        self.current_player.play()
        self.next_player.load()
        self.wait_for_next_cycle()

    def wait_for_next_cycle(self):
        if self.current_player.is_finished() or self.manual_next:
            self.manual_next = False
            self.wait_for_next_load()
        else:
            self.root.after(self.delay, self.wait_for_next_cycle)

    def wait_for_next_load(self):
        if self.next_player.is_loaded():
            self.switch_players()
            self.play_video()
        else:
            self.root.after(self.delay, self.wait_for_next_load)

    def get_info_for_video_display(self):
        if self.has_omx:
            return self.current_player.bank_number, self.current_player.status, self.next_player.bank_number, \
                self.next_player.status, self.current_player.get_position(), self.current_player.length, \
                self.current_player.start, self.current_player.end
        else:
            return 0, 'test', 1, 'test', 0, 10

    def exit_all_players(self):
        self.next_player.exit()
        self.current_player.exit()

