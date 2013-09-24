#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License,
    or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, see <http://www.gnu.org/licenses/>.


	Usages:
		s = Neuron(("",23303)) 		# new instance
		s.start()			# listening to all dendrites
 		target = ("",23304)		# prepare target for spike
		s.axonFire("some messages", target)	# fire!

"""

__author__ = "Isaac Mao"
__version__ = "0.1alpha"
__email__ = "isaac.mao@gmail.com"
__credits__ = ["Isaac Mao"]


import socket
from threading import Thread
import select

class Neuron():

	def __init__(self, address = ('', 23300)):

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		#self.status = {'living': True}
		self._vesicle = ""
		try:
			self.sock.bind(address)
		except socket.error, msg:
			sys.stderr.write("[ERROR] %s.\n" % msg[1])
			sys.exit(1)
		
		
	@property
	def vesicle(self):
		return self._vesicle

		
	def dendrites(self):
		while True:
			msg = "" 
		    
		    	# using a timeout of 10.0s --> "polling for messages"
		    	if select.select([self.sock],[],[],10.0)[0]:
				# FIXME: maintain message length
				msg, clientAddr = self.sock.recvfrom(4096) 
				self._vesicle= msg

	def axonFire(self,msg,target= ('',23301)):
		firesock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		firesock.connect(target)
		firesock.send(msg)  #we have to take ID of sender later, or lose the trace
		firesock.close()


	def start(self):   
		denthread = Thread(target=self.dendrites)
		denthread.start()

	
