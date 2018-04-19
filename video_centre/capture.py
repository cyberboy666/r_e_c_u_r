import os
import subprocess
import datetime
from picamera import PiCamera

class Capture(object):
    def __init__(self, root, message_handler, data):
        self.root = root
        self.message_handler = message_handler
        self.data = data
        self.use_capture = True
        self.device = None
        self.raw_dir = '/home/pi/Videos/raw_recordings'
        self.create_capture_device()

    def create_capture_device(self):
        if self.use_capture:
            self.device = PiCamera()

    def start_preview(self):
        if self.device.closed:
            self.create_capture_device()
        self.device.start_preview()
        self.set_preview_screen_size()            

    def set_preview_screen_size(self):
        if self.data.get_screen_size_setting() == 'dev_mode':
            self.device.preview.fullscreen = False
            self.device.preview.window = (50, 350, 500, 400)
        else:
            self.device.preview.fullscreen = True

    def stop_preview(self):
        self.device.stop_preview()
        if not self.device.recording:
            self.device.close()

    def start_recording(self):
        if self.device.closed:
            self.create_capture_device()
        # need to check the space in destination (or check in a main loop somewhere ?)
        
        if not os.path.exists(self.raw_dir):
            os.makedirs(self.raw_dir)
        self.device.start_recording(self.raw_dir + '/raw.h264')

    def stop_recording(self):
        self.device.stop_recording()
        #set status to saving
        mp4box_process = self.convert_raw_recording()
        print(mp4box_process.poll())
        self.root.after(0, self.wait_for_recording_to_save, mp4box_process)

        # return path to the video
        if not self.device.preview:
            self.device.close()

    def convert_raw_recording(self):
        recording_path = self.generate_recording_path()
        try:
            return subprocess.Popen(['MP4Box -add {} {}'.format(self.raw_dir + '/raw.h264', recording_path)],shell=True)
        except Exception as e:
            print(e)
            if hasattr(e, 'message'):
                error_info = e.message
            else:
                error_info = e
            self.message_handler.set_message('ERROR',error_info)
        
    
    def wait_for_recording_to_save(self, process):
        print('the poll is {}'.format(process.poll()))
        if process.poll() is not None:
            #remove saving status
            os.remove(self.raw_dir + '/raw.h264')
        else:
            self.root.after(300, self.wait_for_recording_to_save, process)

    def generate_recording_path(self):
        rec_dir = '/home/pi/Videos/recordings'
        if not os.path.exists(rec_dir):
            os.makedirs(rec_dir)
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        i = 0
        while os.path.exists('{}/rec-{}-{}.mp4'.format(rec_dir,date, i)):
            i += 1
        return '{}/rec-{}-{}.mp4'.format(rec_dir,date, i)

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


