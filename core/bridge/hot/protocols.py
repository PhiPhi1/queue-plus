#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (protocols.py) is part of Queue Plus.
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
from headless.upstream.factory.the_void import TheVoidFactory

# TODO: change to be setup in config
default_factory_settings = {
	"class": TheVoidFactory,
	"host": None,
	"port": None
}


def switch_protocol(self, protocol):
	self.logger.debug("switching protocol")
	
	# checks if protocol is the same and if its set
	if protocol and protocol == self.upstream:
		self.logger.info("same_connection, You are already connected to this account")
		return
	
	self.disable_forwarding()
	protocol.add_forwarding_bridge(self)
	return


def send_to_the_void(self):
	sessions = self.upstream_controller.sessions.protocols
	from headless.upstream.protocol.the_void import TheVoidProtocol
	
	for session in sessions:
		if isinstance(session, TheVoidProtocol):
			self.switch_protocol(session)
			return
	
	self.upstream_controller.load_pseudo_protocol(self.default_factory_settings["class"], self)
	return
