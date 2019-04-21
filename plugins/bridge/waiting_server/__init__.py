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
import json

from plugins.bridge import BridgePlugin


class WaitingServerPlugin(BridgePlugin):
	def __init__(self, *args, **kwargs):
		super(WaitingServerPlugin, self).__init__(*args, **kwargs)
		
		self.cooldown = None
		self.waiting_session = None
		self.session_account_id = None
		
		path = "plugins/bridge/waiting_server/config.json"
		with open(path) as config_file:
			data = json.load(config_file)
			self.server_host = data["host"]
			self.server_port = data["port"]
			self.server_online = data["online"]
		
	def on_join(self):
		if self.cooldown:
			return
		self.send_message("§9You can join the waiting server with /wait")
		return
	
	def on_leave(self):
		if self.waiting_session:
			self.leave_server()
		return
	
	def join_server(self, account_id):
		if self.waiting_session and self.session_account_id == account_id:
			self.send_message("§cAlready connected to Waiting Server")
			return

		self.send_message("§aConnecting to Waiting Server")
		
		accounts = self.upstream_controller.account_loading.account_data
		self.upstream_controller.load_custom_connection(accounts[account_id], self.server_host, self.server_port, self.server_online, self.join_when_ready)
		self.session_account_id = account_id
		return
	
	def leave_server(self):
		self.waiting_session.close()
		self.waiting_session = None
		self.session_account_id = None
		return
	
	def reset_cooldown(self):
		if self.cooldown:
			self.ticker.remove(self.cooldown)
			
		cooldown_len = 150
		self.cooldown = self.ticker.add_delay(cooldown_len, self.lift_cooldown)
		return
	
	def lift_cooldown(self):
		self.cooldown = None
		return
	

	def send_message(self, message):
		self.bridge.packet_received(self.buff_type(self.buff_type.pack_chat(message) + self.buff_type.pack("B", 1)), "downstream", "chat_message")
		return
	
	def join_when_ready(self, protocol):
		self.bridge.switch_protocol(protocol)
		self.waiting_session = protocol
		
		# self.ticker.add_delay(40, delay_callback)
		return
