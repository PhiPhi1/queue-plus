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


class Plugin:
	config = ConfigController.instance().data
	
	
	def __init__(self, protocol, ticker):
		self.protocol = protocol
		self.ticker = ticker
		
		self.buff_type = self.protocol.buff_type
		
		self.logger = logging.getLogger("Plugin %s (%s)" % (self.__class__.__name__, self.protocol.__class__.__name__))
		self.logger.setLevel(self.config["plugins"]["log_level"])
	
	# return with false to emulate mirroring
	#
	# return types
	# continue - act as a mirror
	# finish - let plugins finish but dont go after that
	# break - no more plugins will be looped
	def handle_packet(self, method_pointer, buff):
		handler = getattr(self, method_pointer, None)
		
		if handler:
			try:
				handled = handler(buff)
				assert len(buff) == 0, "Packet too long: %s" % method_pointer
			except Exception as e:
				print("plugin error", method_pointer, e)
				handled = "continue"
			
			if handled == "finish":
				return "finish"
			elif handled == "break":
				return "break"
		
		return "continue"
	
	# callbacks
	# called right after plugin is constructed
	def setup(self):
		self.logger.debug("setting up")
		return
	
	# called after all plugins are initialized
	def on_ready(self):
		return
	
	# when the protocol "despawns"
	def on_unload(self):
		return
	
	# when the protocol join the game
	def on_join(self):
		return
	
	# when the protocol leaves the game
	def on_leave(self):
		return
