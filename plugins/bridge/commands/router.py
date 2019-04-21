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
# TODO: clean up code
def route_command(self, command_string):
	if command_string.startswith("connect"):
		params = self.get_params("connect", command_string)
		
		if params.__len__() is not 1:
			self.send_error("Expected 1 variable [/connect <session id>]")
			return "finish"
		
		self.command_connect(params)
		return "finish"
	elif command_string.startswith("showqueue"):
		params = self.get_params("showqueue", command_string)
		
		if params.__len__() > 1:
			self.send_error("Expected 0 or 1 variables [/showqueue <session id>]")
			return "finish"
		
		self.command_show_queue(params)
		return "finish"
	elif command_string.startswith("hidequeue"):
		params = self.get_params("hidequeue", command_string)
		
		if params.__len__() > 1:
			self.send_error("Expected 0 or 1 variables [/hidequeue <session id>]")
			return "finish"
		
		self.command_hide_queue(params)
		return "finish"
	elif command_string.startswith("sessions"):
		self.command_sessions()
		return "finish"
	elif command_string.startswith("accounts"):
		self.command_accounts()
		return "finish"
	return "continue"
