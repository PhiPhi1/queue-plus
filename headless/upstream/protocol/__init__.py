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

from quarry.net.client import ClientProtocol
from quarry.net.crypto import Cipher

from controllers.config import ConfigController
from core import CoreProtocol
from core.upstream import UpstreamProtocol, UpstreamBots
from plugins.upstream import get_plugins


class PseudoProtocol(UpstreamProtocol):
	# replaces all connection details with pseudo info
	# noinspection PyMissingConstructor,PyUnusedLocal,PyUnusedLocal
	def __init__(self, factory, *args, **kwargs):
		self.bots = UpstreamBots(self)
		
		def no_bots():
			return []
		self.bots.get_bots = no_bots
		
		self.config = ConfigController.instance().data
		self.core = CoreProtocol(self)

		self.factory = factory

		self.buff_type = self.factory.get_buff_type(self.config["version"])
		self.recv_buff = self.buff_type()
		self.cipher = Cipher()

		self.logger = logging.getLogger("%s{%s}" % (
			self.__class__.__name__,
			"pseudo host"))
		self.logger.setLevel(self.factory.log_level)

		self.ticker = self.factory.ticker_type(self.logger)
		self.ticker.start()
		
		self.setup()
	
	def setup(self):
		super(PseudoProtocol, self).setup()
		super(PseudoProtocol, self).player_joined()
		return
	
	# noinspection PyArgumentList
	def player_joined(self):
		super(ClientProtocol, self).player_joined()
		self.core.on_join_plugins()
		
		if self.factory.protocol_callback:
			try:
				self.factory.protocol_callback(self)
			except Exception as e:
				print("Error in protocol callback", e)
		
		for bridge in self.factory.bridges:
			self.setup_bridge(bridge)
		return

	def packet_received(self, buff, name):
		buff.save()
		for bridge in self.factory.bridges:
			bridge.packet_received(buff, self.recv_direction, name)
			buff.restore()
		buff.discard()
		return
	
	# discards all packets that would normally be forwarded
	def send_packet(self, name, *data):
		pass
	
	
	def player_left(self):
		pass
