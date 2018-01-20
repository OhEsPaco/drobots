#!/usr/bin/python
# -*- coding:utf-8; mode:python -*-

import sys
import Ice
Ice.loadSlice('drobots.ice')
Ice.loadSlice('services.ice')
Ice.loadSlice('comunicacion.ice')
import services
import drobots
import math
import random

class RobotControllerDefendPrueba(drobots.RobotControllerDefend):
	def __init__(self, bot, current=None):
		self.bot=bot
		self.energia=100
		self.enMovimiento=False
		
		print("¡Robot SPARRING-DEFENSA listo para el combate!")

	def turn (self, current=None):

		self.energia=100

		posicion=self.bot.location()
		self.energia-=1;

		self.drive(posicion)

	def drive(self, posicion, current=None):
		if(self.enMovimiento==False):
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

class RobotControllerAttackPrueba(drobots.RobotControllerAttack):
	def __init__(self, bot, current=None):
		self.bot=bot
		self.energia=100
		self.enMovimiento=False
		
		print("¡Robot SPARRING-ATAQUE listo para el combate!")

	def turn (self, current=None):
		self.energia=100

		posicion=self.bot.location()
		self.energia-=1;

		self.drive(posicion)

	def drive(self, posicion, current=None):
		if(self.enMovimiento==False):
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