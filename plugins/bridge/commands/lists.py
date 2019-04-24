#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (lists.py) is part of Queue Plus.
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


def command_sessions(self, params):
	protocol_sessions = self.upstream_controller.sessions.protocols
	from plugins.upstream.player_info import PlayerInfoPlugin
	from headless.upstream.protocol.the_void import TheVoidProtocol
	
	if protocol_sessions.__len__() > 0:
		self.send_response("§aList of all sessions:")
	
	for i, session in enumerate(protocol_sessions):
		player_info = session.core.get_plugin(PlayerInfoPlugin)
		username = player_info.player_username
		
		if (not username) and isinstance(session, TheVoidProtocol):
			username = "Waiting Room"
		
		self.send_response("§a%s: %s" % (i, username))


def command_accounts(self, params):
	accounts = self.upstream_controller.accounts.account_data
	
	if accounts.__len__() > 0:
		self.send_response("§aList of all accounts:")
	
	for i, (email, username, _) in enumerate(accounts):
		self.send_response("§a%s: %s" % (i, username))
