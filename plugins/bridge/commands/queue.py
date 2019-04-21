#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (queue.py) is part of Queue Plus.
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


def command_show_queue(self, params):
	protocol_sessions = self.upstream_controller.sessions.protocols
	
	from plugins.bridge.queue_bossbar import QueueBossBarPlugin
	queue_bar = self.bridge.core.get_plugin(QueueBossBarPlugin)
	
	if params.__len__() is 0:
		self.send_response("§6Showing all queue boss bars")
		for session in protocol_sessions:
			queue_bar.add_watched_protocol(session)
		return
	
	session_index = params[0]
	if not session_index.isdigit():
		self.send_error("Invalid session ID")
		return
	session_index = int(session_index)
	
	if not protocol_sessions.__len__() > session_index:
		self.send_error("Invalid session ID")
		return
	
	self.send_response("§6Showing queue boss bar for %s" % session_index)
	queue_bar.add_watched_protocol(protocol_sessions[session_index])


def command_hide_queue(self, params):
	protocol_sessions = self.upstream_controller.sessions.protocols
	
	from plugins.bridge.queue_bossbar import QueueBossBarPlugin
	queue_bar = self.bridge.core.get_plugin(QueueBossBarPlugin)
	
	if params.__len__() is 0:
		self.send_response("§6Hiding all queue boss bars")
		for session in protocol_sessions:
			queue_bar.removed_watched_protocol(session)
		return
	
	session_index = params[0]
	if not session_index.isdigit():
		self.send_error("Invalid session ID")
		return
	session_index = int(session_index)
	
	if not protocol_sessions.__len__() > session_index:
		self.send_error("Invalid session ID")
		return
	
	self.send_response("§6Hiding queue boss bar for %s" % session_index)
	queue_bar.removed_watched_protocol(protocol_sessions[session_index])
