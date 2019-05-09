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

from plugins.downstream import DownstreamPlugin


class WhitelistPlugin(DownstreamPlugin):
	path = "plugins/downstream/whitelist/whitelist.csv"
	
	def __init__(self, *args, **kwargs):
		self.whitelist = self.get_whitelist()
		print(self.whitelist)
		super(WhitelistPlugin, self).__init__(*args, **kwargs)
		
	def get_whitelist(self):
		out = []
		with open(self.path, newline="") as _accounts_csv:
			_accounts = csv.DictReader(_accounts_csv)
			for index, row in enumerate(_accounts):
				out.append({
					"username": row["username"],
					"uuid": row["uuid"],
				})
		return out
	
	def on_join(self):
		print(self.protocol.real_uuid)
		for account in self.whitelist:
			if account["uuid"] == self.protocol.real_uuid.to_hex():
				print("found account")
				return
		self.protocol.close("You are not whitelisted.")
