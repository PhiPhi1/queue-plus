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
import logging

from controllers.config import ConfigController
from controllers.upstream import UpstreamController
from plugins import Plugin


# noinspection PyMissingConstructor
class BridgePlugin(Plugin):
	def __init__(self, bridge, ticker):
		self.bridge = bridge
		self.ticker = ticker
		self.config = ConfigController.instance().data
		self.upstream_controller = UpstreamController.instance()
		
		self.buff_type = self.bridge.downstream.factory.get_buff_type(self.config["version"])
		
		self.logger = logging.getLogger("Plugin %s (%s)" % (self.__class__.__name__, self.bridge.__class__.__name__))
		self.logger.setLevel(self.config["plugins"]["log_level"])
	
	
	def packet_received(self, buff, direction, name):
		self.mirror_packet(buff, direction, name)
		
		method_pointer = "packet_%s_%s" % (direction, name)
		return self.handle_packet(method_pointer, buff)
	
	
	def mirror_packet(self, buff, direction, name):
		method_pointer = "packet_mirror_%s_%s" % (direction, name)
		self.handle_packet(method_pointer, buff)
		return
	
	
	def send_packet(self, name, *data):
		raise Exception("use self.bridge.endpoint.send_packet instead")
	
	
def get_plugins():
	from plugins.bridge.hot_swap import HotSwapPlugin
	from plugins.bridge.commands import CommmandsPlugin
	from plugins.bridge.id_correction import IdCorrection
	# from plugins.bridge.waiting_server import WaitingServerPlugin
	from plugins.bridge.queue_bossbar import QueueBossBarPlugin
	from plugins.bridge.notifications import NotificationsPlugin
	
	return [
		IdCorrection,
		HotSwapPlugin,
		CommmandsPlugin,
		# WaitingServerPlugin,
		QueueBossBarPlugin,
		NotificationsPlugin
	]
