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
from RobotController import RobotControllerAttack
from RobotController import RobotControllerDefend

class PlayerI(drobots.Player):
	def __init__(self, current=None):
		self.contAtt=1
		self.contDef=1
		self.contFac=1

	def makeController(self, bot, current=None):
		print("Llamada a makeController")
		proxy_container = current.adapter.getCommunicator().stringToProxy("Container")
		container_prx = services.ContainerPrx.checkedCast(proxy_container)
		proxy_factory = current.adapter.getCommunicator().stringToProxy("Factory"+str(self.contFac))
		factory_prx = drobots.FactoryPrx.checkedCast(proxy_factory)

		robot_prx = factory_prx.make(bot, self.contAtt, self.contDef)

		if (bot.ice_isA("::drobots::Attacker")):
			container_prx.link("RobotAttacker"+str(self.contAtt), robot_prx)
			self.contAtt += 1;
			
		elif (bot.ice_isA("::drobots::Defender")):
			container_prx.link("RobotDefender"+str(self.contDef), robot_prx)
			self.contDef += 1;

		if (self.contFac == 3):
			self.contFac = 1
		else:
			self.contFac += 1

		return robot_prx

	def win(self, current=None):
		print("Has ganado.")
		current.adapter.getCommunicator().shutdown()

	def lose(self, current=None):
		print("Has perdido.")
		current.adapter.getCommunicator().shutdown()

	def gameAbort(self, current=None):
		print("Juego abortado.");
		current.adapter.getCommunicator().shutdown()