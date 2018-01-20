#!/bin/bash/python3
#Francisco Manuel Garcia Sanchez-Belmonte
#Fernando Galan Freire
#Adrian Bustos Marin
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('crobots.ice')
import Container
import drobots
import math
import random


class Player(drobots.Player):
    def __init__(self, adapter, sirv, sorv):
        self.adaptador = adapter
        self.con=sirv
        self.con1=sorv
        self.contadorCreados = 0
        self.contadorRobots=0
        self.detector_controller = None
        self.mine_index = 0
        self.mines = [
            drobots.Point(x=randint(0, 199), y=randint(0, 199)),
            drobots.Point(x=randint(200, 399), y=randint(0, 199)),
            drobots.Point(x=randint(0, 199), y=randint(200, 399)),
            drobots.Point(x=randint(200, 399), y=randint(200, 399)),
        ]
    def win(self, current=None):
        print("Has ganado")
        current.adapter.getCommunicator().shutdown()

    def lose(self, current=None):
        print("Has perdido")
        current.adapter.getCommunicator().shutdown()


    def makeController(self, bot, current=None):
        print("LLAMADA MAKECONTROLLER")
        proxies, keys=self.con.list()
        factoria = drobots.factoryPrx.uncheckedCast(proxies[keys[self.contadorCreados]])
        if self.contadorCreados<2:
            self.contadorCreados= self.contadorCreados + 1
        self.contadorRobots=self.contadorRobots+1
        robot = factoria.make(bot, self.contadorRobots)
        self.con1.link(str(self.contadorRobots), robot)
        return robot

    def gameAbort(self, current=None):
        print("Juego Abortado, tiempo de espera a jugadores superado");
        current.adapter.getCommunicator().shutdown()
        
    def getMinePosition(self, current=None):
        """
        Pending implementation:
         Point getMinePosition();
        """
        pos = self.mines[self.mine_index]
        self.mine_index += 1
        return pos

class Cliente(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        adapter = broker.createObjectAdapter("PlayerAdapter")
        adapter2 = broker.createObjectAdapter("ContainerAdapter")
        sirviente = Container.Container()
        conRobotos = Container.Container()
        servant = Player(adapter, sirviente, conRobotos)
        adapter2.add(sirviente, broker.stringToIdentity("Container"))
        adapter2.add(conRobotos, broker.stringToIdentity("Robots"))



        proxyServer = adapter.add(servant, broker.stringToIdentity("Barbassss"))
        prx_id = proxyServer.ice_getIdentity()
        direct_prx = adapter.createDirectProxy(prx_id)
        player = drobots.PlayerPrx.uncheckedCast(direct_prx)

        adapter.activate()
        adapter2.activate()
        proxyClient=self.communicator().propertyToProxy("Game")
        game=drobots.GamePrx.checkedCast(proxyClient)

        name = random.randint(1000, 9999)
        game.login(player, str(name))
    
        self.shutdownOnInterrupt()
        broker.waitForShutdown()


Cliente().main(sys.argv)

