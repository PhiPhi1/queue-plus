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
from plugins.downstream import DownstreamPlugin


# noinspection PyMethodMayBeStatic
class AlwaysAlivePlugin(DownstreamPlugin):
	def __init__(self, *args, **kwargs):
		super(AlwaysAlivePlugin, self).__init__(*args, **kwargs)
		
		self.alive_task = None
	
	
	def on_join(self):
		self.alive_task = self.ticker.add_loop(20, self.update_keep_alive)
		return
	
	
	def on_leave(self):
		self.ticker.remove(self.alive_task)
		return
	
	def update_keep_alive(self):
		# 1.7.x
		if self.config["version"] <= 338:
			payload = self.buff_type.pack_varint(0)
		
		# 1.12.2
		else:
			payload = self.buff_type.pack('Q', 0)
		
		self.send_packet("keep_alive", payload)
		return
	
	# discards all the keep alive packets sent
	def packet_keep_alive(self, buff):
		buff.discard()
		return "break"
