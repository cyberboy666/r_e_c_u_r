import signal
import os
import sys
import dbus
import subprocess
from time import time,strftime
import data_centre

logger = data_centre.setup_logging()


"""
12/6/2016 - rewrite to use dbus
2/11/2016 - connection needs to wait for dbus filemane to be populated
2/11/2016 - remove busy wait for conection
24/11/2016 - move pause after load to after first get_position to ensure omxplayer has loaded track before pause
24/11/2016 - report dbus exception messages in log
30/11/2016 - pause at start waits until position is not 0 as video has not started until it becomes -ve
2/12/2016 - make pause glitch tolerant, try again if fails
3/12/2016 - remove threading to stop pause and unpause for showing happening in wrong order
5/12/2016 - deal with situation where pause at end happened so late that video finished first
5/12/2016 - need to send nice-day when stop is received and paused for end as now do not intercept one from omxplayer

 omxdriver hides the detail of using the omxplayer command  from videoplayer
 This is meant to be used with videoplayer.py
 Its easy to end up with many copies of omxplayer.bin running if this class is not used with care. use pp_videoplayer.py for a safer interface.

 External commands
 ----------------------------
 __init__ just creates the instance and initialises variables (e.g. omx=OMXDriver())
  load  - processes the track up to where it is ready to display, at this time it pauses.
 show  - plays the video from where 'prepare' left off by resuming from the pause.
 play -  plays a track (not used by gapless)
 pause/unpause   -  pause on/off
 toggle_pause  - toggles pause
 control  - sends controls to omxplayer.bin  while track is playing (use stop and pause instead of q and p)
 stop - stops a video that is playing.
 terminate - Stops a video playing. Used when aborting an application.
 kill - kill of omxplayer when it hasn't terminated at the end of a track.
 
Signals
----------
 The following signals are produced while a track is playing
         self.start_play_signal = True when a track is ready to be shown
         self.end_play_signal= True when a track has finished due to stop or because it has come to an end
         self.end_play_reason reports the reason for the end
 Also is_running() tests whether the sub-process running omxplayer is present.

"""

class OMXDriver(object):

    # adjust this to determine freeze after the first frame
    after_first_frame_position =-50000 # microseconds
   
    _LAUNCH_CMD = '/usr/bin/omxplayer --no-keys '  # needs changing if user has installed his own version of omxplayer elsewhere
    KEY_MAP =   { '-': 17, '+': 18, '=': 18} # add more keys here, see popcornmix/omxplayer github file KeyConfig.h

    def __init__(self,widget,pp_dir):


        self.widget=widget
        self.pp_dir=pp_dir
        

        self.start_play_signal=False
        self.end_play_signal=False
        self.end_play_reason='nothing'
        self.duration=0
        self.video_position = 0

        self.pause_at_end_required=False
        self.paused_at_end=False
        self.pause_at_end_time=0
        
        # self.pause_before_play_required='before-first-frame'  #no,before-first-frame, after-first-frame
        # self.pause_before_play_required='no'
        self.paused_at_start='False'

        self.paused=False      

        self.terminate_reason=''

        #  dbus and subprocess
        self._process=None
        self.__iface_root=None
        self.__iface_props = None
        self.__iface_player = None


    def load(self, track, freeze_at_start,options,caller):
        self.pause_before_play_required=freeze_at_start
        self.caller=caller
        track= "'"+ track.replace("'","'\\''") + "'"
        # self.mon.log(self,'TIME OF DAY: '+ strftime("%Y-%m-%d %H:%M"))
        self.dbus_user = os.environ["USER"]

        self.id=str(int(time()*10))



        self.dbus_name = "org.mpris.MediaPlayer2.omxplayer"+self.id
        
        self.omxplayer_cmd = OMXDriver._LAUNCH_CMD + options + " --dbus_name '"+ self.dbus_name + "' " + track
        # self.mon.log(self, 'dbus user ' + self.dbus_user)
        # self.mon.log(self, 'dbus name ' + self.dbus_name)

        # logger.info self.omxplayer_cmd
        logger.info("Send command to omxplayer: "+ self.omxplayer_cmd)
        # self._process=subprocess.Popen(self.omxplayer_cmd,shell=True,stdout=file('/home/pi/pipresents/pp_logs/stdout.txt','a'),stderr=file('/home/pi/pipresents/pp_logs/stderr.txt','a'))
        self._process=subprocess.Popen(self.omxplayer_cmd,shell=True,stdout=file('/dev/null','a'),stderr=file('/dev/null','a'))
        self.pid=self._process.pid

        # wait for omxplayer to start then start monitoring thread
        self.dbus_tries = 0
        self.omx_loaded = False
        self._wait_for_dbus()
        return
    
    def _wait_for_dbus(self):
        connect_success=self.__dbus_connect()
        if connect_success is True:
            # print 'SUCCESS'
            logger.info('connected to omxplayer dbus after ' + str(self.dbus_tries) + ' centisecs')
                
            # get duration of the track in microsecs if fails return a very large duration
            # posibly faile because omxplayer is running but not omxplayer.bin
            duration_success,duration=self.get_duration()
            if duration_success is False:
                logger.info('get duration failed for n attempts using '+ str(duration/60000000)+ ' minutes')
            # calculate time to pause before last frame
            self.duration = duration
            self.pause_at_end_time = duration - 350000
            # start the thread that is going to monitor output from omxplayer.
            self._monitor_status()
        else:
            self.dbus_tries+=1
            self.widget.after(100,self._wait_for_dbus)

    

    def _monitor_status(self):
        # print '\n',self.id, '** STARTING ',self.duration
        self.start_play_signal=False
        self.end_play_signal=False
        self.end_play_reason='nothing'
        self.paused_at_end=False
        self.paused_at_start='False'
        self.delay = 50
        self.widget.after(0,self._status_loop)



    """
    freeze at start
    'no' - unpause in show - test !=0
    'before_first_frame' - don't unpause in show, test !=0
    'after_first_frame' - don't unpause in show, test > -100000
    """
        
    def _status_loop(self):
            if self.is_running() is False:
                # process is not running because quit or natural end - seems not to happen
                self.end_play_signal=True
                self.end_play_reason='nice_day'
                # print ' send nice day - process not running'
                return
            else:
                success, video_position = self.get_position()
                # if video_position <= 0: print 'read position',video_position
                if success is False:
                    # print 'send nice day - exception when reading video position'
                    self.end_play_signal=True
                    self.end_play_reason='nice_day'
                    return
                else:
                    self.video_position=video_position
                    # if timestamp is near the end then pause
                    if self.pause_at_end_required is True and self.video_position>self.pause_at_end_time:    #microseconds
                        # print 'pausing at end, leeway ',self.duration - self.video_position
                        pause_end_success = self.pause(' at end of track')
                        if pause_end_success is True:
                            # print self.id,' pause for end success', self.video_position
                            self.paused_at_end=True
                            self.end_play_signal=True
                            self.end_play_reason='pause_at_end'
                            return
                        else:
                            logger.info( 'pause at end failed, probably because of delay after detection, just run on')
                            self.widget.after(self.delay,self._status_loop)
                    else:
                        # need to do the pausing for preload after first timestamp is received 0 is default value before start
                        # print self.pause_before_play_required,self.paused_at_start,self.video_position,OMXDriver.after_first_frame_position
                        if (self.pause_before_play_required == 'after-first-frame' and self.paused_at_start == 'False' and self.video_position >OMXDriver.after_first_frame_position)\
                        or(self.pause_before_play_required != 'after-first-frame' and self.paused_at_start == 'False' and self.video_position !=0):
                            pause_after_load_success=self.pause('after load')
                            if pause_after_load_success is True:
                                # print self.id,' pause after load success',self.video_position
                                self.start_play_signal = True
                                self.paused_at_start='True'
                            else:
                                # should never fail, just warn at the moment
                                # print 'pause after load failed '+ + str(self.video_position)
                                logger.info( str(self.id)+ ' pause after load fail ' + str(self.video_position))
                            self.widget.after(self.delay,self._status_loop)
                        else:
                            self.widget.after(self.delay,self._status_loop)


    
    def show(self,freeze_at_end_required,initial_volume):
        self.initial_volume=initial_volume
        self.pause_at_end_required=freeze_at_end_required
        # unpause to start playing
        if self.pause_before_play_required =='no':
            unpause_show_success=self.unpause(' to start showing')
            # print 'unpause for show',self.paused
            if unpause_show_success is True:
                pass
                # print self.id,' unpause for show success', self.video_position
            else:
                # should never fail, just warn at the moment
                logger.info(str(self.id)+ ' unpause for show fail ' + str(self.video_position))

        
    def control(self,char):

        val = OMXDriver.KEY_MAP[char]
        #logger.info('>control received and sent to omxplayer ' + str(self.pid))
        if self.is_running():
            try:
                self.__iface_player.Action(dbus.Int32(val))
            except dbus.exceptions.DBusException as ex:
                #logger.info('Failed to send control - dbus exception: {}'.format(ex.get_dbus_message()))
                return
        else:
            logger.info('Failed to send control - process not running')
            return

        
    # USE ONLY at end and after load
    # return succces of the operation, several tries if pause did not work and no error reported.
    def pause(self,reason):
        #logger.info(self,'pause received {}'.format(reason))
        if self.paused is False:
            logger.info('not paused so send pause {}'.format(reason))
            tries=1
            while True:
                if self.send_pause() is False:
                    # failed for good reason
                    return False
                status=self.omxplayer_is_paused() # test omxplayer after sending the command
                if status == 'Paused':
                    self.paused = True
                    return True
                if status == 'Failed':
                    # failed for good reason because of exception or process not running caused by end of track
                    return False
                else:
                    # failed for no good reason
                    logger.info(self, '!!!!! repeat pause {}'.format(str(tries)))
                    # print self.id,' !!!!! repeat pause ',self.video_position, tries
                    tries +=1
                    if tries >5:
                        # print self.id, ' pause failed for n attempts'
                        logger.info('pause failed for n attempts')
                        return False
            # repeat

            
    # USE ONLY for show

    def unpause(self,reason):
        logger.info('MON' + 'Unpause received {}'.format(reason))
        if self.paused is True:
            logger.info('MON' +'Is paused so Track will be unpaused {}'.format(reason))
            tries=1
            while True:
                if self.send_unpause() is False:
                    return False
                status = self.omxplayer_is_paused() # test omxplayer
                if status == 'Playing':
                    self.paused = False
                    self.paused_at_start='done'
                    self.set_volume(self.initial_volume)
                    return True

                if status == 'Failed':
                    # failed for good reason because of exception or process not running caused by end of track
                    return False
                else:
                    logger.info('warn' + '!!!!! repeat unpause {}'.format(tries))
                    # print self.id,' !!!! repeat unpause ',self.video_position, tries
                    tries +=1
                    if tries >5:
                        # print self.id, ' unpause failed for n attempts'                       
                        logger.info('warn' + 'unpause failed for n attempts')
                        return False
                    

    def omxplayer_is_paused(self):
        if self.is_running():
            try:
                result=self.__iface_props.PlaybackStatus()
            except dbus.exceptions.DBusException as ex:
                logger.info('warn'+'Failed to test paused - dbus exception: {}'.format(ex.get_dbus_message()))
                return 'Failed'
            return result
        else:
            logger.info('warn'+'Failed to test paused - process not running')
            # print self.id,' test paused not successful - process'
            return 'Failed'

        
    def send_pause(self):
        if self.is_running():
            try:
                self.__iface_player.Pause()
            except dbus.exceptions.DBusException as ex:
                logger.info('warn'+'Failed to send pause - dbus exception: {}'.format(ex.get_dbus_message()))
                return False
            return True
        else:
            logger.info('warn'+'Failed to send pause - process not running')
            # print self.id,' send pause not successful - process'
            return False


    def send_unpause(self):  
        if self.is_running():
            try:
                self.__iface_player.Action(16)
            except dbus.exceptions.DBusException as ex:
                logger.info('warn'+'Failed to send unpause - dbus exception: {}'.format(ex.get_dbus_message()))
                return False
            return True
        else:
            logger.info('warn'+'Failed to send unpause - process not running')
            # print self.id,' send unpause not successful - process'
            return False

    def pause_on(self):
        logger.info('mon'+'pause on received ')
        # print 'pause on',self.paused
        if self.paused is True:
            return
        if self.is_running():
            try:
                # self.__iface_player.Action(16)                
                self.__iface_player.Pause()  # - this should work but does not!!!
                self.paused=True
                # print 'paused OK'
                return
            except dbus.exceptions.DBusException as ex:
                logger.info('warn'+'Failed to do pause on - dbus exception: {}'.format(ex.get_dbus_message()))
                return
        else:
            logger.info('warn'+'Failed to do pause on - process not running')
            return
                    

    def pause_off(self):
        logger.info('mon'+'pause off received ')
        # print 'pause off',self.paused
        if self.paused is False:
            return
        if self.is_running():
            try:
                self.__iface_player.Action(16)
                self.paused=False
                # print 'not paused OK'
                return
            except dbus.exceptions.DBusException as ex:
                logger.info('warn'+'Failed to do pause off - dbus exception: {}'.format(ex.get_dbus_message()))
                return
        else:
            logger.info('warn'+'Failed to do pause off - process not running')
            return

    def go(self):
        logger.info('log'+'go received ')
        self.unpause('for go')


    def mute(self):
            self.__iface_player.Mute()
            
    def unmute(self):
            self.__iface_player.Unmute()

    def set_volume(self,millibels):
        volume = pow(10, millibels / 2000.0);
        self.__iface_props.Volume(volume)
        

    def toggle_pause(self,reason):
        logger.info('log'+'toggle pause received {}'.format(reason))
        if not self.paused:
            self.paused = True
        else:
            self.paused=False
        if self.is_running():
            try:
                self.__iface_player.Action(16)
            except dbus.exceptions.DBusException as ex:
                logger.info('warn'+'Failed to toggle pause - dbus exception: {}'.format(ex.get_dbus_message()))
                return
        else:
            logger.info('warn'+'Failed to toggle pause - process not running')
            return



    def stop(self):
        logger.info('log'+'>stop received and quit sent to omxplayer {} '.format(self.pid))
        # need to send 'nice day'
        if self.paused_at_end is True:
            self.end_play_signal=True
            self.end_play_reason='nice_day'
            # print 'send nice day for close track'
        if self.is_running():
            try:
                self.__iface_root.Quit()
            except dbus.exceptions.DBusException as ex:
                logger.info('warn'+'Failed to quit - dbus exception: {}'.format(ex.get_dbus_message()))
                return
        else:
            logger.info('warn'+'Failed to quit - process not running')
            return


    # kill the subprocess (omxplayer and omxplayer.bin). Used for tidy up on exit.
    def terminate(self,reason):
        self.terminate_reason=reason
        self.stop()
        
    def get_terminate_reason(self):
        return self.terminate_reason
    

   # test of whether _process is running
    def is_running(self):
        retcode=self._process.poll()
        # print 'is alive', retcode
        if retcode is None:
            return True
        else:
            return False



    # kill off omxplayer when it hasn't terminated at the end of a track.
    # send SIGINT (CTRL C) so it has a chance to tidy up daemons and omxplayer.bin
    def kill(self):
        if self.is_running()is True:
            self._process.send_signal(signal.SIGINT)


    def get_position(self):
        # don't test process as is done just before
        try:
            micros = self.__iface_props.Position()
            return True,micros
        except dbus.exceptions.DBusException as ex:
            # print 'Failed get_position - dbus exception: {}'.format(ex.get_dbus_message())
            return False,-1               


    def get_duration(self):
        tries=1
        while True:
            success,duration=self._try_duration()
            if success is True:
                return True,duration
            else:
                logger.info('warn'+ 'repeat get duration {}'.format(tries))
                tries +=1
                if tries >5:                      
                    return False,sys.maxint*100


    def _try_duration(self):
        """Return the total length of the playing media"""
        if self.is_running() is True:
            try:
                micros = self.__iface_props.Duration()
                return True,micros
            except dbus.exceptions.DBusException as ex:
                logger.info('warn'+'Failed get duration - dbus exception: {}'.format(ex.get_dbus_message()))
                return False,-1
        else:
            return False,-1




    # *********************
    # connect to dbus
    # *********************
    def __dbus_connect(self):
        if self.omx_loaded is False:
            # read the omxplayer dbus data from files generated by omxplayer
            bus_address_filename = "/tmp/omxplayerdbus.{}".format(self.dbus_user)
            bus_pid_filename = "/tmp/omxplayerdbus.{}.pid".format(self.dbus_user)

            if not os.path.exists(bus_address_filename):
                logger.info('log'+'waiting for bus address file {}'.format(bus_address_filename))
                self.omx_loaded=False
                return False
            else:
                f = open(bus_address_filename, "r")
                bus_address = f.read().rstrip()
                if bus_address == '':
                    logger.info('log'+ 'waiting for bus address in file {}'.format(bus_address_filename))
                    self.omx_loaded=False
                    return False
                else:
                    # self.mon.log(self, 'bus address found ' + bus_address)
                    if not os.path.exists(bus_pid_filename):
                        logger.info('warn'+ 'bus pid file does not exist {}'.format(bus_pid_filename))
                        self.omx_loaded=False
                        return False
                    else:
                        f= open(bus_pid_filename, "r")
                        bus_pid = f.read().rstrip()
                        if bus_pid == '':
                            self.omx_loaded=False
                            return False
                        else:
                            # self.mon.log(self, 'bus pid found ' + bus_pid)
                            os.environ["DBUS_SESSION_BUS_ADDRESS"] = bus_address
                            os.environ["DBUS_SESSION_BUS_PID"] = bus_pid
                            self.omx_loaded = True
       
        if self.omx_loaded is True:
            session_bus = dbus.SessionBus()
            try:
                omx_object = session_bus.get_object(self.dbus_name, "/org/mpris/MediaPlayer2", introspect=False)
                self.__iface_root = dbus.Interface(omx_object, "org.mpris.MediaPlayer2")
                self.__iface_props = dbus.Interface(omx_object, "org.freedesktop.DBus.Properties")
                self.__iface_player = dbus.Interface(omx_object, "org.mpris.MediaPlayer2.Player")
            except dbus.exceptions.DBusException as ex:
                # self.mon.log(self,"Waiting for dbus connection to omxplayer: {}".format(ex.get_dbus_message()))
                return False
        return True

