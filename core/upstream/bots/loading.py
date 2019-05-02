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
import importlib
import json


def load_bots(self):
	self.protocol.logger.debug("Loading Bots")
	username = self.protocol.factory.player_username

	if username not in self.bot_info["accounts"]:
		return
	
	packages = self.bot_info["accounts"][self.protocol.factory.player_username]["bots"]

	for package in packages:
		if package in self.bot_info["bots"]:
			self.load_bot(self.bot_info["bots"][package]["class"])
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
		"running": False
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
	path = "bots/config.json"
	out = {
		"bots": {},
		"accounts": {}
	}
	
	with open(path) as config_file:
		data = json.load(config_file)
	
	for bot in data["bots"]:
		m = importlib.import_module("bots." + bot["package"])
		c = getattr(m, bot["class"])
		
		out["bots"][bot["package"]] = {
			"package": m,
			"class": c
		}
	
	for account in data["accounts"]:
		out["accounts"][account["username"]] = {
			"username": account["username"],
			"bots": account["bots"]
		}
		
	return out


def get_bot_classes(self):
	bot_classes = []
	for bot_data in list(self.bot_info["bots"]):
		bot_classes.append(self.bot_info["bots"][bot_data]["class"])
	return bot_classes
