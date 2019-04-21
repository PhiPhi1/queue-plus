#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (entity.py) is part of Queue Plus.
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
#
#      This file (entity.py) is part of Queue Plus.
#
#      Queue Plus is a proxy service that is designed to be highly modular.
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


def packet_mirror_entity(self, buff, name):
	buff.save()
	entity_id = buff.unpack_varint()
	buff.restore()
	
	if entity_id not in list(self.processed_data["entity"]):
		self.processed_data["entity"][entity_id] = []
	
	self.processed_data["entity"][entity_id].append((name, buff.read()))
	return


def serialize_entity(self):
	out = []
	for entity_id in list(self.processed_data["entity"]):
		for entity_buff in list(self.processed_data["entity"][entity_id]):
			out.append(entity_buff)
	return out


def packet_mirror_destroy_entities(self, buff):
	entity_ids = []
	
	# converts the packet array into a readable array
	entity_count = buff.unpack_varint()
	for _ in range(entity_count):
		entity_ids.append(buff.unpack_varint())
		

	for entity_id in entity_ids:
		# removes entity from cache
		del self.processed_data["entity"][entity_id]
		
		# removes entity from attached entities
		if entity_id in list(self.processed_data["attach_entity"]):
			del self.processed_data["attach_entity"][entity_id]
		
		# removes entity from set_passengers
		if entity_id in list(self.processed_data["set_passengers"]):
			del self.processed_data["set_passengers"][entity_id]
			
	return


def packet_mirror_attach_entity(self, buff):
	buff.save()
	attached_eid, controlling_eid = buff.unpack("ii")
	
	if attached_eid not in list(self.processed_data["entity"]):
		buff.discard()
		return
	
	if controlling_eid == -1:
		del self.processed_data["attach_entity"][attached_eid]
		buff.discard()
		return
	
	buff.save()
	self.processed_data["attach_entity"][attached_eid] = buff.read()
	return


def serialize_attach_entity(self):
	out = []
	for attached_eid in list(self.processed_data["attach_entity"]):
		out.append(("attach_entity", self.processed_data["attach_entity"][attached_eid]))
	return out


def packet_mirror_set_passengers(self, buff):
	buff.save()
	entity_id = buff.unpack_varint()
	
	if entity_id not in list(self.processed_data["entity"]):
		buff.discard()
		return

	buff.restore()
	self.processed_data["set_passengers"][entity_id] = buff.read()
	return


def serialize_set_passengers(self):
	out = []
	for entity_id in list(self.processed_data["set_passengers"]):
		out.append(("set_passengers", self.processed_data["set_passengers"][entity_id]))
	return out


def packet_mirror_remove_entity_effect(self, buff):
	buff.save()
	entity_id = buff.unpack_varint()
	
	if entity_id not in list(self.processed_data["entity"]):
		buff.discard()
		return
	
	buff.restore()
	if entity_id not in list(self.processed_data["remove_entity_effect"]):
		self.processed_data["remove_entity_effect"][entity_id] = []
	
	self.processed_data["remove_entity_effect"][entity_id].append(buff.read())
	return


def serialize_remove_entity_effect(self):
	out = []
	for (entity_id) in list(self.processed_data["remove_entity_effect"]):
		for buff_data in list(self.processed_data["remove_entity_effect"][entity_id]):
			out.append(("remove_entity_effect", buff_data))
	return out
