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
from quarry.net.ticker import Ticker

from core import CoreProtocol
from core.bridge.hot import HotBridge
from plugins.bridge import get_plugins


class ProxyBridge(HotBridge):
	ticker_type = Ticker
	
	from core.bridge.proxy.packets import packet_received
	
	def __init__(self, *args, **kwargs):
		self.core = CoreProtocol(self)
		self.ticker = self.ticker_type(self.logger)
		
		super(ProxyBridge, self).__init__(*args, **kwargs)
		
		self.setup()
	
	def setup(self):
		self.core.load_plugins(get_plugins())
		self.core.on_ready_plugins()
		
		self.ticker.start()
		return
	
	
	def downstream_disconnected(self, *args, **kwargs):
		self.core.on_leave_plugins()
		self.core.unload_plugins()
		
		super(ProxyBridge, self).downstream_disconnected(*args, **kwargs)
		return
	
	
	def switch_protocol(self, *args, **kwargs):
		self.core.on_leave_plugins()
		super(ProxyBridge, self).switch_protocol(*args, **kwargs)
		self.core.on_join_plugins()
		return
	
	
	def super_handle_packet(self, buff, direction, name):
		super(ProxyBridge, self).packet_received(buff, direction, name)
		return
