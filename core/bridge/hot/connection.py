#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (connection.py) is part of Queue Plus.
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


def connect(self):
	self.send_to_the_void()
	return


def downstream_disconnected(self):
	if not self.upstream:
		return
	
	if self.upstream and self.upstream.factory.check_permission(self) and not self.config["safe_disconnect"]:
		self.ustream.close()
	
	self.upstream.remove_forwarding_bridge(self)
	return


def upstream_disconnected(self):
	self.disable_forwarding()
	if not self.switching_protocol:
		self.send_to_the_void()
	self.logger.debug("upstream disconnected")
	return
