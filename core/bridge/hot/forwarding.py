#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (forwarding.py) is part of Queue Plus.
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

		
def enable_forwarding(self):
	self.forwarding = True
	
	self.logger.debug("forwarding enabled")
	
	if self.upstream.factory.request_control(self):
		self.logger.info("Has control of protocol")
	else:
		self.logger.info("Does not have control of protocol")
	return


def disable_forwarding(self):
	self.forwarding = False
	
	if self.upstream and (not self.upstream.closed) and (self in self.upstream.factory.bridges):
		self.upstream.remove_forwarding_bridge(self)
	
	self.logger.debug("forwarding disabled sucessfully")
	return


# noinspection PyUnusedLocal
def enable_fast_forwarding(self):
	raise Exception("Fast forwarding is not available for hot swappable bridges")
