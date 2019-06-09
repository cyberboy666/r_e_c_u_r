import os
import subprocess
import datetime
import fractions
import picamera

class OfCapture(object):
    def __init__(self, root, osc_client, message_handler, data):
        self.root = root
        self.osc_client = osc_client
        self.message_handler = message_handler
        self.data = data
        
        self.has_capture = False
        self.is_recording = False
        self.is_previewing = False
        self.video_dir = '/home/pi/Videos/'
        self.update_capture_settings()
        #self.create_capture_device()

    def create_capture_device(self):
        if self.use_capture:
            if self.piCapture_with_no_source():
                print('its picapture with no source !')
                return False
            self.update_capture_settings()
            if not self.check_if_attached_with_picamera():
                return
            
            print('sending setup message !')
            self.osc_client.send_message("/capture/setup", self.capture_type)
            self.has_capture = True
            return True


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

        #self.device.image_effect = self.data.settings['captur']['IMAGE_EFFECT']['value']
        #self.device.shutter_speed = self.convert_shutter_value(self.data.settings['captur']['SHUTTER']['value'])
        
        #self.device.framerate = self.framerate
        #self.device.resolution = self.resolution
            
    def check_if_attached_with_picamera(self):
        print('about to try open pcamera to check..')
        try:
            device = picamera.PiCamera(resolution=self.resolution, framerate=self.framerate, sensor_mode = self.sensor_mode)
            device.close()
            return True
        except picamera.exc.PiCameraError as e:
            self.use_capture = False
            self.data.settings['captur']['DEVICE']['value'] = 'disabled'
            print('camera exception is {}'.format(e))
            self.message_handler.set_message('INFO', 'no capture device attached')
            return False

    def start_preview(self):
        if self.use_capture == False:
            self.message_handler.set_message('INFO', 'capture not enabled')
            return False
        else:
            if not self.has_capture:
                is_created = self.create_capture_device()
                if self.use_capture == False or not is_created:
                    return False

        self.is_previewing = True
        self.set_capture_settings()
        self.osc_client.send_message("/capture/preview/start", True)
        return True

    def set_capture_settings(self):
        if self.capture_type == "piCaptureSd1":
            pass
            #self.device.sensor_mode = 6
            #self.device.awb_mode = "off"
            #self.device.awb_gains = 1.0
            #self.device.exposure_mode = "off"
        else:
            pass
            #self.sensor_mode = 0
            
    def stop_preview(self):
        self.osc_client.send_message("/capture/preview/stop", True)
        self.is_previewing = False

    def start_recording(self):
        if self.use_capture == False:
            self.message_handler.set_message('INFO', 'capture not enabled')
            return False
        else:
            if not self.has_capture:
                is_created = self.create_capture_device()
                if self.use_capture == False or not is_created:
                    return False

        if not self.check_available_disk_space():
            return
        
        if not os.path.exists(self.video_dir):
            os.makedirs(self.video_dir)
        self.is_recording = True
        #self.device.start_recording(self.video_dir + '/raw.h264')
        self.osc_client.send_message("/capture/record/start", True)
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
        #self.device.stop_recording()
        self.osc_client.send_message("/capture/record/stop", True)
        #set status to saving
        mp4box_process, recording_name = self.convert_raw_recording()
        self.is_recording = 'saving'        
        self.root.after(0, self.wait_for_recording_to_save, mp4box_process, recording_name)

        self.update_capture_settings()
        # return path to the video

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
        return -1
        #if not self.device or not self.device.recording or self.device.frame.timestamp == None:
        #   return -1
        #else:
        #    return self.device.frame.timestamp / 1000000

    def get_preview_alpha(self):
        return 0

    def set_colour(self, u_value, v_value):
        pass

    def set_alpha(self, amount):
        pass

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



