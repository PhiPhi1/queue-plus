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
#

import json
import os

from pathlib import Path
from shutil import copyfile

from controllers import Controller


@Controller
class ConfigController:
	data = {}
	path = 'data/config.json'
	copy_path = 'bin/sources/config.json'
	
	def __init__(self):
		if not Path(self.path).is_file():
			dir_name, _ = os.path.split(self.path)
			os.makedirs(dir_name, exist_ok=True)
			copyfile(self.copy_path, self.path)
		
		with open(self.path) as config_file:
			self.data = json.load(config_file)
