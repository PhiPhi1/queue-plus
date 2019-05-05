#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (startup.py) is part of Queue Plus.
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


def start_bot(self, bot):
	bot_running = False
	if bot in self.bots:
		bot_running = bot.running
		
	if bot_running:
		return
	
	bot.running = True
	bot.on_start()


def stop_bot(self, bot):
	bot_running = False
	if bot in self.bots:
		bot_running = bot.running
	
	if not bot_running:
		return
	
	bot.running = False
	bot.on_stop()


def update_bots(self):
	for bot in self.bots:
		# checks if symbiosis is conflicting
		symbiotic_conflict = (not bot.loading["symbiotic"]) == self.protocol.factory.bridges.__len__() > 0
		if symbiotic_conflict:
			self.stop_bot(bot)
		else:
			self.start_bot(bot)
	return
