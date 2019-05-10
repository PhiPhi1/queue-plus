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


class AntiKickPlugin(BridgePlugin):
	player_state_loop = None
	player_full_update_loop = None
	player_position = None
	player_look = None
	on_ground = None
	
	def on_join(self):
		pass
	
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
