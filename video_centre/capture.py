import os
import subprocess
import datetime
import picamera

class Capture(object):
    def __init__(self, root, message_handler, data):
        self.root = root
        self.message_handler = message_handler
        self.data = data
        self.use_capture = True
        self.device = None
        self.is_recording = False
        self.is_previewing = False
        self.video_dir = '/home/pi/Videos/'
        self.create_capture_device()

    def create_capture_device(self):
        if self.use_capture:
            try:
                self.device = picamera.PiCamera()
            except picamera.exc.PiCameraError as e:
                self.use_capture = False
                print('camera exception is {}'.format(e))
                self.message_handler.set_message('INFO', 'no capture device attached') 

    def start_preview(self):
        if self.use_capture == False:
            self.message_handler.set_message('INFO', 'capture not enabled')
            return False
        if self.device.closed:
            self.create_capture_device()
        self.is_previewing = True
        self.device.start_preview()
        self.set_preview_screen_size()
        return True            

    def set_preview_screen_size(self):
        if self.data.settings['other']['DEV_MODE_RESET']['value'] == 'on':
            self.device.preview.fullscreen = False
            self.device.preview.window = (50, 350, 500, 400)
        else:
            self.device.preview.fullscreen = True

    def stop_preview(self):
        self.device.stop_preview()
        self.is_previewing = False
        if not self.device.recording:
            self.device.close()

    def start_recording(self):
        if self.use_capture == False:
            self.message_handler.set_message('INFO', 'capture not enabled')
            return
        if not self.check_available_disk_space():
            return
        if self.device.closed:
            self.create_capture_device()
        
        if not os.path.exists(self.video_dir):
            os.makedirs(self.video_dir)
        self.is_recording = True
        self.device.start_recording(self.video_dir + '/raw.h264')
        self.monitor_disk_space()

    def monitor_disk_space(self):
        if self.is_recording:
            if self.check_available_disk_space():
                self.root.after(10000, self.monitor_disk_space)    
            else:
                self.stop_recording()

    def check_available_disk_space(self):
        mb_free = self.data._get_mb_free_diskspace(self.video_dir)
        if mb_free < 10:
            self.message_handler.set_message('INFO', 'insufficient space on disk')
            return False
        else:
            return True

    def stop_recording(self):
        self.device.stop_recording()
        #set status to saving
        mp4box_process, recording_name = self.convert_raw_recording()
        self.is_recording = 'saving'        
        self.root.after(0, self.wait_for_recording_to_save, mp4box_process, recording_name)

        # return path to the video
        if not self.device.preview:
            self.device.close()

    def convert_raw_recording(self):
        recording_path , recording_name = self.generate_recording_path()
        try:
            mp4box_process = subprocess.Popen(['MP4Box', '-add', self.video_dir + '/raw.h264', recording_path])
            return mp4box_process , recording_name
        except Exception as e:
            print(e)
            if hasattr(e, 'message'):
                error_info = e.message
            else:
                error_info = e
            self.message_handler.set_message('ERROR',error_info)
        
    
    def wait_for_recording_to_save(self, process, name):
        print('the poll is {}'.format(process.poll()))
        if process.poll() is not None:
            self.is_recording = False
            os.remove(self.video_dir + '/raw.h264')
            self.data.create_new_slot_mapping_in_first_open(name)
        else:
            self.root.after(300, self.wait_for_recording_to_save, process, name)

    def generate_recording_path(self):
        rec_dir = self.video_dir + '/recordings'
        if not os.path.exists(rec_dir):
            os.makedirs(rec_dir)
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        i = 0
        while os.path.exists('{}/rec-{}-{}.mp4'.format(rec_dir,date, i)):
            i += 1
        name = 'rec-{}-{}.mp4'.format(date, i)
        return '{}/{}'.format(rec_dir,name), name 

    def get_recording_time(self):
        if not self.device or not self.device.recording or self.device.frame.timestamp == None:
            return -1
        else:
            return self.device.frame.timestamp / 1000000

    def is_previewing(self):
        if self.device.closed or not self.device.preview:
            return False
        else:
            return True

    def is_recording(self):
        if self.device.recording:
            return True
        else:
            return False

    def set_colour(self, u_value, v_value):
        (u, v) = (128, 128)
        if self.device.color_effects is not None:
            (u, v) = self.device.color_effects

        if u_value is not None:
            u = u_value
        if v_value is not None:
            v = v_value
        self.device.color_effects = (u, v)

    def set_alpha(self, amount):
        if self.device.preview is not None:
            self.device.preview.alpha = amount

    







