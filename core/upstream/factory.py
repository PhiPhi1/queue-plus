#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (factory.py) is part of Queue Plus.
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


from quarry.net.client import ClientFactory
from twisted.internet.protocol import ReconnectingClientFactory

from core.upstream import UpstreamProtocol
from controllers.config import ConfigController


class UpstreamFactory(ClientFactory, ReconnectingClientFactory):
	config = ConfigController.instance().data
	protocol = UpstreamProtocol
	account_manager = None
	protocol_callback = None
	
	force_protocol_version = config["version"]
	log_level = config["client"]["log_level"]
	
	
	def __init__(self, *args, **kwargs):
		self.bridges = []
		self.controlling_bridges = []
		
		self.player_username = None
		
		super(UpstreamFactory, self).__init__(*args, **kwargs)
	
	
	def add_bridge(self, bridge):
		self.bridges.append(bridge)
		return
	
	
	def remove_bridge(self, bridge):
		while bridge in self.bridges:
			self.bridges.remove(bridge)
		return
	
	
	def request_control(self, bridge):
		if bridge in self.controlling_bridges:
			return True
		
		self.controlling_bridges.append(bridge)
		return True
	
	
	def remove_control(self, bridge):
		while bridge in self.controlling_bridges:
			self.controlling_bridges.remove(bridge)
		return
	
	
	def check_permission(self, bridge):
		return bridge in self.controlling_bridges
