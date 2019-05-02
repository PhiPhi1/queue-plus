#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (bridges.py) is part of Queue Plus.
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


def setup_bridge(self, bridge):
	if self.in_game:
		self.logger.debug("setting up bridge")
		
		bridge.upstream_factory_class = self.factory.__class__
		bridge.upstream_factory = self.factory
		bridge.upstream = self
		self.logger.debug("set bridge upstream attributes")
		
		bridge.upstream_ready()
	return


def add_forwarding_bridge(self, bridge):
	self.factory.add_bridge(bridge)
	self.setup_bridge(bridge)
	self.bots.on_bridge_add(bridge)
	return


def remove_forwarding_bridge(self, bridge):
	self.logger.debug("removing bridge")
	self.bots.on_bridge_remove(bridge)
	
	self.factory.remove_control(bridge)
	self.factory.remove_bridge(bridge)
	return
