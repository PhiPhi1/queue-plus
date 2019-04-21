#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (world.py) is part of Queue Plus.
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


def is_in_chunk(self, x, z):
	cx, _ = divmod(x, 16)
	cz, _ = divmod(z, 16)
	
	return (cx, cz) in list(self.processed_data["chunk_data"])
	
	
def packet_mirror_chunk_data(self, buff):
	buff.save()
	x, z = buff.unpack('ii')
	buff.restore()
	
	if not (x, z) in list(self.processed_data["chunk_data"]):
		self.processed_data["chunk_data"][x, z] = []
	
	self.processed_data["chunk_data"][x, z].append(buff.read())
	return


def serialize_chunk_data(self):
	out = []
	for (x, z) in list(self.processed_data["chunk_data"]):
		for cached_buff in list(self.processed_data["chunk_data"][x, z]):
			out.append(("chunk_data", cached_buff))
	return out


def packet_mirror_unload_chunk(self, buff):
	x, z = buff.unpack('ii')
	if (x, z) in list(self.processed_data["chunk_data"]):
		del self.processed_data["chunk_data"][x, z]
	return


def packet_mirror_update_block_entity(self, buff):
	buff.save()
	x, y, z = buff.unpack_position()
	action = buff.unpack("B")
	
	buff.restore()
	self.processed_data["update_block_entity"][x, y, z, action] = buff.read()
	return


def serialize_update_block_entity(self):
	out = []
	for (x, y, z, action) in list(self.processed_data["update_block_entity"]):
		if self.is_in_chunk(x, z):
			out.append(("update_block_entity", self.processed_data["update_block_entity"][x, y, z, action]))
		else:
			del self.processed_data["update_block_entity"][x, y, z, action]
	return out


def packet_mirror_block_change(self, buff):
	buff.save()
	x, y, z = buff.unpack_position()
	buff.restore()
	self.processed_data["block_change"][x, y, z] = buff.read()
	return


def serialize_block_change(self):
	out = []
	for (x, y, z) in list(self.processed_data["block_change"]):
		if self.is_in_chunk(x, z):
			out.append(("block_change", self.processed_data["block_change"][x, y, z]))
		else:
			del self.processed_data["block_change"][x, y, z]
	return out
	
	
def packet_mirror_multi_block_change(self, buff):
	buff.save()
	x, z = buff.unpack("ii")
	buff.restore()
	if not (x, z) in list(self.processed_data["multi_block_change"]):
		self.processed_data["multi_block_change"][x, z] = []
	
	self.processed_data["multi_block_change"][x, z].append(buff.read())
	return


def serialize_multi_block_change(self):
	out = []
	for (x, z) in list(self.processed_data["multi_block_change"]):
		if (x, z) in list(self.processed_data["chunk_data"]):
			for buffer_data in list(self.processed_data["multi_block_change"][x, z]):
				out.append(("multi_block_change", buffer_data))
		else:
			del self.processed_data["multi_block_change"][x, z]
	return out
