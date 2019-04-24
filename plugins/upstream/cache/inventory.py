#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (inventory.py) is part of Queue Plus.
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

def packet_mirror_window_items(self, buff):
	buff.save()
	window_id = buff.unpack("B")
	buff.restore()
	self.processed_data["window_items"][window_id] = buff.read()
	return


def serialize_window_items(self):
	out = []
	for (window_id) in list(self.processed_data["window_items"]):
		out.append(("window_items", self.processed_data["window_items"][window_id]))
	return out


def packet_mirror_set_slot(self, buff):
	buff.save()
	window_id, slot = buff.unpack("bh")
	buff.restore()
	self.processed_data["set_slot"][window_id, slot] = buff.read()
	return


def serialize_set_slot(self):
	out = []
	for (window_id, slot) in list(self.processed_data["set_slot"]):
		out.append(("set_slot", self.processed_data["set_slot"][window_id, slot]))
	return out
	
	
def packet_mirror_map_data(self, buff):
	buff.save()
	map_id = buff.unpack_varint()
	buff.restore()
	self.processed_data["map_data"][map_id] = buff.read()
	return


def serialize_map_data(self):
	out = []
	for (map_id) in list(self.processed_data["map_data"]):
		out.append(("map_data", self.processed_data["map_data"][map_id]))
	return out
