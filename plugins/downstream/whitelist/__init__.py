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
import json
from pathlib import Path

from plugins.downstream import DownstreamPlugin


class WhitelistPlugin(DownstreamPlugin):
	fields = ["username", "uuid", "ip"]
	path = "plugins/downstream/whitelist/whitelist.csv"
	
	plugin_config_path = "plugins/downstream/whitelist/config.json"
	
	def __init__(self, *args, **kwargs):
		if not Path(self.path).is_file():
			with open(self.path, 'w', newline='') as out:
				writer = csv.DictWriter(out, fieldnames=self.fields)
				writer.writeheader()
		
		self.plugin_config = None
		self.get_config()
		
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
	
	def get_config(self):
		with open(self.plugin_config_path) as config_file:
			self.plugin_config = json.load(config_file)
	
	def on_join(self):
		self.update_autos()
		if not self.plugin_config["enabled"]:
			return
		
		for account in self.whitelist:
			username_match = account["username"] == self.protocol.display_name or account["username"] == "*"
			uuid_match = account["uuid"] == self.protocol.real_uuid.to_hex() or account["uuid"] == "*"
			ip_match = account["ip"] == self.protocol.remote_addr.host or account["uuid"] == "*"
			
			if username_match and uuid_match and ip_match:
				return
			
		self.protocol.close("You are not whitelisted.")
	
	def add_to_whitelist(self, username, uuid, ip="*"):
		fields = "%s,%s,%s\n" % (username, uuid, ip)
		with open(self.path, 'a') as fd:
			fd.write(fields)
		
		self.whitelist = self.get_whitelist()
		return True
	
	def remove_from_whitelist(self, field, field_name):
		if field_name not in self.fields:
			return False
		
		with open(self.path, 'r') as inp:
			in_whitelist = list(csv.DictReader(inp))
			
		with open(self.path, 'w', newline='') as out:
			writer = csv.DictWriter(out, fieldnames=self.fields)
			writer.writeheader()
			
			for row in in_whitelist:
				if row[field_name] != field:
					writer.writerow(row)
		
		self.whitelist = self.get_whitelist()
		return True
	
	def set_whitelist_status(self, state):
		self.plugin_config['enabled'] = state
		self.write_to_plugin_config()
	
	def write_to_plugin_config(self):
		with open(self.plugin_config_path, 'w') as outfile:
			json.dump(self.plugin_config, outfile, sort_keys=True, indent=4)

	def update_autos(self):
		updated = False
		
		with open(self.path, 'r') as inp:
			in_whitelist = list(csv.DictReader(inp))
			
		for account in in_whitelist:
			username_match = account["username"] == self.protocol.display_name
			if not username_match:
				continue
			
			if account["uuid"] == "auto":
				account["uuid"] = self.protocol.real_uuid.to_hex()
				updated = True
				
			if account["ip"] == "auto":
				account["ip"] = self.protocol.remote_addr.host
				updated = True
		
		if updated:
			with open(self.path, 'w', newline='') as out:
				writer = csv.DictWriter(out, fieldnames=self.fields)
				writer.writeheader()
				
				for row in in_whitelist:
					writer.writerow(row)
