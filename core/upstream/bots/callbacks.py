#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (callbacks.py) is part of Queue Plus.
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


def on_ready_bots(self):
	for bot in list(self.bots):
		self.bots[bot]["protocol"].on_ready()
	
	return


def on_join_bots(self):
	for bot in list(self.bots):
		self.bots[bot]["protocol"].on_join()
	return


def on_leave_bots(self):
	for bot in list(self.bots):
		self.bots[bot]["protocol"].on_leave()
	return


def on_stop_bots(self):
	for bot in list(self.bots):
		self.bots[bot]["protocol"].on_stop()
	return


def on_bridge_add(self, bridge):
	for bot in list(self.bots):
		self.bots[bot]["protocol"].on_bridge_add(bridge)
	self.update_bots()
	return


def on_bridge_remove(self, bridge):
	for bot in list(self.bots):
		self.bots[bot]["protocol"].on_bridge_remove(bridge)
	self.update_bots()
	return
