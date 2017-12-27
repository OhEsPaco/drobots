#!/bin/bash/python3
# -*- coding: utf-8 -*-
#Francisco Manuel Garcia Sanchez-Belmonte
#Fernando Galan Freire
#Adrian Bustos Marin
#if __name__ == "__main__":
 #   print "Hello World"
    
class PlayerI(drobots.Player):  
    def win(self, current = None):
	print("You win!")
	current.adapter.getCommunicator().shutdown()

    def lose(self, current = None):
	print("Looser!")
	current.adapter.getCommunicator().shutdown()

    def gameAbort(self, current = None):
	print("Game aborted")
	current.adapter.getCommunicator().shutdown()

