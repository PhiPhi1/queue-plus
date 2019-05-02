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
#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (bots.py) is part of Queue Plus.
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


class UpstreamBots:
	from core.upstream.bots.loading import load_bots, load_bot, get_loaded_bot, get_bots, unload_bots, unload_bot
	from core.upstream.bots.callbacks import on_join_bots, on_leave_bots, on_bridge_add, on_bridge_remove, on_start_bots, on_ready_bots, on_stop_bots
	
	def __init__(self, protocol):
		self.bots = {}
		self.protocol = protocol
	
	
	def route_bot_packet(self, buff, name):
		for bot in list(self.bots):
			self.bots[bot]["protocol"].packet_received(buff, name)
		return
	
	
	def update_bots(self):
		bot_classes = self.get_bots()
		
		for bot_class in bot_classes:
			# checks i
			loaded_bot = self.get_loaded_bot(bot_class)
			
			if (not bot_class.loading["symbiotic"]) == self.protocol.factory.bridges.__len__() > 0:
				bot_running = False
				if loaded_bot in self.bots:
					bot_running = self.bots[loaded_bot]["running"]
				
				if (loaded_bot is not None) and bot_running:
					self.unload_bot(loaded_bot)
					self.protocol.logger.debug("unloading %s" % loaded_bot)
					
					# sets to true so it can be reloaded
					bot_class.loading["start"] = True
				
				# checks if bot should be restarted
				elif bot_class.loading["start"]:
					self.load_bot(bot_class)
					self.protocol.logger.debug("loaded %s" % bot_class)
		return


