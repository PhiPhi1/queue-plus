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
from quarry.types.uuid import UUID as QuarryUUID

import uuid as py_uuid
from plugins.bridge import BridgePlugin


class QueueBossBarPlugin(BridgePlugin):
	def __init__(self, *args, **kwargs):
		super(QueueBossBarPlugin, self).__init__(*args, **kwargs)

		self.watched_protocols = {}

	def add_watched_protocol(self, session):
		def protocol_update():
			self.update_boss_bar(session)
		
		if session in self.watched_protocols:
			return
		
		upstream_queue = self.get_queue_plugin(session)
		player_info = self.get_player_info(session)
		bar_uuid = self.generate_uuid()
		username = player_info.player_username
		
		if not username:
			return
		
		self.watched_protocols[session] = {
			"protocol": session,
			"username": username,
			"uuid": bar_uuid,
			"callback": protocol_update,
			"spawned": False
		}
		
		self.update_boss_bar(session)
		upstream_queue.add_queue_listener(protocol_update)
	
	def removed_watched_protocol(self, session):
		upstream_queue = self.get_queue_plugin(session)
		session_metadata = self.watched_protocols[session]
		upstream_queue.remove_queue_listener(session_metadata["callback"])

		if session in self.watched_protocols:
			while session in self.watched_protocols:
				del self.watched_protocols[session]

		self.bridge.packet_received(self.buff_type(self.buff_type.pack_uuid(session_metadata["uuid"]) + self.buff_type.pack_varint(1)), "downstream", "boss_bar")

		# sending an update to make sure that the client knows that it has been removed
		self.bridge.packet_received(self.buff_type(self.buff_type.pack_uuid(session_metadata["uuid"]) + self.buff_type.pack_varint(2) + self.buff_type.pack("f", 0)), "downstream", "boss_bar")

		
	def create_boss_bar(self, session):
		if self.watched_protocols[session]["spawned"]:
			return
		
		packed_uuid = self.buff_type.pack_uuid(self.watched_protocols[session]["uuid"])
		action = self.buff_type.pack_varint(0)
		title = self.buff_type.pack_chat(" ")
		health = self.buff_type.pack("f", 1)
		color = self.buff_type.pack_varint(4)
		division = self.buff_type.pack_varint(4)
		flags = self.buff_type.pack("x")

		self.bridge.packet_received(self.buff_type(packed_uuid + action + title + health + color + division + flags), "downstream", "boss_bar")
		self.watched_protocols[session]["spawned"] = True
	
	
	def update_boss_bar(self, session):
		upstream_queue = self.get_queue_plugin(session)
		start_pos = upstream_queue.queue_starting_position
		pos = upstream_queue.queue_position
		
		if not self.watched_protocols[session]["spawned"]:
			self.create_boss_bar(session)
		
		if session not in self.watched_protocols:
			upstream_queue.remove_queue_listener(self.watched_protocols[session]["callback"])
			return
		
		if not upstream_queue.in_queue and upstream_queue.queue_position is -1 and upstream_queue.queue_starting_position is -1:
			from plugins.bridge.notifications import NotificationsPlugin
			notifications = self.bridge.core.get_plugin(NotificationsPlugin)
			
			message = "§c%s has been disconnected" % self.watched_protocols[session]["username"]
			notifications.send_chat_notification(message, True)
			
			self.removed_watched_protocol(session)
			return
		
		if not upstream_queue.in_queue:
			from plugins.bridge.notifications import NotificationsPlugin
			notifications = self.bridge.core.get_plugin(NotificationsPlugin)
			
			message = "§a[%s] %s has finished the queue" % (self.upstream_controller.sessions.protocols.index(session), self.watched_protocols[session]["username"])

			notifications.send_chat_notification(message, True)

			self.removed_watched_protocol(session)
			return
		
		session_metadata = self.watched_protocols[session]

		size = float(pos / start_pos)
		if (start_pos is -1) or (pos is -1):
			size = float(1)
		self.update_bar_health(session_metadata["uuid"], size)
		
		queue_pos_string = str(pos)
		if pos is -1:
			queue_pos_string = "--"
		new_message = "§6%s | position: %s" % (session_metadata["username"], queue_pos_string)
		self.update_bar_display(session_metadata["uuid"], new_message)
	
	def update_bar_health(self, uuid, new_size):
		packed_uuid = self.buff_type.pack_uuid(uuid)
		health = self.buff_type.pack("f", new_size)
		self.bridge.packet_received(self.buff_type(packed_uuid + self.buff_type.pack_varint(2) + health), "downstream", "boss_bar")
	
	def update_bar_display(self, uuid, new_message):
		packed_uuid = self.buff_type.pack_uuid(uuid)
		packed_message = self.buff_type.pack_chat(new_message)
		self.bridge.packet_received(self.buff_type(packed_uuid + self.buff_type.pack_varint(3) + packed_message), "downstream", "boss_bar")
		
	def get_queue_plugin(self, session):
		from plugins.upstream.queue import QueuePlugin
		return session.core.get_plugin(QueuePlugin)
	
	def get_player_info(self, session):
		from plugins.upstream.player_info import PlayerInfoPlugin
		return session.core.get_plugin(PlayerInfoPlugin)
	
	def generate_uuid(self):
		return QuarryUUID.from_hex(py_uuid.uuid4().hex)

	def on_unload(self):
		for session in list(self.watched_protocols):
			self.removed_watched_protocol(session)
