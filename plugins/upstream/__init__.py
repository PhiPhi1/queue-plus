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
from plugins import Plugin


class UpstreamPlugin(Plugin):
	def packet_received(self, buff, name):
		self.mirror_packet(buff, name)
		method_pointer = "packet_%s" % name
		packet_handled = self.handle_packet(method_pointer, buff)
		
		return packet_handled
	
	
	def mirror_packet(self, buff, name):
		method_pointer = "packet_mirror_%s" % name
		
		self.handle_packet(method_pointer, buff)
		return
	
	
	def send_packet(self, name, *data):
		return self.protocol.send_packet(name, *data)
		
		
def get_plugins():
	from plugins.upstream.always_alive import AlwaysAlivePlugin
	from plugins.upstream.cache import CachingPlugin
	from plugins.upstream.player_info import PlayerInfoPlugin
	from plugins.upstream.queue import QueuePlugin
	
	return [
		AlwaysAlivePlugin,
		PlayerInfoPlugin,
		QueuePlugin,
		CachingPlugin
	]
