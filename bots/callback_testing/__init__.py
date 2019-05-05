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
from bots import Bots


class CallbackTestingBot(Bots):
	def __init__(self, *args, **kwargs):
		self.name = "default"
		self.loading = {
			# Load bot when upstream joins
			"start": True,
			# Run while bridge is connected
			"symbiotic": False
		}
	
	
	def on_ready(self):
		print("ready", self)
	
	def on_unload(self):
		print("unload", self)
	
	def on_bridge_add(self, bridge):
		print("bridge added", self)
	
	def on_bridge_remove(self, bridge):
		print("bridge removed", self)
	
	def on_join(self):
		print("joined", self)
	
	def on_leave(self):
		print("left", self)
	
	def on_start(self):
		print("start", self)
	
	def on_stop(self):
		print("stop", self)
