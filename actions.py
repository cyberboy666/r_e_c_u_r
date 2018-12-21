import subprocess
import tracemalloc
import data_centre.length_setter as length_setter
import sys
import shlex
import os
from pythonosc import osc_message_builder
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import dispatcher
import git
import threading
import argparse
from video_centre.capture import Capture
from video_centre.of_capture import OfCapture

class Actions(object):
    def __init__(self, tk, message_handler, data, video_driver, shaders, display, osc_client):
        self.tk = tk
        self.message_handler = message_handler
        self.data = data
        self.video_driver = video_driver
        self.shaders = shaders
        self.display = display
        self.osc_client = osc_client
        self.of_capture = OfCapture(self.tk, self.osc_client, self.message_handler, self.data)
        self.python_capture = self.capture = Capture(self.tk, self.message_handler, self.data)
        self.capture = None
        self.serial_port_process = None
        self.openframeworks_process = None
        self.set_capture_object('value')
        self.server = self.setup_osc_server()
        
    def set_capture_object(self, value):
        if self.data.settings['other']['USE_OF_CAPTURE']['value'] == 'yes':
            self.python_capture.close_capture()
            self.capture = self.of_capture
        else:
            self.python_capture.close_capture()
            self.capture = self.python_capture
        self.display.capture = self.capture

    def move_browser_selection_down(self):
        self.display.browser_menu.navigate_menu_down()

    def move_browser_selection_up(self):
        self.display.browser_menu.navigate_menu_up()

    def enter_on_browser_selection(self):
        self.display.browser_menu.enter_on_browser_selection()

    def move_settings_selection_down(self):
        self.display.settings_menu.navigate_menu_down()

    def move_settings_selection_up(self):
        self.display.settings_menu.navigate_menu_up()

    def enter_on_settings_selection(self):
        is_setting, setting = self.display.settings_menu.enter_on_setting_selection()
        if is_setting:
            if setting['action']:
                if setting['value'] is None:
                    getattr(self, setting['action'])()
                else:
                    getattr(self, setting['action'])(setting['value'])

    def move_shaders_selection_down(self):
        self.shaders.shaders_menu.navigate_menu_down()

    def move_shaders_selection_up(self):
        self.shaders.shaders_menu.navigate_menu_up()

    def enter_on_shaders_selection(self):
        ##want to select shader if its not selected, and want to enter 'param' mode if it already is
        is_shader, is_selected_shader, selected_shader = self.shaders.enter_on_shaders_selection()
        print('is selected shader: {}'.format(is_selected_shader))
        if is_selected_shader and selected_shader['param_number'] > 0:
            self.set_shader_param_mode()
        elif is_shader and selected_shader['shad_type'] == 'gen' and self.shaders.selected_status == '▶':
            self.video_driver.current_player.toggle_pause()

    def clear_all_slots(self):
        self.data.clear_all_slots()
        self.display.browser_menu.generate_browser_list()

    def _load_this_slot_into_next_player(self, slot):
        if self.data.update_next_slot_number(slot):
            self.video_driver.reload_next_player()

    def load_slot_0_into_next_player(self):
        self._load_this_slot_into_next_player(0)

    def load_slot_1_into_next_player(self):
        self._load_this_slot_into_next_player(1)

    def load_slot_2_into_next_player(self):
        self._load_this_slot_into_next_player(2)

    def load_slot_3_into_next_player(self):
        self._load_this_slot_into_next_player(3)

    def load_slot_4_into_next_player(self):
        self._load_this_slot_into_next_player(4)

    def load_slot_5_into_next_player(self):
        self._load_this_slot_into_next_player(5)

    def load_slot_6_into_next_player(self):
        self._load_this_slot_into_next_player(6)

    def load_slot_7_into_next_player(self):
        self._load_this_slot_into_next_player(7)

    def load_slot_8_into_next_player(self):
        self._load_this_slot_into_next_player(8)

    def load_slot_9_into_next_player(self):
        self._load_this_slot_into_next_player(9)

    def switch_to_next_player(self):
        self.video_driver.switch_players_and_start_video()

    def cycle_display_mode(self):
        if self.data.settings['other']['VIDEO_BACKEND']['value'] == 'openframeworks':
            display_modes = [["SETTINGS",'NAV_SETTINGS'],[ "SAMPLER",'PLAYER'],["BROWSER",'NAV_BROWSER'],["SHADERS",'NAV_SHADERS']]
        else:
            display_modes = [["BROWSER",'NAV_BROWSER'],["SETTINGS",'NAV_SETTINGS'],[ "SAMPLER",'PLAYER']]

        current_mode_index = [index for index, i in enumerate(display_modes) if self.data.display_mode in i][0]
        next_mode_index = (current_mode_index + 1) % len(display_modes) 
        self.data.display_mode = display_modes[next_mode_index][0]
        self.data.control_mode = display_modes[next_mode_index][1]


    def toggle_action_on_player(self):
        play = 'play' in self.data.settings['sampler']['ON_ACTION']['value']
        show = 'show' in self.data.settings['sampler']['ON_ACTION']['value']
        if play:
            self.toggle_play_on_player()
        if show:
            self.toggle_show_on_player()

    def toggle_play_on_player(self):
        if self.data.player_mode == 'now':
            self.video_driver.current_player.toggle_pause()
        elif self.data.player_mode == 'next':
            self.video_driver.next_player.toggle_pause()

    def toggle_show_on_player(self):
        if self.data.player_mode == 'now':
            self.video_driver.current_player.toggle_show()
        elif self.data.player_mode == 'next':
            self.video_driver.next_player.toggle_show()

    def increase_seek_time(self):
        options = self.data.settings['sampler']['SEEK_TIME']['options']
        current_index = [index for index, item in enumerate(options) if item == self.data.settings['sampler']['SEEK_TIME']['value'] ][0]
        self.data.settings['sampler']['SEEK_TIME']['value'] = options[(current_index + 1) % len(options) ]
        self.message_handler.set_message('INFO', 'The Seek Time is now ' + str(self.data.settings['sampler']['SEEK_TIME']['value']) + 's')


    def decrease_seek_time(self):
        options = self.data.settings['sampler']['SEEK_TIME']['options']
        current_index = [index for index, item in enumerate(options) if item == self.data.settings['sampler']['SEEK_TIME']['value'] ][0]
        self.data.settings['sampler']['SEEK_TIME']['value'] = options[(current_index - 1)  % len(options) ]
        self.message_handler.set_message('INFO', 'The Seek Time is now ' + str(self.data.settings['sampler']['SEEK_TIME']['value']) + 's')
        

    def seek_forward_on_player(self):    
        self.video_driver.current_player.seek(self.data.settings['sampler']['SEEK_TIME']['value'])

    def seek_back_on_player(self):
        self.video_driver.current_player.seek(-(self.data.settings['sampler']['SEEK_TIME']['value']))

    def toggle_function(self):
        self.data.function_on = not self.data.function_on

    def next_bank(self):
        self.data.update_bank_number_by_amount(1)
        print('current bank is {} , the number of banks is {} '.format(self.data.bank_number, len(self.data.bank_data)))

    def previous_bank(self):
        self.data.update_bank_number_by_amount(-1)
        print('current bank is {} , the number of banks is {} '.format(self.data.bank_number, len(self.data.bank_data)))
              
    def increase_speed(self):
        print("increasing speed !")
        new_rate = self.video_driver.current_player.change_rate(1)
        current_bank, current_slot = self.data.split_bankslot_number(self.video_driver.current_player.bankslot_number)
        self.data.update_slot_rate_to_this(current_slot, new_rate)
        #self._load_this_slot_into_next_player(current_slot)

    def decrease_speed(self):
        print("increasing speed !")
        new_rate = self.video_driver.current_player.change_rate(-1)
        current_bank, current_slot = self.data.split_bankslot_number(self.video_driver.current_player.bankslot_number)
        self.data.update_slot_rate_to_this(current_slot, new_rate)
        #self._load_this_slot_into_next_player(current_slot)

    def set_playing_sample_start_to_current_duration(self):
        current_bank, current_slot = self.data.split_bankslot_number(self.video_driver.current_player.bankslot_number)
        current_position = round(self.video_driver.current_player.get_position(),3)
        self.data.update_slot_start_to_this_time(current_slot, current_position)
        self._load_this_slot_into_next_player(current_slot)

    def clear_playing_sample_start_time(self):
        current_bank, current_slot = self.data.split_bankslot_number(self.video_driver.current_player.bankslot_number)
        self.data.update_slot_start_to_this_time(current_slot, -1)
        self._load_this_slot_into_next_player(current_slot)

    def set_playing_sample_end_to_current_duration(self):
        current_bank, current_slot = self.data.split_bankslot_number(self.video_driver.current_player.bankslot_number)
        current_position = round(self.video_driver.current_player.get_position(),0)
        self.data.update_slot_end_to_this_time(current_slot, current_position)
        self._load_this_slot_into_next_player(current_slot)

    def clear_playing_sample_end_time(self):
        current_bank, current_slot = self.data.split_bankslot_number(self.video_driver.current_player.bankslot_number)
        self.data.update_slot_end_to_this_time(current_slot, -1)
        self._load_this_slot_into_next_player(current_slot)

    def toggle_capture_preview(self):
        is_previewing = self.capture.is_previewing
        if is_previewing:
            self.capture.stop_preview()
            if self.video_driver.current_player.status == 'PAUSED':
                self.video_driver.current_player.toggle_pause()
        else:
            is_successful = self.capture.start_preview()
            if is_successful and self.video_driver.current_player.status != 'PAUSED':
                self.video_driver.current_player.toggle_pause()


    def toggle_capture_recording(self):
        is_recording = self.capture.is_recording
        if is_recording:
            self.capture.stop_recording()
        else: 
            self.capture.start_recording()

    def toggle_screen_mirror(self):
        if self.data.settings['other']['DEV_MODE_RESET']['value'] == 'off':
            if self.data.update_screen:
                self.data.update_screen = False
                subprocess.call(['sudo', 'systemctl', 'start', 'raspi2fb@1'])
            else:
                self.data.update_screen = True
                subprocess.call(['sudo', 'systemctl', 'stop', 'raspi2fb@1'])
        else:
            self.message_handler.set_message('INFO', 'cant mirror in dev mode')

    def toggle_shaders(self):
        if self.shaders.selected_status == '▶':
            self.shaders.stop_selected_shader()
            if self.shaders.selected_shader['shad_type'] == 'gen':
                self.video_driver.current_player.toggle_pause()
        elif self.shaders.selected_status == '■':
            self.shaders.start_selected_shader()
            if self.shaders.selected_shader['shad_type'] == 'gen':
                self.video_driver.current_player.toggle_pause()
        else:
            self.message_handler.set_message('INFO', 'no shader loaded')

    def toggle_player_mode(self):
        if self.data.player_mode == 'now':
            self.data.player_mode = 'next'
        elif self.data.player_mode == 'next':
            self.data.player_mode = 'now'

    def set_the_camera_colour_u_continuous(self, amount):
        self.capture.set_colour(amount*255, None)

    def set_the_camera_colour_v_continuous(self, amount):
        self.capture.set_colour(None, amount*255)

    def set_the_camera_alpha_continuous(self, amount):
        self.capture.set_alpha(amount*255)

    def set_the_current_video_alpha_continuous(self, amount):
        self.video_driver.current_player.set_alpha_value(amount*255)

    def set_the_next_video_alpha_continuous(self, amount):
        self.video_driver.next_player.set_alpha_value(amount*255)

    def set_the_shader_param_0_continuous(self, amount):
        self.shaders.set_param_to_amount(0, amount)

    def set_the_shader_param_1_continuous(self, amount):
        self.shaders.set_param_to_amount(1, amount)

    def set_the_shader_param_2_continuous(self, amount):
        self.shaders.set_param_to_amount(2, amount)

    def set_the_shader_param_3_continuous(self, amount):
        self.shaders.set_param_to_amount(3, amount)

    def get_midi_status(self):
        self.message_handler.set_message('INFO', 'midi status is {}'.format(self.data.midi_status))

    def cycle_midi_port_index(self):
        self.data.midi_port_index = self.data.midi_port_index + 1

    def update_video_settings(self, setting_value):
        self.video_driver.update_video_settings()

    def update_capture_settings(self, setting_value):
        self.capture.update_capture_settings()

    def change_piCapture_input(self, setting_value):
        if self.data.settings['capture']['TYPE']['value'] == 'piCaptureSd1':
            subprocess.call(['pivideo', '-s', setting_value])

    def change_output_mode(self, setting_value):
        if setting_value == 'hdmi':
            self.change_hdmi_settings(setting_value)
        elif setting_value == 'composite':
            self.change_composite_setting(setting_value)

    def change_hdmi_settings(self, setting_value):
        if self.data.settings['video']['OUTPUT']['value'] == 'hdmi':
            if self.data.settings['video']['HDMI_MODE']['value'] == 'preferred':
                subprocess.call(['tvservice', '-p'], shell=True)
            elif self.data.settings['video']['HDMI_MODE']['value'] == 'CEA 4 HDMI':
                subprocess.call(['tvservice -e=\"CEA 4 HDMI\"'], shell=True)
            self._refresh_frame_buffer()

    def check_and_set_output_mode_on_boot(self):
        #### checking if pi display mode is composite
        response = str(subprocess.check_output(['tvservice', '-s']))
        print('tvservice response is {}'.format(response))
        if 'PAL' in response or 'NTSC' in response:
            self.data.update_setting_value('video', 'OUTPUT', 'composite')
        else:
            self.data.update_setting_value('video', 'OUTPUT', 'hdmi')
            self.data.update_setting_value('video', 'HDMI_MODE', 'preferred')
            #### this is to work around a bug where 1080 videos on hdmi drop out ...
            #subprocess.call(['tvservice --sdtvon="PAL 4:3"'],shell=True)
            #self._refresh_frame_buffer()
            #subprocess.call(['tvservice', '-p'])
            #self._refresh_frame_buffer()

    def check_dev_mode(self):
        #### check if in dev mode:(ie not using the lcd screen)
        with open('/boot/config.txt', 'r') as config:
                if '##no_waveshare_overlay' in config.read():
                    self.data.update_setting_value('other','DEV_MODE_RESET', 'on')
                else:
                    self.data.update_setting_value('other','DEV_MODE_RESET', 'off')

    def check_if_should_start_openframeworks(self):
        if self.data.settings['other']['VIDEO_BACKEND']['value'] == 'openframeworks':
            self.openframeworks_process = subprocess.Popen(['/home/pi/openFrameworks/apps/myApps/c_o_n_j_u_r/bin/c_o_n_j_u_r'])
            print('conjur pid is {}'.format(self.openframeworks_process.pid))
    def exit_openframeworks(self):
        self.video_driver.osc_client.send_message("/exit", True)

    def toggle_of_screen_size(self, value):
        self.data.update_conjur_dev_mode(value)
        self.video_driver.osc_client.send_message("/dev_mode", True)

    def switch_video_backend(self, state):
        if state == 'openframeworks':
            self.check_if_should_start_openframeworks()
        elif state == 'omxplayer':
            self.exit_openframeworks()
        self.video_driver.reset_all_players()
        

    def change_composite_setting(self, setting_value):
        if setting_value == 'composite':
            mode = self.data.settings['video']['COMPOSITE_TYPE']['value']
            aspect = self.data.settings['video']['COMPOSITE_RATIO']['value']
            progressive = ''
            if self.data.settings['video']['COMPOSITE_PROGRESSIVE']['value'] == 'on':
                progressive = 'p'
            subprocess.call(['tvservice --sdtvon="{} {} {}"'.format(mode, aspect, progressive)],shell=True)
            self._refresh_frame_buffer()
            self.persist_composite_setting(mode, progressive, aspect)

    @staticmethod
    def _refresh_frame_buffer():
        subprocess.run(["fbset -depth 16; fbset -depth 32; xrefresh -display :0" ], shell=True)

    def persist_composite_setting(self, mode, progressive, aspect):
        sdtv_mode = ''
        sdtv_aspect = ''
        print('mode {} , prog {} aspect {} '.format(mode, progressive, aspect))
        if mode == 'PAL' and progressive == 'p':
            sdtv_mode = '18'
        elif mode == 'PAL' and progressive == '':
            sdtv_mode = '02'
        elif mode == 'NTSC' and progressive == 'p':
            sdtv_mode = '16'
        elif mode == 'NTSC' and progressive == '':
            sdtv_mode = '00'

        if aspect == '4:3':
            sdtv_aspect = '1'
        elif aspect == '14:9':
            sdtv_aspect = '2'
        elif aspect == '16:9':
            sdtv_aspect = '3'

        self.update_config_settings(sdtv_mode, sdtv_aspect)

    def update_config_settings(self, sdtv_mode, sdtv_aspect):
        self.run_script('set_composite_mode',sdtv_mode, sdtv_aspect)

    def switch_dev_mode(self, state):
        if state == 'on':
            self.toggle_of_screen_size('dev')
            self.video_driver.osc_client.send_message("/dev_mode", True)
            self.switch_display_to_hdmi()
        elif state == 'off':
            self.toggle_of_screen_size('full')
            self.video_driver.osc_client.send_message("/dev_mode", True)
            self.switch_display_to_lcd()

    def switch_display_to_hdmi(self):
        with open('/boot/config.txt', 'r') as config: 
            with open('/usr/share/X11/xorg.conf.d/99-fbturbo.conf') as framebuffer_conf:
                if 'dtoverlay=waveshare35a:rotate=270' in config.read() and 'dev/fb1' in framebuffer_conf.read():
                    self.run_script('switch_display_to_hdmi')
                else:
                    self.message_handler.set_message('INFO', 'failed to switch display')
        

    def switch_display_to_lcd(self):
        with open('/boot/config.txt', 'r') as config:
            with open('/usr/share/X11/xorg.conf.d/99-fbturbo.conf') as framebuffer_conf:
                if '##no_waveshare_overlay' in config.read() and 'dev/fb0' in framebuffer_conf.read():
                    print('running the switch script')
                    self.run_script('switch_display_to_lcd')
                else:
                    self.message_handler.set_message('INFO', 'failed to switch display')

    def run_script(self, script_name, first_argument='', second_argument=''):
        print('first arg is {} , second is {}'.format(first_argument,second_argument))
        subprocess.call(['/home/pi/r_e_c_u_r/dotfiles/{}.sh'.format(script_name),first_argument, second_argument ])
           
    def toggle_x_autorepeat(self):
        if self.data.auto_repeat_on:
            subprocess.call(['xset', 'r', 'off'])
            self.data.auto_repeat_on = False
        else:
            subprocess.call(['xset', 'r', 'on'])
            self.data.auto_repeat_on = True


    def quit_the_program(self):
        self.video_driver.exit_all_players()
        self.exit_openframeworks()
        self.exit_osc_server('','')
        self.stop_serial_port_process()
        self.stop_openframeworks_process()
        self.toggle_x_autorepeat()
        self.tk.destroy()

    def restart_the_program(self):
        self.quit_the_program()
        os.execv('/usr/bin/python3', [sys.argv[0],'/home/pi/r_e_c_u_r/r_e_c_u_r.py'])
        
    def set_shader_param_mode(self):
        self.data.control_mode = 'SHADER_PARAM'
        self.message_handler.set_message('INFO', '[ ]: focus  < >: level ■: back')
        self.shaders.focused_param = 0

    def increase_this_param(self):
        self.shaders.increase_this_param()

    def decrease_this_param(self):
        self.shaders.decrease_this_param()

    def increase_param_focus(self):
        self.shaders.focused_param = (self.shaders.focused_param + 1)%self.shaders.selected_shader['param_number']

    def decrease_param_focus(self):
        self.shaders.focused_param = (self.shaders.focused_param - 1)%self.shaders.selected_shader['param_number']

    def set_fixed_length(self, value):
        self.data.control_mode = 'LENGTH_SET'
        self.message_handler.set_message('INFO', 'tap: ■ ;   < > : back')
        self.fixed_length_setter = length_setter.FixedLengthSetter(self.data)


    def return_to_default_control_mode(self):
        if self.data.control_mode == 'LENGTH_SET':
            self.data.control_mode = 'NAV_SETTINGS'
        if self.data.control_mode == 'SHADER_PARAM':
            self.data.control_mode = 'NAV_SHADERS'

    def record_fixed_length(self):
        if self.fixed_length_setter:
            self.fixed_length_setter.record_input()
        self.display.settings_menu.generate_settings_list()


    def setup_osc_server(self):
        server_parser = argparse.ArgumentParser()
        server_parser.add_argument("--ip", default="127.0.0.1", help="the ip")
        server_parser.add_argument("--port", type=int, default=9000, help="the port")

        server_args = server_parser.parse_args()

        this_dispatcher = dispatcher.Dispatcher()
        this_dispatcher.map("/player/a/position", self.video_driver.receive_position, "a.a")
        this_dispatcher.map("/player/b/position", self.video_driver.receive_position, "b.b")
        this_dispatcher.map("/player/c/position", self.video_driver.receive_position, "c.c")
        this_dispatcher.map("/player/a/status", self.video_driver.receive_status, "a.a")
        this_dispatcher.map("/player/b/status", self.video_driver.receive_status, "b.b")
        this_dispatcher.map("/player/c/status", self.video_driver.receive_status, "c.c")
        this_dispatcher.map("/shutdown", self.exit_osc_server)
        #this_dispatcher.map("/player/a/status", self.set_status)

        server = osc_server.ThreadingOSCUDPServer((server_args.ip, server_args.port), this_dispatcher)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.start()
        return server

    def exit_osc_server(self, unused_addr, args):
        self.server.shutdown()

    def create_serial_port_process(self):
        if self.serial_port_process == None:
            self.serial_port_process = subprocess.Popen("exec " + "ttymidi -s /dev/serial0 -b 38400 -n serial", shell=True)
            print('created the serial port process ? {}'.format(self.serial_port_process))        

    def stop_serial_port_process(self):
        if self.serial_port_process is not None:
            self.serial_port_process.kill()
            self.serial_port_process = None

    def restart_openframeworks(self):
        self.exit_openframeworks()
        self.stop_openframeworks_process()
        self.check_if_should_start_openframeworks()

    def stop_openframeworks_process(self):
        if self.openframeworks_process is not None:
            print('killing process')
            self.openframeworks_process.kill()
            self.openframeworks_process = None

    def try_pull_code_and_reset(self):
        #self.message_handler.set_message('INFO', 'checkin fo updates pls wait')
        recur_repo = git.Repo("~/r_e_c_u_r")
        conjur_repo = git.Repo("~/openFrameworks/apps/myApps/c_o_n_j_u_r")
        current_recur_hash = recur_repo.head.object.hexsha
        current_conjur_hash = conjur_repo.head.object.hexsha
        try:
            recur_repo.remotes.origin.pull()
            conjur_repo.remotes.origin.pull()
        except git.exc.GitCommandError as e: 
            if 'unable to access' in str(e):
                self.message_handler.set_message('INFO', 'not connected to network')
            else:
                if hasattr(e, 'message'):
                    error_info = e.message
                else:
                    error_info = e
                self.message_handler.set_message('ERROR',error_info)
            return
    
        new_recur_hash = recur_repo.head.object.hexsha
        new_conjur_hash = conjur_repo.head.object.hexsha
        if current_recur_hash != new_recur_hash or current_conjur_hash != new_conjur_hash :
            #something has changed!
            os.remove('/home/pi/r_e_c_u_r/json_objects/settings.json')
            if current_conjur_hash != new_conjur_hash :
                self.message_handler.set_message('INFO', 'compiling OF pls wait')
                self.tk.after(100,self.complie_openframeworks)
            else:
                self.restart_the_program()
        else:
            self.message_handler.set_message('INFO', 'up to date !')

    def complie_openframeworks(self):
        subprocess.call(['make', '--directory=~/openFrameworks/apps/myApps/c_o_n_j_u_r' ])
        self.message_handler.set_message('INFO', 'finished compiling!')
        self.restart_the_program()




        
        
