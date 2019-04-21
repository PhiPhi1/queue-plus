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
#      This file (__init__.py) is part of Queue Plus.
#
#      Queue Plus is a proxy service that is designed to be highly modular.
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


class CoreProtocol:
	def __init__(self, protocol):
		self.plugins = []
		
		self.protocol = protocol
		
	def load_plugins(self, plugins):
		self.protocol.logger.debug("Loading Plugins")
		for index, plugin in enumerate(plugins):
			init_pl = plugin(self.protocol, self.protocol.ticker)
			init_pl.setup()
			self.plugins.append(init_pl)

		return
	
	def on_ready_plugins(self):
		for index, plugin in enumerate(self.plugins):
			plugin.on_ready()
			
		return

	def on_join_plugins(self):
		for index, plugin in enumerate(self.plugins):
			plugin.on_join()
		return

	def on_leave_plugins(self):
		for index, plugin in enumerate(self.plugins):
			plugin.on_leave()
		return
	
	def unload_plugins(self):
		for index, plugin in enumerate(self.plugins):
			plugin.on_unload()
			del self.plugins[index]
		return

	def get_plugin(self, plugin_class):
		for index, plugin in enumerate(self.plugins):
			if isinstance(plugin, plugin_class):
				return plugin
		return None
	
	
	def route_packet_to_plugins(self, buff, *args, **kwargs):
		routed = False
		
		buff.save()
		for index, plugin in enumerate(self.plugins):
			route = plugin.packet_received(buff, *args, **kwargs)
			buff.restore()
			if route == "continue" and not routed:
				routed = False
			elif route == "finish" and not routed:
				routed = True
			elif route == "break":
				routed = True
				break
		
		return routed
