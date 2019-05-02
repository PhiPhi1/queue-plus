#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (packets.py) is part of Queue Plus.
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


def packet_received(self, buff, name):
	buff.save()
	
	dispatched = self.core.route_packet_to_plugins(buff, name)
	
	if not dispatched:
		for bridge in self.factory.bridges:
			if bridge.forwarding:
				buff.restore()
				bridge.packet_received(buff, self.recv_direction, name)
		
		buff.restore()
		self.bots.route_bot_packet(buff, name)
		
		if not self.factory.bridges.__len__() > 0:
			buff.restore()
			self.super_handle_packet(buff, name)
	
	buff.discard()
	return


def log_packet(self, prefix, name):
	forwarding = ""
	
	if self.factory.bridges.__len__() > 0 and self.protocol_mode == "recv":
		forwarding = "%s %s bridges " % (prefix, self.factory.bridges.__len__())
	
	message = "Packet %s%s %s/%s" % (forwarding, prefix, self.protocol_mode, name)
	
	self.logger.debug(message)
	return
