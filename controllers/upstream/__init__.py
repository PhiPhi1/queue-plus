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

from quarry.net.auth import OfflineProfile, Profile
from core.upstream.factory import UpstreamFactory
from twisted.internet import defer

from controllers import Controller
from controllers.config import ConfigController
from controllers.upstream.accounts import Accounts
from controllers.upstream.sessions import Sessions


@Controller
class UpstreamController:
	def __init__(self):
		self.config = ConfigController.instance().data
		
		self.accounts = Accounts()
		self.sessions = Sessions()
		
		self.setup()
		
	def setup(self):
		new_accounts = self.accounts.check_save()
		for account in new_accounts:
			self.load_account(account)
				
	def load_account(self, account_info, callback=None):
		host = self.config["client"]["host"]
		port = self.config["client"]["port"]
		
		online = self.config["client"]["online"]
		self.load_custom_connection(account_info, host, port, online, callback)

	@defer.inlineCallbacks
	def load_custom_connection(self, account_info, host="localhost", port=25565, online=True, callback=None):
		email, username, password = account_info
		
		if online:
			profile = yield Profile.from_credentials(email, password)
		else:
			profile = yield OfflineProfile.from_display_name(username)
		
		# TODO: finish connection process
		factory = UpstreamFactory(profile)
		factory.account_manager = self
		factory.protocol_callback = callback

		yield factory.connect(host, port)
	
	@defer.inlineCallbacks
	def load_pseudo_protocol(self, factory_class, bridge, callback=None):
		bridge.logger.debug("starting pseudo protocol")
		profile = yield OfflineProfile.from_display_name("protocol")
		
		factory = factory_class(profile)
		factory.account_manager = self
		factory.protocol_callback = callback
		
		bridge.logger.debug("connecting bridge to pseudo protocol")
		protocol = yield factory.connect(None, None)
		
		bridge.switch_protocol(protocol)
