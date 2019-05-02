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
from bots import get_bots, Bots


class UpstreamBots:
	def __init__(self, protocol):
		self.bots = []
		self.protocol = protocol
	
	def route_bot_packet(self, buff, name):
		for bot in self.bots:
			bot.packet_received(buff, name)
		return

	def load_bots(self):
		self.protocol.logger.debug("Loading Bots")
		for bot_class in self.get_bots():
			self.load_bot(bot_class)
		return
	
	def load_bot(self, bot_class):
		# does not load an already loaded bot
		loaded_bot = self.get_loaded_bot(bot_class)
		if loaded_bot is not None:
			loaded_bot.on_start()
			return
		
		bot = bot_class(self.protocol, self.protocol.ticker)
		self.bots.append(bot)
		self.protocol.logger.debug("loaded bot %s" % bot)
		
		bot.on_start()
		return
	
	def unload_bots(self):
		for bot in self.bots:
			bot.on_stop()
			self.unload_bot(bot)
		return
	
	def unload_bot(self, bot):
		# does not load an already loaded bot
		if bot not in self.bots:
			return
		
		# bot.on_unload()
		# while bot in self.bots:
		# 	self.bots.remove(bot)
		
		bot.on_stop()
		
		# if bot:
		# 	del bot
			
		return
	
	
	def on_ready_bots(self):
		for bot in self.bots:
			bot.on_ready()
		
		return
	
	
	def on_join_bots(self):
		for bot in self.bots:
			bot.on_join()
		return
	
	
	def on_leave_bots(self):
		for bot in self.bots:
			bot.on_leave()
		return
	
	def on_start_bots(self):
		for bot_class in self.get_bots():
			if bot_class.loading["start"]:
				self.load_bot(bot_class)
		return
	
	def on_stop_bots(self):
		for bot in self.bots:
			bot.on_stop()
		return
	
	def on_bridge_add(self, bridge):
		for bot in self.bots:
			bot.on_bridge_add(bridge)
		self.update_bots()
		return
	
	def on_bridge_remove(self, bridge):
		for bot in self.bots:
			bot.on_bridge_remove(bridge)
		self.update_bots()
		return
	
	def update_bots(self):
		bot_classes = self.get_bots()
		
		for bot_class in bot_classes:
			# checks i
			loaded_bot = self.get_loaded_bot(bot_class)
			
			if (not bot_class.loading["symbiotic"]) == self.protocol.factory.bridges.__len__() > 0:
				if loaded_bot is not None:
					self.unload_bot(loaded_bot)
					self.protocol.logger.debug("unloading %s" % loaded_bot)
					
					# sets to true so it can be reloaded
					bot_class.loading["start"] = True
					
				# checks if bot should be restarted
				elif bot_class.loading["start"]:
					self.load_bot(bot_class)
					self.protocol.logger.debug("loaded %s" % bot_class)
		return
	
	
	def get_loaded_bot(self, bot_class):
		for bot in self.bots:
			if isinstance(bot, bot_class):
				return bot
		return None
	
	def get_bots(self):
		return get_bots()
