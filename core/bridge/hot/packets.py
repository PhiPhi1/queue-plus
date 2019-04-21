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


def packet_received(self, buff, direction, name):
	if name == "join_game" and not self.joined_game:
		self.joined_game = True
	
	buff.save()
	
	self.mirror_packet(buff, direction, name)
	
	# check if has forwarding permission before dispatching
	if (direction == "upstream" and self.upstream and self.upstream.factory.check_permission(self)) or direction == "downstream":
		buff.restore()
		
		dispatched = self.dispatch((direction, name), buff)
		
		if not dispatched:
			self.packet_unhandled(buff, direction, name)
	return


def mirror_packet(self, buff, direction, name):
	if not self.dispatch(("mirror", direction, name), buff):
		buff.discard()
	return


def packet_unhandled(self, buff, direction, name):
	if direction == "downstream":
		self.downstream.send_packet(name, buff.read())
	elif direction == "upstream":
		self.upstream.send_packet(name, buff.read())
	return
