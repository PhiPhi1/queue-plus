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
from decimal import Decimal
from plugins.bridge import BridgePlugin
import glm


class AntiKickPlugin(BridgePlugin):
	player_on_ground_loop = None
	player_full_update_loop = None
	player_position = None
	player_look = None
	on_ground = None
	
	def on_join(self):
		self.player_on_ground_loop = self.ticker.add_loop(1, self.on_ground_cb)
		self.player_full_update_loop = self.ticker.add_loop(20, self.full_pos_callback)
	
	def packet_mirror_downstream_player_position_and_look(self, buff):
		x, y, z, x_rot, y_rot, _ = buff.unpack("dddffb")
		self.player_position = glm.vec3(x, y, z)
		self.player_look = glm.vec2(x_rot, y_rot)
		buff.discard()
		return

	def packet_mirror_upstream_player_position_and_look(self, buff):
		x, y, z, x_rot, y_rot, self.on_ground = buff.unpack("dddff?")
		self.player_position = glm.vec3(x, y, z)
		self.player_look = glm.vec2(x_rot, y_rot)
		return
	
	def packet_mirror_upstream_player_position(self, buff):
		x, y, z, self.on_ground = buff.unpack("ddd?")
		self.player_position = glm.vec3(x, y, z)
		return

	def packet_mirror_upstream_player_look(self, buff):
		x_rot, y_rot, self.on_ground = buff.unpack("ff?")
		self.player_look = glm.vec2(x_rot, y_rot)
		return
	
	def on_ground_cb(self):
		if self.on_ground:
			self.bridge.packet_received(self.buff_type(self.buff_type.pack('?', self.on_ground)), "upstream", "player")

	def full_pos_callback(self):
		if self.player_look and self.player_position and self.on_ground:
			x, y, z = self.player_position
			x_rot, y_rot = self.player_look
			
			self.bridge.packet_received(self.buff_type(self.buff_type.pack('dddff?', Decimal(x), Decimal(y), Decimal(z), float(x_rot), float(y_rot), self.on_ground)),
																	"upstream", "player_position_and_look")
