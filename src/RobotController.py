#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('crobots.ice')
Ice.loadSlice('container.ice')
Ice.loadSlice('coordinacion.ice')
import Services
import drobots
import drobots2
import math
import random
import time

class RobotFactory(drobots.factory):
    def make(self, bot,i, current=None):
        if (bot.ice_isA("::drobots::Attacker")):
            servant= RobotControllerAta(bot, i)
        elif (bot.ice_isA("::drobots::Defender")):
            servant= RobotControllerDef(bot, i)
        proxy=current.adapter.addWithUUID(servant)
        prx_id = proxy.ice_getIdentity()
        direct_prx = current.adapter.createDirectProxy(prx_id)
        robot=drobots.RobotControllerPrx.uncheckedCast(direct_prx)
        return robot

class RobotControllerDef(drobots.RobotController, drobots2.Coordinacion):
    def __init__(self, bot, i):
        self.bot=bot
        self.velocidad=40
        self.estadoAct="M"
        self.turnos=0
        self.angulo=0
        self.id=i
        self.coordenadas=[]
        print("CREADO ROBOT DEFENSOR")

    def turn(self, current=None):
        ProxyCon=current.adapter.getCommunicator().stringToProxy("Robots")
        container=Services.ContainerPrx.checkedCast(ProxyCon)
        async = container.begin_listR()
        print("A E S T H E T I C")
        proxis = container.end_listR(async)
        if(self.estadoAct=="S"):
            print("escaneando")
            self.turnos=self.turnos+1
            encontrados=self.bot.scan(self.angulo, 10)
            if((self.turnos==20)):
                self.estadoAct="M"
            elif(encontrados>0):
                print("ENEMIGO A LA VISTA")
                con=drobots2.CoordinacionPrx.uncheckedCast(proxis["3"])
                con2=drobots2.CoordinacionPrx.uncheckedCast(proxis["4"])
                con.EnemigoDetec(self.angulo)
                con2.EnemigoDetec(self.angulo)
                if((self.turnos==10)):
                    self.angulo= self.angulo+15
                else:
                    self.angulo=self.angulo+18

            elif(encontrados==0):
                con=drobots2.CoordinacionPrx.uncheckedCast(proxis["3"])
                con2=drobots2.CoordinacionPrx.uncheckedCast(proxis["4"])
                con.NoEnemy()
                con2.NoEnemy()
                self.angulo=self.angulo+15


        elif(self.estadoAct=="M"):

            print("cambiando rumbo")
            xDest=random.randint(10,990)
            yDest=random.randint(10,990)

            localizacion = self.bot.location()
            x = localizacion.x
            y = localizacion.y


            distancia=int(math.sqrt((x-xDest)**2+(y-yDest)**2))
            datoAngulo=math.degrees(math.atan2(xDest-y,yDest-x))
            if(distancia>4):
                self.bot.drive(datoAngulo,100)

            self.angulo=0
            self.turnos=0
            self.estadoAct="S"



    def robotDestroyed(self, current=None):
        print("Robot destruido")

    def EnemigoDetec(self, ang,  current=None):
        None
    def NoEnemy(self, current=None):
        None


class RobotControllerAta(drobots.RobotController, drobots2.Coordinacion):
    def __init__(self, bot,i):
        self.bot=bot
        self.velocidad=40
        self.estadoAct="M"
        self.turnos=0
        self.angulo=0
        self.id=i
        self.coordenadas=[]
        print("CREADO ROBOT ATACANTE")

    def turn(self, current=None):
        if(self.estadoAct=="D"):
            self.turnos=self.turnos+1
            print("disparando")

            dist=random.randint(100,620)
            self.bot.cannon(self.angulo, dist)
            dist=random.randint(100,620)
            self.bot.cannon(self.angulo, dist)
            if((self.turnos==20)):
                self.estadoAct="M"

        elif(self.estadoAct=="M"):

            print("cambiando rumbo")
            xDest=random.randint(10,990)
            yDest=random.randint(10,990)

            localizacion = self.bot.location()
            x = localizacion.x
            y = localizacion.y
            distancia=int(math.sqrt((x-xDest)**2+(y-yDest)**2))
            datoAngulo=math.degrees(math.atan2(xDest-y,yDest-x))
            if(distancia>4):
                self.bot.drive(datoAngulo,100)

            self.angulo=0
            self.turnos=0

        print("angulo: " + str(self.angulo))

    def robotDestroyed(self, current=None):
        print("Robot destruido")

    def EnemigoDetec(self, ang,  current=None):
        print("ENEMIGO DETECTADO")
        self.angulo=360-ang
        self.estadoAct="D"
    def NoEnemy(self, current=None):
        print("NO HAY MOROS A LA VISTA")
        self.estado="M"



class Nodo(Ice.Application):
    def run(self, argv):
        time.sleep(3)
        broker = self.communicator()
        adapter= broker.createObjectAdapter("FactoriaAdapter")
        sirviente = RobotFactory()
        proxy= adapter.add(sirviente, broker.stringToIdentity("RobotFactory"))
        proxyCOn=self.communicator().stringToProxy("Container")
        container = Services.ContainerPrx.uncheckedCast(proxyCOn)


        adapter.activate()

        container.link(str(random.randint(1,100)), proxy)

        self.shutdownOnInterrupt()
        broker.waitForShutdown()

Nodo().main(sys.argv)