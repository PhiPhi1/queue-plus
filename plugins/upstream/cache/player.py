#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (player.py) is part of Queue Plus.
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


def packet_mirror_join_game(self, buff):
	buff.save()
	_, gamemode, dimension, difficulty, _ = buff.unpack("iBiBB")
	level_type = buff.unpack_string()
	_ = buff.unpack("?")
	
	self.static_data["respawn"] = buff.pack("iBB", dimension, difficulty, gamemode) + buff.pack_string(level_type)
	buff.restore()
	self.static_data["join_game"] = buff.read()
	return
	
	
def packet_mirror_player_position_and_look(self, buff):
	new_buffer = b""
	x, y, z, yaw, pitch, flags = buff.unpack("dddffb")
	buff.discard()
	new_buffer += buff.pack("dddffb", x, y, z, yaw, pitch, flags) + buff.pack_varint(-1)
	self.static_data["player_position_and_look"] = new_buffer
	return
