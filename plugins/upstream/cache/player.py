#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (player.py) is part of Queue Plus.
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


def packet_mirror_join_game(self, buff):
	buff.save()
	_, gamemode, dimension, difficulty, _ = buff.unpack("iBiBB")
	level_type = buff.unpack_string()
	_ = buff.unpack("?")
	
	self.static_data["respawn"] = buff.pack("iBB", dimension, difficulty, gamemode) + buff.pack_string(level_type)
	buff.restore()
	self.static_data["join_game"] = buff.read()
	return
	
	
def packet_mirror_player_position_and_look(self, buff):
	new_buffer = b""
	x, y, z, yaw, pitch, flags = buff.unpack("dddffb")
	buff.discard()
	new_buffer += buff.pack("dddffb", x, y, z, yaw, pitch, flags) + buff.pack_varint(-1)
	self.static_data["player_position_and_look"] = new_buffer
	return


def packet_mirror_player_list_item(self, buff):
	buff.save()
	action = buff.unpack_varint()
	
	if self.processed_data["player_list_item"] is None:
		self.processed_data["player_list_item"] = {}

	for _ in range(buff.unpack_varint()):
		uuid = buff.unpack_uuid()
		
		if uuid not in self.processed_data["player_list_item"]:
			self.processed_data["player_list_item"][uuid] = {}

		if action == 0:
			name = buff.unpack_string()
			properties = {}
			
			for _ in range(buff.unpack_varint()):
				p_name = buff.unpack_string()
				properties[p_name] = {
					"name": p_name
				}
				properties[p_name]["value"] = buff.unpack_string()
				
				if buff.unpack("?"):
					properties[p_name]["sig"] = buff.unpack_string()
				else:
					properties[p_name]["sig"] = None
					
			gamemode = buff.unpack_varint()
			ping = buff.unpack_varint()
			
			if buff.unpack("?"):
				disp_name = buff.unpack_chat()
			else:
				disp_name = None
			
			self.processed_data["player_list_item"][uuid] = {
				"uuid": uuid,
				"name": name,
				"properties": properties,
				"gamemode": gamemode,
				"ping": ping,
				"display": disp_name
			}
		elif action == 1:
			self.processed_data["player_list_item"][uuid]["gamemode"] = buff.unpack_varint()
		elif action == 2:
			self.processed_data["player_list_item"][uuid]["ping"] = buff.unpack_varint()
		elif action == 3:
			if buff.unpack("?"):
				self.processed_data["player_list_item"][uuid]["display"] = buff.unpack_chat()
			else:
				self.processed_data["player_list_item"][uuid]["display"] = None
		elif action == 4:
			del self.processed_data["player_list_item"][uuid]
		
		buff.discard()
		return


def serialize_player_list_item(self):
	out = []
	for uuid in self.processed_data["player_list_item"]:
		player_item = self.processed_data["player_list_item"][uuid]
		if not ("uuid" in player_item and "name" in player_item and "properties" in player_item and "gamemode" in player_item and "ping" in player_item and "ping" in player_item):
			continue
			
		serialized = b""
		serialized += self.buff_type.pack_varint(0)
		serialized += self.buff_type.pack_varint(1)
		
		serialized += self.buff_type.pack_uuid(player_item["uuid"])
		serialized += self.buff_type.pack_string(player_item["name"])
		serialized += self.buff_type.pack_varint(len(player_item["properties"]))
		
		for prop in player_item["properties"]:
			serialized += self.buff_type.pack_string(player_item["properties"][prop]["name"])
			serialized += self.buff_type.pack_string(player_item["properties"][prop]["value"])
			serialized += self.buff_type.pack("?", player_item["properties"][prop]["sig"] is not None)
			if player_item["properties"][prop]["sig"] is not None:
				signature = player_item["properties"][prop]["sig"]
				serialized += self.buff_type.pack_string(signature)
				
		serialized += self.buff_type.pack_varint(player_item["gamemode"])
		serialized += self.buff_type.pack_varint(player_item["ping"])
		serialized += self.buff_type.pack("?", player_item["display"] is not None)
		if player_item["display"] is not None:
			serialized += self.buff_type.pack_chat(player_item["display"])
		
		out.append(("player_list_item", serialized))
	return out
