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
#
#      This file (packets.py) is part of Queue Plus.
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


def packet_received(self, buff, name):
	buff.save()
	
	dispatched = self.core.route_packet_to_plugins(buff, name)
	
	if not dispatched:
		buff.restore()
		
		if self.bridge.forwarding:
			self.bridge.packet_received(buff, self.recv_direction, name)
		else:
			self.super_handle_packet(buff, name)
	else:
		buff.discard()
	return


def log_packet(self, prefix, name):
	forwarding = ""
	
	if self.bridge.forwarding and self.protocol_mode == "recv":
		forwarding = "%s %s bridges " % (prefix, 1)
	
	message = "Packet %s%s %s/%s" % (forwarding, prefix, self.protocol_mode, name)
	
	self.logger.debug(message)
