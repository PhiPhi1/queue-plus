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
import random

from plugins.downstream import DownstreamPlugin


class PlayerInfoPlugin(DownstreamPlugin):
	def __init__(self, *args, **kwargs):
		super(PlayerInfoPlugin, self).__init__(*args, **kwargs)
		
		self.player_eid = random.randint(2047483647, 2147483646)
		self.player_username = None
		self.player_uuid = None
		
	def on_join(self):
		self.player_username = self.protocol.display_name
		self.player_uuid = self.protocol.uuid
		return

