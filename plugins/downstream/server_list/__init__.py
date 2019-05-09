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
import base64
import json

from plugins.downstream import DownstreamPlugin


class ServerListPlugin(DownstreamPlugin):
	img_path = "plugins/downstream/server_list/server-icon.png"
	
	def packet_status_request(self, buff):
		with open(self.img_path, "rb") as image_file:
			encoded_image = base64.b64encode(image_file.read())

		out = {
			"version": {
				"name": self.protocol.factory.minecraft_versions.get(self.config["version"], "???"),
				"protocol": self.config["version"]
			},
			"players": {
				"max": self.protocol.factory.max_players,
				"online": self.protocol.factory.players.__len__(),
				"sample": []
			},
			"description": {
				"text": "§9Queue §7Plus"
			},
			"favicon": "data:image/png;base64,%s" % str(encoded_image, "ascii")
		}
		
		out_json = json.dumps(out)

		self.send_packet("status_response", self.buff_type.pack_string(out_json))
