#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (connection.py) is part of Queue Plus.
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


def command_connect(self, params):
	if params.__len__() is not 1:
		self.send_error("Expected 1 variable [/connect <session id>]")
		return
	
	session_index = params[0]
	
	if not session_index.isdigit():
		self.send_error("Invalid session ID")
		return
	
	sessions = self.upstream_controller.sessions.protocols
	session_index = int(session_index)
	
	if not sessions.__len__() > session_index:
		self.send_error("Invalid session ID")
		return
	
	self.send_response("§6Switching sessions")
	self.bridge.switch_protocol(sessions[session_index])
	
	self.send_response("§6Loading cache")
	from plugins.bridge.hot_swap import HotSwapPlugin
	hot_swap = self.bridge.core.get_plugin(HotSwapPlugin)
	
	if hot_swap:
		# TODO make this a new process
		hot_swap.load_cache()
	else:
		self.send_error("Failed to load cache. This is likely an error, please report this and save the logs.")
	return
	
	
def command_disconnect(self, params):
	if not params.__len__() > 0:
		if not self.check_if_void():
			self.bridge.upstream.close()
			self.send_response("§cClosed current session")
		else:
			self.send_error("Cannot disconnect The Void")
		return
	
	if params.__len__() > 1:
		self.send_error("Incorrect syntax: [/disconnect <session id>]")
		return

	if not params[0].isdigit():
		self.send_error("Invalid session ID")
		return

	session_index = int(params[0])
	sessions = self.upstream_controller.sessions.protocols

	if not (sessions.__len__() > session_index):
		self.send_error("Invalid session ID")
		return

	self.send_response("§cClosed session %s" % session_index)
	sessions[session_index].close()


def command_reconnect(self, params):
	if not params.__len__() == 1:
		self.send_error("Incorrect syntax: [/reconnect <account id>]")
		return
	
	if not params[0].isdigit():
		self.send_error("Invalid account ID")
		return
	
	account_index = int(params[0])
	accounts = self.upstream_controller.accounts.account_data
	
	if not accounts.__len__() > account_index:
		self.send_error("Invalid account ID")
		return
	
	self.upstream_controller.load_account(accounts[account_index])


def check_if_void(self):
	from headless.upstream.protocol.the_void import TheVoidProtocol
	return isinstance(self.bridge.upstream, TheVoidProtocol)
