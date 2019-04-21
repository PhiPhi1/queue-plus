#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (accounts.py) is part of Queue Plus.
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
from pathlib import Path
from shutil import copyfile


class Accounts:
	accounts_path = "data/accounts.csv"
	accounts_path_copy = "bin/sources/accounts.csv"
	
	
	def __init__(self):
		self.account_data = []
	
	
	def check_save(self):
		if not Path(self.accounts_path).is_file():
			dir_name, _ = os.path.split(self.accounts_path)
			os.makedirs(dir_name, exist_ok=True)
			copyfile(self.accounts_path_copy, self.accounts_path)
		
		new_accounts = []
		
		with open(self.accounts_path, newline="") as _accounts_csv:
			_accounts = csv.DictReader(_accounts_csv)
			for index, row in enumerate(_accounts):
				if not (row["email"], row["username"], row["password"]) in self.account_data:
					new_accounts.append((row["email"], row["username"], row["password"]))
		
		self.account_data = self.account_data + list(set(new_accounts) - set(self.account_data))
		return new_accounts
