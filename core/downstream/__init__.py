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


from quarry.net.proxy import Downstream
from quarry.net.server import ServerProtocol

from core import CoreProtocol
from plugins.downstream import get_plugins


class DownstreamProtocol(Downstream):
	from core.downstream.packets import packet_received, log_packet
	
	def __init__(self, *args, **kwargs):
		self.core = CoreProtocol(self)
		
		super(DownstreamProtocol, self).__init__(*args, **kwargs)
	
	def setup(self):
		super(DownstreamProtocol, self).setup()
		self.core.load_plugins(get_plugins())
		self.core.on_ready_plugins()
		return
		
	def connection_lost(self, reason=None):
		super(ServerProtocol, self).connection_lost(reason)
		self.bridge.downstream_disconnected()
		self.core.unload_plugins()
		return
	
	def player_joined(self):
		super(DownstreamProtocol, self).player_joined()
		self.core.on_join_plugins()
		return

	def player_left(self):
		super(DownstreamProtocol, self).player_left()
		self.core.on_leave_plugins()
		return
	
	def super_handle_packet(self, buff, name):
		super(DownstreamProtocol, self).packet_received(buff, name)
