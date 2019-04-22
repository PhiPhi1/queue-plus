#
#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of queue-plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (__init__.py) is part of queue-plus.
#
#      queue-plus is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      any later version.
#
#      queue-plus is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with queue-plus.  If not, see <https://www.gnu.org/licenses/>.
#
from plugins.bridge import BridgePlugin


class AntiAfkControllerPlugin(BridgePlugin):
	def on_join(self):
		from plugins.upstream.anti_afk import AntiAfkPlugin
		if hasattr(self.bridge.upstream, "core"):
			anti_afk = self.bridge.upstream.core.get_plugin(AntiAfkPlugin)
			if anti_afk:
				anti_afk.stop()
		
	def on_leave(self):
		from plugins.upstream.anti_afk import AntiAfkPlugin
		if hasattr(self.bridge.upstream, "core"):
			anti_afk = self.bridge.upstream.core.get_plugin(AntiAfkPlugin)
			if anti_afk:
				anti_afk.start()

