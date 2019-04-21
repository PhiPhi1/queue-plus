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

#
#      This file (__init__.py) is part of Queue Plus.
#
#      Queue Plus is a proxy service that is designed to be highly modular.
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
#
#
#      This file (__init__.py) is part of queue-plus.
#
#      queue-plus is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      any later version.
#
#      queue-plus is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with queue-plus.  If not, see <https://www.gnu.org/licenses/>.
#
from quarry.net.client import ClientProtocol

from core import CoreProtocol

# TODO: implement plugins
# from plugins.upstream import get_plugins
from plugins.upstream import get_plugins


class UpstreamProtocol(ClientProtocol):
	from core.upstream.bridges import setup_bridge, add_forwarding_bridge, remove_forwarding_bridge
	from core.upstream.packets import log_packet, packet_received
	
	def __init__(self, *args, **kwargs):
		self.core = CoreProtocol(self)
		
		super(UpstreamProtocol, self).__init__(*args, **kwargs)


	def setup(self):
		self.core.load_plugins(get_plugins())
		self.core.on_ready_plugins()

	def player_joined(self):
		super(UpstreamProtocol, self).player_joined()
		
		self.factory.account_manager.sessions.add_session(self)
		self.core.on_join_plugins()
		
		if self.factory.protocol_callback:
			try:
				self.factory.protocol_callback(self)
			except Exception as e:
				print("Error in protocol callback", e)
		
		for bridge in self.factory.bridges:
			self.setup_bridge(bridge)
	
	def player_left(self):
		super(UpstreamProtocol, self).player_left()
		
		self.factory.account_manager.sessions.remove_session(self)
		
		self.core.on_leave_plugins()
		self.core.unload_plugins()
		
		for bridge in self.factory.bridges:
			self.remove_forwarding_bridge(bridge)
			bridge.upstream_disconnected()
	
	def close(self, *args, **kwargs):
		super(UpstreamProtocol, self).close(*args, **kwargs)
		self.factory.stopTrying()
		del self
		
	def super_handle_packet(self, buff, name):
		super(UpstreamProtocol, self).packet_received(buff, name)
