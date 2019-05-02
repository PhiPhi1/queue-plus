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
import glm
import json
import random
from decimal import Decimal

from bots import Bots


class AntiAfkBot(Bots):
	loading = {
		# Load bot when upstream joins
		"start": True,
		# Run while bridge is connected
		"symbiotic": False
	}
	
	
	def __init__(self, *args, **kwargs):
		super(AntiAfkBot, self).__init__(*args, **kwargs)
		
		self.running = False
		self.walk_cycle_running = False
		self.anti_afk_task = None
		self.player_position = glm.vec3(0, 0, 0)
		self.queue_start = False
		self.ready = False
		
		path = "bots/anti_afk/config.json"
		with open(path) as config_file:
			self.config = json.load(config_file)
		
		self.loading["start"] = self.config["on_start"]
	
	
	def packet_player_position_and_look(self, buff):
		x, y, z, _, _, _ = buff.unpack("dddffb")
		tp_id = buff.unpack_varint()
		self.player_position = glm.vec3(x, y, z)
		if self.running:
			self.protocol.send_packet("teleport_confirm", self.buff_type.pack_varint(tp_id))
		
		self.ready = True
		
		if self.queue_start:
			self.start()
	
	
	def on_start(self):
		print("starting")
		from plugins.upstream.cache import CachingPlugin
		cache = self.protocol.core.get_plugin(CachingPlugin)
		
		if "player_position_and_look" in cache.static_data:
			buff = cache.static_data["player_position_and_look"]
			unpacked_buff = self.protocol.buff_type(buff)
			self.packet_player_position_and_look(unpacked_buff)
			print("using position from cache")
			
		self.start()
		
		
	def on_stop(self):
		print("stopping")
		self.stop()
	
	
	def start(self):
		print(self.ready)
		if self.ready:
			self.running = True
			
			self.queue_start = False
			self.anti_afk_loop()
		else:
			self.queue_start = True
	
	
	def stop(self):
		self.running = False
		
		if self.anti_afk_task:
			self.ticker.remove(self.anti_afk_task)
			self.anti_afk_task = None
	
	
	def anti_afk_loop(self):
		if not self.running:
			self.stop()
			return
		
		self.walk_cycle()
		self.anti_afk_task = self.ticker.add_delay(self.config["frequency"], self.anti_afk_loop)
	
	
	def walk_cycle(self):
		if self.walk_cycle_running:
			return
		
		speed_divider = self.config["walk"]["smoothing"]
		self.walk_cycle_running = True
		
		limit = self.config["walk"]["distance"]
		direction = random.choice([glm.vec3(1, 0, 0), glm.vec3(-1, 0, 0), glm.vec3(0, 0, 1), glm.vec3(0, 0, -1)])
		
		sequence = []
		
		for _ in range(limit * speed_divider):
			sequence.append(direction / speed_divider)
		
		for _ in range(limit * speed_divider):
			sequence.append((direction / speed_divider) * glm.vec3(-1, 1, -1))
		
		
		def walk(position):
			x, y, z = self.player_position = self.player_position - position
			self.protocol.send_packet("player_position", self.buff_type.pack("ddd?", Decimal(x), Decimal(y), Decimal(z), True))
		
		
		# Not defining the index in the namespace
		# only making it part of the class because I dont want to use global
		self.walk_cycle_index = 0
		
		
		def ticker_loop():
			walk(sequence[self.walk_cycle_index])
			
			if not self.walk_cycle_index + 1 > sequence.__len__() - 1:
				self.walk_cycle_index += 1
				self.ticker.add_delay(self.config["walk"]["speed"] / speed_divider, ticker_loop)
			else:
				self.walk_cycle_running = False
		
		
		ticker_loop()
	
	
	def get_delay(self):
		if self.config["randomize"]["enabled"]:
			return random.randint(self.config["frequency"] * self.config["randomize"]["enabled"], self.config["frequency"])
		return self.config["frequency"]
	
	# packet handling
	def packet_update_health(self, buff):
		hp = buff.unpack("f")
		buff.discard()
		if self.running and hp <= 0:
			self.ticker.add_delay(20, self.respawn)
	
	
	# TODO: move auto respawn to a sperate plugin to handle low hp
	def respawn(self):
		self.protocol.send_packet("client_status", self.buff_type.pack_varint(0))

