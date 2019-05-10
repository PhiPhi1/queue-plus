#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (whitelist.py) is part of Queue Plus.
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


def command_pwhitelist(self, params):
	if not params.__len__() > 0:
		self.send_error("/pwhitelist <add | remove | disable | enable | list>")
		return
	
	if params[0] == "add":
		if not params.__len__() >= 4:
			self.send_error("/pwhitelist add <username> <uuid> <ip>")
			return
		
		self.add_to_whitelist(params[1], params[2], params[3])
		return
	elif params[0] == "remove":
		if not params.__len__() >= 3:
			self.send_error("/pwhitelist remove <field name> <field value>")
			return
		
		self.remove_from_whitelist(params[2], params[1])
		return
	elif params[0] == "enable":
		if params.__len__() > 1:
			self.send_error("/pwhitelist enable")
			return
		
		self.set_whitelist(True)
		self.send_response("§aWhitelist enabled.")
		return
	elif params[0] == "disable":
		if params.__len__() > 1:
			self.send_error("/pwhitelist disable")
			return
		
		self.set_whitelist(False)
		self.send_response("§aWhitelist disabled.")
		return
	elif params[0] == "list":
		if params.__len__() > 1:
			self.send_error("/pwhitelist list")
			return
		
		self.list_whitelist()
		return
	
	self.send_error("/pwhitelist <add | remove | disable | enable | list>")
	return
	
	
def add_to_whitelist(self, username, uuid, ip):
	from plugins.downstream.whitelist import WhitelistPlugin
	whitelist = self.bridge.downstream.core.get_plugin(WhitelistPlugin)
	
	if whitelist.add_to_whitelist(username, uuid, ip):
		self.send_response("§aAdded %s username to the whitelist." % username)
	else:
		self.send_error("[username: %s, uuid: %s, ip: %s] is already whitelisted." % (username, uuid, ip))
	return


def remove_from_whitelist(self, field, field_name):
	from plugins.downstream.whitelist import WhitelistPlugin
	whitelist = self.bridge.downstream.core.get_plugin(WhitelistPlugin)
	
	if whitelist.remove_from_whitelist(field, field_name):
		self.send_response("§aRemoved all %ss that are %s from the whitelist." % (field_name, field))
	else:
		fields = whitelist.fields
		self.send_error("\"%s\" is not a valid field." % field_name)
		
		if fields.__len__() > 0:
			self.send_error("You can use: username, uuid, ip")
	return


def set_whitelist(self, state):
	from plugins.downstream.whitelist import WhitelistPlugin
	whitelist = self.bridge.downstream.core.get_plugin(WhitelistPlugin)
	
	whitelist.set_whitelist_status(state)


def list_whitelist(self):
	from plugins.downstream.whitelist import WhitelistPlugin
	whitelist_plugin = self.bridge.downstream.core.get_plugin(WhitelistPlugin)
	whitelist = whitelist_plugin.get_whitelist()
	
	if not whitelist.__len__() > 0:
		self.send_error("No accounts are currently whitelisted.")
		return
	
	self.send_response("§aWhitelisted Accounts:")
	for account in whitelist:
		self.send_response("§a[%s]: %s" % (account["uuid"].upper(), account["username"]))
