#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (loading.py) is part of Queue Plus.
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
from bots import get_bots as _get_bots, Bots


def load_bots(self):
	self.protocol.logger.debug("Loading Bots")
	for bot_class in self.get_bots():
		self.load_bot(bot_class)
	return


def load_bot(self, bot_class):
	# does not load an already loaded bot
	loaded_bot = self.get_loaded_bot(bot_class)
	if loaded_bot is not None:
		bot_running = False
		if loaded_bot in list(self.bots):
			bot_running = self.bots[loaded_bot]["running"]
		
		if not bot_running:
			self.bots[loaded_bot]["running"] = True
			loaded_bot.on_start()
		return
	
	bot = bot_class(self.protocol, self.protocol.ticker)
	self.bots[bot] = {
		"protocol": bot,
		"running" : False
	}
	self.protocol.logger.debug("loaded bot %s" % bot)
	
	self.bots[bot]["running"] = True
	bot.on_start()
	return


def unload_bots(self):
	for bot in list(self.bots):
		# bot.on_stop()
		self.unload_bot(self.bots[bot]["protocol"])
	return


def unload_bot(self, bot):
	# does not load an already loaded bot
	found_bot = False
	for _bot in list(self.bots):
		if self.bots[_bot]["protocol"] == bot:
			found_bot = True
			break
	
	if not found_bot:
		return
	
	# bot.on_unload()
	# while bot in list(self.bots:
	# 	self.bots.remove(bot)
	
	bot.on_stop()
	
	bot_running = False
	if bot in list(self.bots):
		bot_running = self.bots[bot]["running"]
	
	self.bots[bot]["running"] = False
	# if bot:
	# 	del bot
	
	return


def get_loaded_bot(self, bot_class):
	for bot in list(self.bots):
		if isinstance(self.bots[bot]["protocol"], bot_class):
			return self.bots[bot]["protocol"]
	return None


def get_bots(self):
	return _get_bots()
