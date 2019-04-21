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


from quarry.net.proxy import Bridge

from controllers.config import ConfigController
from controllers.upstream import UpstreamController


class HotBridge(Bridge):
	forwarding = None
	joined_game = None
	
	config = ConfigController.instance().data
	upstream_controller = UpstreamController.instance()
	
	log_level = config["bridge"]["log_level"]
	
	from core.bridge.hot.connection import connect, downstream_disconnected, upstream_disconnected
	from core.bridge.hot.forwarding import enable_fast_forwarding, enable_forwarding, disable_forwarding
	from core.bridge.hot.packets import packet_received, packet_unhandled, mirror_packet
	from core.bridge.hot.protocols import default_factory_settings, switch_protocol, send_to_the_void
	
	def __init__(self, *args, **kwargs):
		self.forwarding = False
		self.joined_game = False
		
		super(HotBridge, self).__init__(*args, **kwargs)

	def make_profile(self):
		raise Exception("make_profile is not available for hot swappable bridges")
	
	def upstream_ready(self):
		self.logger.debug("Upstream ready")
		self.enable_forwarding()
