#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (__init__.py) is part of Queue Plus.
#
#      Queue Plus is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      any later version.
#
#      Queue Plus is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with Queue Plus.  If not, see <https://www.gnu.org/licenses/>.
from plugins.bridge import BridgePlugin
import glm


class NotificationsPlugin(BridgePlugin):
	def __init__(self, *args, **kwargs):
		super(NotificationsPlugin, self).__init__(*args, **kwargs)
		self.player_pos = glm.vec3(0, 0, 0)
	
	# 8, 6, 6, 18, 19
	def send_chat_notification(self, message, sound=False):
		if sound:
			self.queue_tune([
				(self.convert_to_pitch(8), 0),
				(self.convert_to_pitch(3), 4),
				(self.convert_to_pitch(3), 2),
				(self.convert_to_pitch(7), 4),
				(self.convert_to_pitch(3), 4)
			], self.get_notification_sound())
		self.bridge.packet_received(self.buff_type(self.buff_type.pack_chat(message) + self.buff_type.pack("B", 1)), "downstream", "chat_message")
	
	@staticmethod
	def convert_to_pitch(pitch):
		return 0.5 + (pitch * 0.06)
		
	def queue_tune(self, tune, sound_id):
		# Not defining the index in the namespace
		# only making it part of the class because I dont want to use global
		self.queue_tune_index = 0
		
		def sound_loop():
			pitch, _ = tune[self.queue_tune_index]
			
			if self.queue_tune_index + 1 < tune.__len__():
				_, delay = tune[self.queue_tune_index + 1]
			else:
				delay = 0
				
			self.play_sound(sound_id, pitch)
			
			if self.queue_tune_index + 1 < tune.__len__():
				self.queue_tune_index += 1
				self.ticker.add_delay(delay, sound_loop)
		
		sound_loop()
		
	def get_notification_sound(self):
		version = self.bridge.downstream.protocol_version
		
		# checking if 1.12 - 1.12.2
		if 340 <= version >= 335:
			return 74
		# checking if 1.13 - 1.13.2
		elif 404 <= version >= 393:
			return 104
		else:
			return 0
		
	def play_sound(self, sound_id, pitch, volume=1):
		x, y, z = self.player_pos
		x, y, z = (int(x*8), int(y*8), int(z*8))
		
		packed = {
			"sound_id": self.buff_type.pack_varint(sound_id),
			"category": self.buff_type.pack_varint(0),
			"pos": self.buff_type.pack("iii", x, y, z),
			"volume": self.buff_type.pack("f", volume),
			"pitch": self.buff_type.pack("f", pitch)
		}

		self.bridge.packet_received(self.buff_type(packed["sound_id"] + packed["category"] + packed["pos"] + packed["volume"] + packed["pitch"]), "downstream", "sound_effect")
	
	def packet_mirror_downstream_player_position_and_look(self, buff):
		x, y, z = buff.unpack("ddd")
		buff.discard()
		
		self.update_player_pos(x, y, z)
	
	def packet_mirror_upstream_player_position_and_look(self, buff):
		x, y, z = buff.unpack("ddd")
		buff.discard()
		
		self.update_player_pos(x, y, z)

	def update_player_pos(self, x, y, z):
		self.player_pos = glm.vec3(x, y, z)
