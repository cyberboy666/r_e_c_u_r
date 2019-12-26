import subprocess
import tracemalloc
import data_centre.length_setter as length_setter
import sys
import shlex
import os
import re
from pythonosc import osc_message_builder
from pythonosc import dispatcher
from pythonosc import osc_server
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
        if self.data.settings['video']['VIDEOPLAYER_BACKEND']['value'] != 'omxplayer':
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
        if is_selected_shader and selected_shader['param_number'] > 0:
            self.set_shader_param_mode()

    def map_on_shaders_selection(self):
        self.shaders.map_on_shaders_selection()

    def clear_all_slots(self):
        self.data.clear_all_slots()
        self.display.browser_menu.generate_browser_list()

    def _load_this_slot_into_next_player(self, slot):
 ### load next player for seamless type otherwise respect player mode
        if self.data.settings['sampler']['LOOP_TYPE']['value'] == 'seamless':
            if self.data.update_next_slot_number(slot):
                print('should reload next player !! ')
                self.video_driver.reload_next_player()
        else:
            if self.data.player_mode == 'next':
                if self.data.update_next_slot_number(slot, is_current=False):
                    self.video_driver.reload_next_player()
            else:
                if self.data.update_next_slot_number(slot, is_current=True):
                    self.video_driver.reload_current_player()
           


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
        if self.data.settings['sampler']['LOOP_TYPE']['value'] == 'seamless':
            self.video_driver.switch_players_and_start_video()
        else:
            self.video_driver.current_player.toggle_show()
            if self.video_driver.current_player.show_toggle_on == self.video_driver.next_player.show_toggle_on:
                self.video_driver.next_player.toggle_show()


    def cycle_display_mode(self):
        display_modes = self.data.get_display_modes_list(with_nav_mode=True)

        current_mode_index = [index for index, i in enumerate(display_modes) if self.data.display_mode in i][0]
        next_mode_index = (current_mode_index + 1) % len(display_modes) 
        self.data.display_mode = display_modes[next_mode_index][0]
        self.data.control_mode = display_modes[next_mode_index][1]

    def cycle_display_mode_back(self):
        display_modes = self.data.get_display_modes_list(with_nav_mode=True)

        current_mode_index = [index for index, i in enumerate(display_modes) if self.data.display_mode in i][0]
        next_mode_index = (current_mode_index - 1) % len(display_modes) 
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

    def function_on(self):
        self.data.function_on = True

    def function_off(self):
        self.data.function_on = False

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
            #if self.video_driver.current_player.status == 'PAUSED':
                #self.video_driver.current_player.toggle_pause()
        else:
            is_successful = self.capture.start_preview()
            #if is_successful and self.video_driver.current_player.status != 'PAUSED':
                #self.video_driver.current_player.toggle_pause()


    def toggle_capture_recording(self):
        is_recording = self.capture.is_recording
        if is_recording:
            self.capture.stop_recording()
        else: 
            self.capture.start_recording()

    def toggle_screen_mirror(self):
        if self.data.settings['system']['DEV_MODE_RESET']['value'] == 'off':
            if self.data.update_screen:
                self.data.update_screen = False
                subprocess.call(['sudo', 'systemctl', 'start', 'raspi2fb@1'])
            else:
                self.data.update_screen = True
                subprocess.call(['sudo', 'systemctl', 'stop', 'raspi2fb@1'])
        else:
            self.message_handler.set_message('INFO', 'cant mirror in dev mode')

    def toggle_shader_layer(self, layer):
        if self.shaders.selected_status_list[layer] == '▶':
            self.shaders.stop_shader(layer)
        elif self.shaders.selected_status_list[layer] == '■':
            self.shaders.start_shader(layer)
        else:
            self.message_handler.set_message('INFO', "no shader loaded into layer %s" % layer)

    def toggle_shaders(self):
        self.toggle_shader_layer(self.data.shader_layer)

    def toggle_shader_speed(self):
        self.shaders.toggle_shader_speed()

    def toggle_player_mode(self):
        if self.data.player_mode == 'now':
            self.data.player_mode = 'next'
        elif self.data.player_mode == 'next':
            self.data.player_mode = 'now'

    def toggle_detour_mode(self):
        if self.data.settings['detour']['TRY_DEMO']['value'] == 'enabled':
            if self.data.detour_active:
                self.data.detour_active = False
                self.video_driver.osc_client.send_message("/detour/end", True)
            else:
                self.data.detour_active = True
                shader_input = self.data.settings['detour']['SHADER_POSITION']['value'] == 'input'
                self.video_driver.osc_client.send_message("/detour/start", shader_input)
                self.load_this_detour_shader() 

    def toggle_detour_play(self):
        if self.data.settings['detour']['TRY_DEMO']['value'] == 'enabled':
            is_playing =  not self.data.detour_settings['is_playing']
            self.data.detour_settings['is_playing'] = is_playing 
            self.video_driver.osc_client.send_message("/detour/is_playing", is_playing)

    def toggle_feedback(self):
        print('toggle here')
        self.set_feedback_state(not self.data.feedback_active)

    def enable_feedback(self):
        self.set_feedback_state(True)

    def disable_feedback(self):
        self.set_feedback_state(False)

    def set_feedback_state(self, state):
        self.data.feedback_active = state
        self.video_driver.osc_client.send_message("/toggle_feedback", self.data.feedback_active)

    def play_shader_0(self):
        self.play_this_shader(0)

    def play_shader_1(self):
        self.play_this_shader(1)

    def play_shader_2(self):
        self.play_this_shader(2)

    def play_shader_3(self):
        self.play_this_shader(3)

    def play_shader_4(self):
        self.play_this_shader(4)

    def play_shader_5(self):
        self.play_this_shader(5)

    def play_shader_6(self):
        self.play_this_shader(6)

    def play_shader_7(self):
        self.play_this_shader(7)

    def play_shader_8(self):
        self.play_this_shader(8)

    def play_shader_9(self):
        self.play_this_shader(9)

    def play_this_shader(self, number):
        self.shaders.play_this_shader(number)

    def previous_shader_layer(self):
        self.data.update_shader_layer_by_amount(-1)

    def next_shader_layer(self):
        self.data.update_shader_layer_by_amount(1)

    def clear_shader_bank(self):
        self.data.clear_all_shader_slots()

    def toggle_x3_as_speed(self):
        if self.data.settings['shader']['X3_AS_SPEED']['value'] == 'enabled':
            self.shaders.set_x3_as_speed(False)
        else:
            self.shaders.set_x3_as_speed(True)

    def toggle_detour_record(self):
        if self.data.settings['detour']['TRY_DEMO']['value'] == 'enabled':
            is_recording =  not self.data.detour_settings['is_recording']
            self.data.detour_settings['is_recording'] = is_recording 
            self.video_driver.osc_client.send_message("/detour/is_recording", is_recording)

    def toggle_detour_record_loop(self):
        if self.data.settings['detour']['TRY_DEMO']['value'] == 'enabled':
            record_loop = not self.data.detour_settings['record_loop']
            self.data.detour_settings['record_loop'] = record_loop 
            self.video_driver.osc_client.send_message("/detour/record_loop", record_loop)

    def clear_this_detour(self):
        if self.data.settings['detour']['TRY_DEMO']['value'] == 'enabled':
            self.video_driver.osc_client.send_message("/detour/clear_this_detour", True)

    def increase_mix_shader(self):
        if self.data.settings['detour']['TRY_DEMO']['value'] == 'enabled':
            l = self.data.detour_mix_shaders
            self.data.detour_mix_shaders = l[1:] + l[:1]
            self.data.detour_settings['mix_shader'] = l[0]
            self.load_this_detour_shader()

    def decrease_mix_shader(self):
        if self.data.settings['detour']['TRY_DEMO']['value'] == 'enabled':
            l = self.data.detour_mix_shaders
            self.data.detour_mix_shaders = l[-1:] + l[:-1]
            self.data.detour_settings['mix_shader'] = l[0]
            self.load_this_detour_shader()

    def load_this_detour_shader(self):
        self.video_driver.osc_client.send_message("/detour/load_mix", "/home/pi/r_e_c_u_r/Shaders/2-input/" + self.data.detour_settings['mix_shader'])

    def switch_to_detour_0(self):
        self.switch_to_this_detour(0)

    def switch_to_detour_1(self):
        self.switch_to_this_detour(1)

    def switch_to_detour_2(self):
        self.switch_to_this_detour(2)

    def switch_to_detour_3(self):
        self.switch_to_this_detour(3)

    def switch_to_this_detour(self, number):
        if self.data.settings['detour']['TRY_DEMO']['value'] == 'enabled':
            self.data.detour_settings['current_detour'] = number 
            self.video_driver.osc_client.send_message("/detour/switch_to_detour_number", number)


    def set_detour_delay_mode(self, state):
        self.video_driver.osc_client.send_message("/detour/set_delay_mode", state == 'enabled')
        self.data.update_conjur_delay_mode(state == 'enabled')

    def set_detour_speed_position_continuous(self, amount):
        self.video_driver.osc_client.send_message("/detour/set_speed_position", amount)

    def set_detour_start_continuous(self, amount):
        self.video_driver.osc_client.send_message("/detour/set_start", amount)

    def set_detour_end_continuous(self, amount):
        self.video_driver.osc_client.send_message("/detour/set_end", amount)

    def set_detour_mix_continuous(self, amount):
        self.video_driver.osc_client.send_message("/detour/set_mix", amount)

    def receive_detour_info(self, unused_addr, position, start, end, size, speed, mix, memory_full):
        self.data.detour_settings['detour_position'] = position
        self.data.detour_settings['detour_start'] = start
        self.data.detour_settings['detour_end'] = end
        self.data.detour_settings['detour_size'] = size
        self.data.detour_settings['detour_speed'] = round(speed, 2)
        self.data.detour_settings['detour_mix'] = round(mix, 4)
        self.data.detour_settings['memory_full'] = memory_full

    def set_the_detour_mix_0(self):
        self.set_detour_mix_continuous(0)

    def set_the_detour_mix_1(self):
        self.set_detour_mix_continuous(1)

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

    def set_the_shader_param_0_layer_offset_0_continuous(self, amount):
        self.shaders.set_param_to_amount(0, amount, layer_offset=0)

    def set_the_shader_param_1_layer_offset_0_continuous(self, amount):
        self.shaders.set_param_to_amount(1, amount, layer_offset=0)

    def set_the_shader_param_2_layer_offset_0_continuous(self, amount):
        self.shaders.set_param_to_amount(2, amount, layer_offset=0)

    def set_the_shader_param_3_layer_offset_0_continuous(self, amount):
        self.shaders.set_param_to_amount(3, amount, layer_offset=0)

    def set_the_shader_param_0_layer_offset_1_continuous(self, amount):
        self.shaders.set_param_to_amount(0, amount, layer_offset=1)

    def set_the_shader_param_1_layer_offset_1_continuous(self, amount):
        self.shaders.set_param_to_amount(1, amount, layer_offset=1)

    def set_the_shader_param_2_layer_offset_1_continuous(self, amount):
        self.shaders.set_param_to_amount(2, amount, layer_offset=1)

    def set_the_shader_param_3_layer_offset_1_continuous(self, amount):
        self.shaders.set_param_to_amount(3, amount, layer_offset=1)

    def set_the_shader_param_0_layer_offset_2_continuous(self, amount):
        self.shaders.set_param_to_amount(0, amount, layer_offset=2)

    def set_the_shader_param_1_layer_offset_2_continuous(self, amount):
        self.shaders.set_param_to_amount(1, amount, layer_offset=2)

    def set_the_shader_param_2_layer_offset_2_continuous(self, amount):
        self.shaders.set_param_to_amount(2, amount, layer_offset=2)

    def set_the_shader_param_3_layer_offset_2_continuous(self, amount):
        self.shaders.set_param_to_amount(3, amount, layer_offset=2)

    def set_the_shader_param_0_layer_offset_3_continuous(self, amount):
        self.shaders.set_param_to_amount(0, amount, layer_offset=2)

    def set_the_shader_param_1_layer_offset_3_continuous(self, amount):
        self.shaders.set_param_to_amount(1, amount, layer_offset=2)

    def set_the_shader_param_2_layer_offset_3_continuous(self, amount):
        self.shaders.set_param_to_amount(2, amount, layer_offset=2)

    def set_the_shader_param_3_layer_offset_3_continuous(self, amount):
        self.shaders.set_param_to_amount(3, amount, layer_offset=2)

    def set_strobe_amount_continuous(self, amount):
        scaled_amount = int(amount * 10)
        if self.data.settings['shader']['STROBE_AMOUNT']['value'] != scaled_amount:
            print(scaled_amount)
            self.video_driver.osc_client.send_message("/set_strobe", scaled_amount)
            self.data.settings['shader']['STROBE_AMOUNT']['value'] = scaled_amount

    def get_midi_status(self):
        self.message_handler.set_message('INFO', ("midi status is {} to %s"%(self.data.midi_device_name)).format(self.data.midi_status))

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
        ### this seems no longer supported in the firmware...
        if setting_value == 'hdmi':
            self.change_hdmi_settings(setting_value)
        elif setting_value == 'composite':
            self.change_composite_setting(setting_value)
        self.restart_openframeworks()

    def change_hdmi_settings(self, setting_value):
        if self.data.settings['video']['OUTPUT']['value'] == 'hdmi':
            if self.data.settings['video']['HDMI_MODE']['value'] == 'preferred':
                subprocess.call(['tvservice --preferred'], shell=True)
            elif self.data.settings['video']['HDMI_MODE']['value'] == 'CEA 4 HDMI':
                subprocess.call(['tvservice -e=\"CEA 4 HDMI\"'], shell=True)
            elif self.data.settings['video']['HDMI_MODE']['value'] == 'CEA 17 HDMI':
                subprocess.call(['tvservice -e=\"CEA 17 HDMI\"'], shell=True)
            elif self.data.settings['video']['HDMI_MODE']['value'] == 'CEA 1 HDMI':
                subprocess.call(['tvservice -e=\"CEA 1 HDMI\"'], shell=True)
            self.refresh_frame_buffer_and_restart_openframeworks()

    def check_and_set_output_mode_on_boot(self):
        #### checking if pi display mode is composite
        response = str(subprocess.check_output(['tvservice', '-s']))
        print('tvservice response is {}'.format(response))
        if 'PAL' in response or 'NTSC' in response:
            self.data.update_setting_value('video', 'OUTPUT', 'composite')
        else:
            self.data.update_setting_value('video', 'OUTPUT', 'hdmi')
            
            if self.data.settings['video']['HDMI_MODE']['value'] == "CEA 4 HDMI":
                
                self.data.update_setting_value('video', 'HDMI_MODE', 'CEA 4 HDMI')

                self.change_hdmi_settings('CEA 4 HDMI')
                

    def check_dev_mode(self):
        #### check if in dev mode:(ie not using the lcd screen)
        with open('/boot/config.txt', 'r') as config:
                if '##no_waveshare_overlay' in config.read():
                    self.data.update_setting_value('system','DEV_MODE_RESET', 'on')
                else:
                    self.data.update_setting_value('system','DEV_MODE_RESET', 'off')

    def check_if_should_start_openframeworks(self):
        if self.data.settings['video']['VIDEOPLAYER_BACKEND']['value'] != 'omxplayer':
            self.openframeworks_process = subprocess.Popen([self.data.PATH_TO_OPENFRAMEWORKS +'apps/myApps/c_o_n_j_u_r/bin/c_o_n_j_u_r'])
            print('conjur pid is {}'.format(self.openframeworks_process.pid))

    def exit_openframeworks(self):
        self.video_driver.osc_client.send_message("/exit", True)

    def switch_conjur_player_type(self, value):
        self.data.update_conjur_player_type(value)
        self.restart_openframeworks()

    def toggle_of_screen_size(self, value):
        self.data.update_conjur_dev_mode(value)
        self.video_driver.osc_client.send_message("/dev_mode", True)

    def switch_video_backend(self, state):
        if state == 'ofvideoplayer' or state == 'ofxomxplayer':
            self.switch_conjur_player_type(state)
        elif state == 'omxplayer':
            self.data.update_setting_value('sampler', 'LOOP_TYPE', 'seamless')
            self.exit_openframeworks()
        self.set_capture_object('nothing')
        self.display.settings_menu.generate_settings_list()
        self.reset_players()
        
    def reset_players(self):
        self.video_driver.reset_all_players()

    def change_composite_setting(self, setting_value):
        output = self.data.settings['video']['OUTPUT']['value']
        mode = self.data.settings['video']['COMPOSITE_TYPE']['value']
        aspect = self.data.settings['video']['COMPOSITE_RATIO']['value']
        progressive = ''
        if self.data.settings['video']['COMPOSITE_PROGRESSIVE']['value'] == 'on':
            progressive = 'p'
        
        if output == 'composite':
            subprocess.call(['tvservice --sdtvon="{} {} {}"'.format(mode, aspect, progressive)],shell=True)
            self.refresh_frame_buffer_and_restart_openframeworks()
        self.persist_composite_setting(mode, progressive, aspect)

    
    def _refresh_frame_buffer(self):
        self.data.open_omxplayer_for_reset()
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
        self.shaders.increase_this_param(self.data.settings['shader']['SHADER_PARAM']['value'])

    def decrease_this_param(self):
        self.shaders.decrease_this_param(self.data.settings['shader']['SHADER_PARAM']['value'])

    def increase_param_focus(self):
        self.shaders.focused_param = (self.shaders.focused_param + 1)%self.shaders.selected_shader_list[self.data.shader_layer]['param_number']

    def decrease_param_focus(self):
        self.shaders.focused_param = (self.shaders.focused_param - 1)%self.shaders.selected_shader_list[self.data.shader_layer]['param_number']

    def increase_shader_param(self):
        options = self.data.settings['shader']['SHADER_PARAM']['options']
        current_index = [index for index, item in enumerate(options) if item == self.data.settings['shader']['SHADER_PARAM']['value'] ][0]
        self.data.settings['shader']['SHADER_PARAM']['value'] = options[(current_index + 1) % len(options) ]
        self.message_handler.set_message('INFO', 'The Param amount is now ' + str(self.data.settings['shader']['SHADER_PARAM']['value']))

    def decrease_shader_param(self):
        options = self.data.settings['shader']['SHADER_PARAM']['options']
        current_index = [index for index, item in enumerate(options) if item == self.data.settings['shader']['SHADER_PARAM']['value'] ][0]
        self.data.settings['shader']['SHADER_PARAM']['value'] = options[(current_index - 1) % len(options) ]
        self.message_handler.set_message('INFO', 'The Param amount is now ' + str(self.data.settings['shader']['SHADER_PARAM']['value']))


    def set_fixed_length(self, value):
        self.data.control_mode = 'LENGTH_SET'
        self.message_handler.set_message('INFO', 'tap: ■ ;   < > : back')
        self.fixed_length_setter = length_setter.FixedLengthSetter(self.data)


    def return_to_default_control_mode(self):
        display_list = self.data.get_display_modes_list(with_nav_mode=True)
        for display, control in display_list:
            if display == self.data.display_mode:
                 self.data.control_mode = control

    def perform_confirm_action(self):
        action = self.data.confirm_action
        if action:
            getattr(self, action)()
        self.data.confirm_action = None

    def start_confirm_action(self, action_title, message=None):
        if not message:
            message = action_title
        self.data.confirm_action = action_title
        self.data.control_mode = 'CONFIRM'
        self.message_handler.set_message('INFO', 'confirm: {} ■:y < >:no'.format(action_title[:22]))

    def confirm_shutdown(self):
        self.start_confirm_action('shutdown_pi' )

    def confirm_quit(self):
        self.start_confirm_action('quit_the_program', message='quit' )

    def confirm_switch_dev_mode(self, state):
        # i startd writing a confirm dev mod but it messed with the state if you say no ...
        self.start_confirm_action('switch_dev_mode', args=[state])

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
        this_dispatcher.map("/detour/detour_info", self.receive_detour_info)
        this_dispatcher.map("/capture/recording_finished", self.capture.receive_recording_finished)
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
        self.reset_players()
        self.exit_openframeworks()
        self.stop_openframeworks_process()
        self.check_if_should_start_openframeworks()        

    def refresh_frame_buffer_and_restart_openframeworks(self):
        if self.data.settings['video']['VIDEOPLAYER_BACKEND']['value'] != 'omxplayer':
            self.exit_openframeworks()
            self.reset_players()
            self.stop_openframeworks_process()
            self._refresh_frame_buffer()
            self.check_if_should_start_openframeworks()
            #self.tk.after(1000, self.check_if_should_start_openframeworks)
        else:
            self._refresh_frame_buffer()

    def stop_openframeworks_process(self):
        if self.openframeworks_process is not None:
            print('killing process')
            self.openframeworks_process.kill()
            self.openframeworks_process = None
            subprocess.call(['killall', 'c_o_n_j_u_r'])

    def try_pull_code_and_reset(self):
        #self.message_handler.set_message('INFO', 'checkin fo updates pls wait')
        recur_repo = git.Repo("~/r_e_c_u_r")
        conjur_repo = git.Repo(self.data.PATH_TO_OPENFRAMEWORKS + "apps/myApps/c_o_n_j_u_r")
        ofxVideoArtTools_repo = git.Repo(self.data.PATH_TO_OPENFRAMEWORKS +  "/addons/ofxVideoArtTools")
        current_recur_hash = recur_repo.head.object.hexsha
        current_conjur_hash = conjur_repo.head.object.hexsha
        current_ofxVideoArtTools_hash = ofxVideoArtTools_repo.head.object.hexsha

        self.data.try_remove_file(self.data.PATH_TO_DATA_OBJECTS + self.data.SETTINGS_JSON )
        self.data.try_remove_file(self.data.PATH_TO_DEFAULT_CONJUR_DATA) 
        try:
            recur_repo.remotes.origin.pull()
            conjur_repo.remotes.origin.pull()
            ofxVideoArtTools_repo.remotes.origin.pull()
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
        new_ofxVideoArtTools_hash = ofxVideoArtTools_repo.head.object.hexsha
        if current_recur_hash != new_recur_hash or current_conjur_hash != new_conjur_hash or current_ofxVideoArtTools_hash != new_ofxVideoArtTools_hash :
            #something has changed!            
            self.restart_the_program()
        else:
            self.message_handler.set_message('INFO', 'up to date !')

#    def complie_openframeworks(self):
#        subprocess.call(['make', '--directory=' + self.data.PATH_TO_OPENFRAMEWORKS + 'apps/myApps/c_o_n_j_u_r' ])
#        self.message_handler.set_message('INFO', 'finished compiling!')
#        self.restart_the_program()

    def shutdown_pi(self):
        subprocess.call(['sudo', 'shutdown', '-h', 'now'])

    def clear_message(self):
        self.message_handler.clear_all_messages()

    @staticmethod
    def try_remove_file(path):
        if os.path.exists(path):
            os.remove(path)

    # TODO: make this interrogate the various components for available routes to parse
    # this would include eg a custom script module..
    @property
    def parserlist(self):
        return {
                ( r"play_shader_([0-9])_([0-9])", self.shaders.play_that_shader ),
                ( r"toggle_shader_layer_([0-2])", self.toggle_shader_layer ),
                ( r"start_shader_layer_([0-2])",  self.shaders.start_shader ),
                ( r"stop_shader_layer_([0-2])",   self.shaders.stop_shader ),
                ( r"set_the_shader_param_([0-3])_layer_([0-2])_continuous",      self.shaders.set_param_layer_to_amount ),
                ( r"modulate_the_shader_param_([0-3])_layer_([0-2])_continuous", self.shaders.modulate_param_layer_to_amount ),
                ( r"modulate_the_shader_param_([0-3])_layer_offset_([0-2])_continuous", self.shaders.modulate_param_layer_offset_to_amount ),
                ( r"set_shader_speed_layer_offset_([0-2])_amount",               self.shaders.set_speed_offset_to_amount ),
                ( r"set_shader_speed_layer_([0-2])_amount",                      self.shaders.set_speed_layer_to_amount ),
        }

    def get_callback_for_method(self, method_name, argument):
        for a in self.parserlist:
            regex = a[0]
            me = a[1]
            matches = re.search(regex, method_name)

            if matches:
                found_method = me 
                parsed_args = list(map(int,matches.groups()))
                if argument is not None:
                    args = parsed_args + [argument]
                else:
                    args = parsed_args 
                
                return (found_method, args)

    def call_method_name(self, method_name, argument=None):
        # if the target method doesnt exist, call the handler
        if not hasattr(self, method_name):
            self.call_parse_method_name(method_name, argument)
            return

        if argument is not None:
            getattr(self, method_name)(argument)
        else:
            getattr(self, method_name)()


    def call_parse_method_name(self, method_name, argument):
        # first test if a registered plugin handles this for us
        from data_centre.plugin_collection import ActionsPlugin
        for plugin in self.data.plugins.get_plugins(ActionsPlugin):
            if plugin.is_handled(method_name):
                print ("Plugin %s is handling %s" % (plugin, method_name))
                method, arguments = plugin.get_callback_for_method(method_name, argument)
                method(*arguments)
                return

        # if not then fall back to using internal method
        try:
            method, arguments = self.get_callback_for_method(method_name, argument)
            method(*arguments)
        except:
            print ("Failed to find a method for '%s'" % method_name)
            import traceback
            traceback.print_exc()

