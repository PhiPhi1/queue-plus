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
import csv
import os

from plugins.downstream import DownstreamPlugin


class WhitelistPlugin(DownstreamPlugin):
	path = "plugins/downstream/whitelist/whitelist.csv"
	
	def __init__(self, *args, **kwargs):
		self.whitelist = self.get_whitelist()
		super(WhitelistPlugin, self).__init__(*args, **kwargs)
		
	def get_whitelist(self):
		out = []
		with open(self.path, newline="") as _accounts_csv:
			_accounts = csv.DictReader(_accounts_csv)
			for index, row in enumerate(_accounts):
				out.append({
					"username": row["username"],
					"uuid": row["uuid"],
					"ip": row["ip"],
				})
		return out
	
	def on_join(self):
		for account in self.whitelist:
			if self.config["server"]["online"]:
				if account["uuid"] == self.protocol.real_uuid.to_hex():
					return
			else:
				if account["ip"] == self.protocol.remote_addr.host:
					return
		self.protocol.close("You are not whitelisted.")
	
	def add_to_whitelist(self, username, uuid, ip=None):
		if not ip:
			ip = "none"
		
		fields = "%s,%s,%s\n" % (username, uuid, ip)
		with open(self.path, 'a') as fd:
			fd.write(fields)
		
		self.whitelist = self.get_whitelist()
		return True
	
	def remove_from_whitelist(self, field, field_name):
		fields = ["username", "uuid", "ip"]
		if field_name not in fields:
			return False
		
		with open(self.path, 'r') as inp:
			in_whitelist = list(csv.DictReader(inp))
			
		with open(self.path, 'w', newline='') as out:
			writer = csv.DictWriter(out, fieldnames=fields)
			writer.writeheader()
			
			for row in in_whitelist:
				if row[field_name] != field:
					writer.writerow(row)
		
		self.whitelist = self.get_whitelist()
		return True
