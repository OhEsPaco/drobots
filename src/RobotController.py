#!/usr/bin/python
#-*- coding:utf-8; mode:python -*-

import sys
import Ice
Ice.loadSlice('drobots.ice')
Ice.loadSlice('services.ice')
Ice.loadSlice('comunicacion.ice')
import services
import drobots
import comunicacion
import math
import random

class RobotControllerDefend(drobots.RobotControllerDefend, comunicacion.Coordinacion):
	def __init__(self, bot, contD, current=None):
		self.bot=bot
		self.energia=100
		self.enMovimiento=False
		self.angulo=random.randint(0,359)
		self.anchuraScan=20
		self.contador=0
		self.posAliado=drobots.Point(-1,-1)
		self.tipo="Defender"
		self.contD=contD
		self.isDestroyed=False
		self.robotsDefend=[]
		self.robotsAttack=[]

		print("¡Robot DEFENSA listo para el combate!")

	def turn (self, current=None):
		print("\nTurno del robot:  %s%i" % (self.tipo, self.contD))
		proxy_container=current.adapter.getCommunicator().stringToProxy("Container")
		container_prx = services.ContainerPrx.uncheckedCast(proxy_container)
		proxies_robots = container_prx.list()
		listaKeys=list(proxies_robots.keys())

		for i in range(len(listaKeys)):
			robot = drobots.RobotControllerPrx.uncheckedCast(proxies_robots[listaKeys[i]])
			if(robot.getTipo()=="Defender"):
				self.robotsDefend.append(proxies_robots[listaKeys[i]])
			if(robot.getTipo()=="Attacker"):
				self.robotsAttack.append(proxies_robots[listaKeys[i]])

		self.energia=100

		posicion=self.bot.location()
		self.energia-=1;

		print("Posicion actual:")
		print(posicion)

		self.setPosicionAliado(posicion.x, posicion.y)

		self.drive(posicion)
		self.scan(posicion)

		if (self.contador==7):
			self.contador=0
		else:
			self.contador+=1

		self.vaciarListas()


	def drive(self, posicion, current=None):
		if(self.enMovimiento==False):
			print("Cambiando rumbo")
			if(posicion.x<=500 and posicion.y<=500):
				grados=random.randint(0, 90)
				self.bot.drive(grados, 100)
			elif(posicion.x<500 and posicion.y>500):
				grados=random.randint(270, 359)
				self.bot.drive(grados, 100)
			elif(posicion.x>500 and posicion.y<500):
				grados=random.randint(90, 180)
				self.bot.drive(grados, 100)
			elif(posicion.x>=500 and posicion.y>=500):
				grados=random.randint(180, 270)
				self.bot.drive(grados, 100)

			self.enMovimiento=True
			self.energia-=60

		else:
			if(posicion.x<20 or posicion.y<20 or posicion.x>980 or posicion.y>980):
				self.bot.drive(0, 0)
				self.enMovimiento=False
				self.energia-=1

			self.comprobarColision(posicion)

	def comprobarColision (self, posicion, current=None):
			for i in self.robotsDefend:
				robotD=drobots.RobotControllerDefendPrx.uncheckedCast(i)

				coorD=robotD.getPosicionAliado()
				distanciaAliadoD=self.distanciaAliados(coorD, posicion)

				if(distanciaAliadoD<30 and distanciaAliadoD!=0):
					self.bot.drive(0, 0)
					self.enMovimiento=False
					self.energia-=1

			for i in self.robotsAttack:
				robotA=drobots.RobotControllerAttackPrx.uncheckedCast(i)

				coorA=robotA.getPosicionAliado()
				distanciaAliadoA=self.distanciaAliados(coorD, posicion)

				if(distanciaAliadoA<30 and distanciaAliadoA!=0):
					self.bot.drive(0, 0)
					self.enMovimiento=False
					self.energia-=1


	def scan(self, posicion, current=None):
		print("ESCANEO")
		while (self.energia>10):
			robotDetectados=self.bot.scan(self.angulo, self.anchuraScan)
			print("Escaneando con angulo: %i"%self.angulo)
			print("Escaneando con anchura: %i"%self.anchuraScan)
			print("Robot detectados: %i" %robotDetectados)
			self.energia-=10
			if(robotDetectados==0):
				self.angulo+=25
				self.anchuraScan=20
				self.contador=0
				if (self.angulo>=359):
					self.angulo=random.randint(0,10)

			else:
				if(self.contador<7):
					for i in self.robotsAttack:
						robotA=comunicacion.CoordinacionPrx.uncheckedCast(i)
						robotA.RobotDetectado(self.angulo, posicion.x, posicion.y, self.anchuraScan)
					if(self.anchuraScan>5):
						self.anchuraScan-=5
				else:
					self.angulo+=25
					self.anchuraScan=20
	

	def setPosicionAliado(self, x, y, current=None):
		self.posAliado.x=x
		self.posAliado.y=y

	def getPosicionAliado(self, current=None):
		return self.posAliado

	def getTipo(self, current=None):
		return self.tipo

	def distanciaAliados(self, aliado, posicion, current=None):
		return int(math.hypot(math.fabs(aliado.x - posicion.x), math.fabs(aliado.y - posicion.y)))

	def vaciarListas(self, current=None):
		listaVacia=[]
		self.robotsDefend=listaVacia
		self.robotsAttack=listaVacia

	def robotDestroyed(self, current=None):
		if(self.isDestroyed==False):
			proxy_container=current.adapter.getCommunicator().stringToProxy("Container")
			container_prx = services.ContainerPrx.uncheckedCast(proxy_container)
			proxies_robots = container_prx.list()
			container_prx.unlink("RobotDefender"+str(self.contD))
			self.isDestroyed=True
			print("El robot ha sido destruido")


class RobotControllerAttack(drobots.RobotControllerAttack, comunicacion.Coordinacion):
	def __init__(self, bot, contA, current=None):
		self.bot=bot
		self.energia=100
		self.enMovimiento=False
		self.siDetectado=False
		self.aliadoCerca=False
		self.distanciaCorrecta=True
		self.anguloDisparo=0
		self.anguloScan=0
		self.distancia=0
		self.aumentarDistancia=100
		self.aumentarDistancia2=0
		self.anchuraScan=20
		self.posAttack=drobots.Point(random.randint(0,999),random.randint(0,999))
		self.posAliado=drobots.Point(-1,-1)
		self.tipo="Attacker"
		self.contA=contA
		self.isDestroyed=False
		self.robotsDefend=[]
		self.robotsAttack=[]

		print("¡Robot ATAQUE listo para el combate!")

	def turn (self, current=None):
		print("\nTurno del robot:  %s%i" % (self.tipo, self.contA))
		proxy_container=current.adapter.getCommunicator().stringToProxy("Container")
		container_prx = services.ContainerPrx.uncheckedCast(proxy_container)
		proxies_robots = container_prx.list()
		listaKeys=list(proxies_robots.keys())

		for i in range(len(listaKeys)):
			robot = drobots.RobotControllerPrx.uncheckedCast(proxies_robots[listaKeys[i]])
			if(robot.getTipo()=="Defender"):
				self.robotsDefend.append(proxies_robots[listaKeys[i]])
			if(robot.getTipo()=="Attacker"):
				self.robotsAttack.append(proxies_robots[listaKeys[i]])

		self.energia=100
		self.aliadoCerca=False
		self.distanciaCorrecta=True

		posicion=self.bot.location()
		self.energia-=1;

		print("Posicion actual:")
		print(posicion)

		self.setPosicionAliado(posicion.x, posicion.y)

		self.drive(posicion)

		if(self.energia>50):
			self.attack(posicion)
		else:
			print("Aun no puedo atacar, no tengo suficiente energia.")

		self.siDetectado=False
		self.anchuraScan=20

		self.vaciarListas()

	def drive(self, posicion, current=None):
		if(self.enMovimiento==False):
			print("Cambiando rumbo")
			if(posicion.x<=500 and posicion.y<=500):
				grados=random.randint(0, 90)
				self.bot.drive(grados, 100)
			elif(posicion.x<500 and posicion.y>500):
				grados=random.randint(270, 359)
				self.bot.drive(grados, 100)
			elif(posicion.x>500 and posicion.y<500):
				grados=random.randint(90, 180)
				self.bot.drive(grados, 100)
			elif(posicion.x>=500 and posicion.y>=500):
				grados=random.randint(180, 270)
				self.bot.drive(grados, 100)

			self.enMovimiento=True
			self.energia-=60

		else:
			if(posicion.x<20 or posicion.y<20 or posicion.x>980 or posicion.y>980):
				self.bot.drive(0, 0)
				self.enMovimiento=False
				self.energia-=1

			self.comprobarColision(posicion)


	def comprobarColision (self, posicion, current=None):
		for i in self.robotsDefend:
			robotD=drobots.RobotControllerDefendPrx.uncheckedCast(i)

			coorD=robotD.getPosicionAliado()
			distanciaAliadoD=self.distanciaAliados(coorD, posicion)

			if(distanciaAliadoD<30 and distanciaAliadoD!=0):
				self.bot.drive(0, 0)
				self.enMovimiento=False
				self.energia-=1

		for i in self.robotsAttack:
			robotA=drobots.RobotControllerAttackPrx.uncheckedCast(i)

			coorA=robotA.getPosicionAliado()
			distanciaAliadoA=self.distanciaAliados(coorD, posicion)

			if(distanciaAliadoA<30 and distanciaAliadoA!=0):
				self.bot.drive(0, 0)
				self.enMovimiento=False
				self.energia-=1


	def attack(self, posicion, current=None):
		print("AL ATAQUEEEEE!")
		self.calcularDisparo(posicion)
		self.aliadoCerca=self.evitarFuegoAmigo(posicion)
		self.comprobarDistanciasDeDisparo();

		if (self.energia>50 and self.aliadoCerca==False and self.distanciaCorrecta==True):
			print("Disparando misil hacia la posicion:")
			print(self.posAttack)
			print("Distancia de disparo: %i"%self.distancia)
			self.bot.cannon(self.anguloDisparo, self.distancia)
			self.energia-=50

		elif(self.energia>50):
			self.disparoAleatorio(posicion)
			while(self.evitarFuegoAmigo(posicion)==True):
				self.disparoAleatorio(posicion)
			print("Disparando misil hacia la posicion:")
			print(self.posAttack)
			print("Distancia de disparo: %i"%self.distancia)
			self.bot.cannon(self.anguloDisparo, self.distancia)
			self.energia-=50

	def evitarFuegoAmigo(self, posicion, current=None):
		aliadoCerca=False
		for i in self.robotsDefend:
			robotD=drobots.RobotControllerDefendPrx.uncheckedCast(i)

			coorD=robotD.getPosicionAliado()
			distanciaAliadoD=self.distanciaAliados(coorD, self.posAttack)

			if(distanciaAliadoD<=80):
				print("No puedo disparar ahí, hay un aliado cerca")
				aliadoCerca=True

		for i in self.robotsAttack:
			robotA=drobots.RobotControllerAttackPrx.uncheckedCast(i)

			coorA=robotA.getPosicionAliado()
			distanciaAliadoA=self.distanciaAliados(coorA, self.posAttack)

			if(distanciaAliadoA<=80):
				print("No puedo disparar ahí, hay un aliado cerca")
				aliadoCerca=True

		return aliadoCerca

	def comprobarDistanciasDeDisparo(self, current=None):
		if(self.distancia>700 or self.distancia<80):
			print("No puedo disparar a esa distancia.")
			self.distanciaCorrecta=False

		if(self.posAttack.x>=1000 or self.posAttack.y>=1000 or self.posAttack.x<0 or self.posAttack.y<0):
			print("Zona de disparo fuera de los limites. Recalculando.")
			self.distanciaCorrecta=False


	def RobotDetectado(self, angulo, posX, posY, anchuraScan, current=None):
		self.posAttack.x=posX
		self.posAttack.y=posY
		self.anguloScan=angulo
		self.anchuraScan=anchuraScan
		self.siDetectado=True

	def setPosicionAliado(self, x, y, current=None):
		self.posAliado.x=x
		self.posAliado.y=y

	def getPosicionAliado(self, current=None):
		return self.posAliado

	def getTipo(self, current=None):
		return self.tipo

	def distanciaAliados(self, aliado, posicion, current=None):
		return int(math.hypot(math.fabs(aliado.x - posicion.x), math.fabs(aliado.y - posicion.y)))

	def calcularDisparo(self, posicion, current=None):
		if(self.siDetectado):
			print("Calculando disparo contra enemigo detectado!")

			if((self.anguloScan>=0 and self.anguloScan<45) or (self.anguloScan<=359 and self.anguloScan>=315)):
				self.posAttack.x+=self.aumentarDistancia
				if(self.anguloScan>=0 and self.anguloScan<45):
					self.posAttack.y+=self.aumentarDistancia2
				elif(self.anguloScan>=315 and self.anguloScan<=359):
					self.posAttack.y-=self.aumentarDistancia2

			elif(self.anguloScan>=45 and self.anguloScan<135):
				self.posAttack.y+=self.aumentarDistancia
				if(self.anguloScan>=45 and self.anguloScan<90):
					self.posAttack.x+=self.aumentarDistancia2
				elif(self.anguloScan>=90 and self.anguloScan<135):
					self.posAttack.x-=self.aumentarDistancia2

			elif(self.anguloScan>=135 and self.anguloScan<225):
				self.posAttack.x-=self.aumentarDistancia
				if(self.anguloScan>=135 and self.anguloScan<180):
					self.posAttack.y+=self.aumentarDistancia2
				elif(self.anguloScan>=180 and self.anguloScan<225):
					self.posAttack.y-=self.aumentarDistancia2

			elif(self.anguloScan>=225 and self.anguloScan<315):
				self.posAttack.y-=self.aumentarDistancia
				if(self.anguloScan>=225 and self.anguloScan<270):
					self.posAttack.x-=self.aumentarDistancia2
				elif(self.anguloScan>=270 and self.anguloScan<315):
					self.posAttack.x+=self.aumentarDistancia2

			self.aumentarZonaDisparo1()
			self.aumentarZonaDisparo2()

		x=self.posAttack.x-posicion.x
		y=self.posAttack.y-posicion.y
		self.anguloDisparo=int(math.degrees(math.atan2(y,x)))
		self.distancia=self.distanciaAliados(posicion, self.posAttack)


	def disparoAleatorio(self, posicion, current=None):
		print("Calculando disparo aleatorio")
		self.posAttack=drobots.Point(random.randint(0,999),random.randint(0,999))
		x=self.posAttack.x-posicion.x
		y=self.posAttack.y-posicion.y
		self.anguloDisparo=int(math.degrees(math.atan2(y,x)))
		self.distancia=self.distanciaAliados(posicion, self.posAttack)


	def aumentarZonaDisparo1(self, current=None):
		if(self.aumentarDistancia>=700):
			self.aumentarDistancia=100
		else:
			self.aumentarDistancia+=100

	def aumentarZonaDisparo2(self, current=None):
		self.aumentarDistancia2=random.randint(0,100)

	def vaciarListas(self, current=None):
		listaVacia=[]
		self.robotsDefend=listaVacia
		self.robotsAttack=listaVacia

	def robotDestroyed(self, current=None):
		if(self.isDestroyed==False):
			proxy_container=current.adapter.getCommunicator().stringToProxy("Container")
			container_prx = services.ContainerPrx.uncheckedCast(proxy_container)
			proxies_robots = container_prx.list()
			container_prx.unlink("RobotAttacker"+str(self.contA))
			self.isDestroyed=True
			print("El robot ha sido destruido")
		
