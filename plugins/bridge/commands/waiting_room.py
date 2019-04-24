#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (waiting_room.py) is part of Queue Plus.
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


def command_wait(self, params):
	if params.__len__() is not 1 and params.__len__() is not 0:
		self.send_error("[/wait <account id>]")
		return
	
	if params.__len__() is 0:
		account_index = 0
	else:
		account_index = params[0]
		
		if not account_index.isdigit():
			self.send_error("Invalid account ID")
			return
	
	account_index = int(account_index)
	
	accounts = self.upstream_controller.accounts.account_data
	if not accounts.__len__() > account_index:
		if accounts.__len__() is 0:
			self.send_error("There are no accounts configured")
		else:
			self.send_error("Invalid account ID")
		return
	
	from plugins.bridge.waiting_server import WaitingServerPlugin
	waiting_server = self.bridge.core.get_plugin(WaitingServerPlugin)
	waiting_server.join_server(account_index)
