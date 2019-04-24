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
from plugins.bridge import BridgePlugin


class IdCorrection(BridgePlugin):
	def __init__(self, *args, **kwargs):
		super(IdCorrection, self).__init__(*args, **kwargs)
		
		self.proxy_player_eid = None
		self.proxy_player_uuid = None
		self.proxy_player_username = None
		
		self.player_username = None
		self.player_uuid = None
		self.player_eid = None
		
		self.offline_mode = False
		
		# self.override_process = ["join_game"]
		# self.override_list = []
		# self.override_prefixes = []
		
		self.override_process = ["join_game", "combat_event", "face_player", "attach_entity", "set_passengers", "collect_item", "entity_status", "player_list_item", "spectate"]
		self.override_list = ["animation", "block_break_animation", "use_bed", "remove_entity_effect", "camera"]
		self.override_prefixes = ["entity"]
	
	def on_join(self):
		from plugins.upstream.player_info import PlayerInfoPlugin as UpstreamPlayerInfoPlugin
		from plugins.downstream.player_info import PlayerInfoPlugin as DownstreamPlayerInfoPlugin
		
		upstream_player_info = self.bridge.upstream.core.get_plugin(UpstreamPlayerInfoPlugin)
		downstream_player_info = self.bridge.downstream.core.get_plugin(DownstreamPlayerInfoPlugin)
		
		self.proxy_player_eid = upstream_player_info.player_eid
		self.proxy_player_username = upstream_player_info.player_username
		self.proxy_player_uuid = upstream_player_info.player_uuid
		
		self.offline_mode = (not self.config["client"]["online"]) or (not self.config["server"]["online"])
		
		self.player_eid = downstream_player_info.player_eid
		self.player_username = downstream_player_info.player_username
		self.player_uuid = downstream_player_info.player_uuid
		return
	
	def packet_received(self, buff, direction, name):
		if name in self.override_process:
			method_pointer = "packet_%s_%s" % (direction, name)
			return self.handle_packet(method_pointer, buff)
		elif name in self.override_list:
			return self.eid_checker(buff, direction, name)
		else:
			for prefix in self.override_prefixes:
				if name.startswith(prefix):
					return self.eid_checker(buff, direction, name)
		
		buff.discard()
		return "continue"
	
	def packet_downstream_join_game(self, buff):
		p_player_eid = buff.unpack("i")
		buff.discard()
		
		if p_player_eid == self.proxy_player_eid:
			self.proxy_player_eid = p_player_eid
		else:
			return "continue"
		
		return "break"
	
	def packet_downstream_combat_event(self, buff):
		buff.save()
		event_type = buff.unpack_varint()
		
		if event_type == 1:
			_ = buff.unpack_varint()
			buff_eid = buff.unpack("i")
			
			if buff_eid == self.proxy_player_eid:
				old = self.buff_type.pack("i", buff_eid)
				new = self.buff_type.pack("i", self.player_eid)
				
				buff.restore()
				self.resend_parsed(buff, old, new, "downstream", "combat_event")
				return "break"
		elif event_type == 2:
			buff_eid = buff.unpack_varint()
			buffe_eid = buff.unpack("i")
			_ = buff.unpack_chat()
			
			if buff_eid == self.proxy_player_eid:
				old = self.buff_type.pack_varint(buff_eid)
				new = self.buff_type.pack_varint(self.player_eid)
				
				buff.restore()
				self.resend_parsed(buff, old, new, "downstream", "combat_event")
				return "break"
			
			if buffe_eid == self.proxy_player_eid:
				old = self.buff_type.pack("i", buffe_eid)
				new = self.buff_type.pack("i", self.player_eid)
				
				buff.restore()
				self.resend_parsed(buff, old, new, "downstream", "combat_event")
				return "break"
		
		buff.discard()
		return "continue"

	def packet_downstream_face_player(self, buff):
		buff.save()
		buff.unpack_varint()
		buff.unpack("ddd?")
		buff_eid = buff.unpack_varint()
		
		if buff_eid == self.proxy_player_eid:
			old = self.buff_type.pack_varint(buff_eid)
			new = self.buff_type.pack_varint(self.player_eid)
			
			buff.restore()
			self.resend_parsed(buff, old, new, "downstream", "face_player")
			return "break"
		
		buff.discard()
		return "continue"
	
	def packet_downstream_attach_entity(self, buff):
		buff.save()
		attached_buff_eid = buff.unpack("i")
		holding_buff_eid = buff.unpack("i")
		
		if attached_buff_eid == self.proxy_player_eid or holding_buff_eid == self.proxy_player_eid:
			old = self.buff_type.pack("i", self.proxy_player_eid)
			new = self.buff_type.pack("i", self.player_eid)
			
			buff.restore()
			self.resend_parsed(buff, old, new, "downstream", "attach_entity")
			return "break"
		
		buff.discard()
		return "continue"
	
	def packet_downstream_set_passengers(self, buff):
		buff.save()
		v_eid = buff.unpack_varint()
		array_of_pass_eid = []
		
		for _ in range(buff.unpack_varint()):
			array_of_pass_eid.append(buff.unpack_varint())
			
		if v_eid == self.proxy_player_eid or self.proxy_player_eid in array_of_pass_eid:
			old = self.buff_type.pack_varint(self.proxy_player_eid)
			new = self.buff_type.pack_varint(self.player_eid)
			
			buff.restore()
			self.resend_parsed(buff, old, new, "downstream", "set_passengers")
			return "break"
		
		buff.discard()
		return "continue"
	
	def packet_downstream_collect_item(self, buff):
		buff.save()
		_ = buff.unpack_varint()
		buff_eid = buff.unpack_varint()
		
		if buff_eid == self.proxy_player_eid:
			old = self.buff_type.pack_varint(buff_eid)
			new = self.buff_type.pack_varint(self.player_eid)
			
			buff.restore()
			self.resend_parsed(buff, old, new, "downstream", "collect_item")
			return "break"
		
		buff.discard()
		return "continue"
		
	def packet_downstream_entity_status(self, buff):
		buff.save()
		buff_eid = buff.unpack("i")
		
		if buff_eid == self.proxy_player_eid:
			old = self.buff_type.pack("i", buff_eid)
			new = self.buff_type.pack("i", self.player_eid)
			
			buff.restore()
			self.resend_parsed(buff, old, new, "downstream", "entity_status")
			return "break"
		
		buff.discard()
		return "continue"
	
	def eid_checker(self, buff, direction, name):
		buff.save()
		in_eid = buff.unpack_varint()

		if in_eid == self.proxy_player_eid:
			buff.restore()
			old = self.buff_type.pack_varint(in_eid)
			new = self.buff_type.pack_varint(self.player_eid)
			self.resend_parsed(buff, old, new, direction, name)
			return "break"
		
		buff.discard()
		return "continue"
	
	# TODO plugin error packet_downstream_player_list_item maximum recursion depth exceeded while calling a Python object
	def packet_downstream_player_list_item(self, buff):
		buff.save()
		_ = buff.unpack_varint()
		for _ in range(buff.unpack_varint()):
			uuid = buff.unpack_uuid()
			buff.restore()
			
			if uuid == self.proxy_player_uuid:
				old = self.buff_type.pack_uuid(uuid)
				new = self.buff_type.pack_uuid(self.player_uuid)
				
				buff.restore()
				self.resend_parsed(buff, old, new, "downstream", "player_list_item")
				return "break"
		
		buff.discard()
		return "continue"
	
	# def packet_downstream_teams(self, buff):
	# 	buff.save()
	#
	# 	return "continue"
	
	def packet_upstream_spectate(self, buff):
		buff.save()
		buff_uuid = buff.unpack_uuid()
		if buff_uuid == self.proxy_player_uuid:
			old = self.buff_type.pack_uuid(buff_uuid)
			new = self.buff_type.pack_uuid(self.player_uuid)
			
			buff.restore()
			self.resend_parsed(buff, old, new, "upstream", "spectate")
			return "break"
		
		buff.discard()
		return "continue"

	def resend_parsed(self, buff, old, new, direction, name):
		read_buff = buff.read()
		out_buff = read_buff.replace(old, new, 1)
		
		# TODO: change to direction buff type
		parsed_buff = self.buff_type(out_buff)
		
		self.bridge.packet_received(parsed_buff, direction, name)
		return
