import sys

class Logger:
	def __init__(self):
		pass

	def l(self, message, importance='info'):
		print message; sys.stdout.flush()