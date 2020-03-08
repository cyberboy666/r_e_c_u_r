import math
import data_centre.plugin_collection
from data_centre.plugin_collection import ActionsPlugin, SequencePlugin, DisplayPlugin, AutomationSourcePlugin

import pyaudio
import numpy as np
from random import randint
from statistics import mean

#import matplotlib.pyplot as plt

np.set_printoptions(suppress=True) # don't use scientific notationn

class SoundReactPlugin(ActionsPlugin,SequencePlugin,DisplayPlugin):

    DEBUG = False

    active = True
    stop_flag = False
    pause_flag = False

    stream = None

    CHUNK = 4096 # number of data points to read at a time
    RATE = 48000 #44100 # time resolution of the recording device (Hz)
    
    frequency = 10 # how often messages are sampled+calculated+sent, not anything to do with audio frequency

    config = {}

    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

        """#self.PRESET_FILE_NAME = "ShaderLoopRecordPlugin/frames.json"
        if self.active and not self.disabled:
            try:
                p=pyaudio.PyAudio()
                self.stream=p.open(format=pyaudio.paInt16,channels=1,rate=self.RATE,input=True,
                    frames_per_buffer=self.CHUNK)
            except:
                print("Failed to open sound device - disabling SoundReactPlugin!")
                self.disabled = True
                return

        print ("now setting to run automation..")

        self.pc.shaders.root.after(500, self.run_automation)"""
        if not self.disabled:
            self.start_plugin()

    def stop_plugin(self):
        self.close_sound_device()
        super().stop_plugin()

    def start_plugin(self):
        super().start_plugin()
        self.open_sound_device()

    def open_sound_device(self):
        try:
            self.p=pyaudio.PyAudio()
            self.stream=self.p.open(format=pyaudio.paInt16,channels=1,rate=self.RATE,input=True,
                frames_per_buffer=self.CHUNK)
        except:
            print("Failed to open sound device - disabling SoundReactPlugin!")
            self.active = False
            return

        self.pc.shaders.root.after(250, self.run_automation)

    def close_sound_device(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        if self.p:
            self.p.terminate()

    @property
    def sources(self):
        # TODO: write more interpreters
        return {
            "energy": self.energy,
            #"low": self.low,
            #"mid": self.mid,
            #"high": self.high,
            "peakfreq": self.peakfreq
        }

    values = {}
    levels = {
            "energy": [ 0.0, 0.0, 1.0, 0.0 ],
            "peakfreq": [ 0.0, 0.0, 0.0, 1.0 ]
    }
    last_values = {}
    display_values = {}
    # triggers?
    #   sudden drop - sudden leap?

    # DisplayPlugin methods
    def get_display_modes(self):
        return ['SOUNDMOD','NAV_SND']

    def show_plugin(self, display, display_mode):
        from tkinter import Text, END
        #super(DisplayPlugin).show_plugin(display, display_mode)
        display.display_text.insert(END, '{} \n'.format(display.body_title))
        display.display_text.insert(END, "SoundReactPlugin - ")

        display.display_text.insert(END, "ACTIVE\n" if self.active else "not active\n")

        #display.display_text.insert(END, "\tSpeed: {:03.2f}\n\n".format(self.speed))
        
        for sourcename in sorted(self.sources):
            value = "{:8}:\t".format(sourcename)
            for i,level in enumerate(self.levels[sourcename]):
                g = "ABCD"[i]+'%s '%self.pc.display.get_bar(level)
                value += g
            value += "\t"
            value += self.display_values.get(sourcename) or "{:4.2f}%".format(self.values.get(sourcename,0)*100) or "None"
            display.display_text.insert(END,value + "\n")
            """display.display_text.insert(END, "%s\n" %self.last_lfo_status[lfo])
            display.display_text.insert(END, "\t%s\n" % self.formula[lfo])"""

        #display.display_text.insert(END, "\nLevels:%s\n\n" % self.levels)
        display.display_text.insert(END, "\n\n\n")

    energy_history = []
    def run_sequence(self, position):
        # position is irrelvant for this plugin, we just want to run continuously
        if not self.active or self.stream is None:
            return

        data = np.fromstring(self.stream.read(self.CHUNK, exception_on_overflow = False),dtype=np.int16)
        previous_value = {}

        for sourcename in self.sources:
            value = self.sources[sourcename](data)
            self.values[sourcename] = value
            if value is None: 
                continue
            for slot,level in enumerate(self.levels.get(sourcename,[])):
                if level>0.0 and self.values.get(sourcename)!=self.last_values.get(sourcename):
                    self.pc.actions.call_method_name("modulate_param_%s_to_amount_continuous"%slot, self.values[sourcename])
                    previous_value[sourcename] = self.last_values.get(sourcename) or value
                    self.last_values[sourcename] = self.values[sourcename]

            if sourcename is 'energy' and self.last_values.get('energy') is not None:
                diff = abs(self.last_values.get('energy',value)-previous_value.get(sourcename,value)) #mean(self.energy_history))
                if len(self.energy_history)>5: #self.duration:
                    meandiff = abs(diff-mean(self.energy_history[:int(len(self.energy_history)/2)]))
                    #print ("    diff is %s, meandiff %s" % (diff, meandiff))
                    if meandiff>=self.config['energy'].get('triggerthreshold',0.15):
                        self.energy_history = []
                        print ("\n>>>>>>Triggering dynamic change for meandiff %s?\n" % meandiff)
                        # TODO: add configurable triggering - eg trigger next preset, next shader, next video..
                        #self.pc.actions.call_method_name("load_slot_%s_into_next_player"%randint(0,9))
                self.energy_history.append(diff) #self.values.get(sourcename,0.0))
                #print("logging %s" % diff) #self.values.get(sourcename,0.0))




    config.setdefault('energy',{})['gain'] = 0.5 # how much to multiply signal by
    config.setdefault('energy',{})['threshold'] = 0.5 # subtract from post-gain signal (hence ignore all values below)
    GAIN_MULT = 1.0
    def energy(self,data):
        peak=np.average(np.abs(data))*2
        value = (peak/2**16)/16 * 100

        value *= (self.GAIN_MULT * self.config['energy']['gain'])

        value = value - self.config['energy']['threshold']
        if value<0.0:
            value = 0.0
        if value>1.0:
            value = 1.0

        bars="#"*int(50*value)
        if self.DEBUG: print("energy:\t\t%05d %s\t(converted to %s)"%(peak,bars,value))
        self.display_values['energy'] = "{} gn:{} trsh:{} trg:{}".format(
                self.pc.display.get_bar(value), 
                self.pc.display.get_bar(self.config['energy']['gain']), 
                self.pc.display.get_bar(self.config['energy']['threshold']), 
                self.pc.display.get_bar(self.config['energy'].setdefault('triggerthreshold',0.15))
            )

        return value 

    # dont think this works properly, or maybe it do just be like that
    def peakfreq(self,data):
        data = data.copy() * np.hanning(len(data)) # smooth the FFT by windowing data
        fft = abs(np.fft.fft(data).real)
        fft = fft[:int(len(fft)/2)] # keep only first half
        freq = np.fft.fftfreq(self.CHUNK,1.0/self.RATE)
        freq = freq[:int(len(freq)/2)] # keep only first half
        freqPeak = freq[np.where(fft==np.max(fft))[0][0]]+1
        if freqPeak<400:
            return False
        value = freqPeak/2000 # ?
        #value = (value**16)
        if self.DEBUG: print("peak frequency:\t%d\tHz\t(converted to %s)"%(freqPeak,value))
        self.display_values['peakfreq'] = ("%d Hz\t"%freqPeak) + "{:03.2f}".format(value)

        return value


    # ActionsPlugin methods
    @property
    def parserlist(self):
        return [
                ( r"^toggle_sound_react_active$", self.toggle_active ),
                ( r"^sound_set_config_([a-z]*)_([a-z]*)$", self.set_config ),
                ( r"^sound_set_modulation_([a-z]*)_slot_([0-3])_level$", self.set_modulation_source_slot_level ),
        ]

    def set_modulation_source_slot_level(self, sourcename, slot, level):
        self.levels.setdefault(sourcename,[0.0,0.0,0.0,0.0])[slot] = level

    def set_config(self, sourcename, setting, value):
        if type(self.config.get(sourcename,{}).get(setting)) is str:
            print ("SoundReactPlugin: type of existing setting is string, probably doesnt make sense to set this to a value of this type!")
        self.config[sourcename][setting] = value

    def toggle_active(self):
        self.active = not self.active
