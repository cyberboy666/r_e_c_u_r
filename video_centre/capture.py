import os
import subprocess
import datetime
import picamera
import fractions

class Capture(object):
    PREVIEW_LAYER = 255

    def __init__(self, root, message_handler, data):
        self.root = root
        self.message_handler = message_handler
        self.data = data
        
        self.device = None
        self.is_recording = False
        self.is_previewing = False
        self.video_dir = '/home/pi/Videos/'
        self.update_capture_settings()
        self.create_capture_device()

        ## some capture settings


    def create_capture_device(self):
        if self.use_capture:
            if self.piCapture_with_no_source():
                return False
            self.update_capture_settings()
            
            try:
                self.device = picamera.PiCamera(resolution=self.resolution, framerate=self.framerate, sensor_mode = self.sensor_mode)
                return True
            except picamera.exc.PiCameraError as e:
                self.use_capture = False
                self.data.settings['captur']['DEVICE']['value'] = 'disabled'
                print('camera exception is {}'.format(e))
                self.message_handler.set_message('INFO', 'no capture device attached')
                return False

    def piCapture_with_no_source(self):
        is_piCapture = subprocess.check_output(['pivideo', '--query', 'ready'])
        if 'Video Processor was not found' not in str(is_piCapture):
            self.data.settings['captur']['TYPE']['value'] = "piCaptureSd1"
            is_source = subprocess.check_output(['pivideo', '--query', 'lock'])
            if 'No active video detected' in str(is_source):
                self.message_handler.set_message('INFO', 'piCapture detected w no input source')
                return True
        return False

    def update_capture_settings(self):
        ##setting class variables
        self.use_capture = self.data.settings['captur']['DEVICE']['value'] == 'enabled'
        self.resolution = self.convert_resolution_value(self.data.settings['captur']['RESOLUTION']['value'])
        self.framerate = self.convert_framerate_value(self.data.settings['captur']['FRAMERATE']['value'])
        self.capture_type = self.data.settings['captur']['TYPE']['value']
        if self.capture_type == "piCaptureSd1":
            self.sensor_mode = 6
        else:
            self.sensor_mode = 0 
        ##update current instance (device) if in use
        if self.device and not self.device.closed:
            self.device.image_effect = self.data.settings['captur']['IMAGE_EFFECT']['value']
            self.device.shutter_speed = self.convert_shutter_value(self.data.settings['captur']['SHUTTER']['value'])
        ## can only update resolution and framerate if not recording
            if not self.is_recording:
                self.device.framerate = self.framerate
                self.device.resolution = self.resolution
            

    def start_preview(self):
        if self.use_capture == False:
            self.message_handler.set_message('INFO', 'capture not enabled')
            return False
        else:
            if not self.device or self.device.closed:
                is_created = self.create_capture_device()
                if self.use_capture == False or not is_created:
                    return False
            self.is_previewing = True
            self.device.start_preview()
            self.set_preview_screen_size()
            self.set_capture_settings()
            self.device.preview.layer = self.PREVIEW_LAYER
            return True            

    def set_capture_settings(self):
        if self.capture_type == "piCaptureSd1":
            self.device.sensor_mode = 6
            self.device.awb_mode = "off"
            self.device.awb_gains = 1.0
            self.device.exposure_mode = "off"
        else:
            self.sensor_mode = 0
            

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
        if self.device is None or self.device.closed:
            is_created = self.create_capture_device()
            if self.use_capture == False or not is_created:
                return
        
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

        self.update_capture_settings()
        # return path to the video
        if not self.device.preview:
            self.device.close()

    def convert_raw_recording(self):
        recording_path , recording_name = self.generate_recording_path()
        try:
            if self.sensor_mode == 6:
                mp4box_process = subprocess.Popen(['MP4Box', '-fps', '60', '-add', self.video_dir + '/raw.h264', recording_path])
                return mp4box_process , recording_name
            else:
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

    def get_preview_alpha(self):
        if self.is_previewing and self.device is not None:
            try:
                return self.device.preview.alpha
            except Exception as e:
                print(e)
                if hasattr(e, 'message'):
                    error_info = e.message
                else:
                    error_info = e
                self.message_handler.set_message('ERROR',error_info)
                return 0
            return 0

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

    @staticmethod
    def convert_resolution_value(setting_value):
        split_values = setting_value.split('x')
        return (int(split_values[0]), int(split_values[1]))

    @staticmethod
    def convert_framerate_value(setting_value):
        return fractions.Fraction(setting_value).limit_denominator()

    def convert_shutter_value(self, setting_value):
        if setting_value == 'auto':
            return 0
        elif setting_value == 'max':
            return int(1000000 / self.framerate)
        else:
            return int(fractions.Fraction(setting_value) * 1000000)

    def receive_state(self, unused_addr, args):
        pass

    def close_capture(self):
        if self.device is not None:
            print('closing the old camera...')
            self.device.close() 

    def receive_recording_finished(self, path, value):
        pass

