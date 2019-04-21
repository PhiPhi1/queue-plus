#      Copyright (C) 2019 - 2019 Akiva Silver and contributors of Queue Plus
#      GitHub Page: <https://github.com/the-emperium/queue-plus>
#
#      This file (start.py) is part of Queue Plus.
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
from twisted.internet import reactor

from core.bridge.proxy import ProxyBridge
from core.downstream.factory import DownstreamFactory
from controllers.config import ConfigController

# TODO: implement core startup here
from controllers.upstream import UpstreamController


def main():
	# initializes the config controller and returns the data
	config = ConfigController.instance().data
	
	# Initializes the upstream controller
	upstream_controller = UpstreamController.instance()

	# Create factory
	factory = DownstreamFactory()
	factory.bridge_class = ProxyBridge

	# get connection details from config
	host = config["server"]["host"]
	port = config["server"]["port"]
	
	# starts the downstream server
	factory.listen(host, port)
	return

	
if __name__ == "__main__":
	main()
	reactor.run()
