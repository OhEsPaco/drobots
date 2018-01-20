#!/usr/bin/python
# -*- coding:utf-8; mode:python -*-

import sys
import Ice
Ice.loadSlice('drobots.ice')
Ice.loadSlice('services.ice')
import services
import drobots
import math
import random
from RobotControllerPrueba import RobotControllerAttackPrueba
from RobotControllerPrueba import RobotControllerDefendPrueba

class PlayerPruebaI(drobots.Player):
	def __init__(self, container, current=None):
		self.container=container
		self.contador=1

	def makeController(self, bot, current=None):
		print("Llamada a makeController de prueba")
		if (bot.ice_isA("::drobots::Attacker")):
			servantController = RobotControllerAttackPrueba(bot)
		elif (bot.ice_isA("::drobots::Defender")):
			servantController = RobotControllerDefendPrueba(bot)

		proxyController=current.adapter.addWithUUID(servantController)
		prx_id = proxyController.ice_getIdentity()
		direct_prx = current.adapter.createDirectProxy(prx_id)
		robotController_prx=drobots.RobotControllerPrx.uncheckedCast(direct_prx)

		self.container.link("Sparring"+str(self.contador), robotController_prx)
		self.contador+=1

		return robotController_prx

	def win(self, current=None):
		print("Has ganado")
		current.adapter.getCommunicator().shutdown()

	def lose(self, current=None):
		print("Has perdido")
		current.adapter.getCommunicator().shutdown()

	def gameAbort(self, current=None):
		print("Juego abortado.");
		current.adapter.getCommunicator().shutdown()