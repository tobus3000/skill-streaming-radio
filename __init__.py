# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

import time

#from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill #, intent_file_handler
from mycroft.util.log import getLogger
try:
    from mycroft.skills.audioservice import AudioService
except:
    from mycroft.util import play_mp3
    AudioService = None

__author__ = 'nmoore'


LOGGER = getLogger(__name__)


class InternetRadioSkill(MycroftSkill):
    def __init__(self):
        super(InternetRadioSkill, self).__init__(name="StreamingRadioSkill")
        self.audioservice = None
        self.process = None

    def initialize(self):
        self.register_intent_file('play.intent', self.handle_play_intent)
   
        if AudioService:
            self.audioservice = AudioService(self.emitter)

    def handle_play_intent(self, message):
		self.stop()  # ???? Just in case something is already playing ????
		station = message.data.get('station')
		LOGGER.info('Requested Station is ' + station)   
		LOGGER.info('Stream URL: ' + self.settings[station])
		# check if the station has been defined
#                try:
        	LOGGER.info('Settings: ' + str(self.settings))
		stream_url = self.settings[station]
	 	LOGGER.info('Stream URL: ' + stream_url)
		if stream_url:
                    LOGGER.info('Made it here')
		    self.speak_dialog('start')
		    time.sleep(4)
		    if self.audioservice:
			self.audioservice.play(self.settings[station])
		    else: # othervice use normal mp3 playback
			self.process = play_mp3(self.settings[station])
#		except:
#			self.speak_dialog('StationNotFound')
             
    def handle_stop(self, message):
        self.stop()
        self.speak_dialog('streaming.radio.stop')

    def stop(self):
        if self.audioservice:
           self.audioservice.stop()
        else:
            if self.process and self.process.poll() is None:
               self.process.terminate()
               self.process.wait()

def create_skill():
    return InternetRadioSkill()
