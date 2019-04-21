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


class Controller:
	def __init__(self, decorated):
		self._decorated = decorated
	
	
	def instance(self):
		try:
			return self._instance
		except AttributeError:
			# noinspection PyAttributeOutsideInit
			self._instance = self._decorated()
			return self._instance
	
	
	def __call__(self):
		raise TypeError('Singletons must be accessed through `instance()`.')
	
	
	def __instancecheck__(self, inst):
		return isinstance(inst, self._decorated)
	
	
	def setup(self):
		return

