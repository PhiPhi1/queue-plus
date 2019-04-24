#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (the_void.py) is part of Queue Plus.
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
import random

from headless.upstream.protocol import PseudoProtocol


class TheVoidProtocol(PseudoProtocol):
		
	# noinspection PyArgumentList
	def setup_bridge(self, bridge):
		super(TheVoidProtocol, self).setup_bridge(bridge)
		
		from plugins.downstream.player_info import PlayerInfoPlugin
		downstream_player_info = bridge.downstream.core.get_plugin(PlayerInfoPlugin)
		print(downstream_player_info.player_eid)
		
		self.logger.debug("The void started")
		
		if not bridge.joined_game:
			out_buff = self.buff_type(self.buff_type.pack("iBiBB", downstream_player_info.player_eid, 3, 0, 0, 0) + self.buff_type.pack_string("flat") + self.buff_type.pack("?", False))
			bridge.packet_received(out_buff, "downstream", "join_game")
		else:
			out_buff = self.buff_type(self.buff_type.pack("iBB", 0, 0, 3) + self.buff_type.pack_string("flat"))
			bridge.packet_received(out_buff, "downstream", "respawn")
		
		bridge.packet_received(self.buff_type(self.buff_type.pack("dddff?", 0, 255, 0, 0, 0, 0b00000) + self.buff_type.pack_varint(0)), "downstream", "player_position_and_look")
		return
