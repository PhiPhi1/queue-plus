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
from plugins.upstream import UpstreamPlugin


class QueuePlugin(UpstreamPlugin):
	def __init__(self, *args, **kwargs):
		super(QueuePlugin, self).__init__(*args, **kwargs)
		
		self.in_queue = False
		self.queue_position = -1
		self.queue_starting_position = -1
		
		self.queue_listeners = []
		
		self.queue_messages = ["Position in queue: "]
	
	def packet_mirror_chat_message(self, buff):
		chat_message = buff.unpack_chat().to_string(True)
		_ = buff.unpack("b")
		
		print(chat_message)
		
		if chat_message.startswith("Connecting"):
			self.remove_from_queue()
		
		is_queue_message = False
		for message in self.queue_messages:
			if chat_message.startswith(message):
				is_queue_message = True
		
		if not is_queue_message:
			return
		
		bloat_removed = chat_message
		
		for bloat in self.queue_messages:
			bloat_removed = bloat_removed.replace(bloat, "")
			
		if not bloat_removed.isdigit():
			return
		
		if not self.in_queue:
			print("adding to queue")
			self.in_queue = True
			self.queue_starting_position = int(bloat_removed)
			
		self.queue_position = int(bloat_removed)
		self.queue_update()
		return
		
	def remove_from_queue(self):
		print("removing queue")
		
		self.in_queue = False
		self.queue_position = 0
		self.queue_starting_position = 0
		self.queue_update()
		return
		
	def add_queue_listener(self, callback):
		self.queue_listeners.append(callback)
		return
	
	def remove_queue_listener(self, callback):
		while callback in self.queue_listeners:
			self.queue_listeners.remove(callback)
		return
	
	def queue_update(self):
		for callback in self.queue_listeners:
			try:
				callback()
			except Exception as e:
				print("error while running queue callback:", e)
		return
