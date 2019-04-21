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
from quarry.net.protocol import ProtocolError
from quarry.types.buffer import BufferUnderrun

from twisted.internet import protocol

from plugins.bridge import BridgePlugin
from plugins.upstream.cache import CachingPlugin


class HotSwapPlugin(BridgePlugin, protocol.Protocol):
	
	# TODO: stagger cache loading
	def load_cache(self):
		cache = self.bridge.upstream.core.get_plugin(CachingPlugin)
		cache_data = cache.concat_to_array()
		
		for index, (name, buff) in enumerate(cache_data):
			# self.bridge.downstream.send_packet(name, buff)
			unpacked_buff = self.buff_type(buff)
			
			try:
				self.bridge.packet_received(unpacked_buff, "downstream", name)
			except BufferUnderrun:
				raise ProtocolError("Packet is too short: %s" % name)
			if len(unpacked_buff) > 0:
				raise ProtocolError("Packet is too long: %s" % name)
			
		return
