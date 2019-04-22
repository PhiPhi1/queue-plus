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
import csv
import os

from plugins.upstream import UpstreamPlugin


class CachingPlugin(UpstreamPlugin):
	# importing entity packets into namespace
	from plugins.upstream.cache.entity import packet_mirror_attach_entity, packet_mirror_destroy_entities, packet_mirror_entity, packet_mirror_remove_entity_effect, \
		packet_mirror_set_passengers, serialize_attach_entity, serialize_entity, serialize_remove_entity_effect, serialize_set_passengers, packet_mirror_spawn_player, serialize_spawn_player
	
	# importing world packets into namespace
	from plugins.upstream.cache.world import packet_mirror_block_change, packet_mirror_chunk_data, packet_mirror_multi_block_change, packet_mirror_unload_chunk, \
		packet_mirror_update_block_entity, serialize_block_change, serialize_chunk_data, serialize_multi_block_change, serialize_update_block_entity, is_in_chunk
	
	# importing player into namespace
	from plugins.upstream.cache.player import packet_mirror_join_game, packet_mirror_player_position_and_look
	
	# importing inventory into namespace
	from plugins.upstream.cache.inventory import packet_mirror_map_data, packet_mirror_set_slot, packet_mirror_window_items, serialize_map_data, serialize_set_slot, serialize_window_items
	
	# importing scoreboard into namespace
	from plugins.upstream.cache.scoreboard import packet_mirror_boss_bar, packet_mirror_display_scoreboard, packet_mirror_scoreboard_objective, packet_mirror_teams, packet_mirror_update_score
	
	@classmethod
	def load_data(cls, file, output):
		file = os.path.join(os.getcwd(), file)
		with open(file, "r") as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				output.append(row["packet"])
		return
	
	
	def __init__(self, *args, **kwargs):
		self.packet_blacklist = []
		self.packet_process = []
		self.packet_static = []
		self.loading_strategy = []
		
		self.data = []
		self.static_data = {}
		self.processed_data = {}
		
		super(CachingPlugin, self).__init__(*args, **kwargs)
	
	
	def setup(self):
		self.load_data('assets/cache/blacklist.csv', self.packet_blacklist)
		self.load_data('assets/cache/process.csv', self.packet_process)
		self.load_data('assets/cache/static.csv', self.packet_static)
		self.load_data('assets/cache/loading_strategy.csv', self.loading_strategy)
		
		for name in self.packet_process:
			self.processed_data[name] = {}
		return
	
	# noinspection PyArgumentList
	def mirror_packet(self, buff, name):
		if name in self.packet_blacklist:
			buff.discard()
		
		elif name in self.packet_static:
			self.static_data[name] = buff.read()
		
		elif name.startswith("entity") or name.startswith("spawn"):
			self.packet_mirror_entity(buff, name)
		
		elif name in self.packet_process:
			method_pointer = "packet_mirror_%s" % name
			self.handle_packet(method_pointer, buff)
		
		else:
			self.data.append((name, buff.read()))
		
		return
	
	def concat_to_array(self):
		out = []
		
		# TODO: try to make unhandled packets adhere to the loading strategy
		out.extend(self.data)
		
		for name in self.loading_strategy:
			if name in self.processed_data:
				method_pointer = "serialize_%s" % name
				handler = getattr(self, method_pointer, None)
				if handler:
					data = handler()
					out.extend(data)
			
			if name in self.static_data:
				out.append((name, self.static_data[name]))
		
		return out
