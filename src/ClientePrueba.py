#!/usr/bin/python
# -*- coding:utf-8; mode:python -*-

import sys
import Ice
Ice.loadSlice('drobots.ice')
import drobots
import math
import random
from PlayerPrueba import PlayerPruebaI
from Container import ContainerI

class ClientePrueba(Ice.Application):
	def run(self, argv):
		broker = self.communicator()
		adapter = broker.createObjectAdapter("Player_AdapterP")
		servant2 = ContainerI()
		servant = PlayerPruebaI(servant2)

		identidad=broker.stringToIdentity("Sparring")

		proxy_server = adapter.add(servant, identidad)

		direct_prx = adapter.createDirectProxy(identidad)
		player = drobots.PlayerPrx.uncheckedCast(direct_prx)

		if not player:
			raise RuntimeError('Invalid proxy')

		adapter.activate()

		proxy_client = broker.propertyToProxy("Proxy_game")
		game = drobots.GamePrx.checkedCast(proxy_client) 

		if not game:
			raise RuntimeError('Invalid proxy')

		my_nick = "Sparr" + str(random.randint(1, 100))
		game.login(player, my_nick)

		self.shutdownOnInterrupt()
		broker.waitForShutdown()

		return 0

sys.exit(ClientePrueba().main(sys.argv))
