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


class CommmandsPlugin(BridgePlugin):
	from plugins.bridge.commands.router import route_command, command_phelp
	from plugins.bridge.commands.connection import command_connect, command_disconnect, command_reconnect, check_if_void
	from plugins.bridge.commands.lists import command_accounts, command_sessions
	from plugins.bridge.commands.queue import command_hidequeue, command_showqueue
	from plugins.bridge.commands.waiting_room import command_wait
	from plugins.bridge.commands.whitelist import command_pwhitelist, add_to_whitelist, remove_from_whitelist, set_whitelist, list_whitelist
	
	def packet_upstream_chat_message(self, buff):
		message = buff.unpack_string()
		
		if message.startswith("/"):
			return self.route_command(message[1:].lower())
		else:
			return "continue"
	
	# noinspection PyMethodMayBeStatic
	def get_params(self, alias, message):
		message = message.replace(alias, "")
		message = message.replace(" ", "", 1)
		
		split_message = []
		split_message.extend(message.split(" "))
		while '' in split_message:
			split_message.remove('')
		return split_message
	
	
	def send_error(self, message):
		out_message = "§c%s" % message
		self.send_response(out_message)
		return
	
	
	def send_response(self, message):
		self.bridge.packet_received(self.buff_type(self.buff_type.pack_chat(message) + self.buff_type.pack("B", 1)), "downstream", "chat_message")
		return
