import sys

class Logger:
	def __init__(self, location):
		self.location = location

	def l(self, message, importance='info'):
		if importance == 'error':
			print self.location + " :ERROR: " + message; sys.stdout.flush()	
		elif importance == 'verbose':
			pass
		else:
			print self.location + " :: " + message; sys.stdout.flush()

	def e(self, message):
		self.l(message, importance='error')

	def v(self, message):
		self.l(message, importance='verbose')