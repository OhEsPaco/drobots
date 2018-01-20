#!/usr/bin/python

import Ice
import sys
Ice.loadSlice('drobots.ice')
Ice.loadSlice('services.ice')
import drobots
import Container
from RobotController import RobotControllerAttack
from RobotController import RobotControllerDefend

class FactoryI(drobots.Factory):
	def make(self, robot, contA, contD, current=None):

		if (robot.ice_isA("::drobots::Attacker")):
			servantController = RobotControllerAttack(robot, contA)
		elif (robot.ice_isA("::drobots::Defender")):
			servantController = RobotControllerDefend(robot, contD)

		proxyController=current.adapter.addWithUUID(servantController)
		prx_id = proxyController.ice_getIdentity()
		direct_prx = current.adapter.createDirectProxy(prx_id)

		robotController_prx=drobots.RobotControllerPrx.checkedCast(direct_prx)

		return robotController_prx
		
class ServerFactory(Ice.Application):
	def run(self, argv):
		broker = self.communicator()
		getproperties = broker.getProperties()
		adapter = broker.createObjectAdapter("Factory_Adapter")
		servant = FactoryI()

		identidad = broker.stringToIdentity(getproperties.getProperty("Identity"))
		
		proxy_server = adapter.add(servant, identidad)

		string_proxy=str(proxy_server)

		print(string_proxy)

		adapter.activate()

		self.shutdownOnInterrupt()
		broker.waitForShutdown()

		return 0

sys.exit(ServerFactory().main(sys.argv))