#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (router.py) is part of Queue Plus.
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


def route_command(self, command_string):
	command = command_string.split(" ")[0]
	method_pointer = "command_%s" % command
	handler = getattr(self, method_pointer, None)
	if handler:
		try:
			handler(self.get_params(command, command_string))
		except Exception as e:
			print("command error", method_pointer, e)
		return "finish"
	else:
		return "continue"


def command_phelp(self, params):
	commands = [
		{
			"command": "phelp",
			"description": "shows all commands"
		},
		{
			"command": "connect <session id>",
			"description": "connect to a session"
		},
		{
			"command": "sessions",
			"description": "lists all sessions"
		},
		{
			"command": "accounts",
			"description": "lists all accounts"
		},
		{
			"command": "showqueue [<session id>]",
			"description": "shows a queue boss bar"
		},
		{
			"command": "hidequeue [<session id>]",
			"description": "hides a queue boss bar"
		},
		{
			"command": "wait [<account id>]",
			"description": "connects to a separate \"waiting\" server"
		},
		{
			"command": "disconnect [<session id>]",
			"description": "manually disconnect a session"
		},
		{
			"command": "reconnect [<account id>]",
			"description": "manually reconnect an account"
		}
	]
	
	self.send_response("§6======================================")
	
	for command in commands:
		self.send_response("§a/%s: §r%s" % (command["command"], command["description"]))
	
	self.send_response("§6======================================")
