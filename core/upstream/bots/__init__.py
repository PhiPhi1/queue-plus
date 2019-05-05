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
	from core.upstream.bots.loading import load_bots, load_bot, get_loaded_bot, get_bots, unload_bots, unload_bot, get_bot_classes
	from core.upstream.bots.callbacks import on_join_bots, on_leave_bots, on_bridge_add, on_bridge_remove, on_ready_bots, on_stop_bots
	
	def __init__(self, protocol):
		self.player_uuid = None
		self.player_username = None
		
		self.bots = {}
		self.protocol = protocol
		
		self.bot_info = self.get_bots()
	
	
	def route_bot_packet(self, buff, name):
		buff.save()
		for bot in list(self.bots):
			self.bots[bot]["protocol"].packet_received(buff, name)
		return
	
	
	def update_bots(self):
		pass


