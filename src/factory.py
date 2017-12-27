#!/bin/bash/python3
# -*- coding: utf-8 -*-

#Francisco Manuel Garcia Sanchez-Belmonte
#Fernando Galan Freire
#Adrian Bustos Marin
import sys
import Ice
Ice.loadSlice('drobots.ice')
import drobots
from robotControllerIAttack import robotControllerIAttack
from robotControllerIDefense import robotControllerIDefense
from drobots import (
    GameInProgress, GamePrx, Player, PlayerPrx, Point, RobotPrx,
    RobotController, RobotControllerPrx,Container)

class FactoryI(drobots.factory):
    def make(self, bot, current=None):
	if bot.ice_isA("::drobots::Attacker"):
		controller = ControllerIAtac(bot)
	elif (bot.ice_isA("::drobots::Defender")):
		controller = ControllerIDef(bot)
	
	proxy = current.adapter.addWithUUID(controller)
	proxy_id=proxy.ice_getIdentity()
	direct_prx=current.adapter.createDirectProxy(proxy_id)
	proxyRobotController=drobots.RobotControllerPrx.uncheckedCast(direct_prx)
        #lo de arriba o 
        #proxyRobotController=drobots.RobotControllerPrx.checkedCast(direct_prx)
        return proxyRobotController

class Server(Ice.Application):
    def run(self, argv):
		broker = self.communicator()
		getproperties = broker.getProperties()
		adapter = broker.createObjectAdapter("Factory_Adapter")
		servant = FactoryI()
                
                
		identidad = broker.stringToIdentity(getproperties.getProperty("Identity"))
		proxy_server = adapter.add(servant, identidad)
                
                
		string_proxy=str(proxy_server)
		print(string_proxy)
                
                
		#sys.stdout.flush()
		adapter.activate()
                
		print("Factoria preparada "+str(proxy_server))
		self.shutdownOnInterrupt()
		broker.waitForShutdown()

      		return 0


server = Server()
sys.exit(server.main(sys.argv))

