#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (scoreboard.py) is part of Queue Plus.
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


def packet_mirror_scoreboard_objective(self, buff):
	buff.save()
	name = buff.unpack_string()
	mode = buff.unpack("b")
	buff.restore()
	if name not in list(self.processed_data["scoreboard_objective"]):
		self.processed_data["scoreboard_objective"][name] = []

	if mode == 1:
		del self.processed_data["scoreboard_objective"][name]
		return
	
	self.processed_data["scoreboard_objective"][name].append(buff.read())
	return


def serialize_scoreboard_objective(self):
	out = []
	for (name) in list(self.processed_data["scoreboard_objective"]):
		for buffer_data in self.processed_data["scoreboard_objective"][name]:
			out.append(("scoreboard_objective", buffer_data))
	return out


def packet_mirror_display_scoreboard(self, buff):
	buff.save()
	position = buff.unpack("b")
	# name = buff.unpack_string()
	buff.restore()
	
	self.processed_data["display_scoreboard"][position] = buff.read()
	return


def serialize_display_scoreboard(self):
	out = []
	for (position) in list(self.processed_data["display_scoreboard"]):
		out.append(("display_scoreboard", self.processed_data["display_scoreboard"][position]))
	return out


def packet_mirror_update_score(self, buff):
	buff.save()
	uuid = buff.unpack_uuid()
	action = buff.unpack("b")
	buff.restore()
	
	self.processed_data["update_score"][uuid] = buff.read()
	
	if action == 1:
		del self.processed_data["update_score"][uuid]
	return


def serialize_update_score(self):
	out = []
	for (uuid) in self.processed_data["update_score"]:
		out.append(("update_score", self.processed_data["update_score"][uuid]))
	return out


def packet_mirror_teams(self, buff):
	buff.save()
	name = buff.unpack_string()
	mode = buff.unpack("b")
	buff.restore()
	
	if name not in list(self.processed_data["teams"]):
		self.processed_data["teams"][name] = []
	
	if mode == 1:
		del self.processed_data["teams"][name]
		buff.discard()
		return
	
	self.processed_data["teams"][name].append(buff.read())
	return


def serialize_teams(self):
	out = []
	for (name) in list(self.processed_data["teams"]):
		for buffer_data in list(self.processed_data["teams"][name]):
			out.append(("teams", buffer_data))
	return out
	
	
def packet_mirror_boss_bar(self, buff):
	buff.save()
	
	uuid = buff.unpack_uuid()
	action = buff.unpack_varint()
	
	if uuid not in self.processed_data["boss_bar"]:
		self.processed_data["boss_bar"][uuid] = {}
	
	if action == 1:
		del self.processed_data["boss_bar"][uuid]
		return
	
	buff.restore()
	self.processed_data["boss_bar"][uuid][action] = buff.read()
	
	# fix for boss bar not showing up when created
	if action == 0:
		self.processed_data["boss_bar"][uuid][2] = buff.pack_uuid(uuid) + buff.pack_varint(2) + buff.pack("f", 1)
	
	return


def serialize_boss_bar(self):
	out = []
	for (uuid) in list(self.processed_data["boss_bar"]):
		for (action) in list(self.processed_data["boss_bar"][uuid]):
			out.append(("boss_bar", self.processed_data["boss_bar"][uuid][action]))
	return out
