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

	for bot_package in self.bot_info:
		self.load_bot(self.bot_info[bot_package]["class"])
	return


def load_bot(self, bot_class):
	# does not load an already loaded bot
	loaded_bot = self.get_loaded_bot(bot_class)
	if loaded_bot is not None:
		self.start_bot(loaded_bot)
		return

	bot = bot_class(self.protocol, self.protocol.ticker)
	self.bots.append(bot)
	self.protocol.logger.debug("loaded bot %s" % bot)
	return


def unload_bots(self):
	for bot in list(self.bots):
		self.unload_bot(bot)
	return


def unload_bot(self, bot):
	# # does not load an already loaded bot
	# found_bot = False
	# for _bot in list(self.bots):
	# 	if self.bots[_bot]["protocol"] == bot:
	# 		found_bot = True
	# 		break
	#
	# if not found_bot:
	# 	return
	#
	# # bot.on_unload()
	# # while bot in list(self.bots:
	# # 	self.bots.remove(bot)
	#
	# bot.on_stop()
	#
	# bot_running = False
	# if bot in list(self.bots):
	# 	bot_running = self.bots[bot]["running"]
	#
	# self.bots[bot]["running"] = False
	# # if bot:
	# # 	del bot
	
	return


def get_bots(self):
	username = self.protocol.factory.player_username
	path = "bots/config.json"
	out = {}

	with open(path) as config_file:
		data = json.load(config_file)

	accounts = [d['username'] for d in data["accounts"]]

	if username not in accounts:
		return out
	
	username_index = accounts.index(username)
	bot_packages = data["accounts"][username_index]["bots"]
	
	for bot in data["bots"]:
		if bot["package"] not in bot_packages:
			continue

		m = importlib.import_module("bots." + bot["package"])
		c = getattr(m, bot["class"])

		out[bot["package"]] = {
			"package": m,
			"class": c
		}
	
	return out


def get_bot_classes(self):
	bot_classes = []
	for bot_data in list(self.bot_info):
		bot_classes.append(self.bot_info[bot_data]["class"])
	return bot_classes


def get_loaded_bot(self, bot_class):
	for bot in list(self.bots):
		if isinstance(self.bots[bot]["protocol"], bot_class):
			return self.bots[bot]["protocol"]
	return None
