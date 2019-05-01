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
from bots import get_bots


class UpstreamBots:
	def __init__(self, protocol):
		self.bots = []
		self.protocol = protocol
		self.ticker = protocol.ticker
	
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
		bot = bot_class(self.protocol, self.ticker)
		self.bots.append(bot)
		print("loaded bot %s" % bot)
		return
	
	def unload_bots(self):
		for bot in self.bots:
			self.unload_bot(bot)
		return
	
	def unload_bot(self, bot):
		bot.on_unload()
		while bot in self.bots:
			self.bots.remove(bot)
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
	
	def get_bots(self):
		return get_bots()
