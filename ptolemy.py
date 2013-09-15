#! /usr/bin/python

import sys
import os
sys.path.append('/Library/WebServer/CGI-Executables/ptolemy')
import string
import re
import math
import pesto
import pesto.session.memorysessionmanager


dispatcher = pesto.dispatcher_app()
@dispatcher.match('/', 'GET')
def index(request):
	# M A I N   P A G E :   G E T 
	html = ''; result = ''

	if (request.get('query')):
		query = request.get('query')
		parts = re.split('([\*\+\-\/\:\^])', query)	

		# Print Query
		html += '<div class="controls"><small>QUERY</small><br/>%s</div>' % formatParts(parts)
		
		while True:
			if (len(parts) < 4):
				result = evaluate(parts[0], parts[2], parts[1])
				break
			c = 0; triplets = []; length = len(parts) - 2	
			
			while (c < length):
				triplets.extend([parts[c:c+3]])
				c = c + 1
			d = nextTripletToEvaluate(triplets)

			subResult = evaluate(parts[d], parts[d+2], parts[d+1])

			parts.pop(d)
			parts.pop(d+1)
			parts[d] = subResult
			html += summarizeRow(parts)

		# # Print Result
		html += '<div class="controls"><small>RESULT</small><br/><big>%s</big><br/><br/>' % sexagesimal(result)
		html += '<small>NEW QUERY</small><br/><form><input type="text" name="query" value=%s></form>' % (sexagesimal(result))
		html += '</div>'
	else:
		html += '<div class="controls">Query:<br/><form><input type="text" name="query"></form></div>'

	# Put page together and send as response
	html = createPage(html, "Ptolemy", "Ptolemy: Sexagesimal Calculator")
	return pesto.Response([html])

sessioning = pesto.session_middleware(pesto.session.memorysessionmanager.MemorySessionManager())
application = sessioning(dispatcher)


def decimal(s):
	if (';' in str(s)):
		wholeFrac = string.split(s, ";")
		numInDec = float(wholeFrac[0])
		fracs = string.split(wholeFrac[1], ",")
		y = 1
		for x in fracs:
			x = float(x)
			denom = pow(60, y)
			numInDec += x/denom
			y += 1
		return numInDec
	else:
		return float(s)

def sexagesimal(n, places=2):
	# If sexagesimal, return n
	# If not, return a sexigesimal representation of n
	# If not a number, return n

	if (';' in str(n)):
		return n
	elif ('.' in str(n)):
		s = ''
		i, d = divmod(n, 1)
		s += str(int(i)) + ";"
		while (places > 0):
			i, d = divmod(d * 60, 1)
			s += str(int(i))
			if (places > 1):
				s += ","
			places -= 1
		return s
	else:
		return n

def evaluate(x, y, operator):
	if (operator == "*"):
		return decimal(x) * decimal(y)
	elif (operator == "+"):
		return decimal(x) + decimal(y)
	elif (operator == ':'):
		return decimal(x) / decimal(y)
	elif (operator == '-'):
		return decimal(x) - decimal(y)
	elif (operator == '^'):
		return decimal(x) ** decimal(y)
	else:
		return 1000 #For debugging purposes

def nextTripletToEvaluate(triplets):
	order = ['^', '*', ':', '+', '-']
	for operator in order:
		c = 0
		for x in triplets:		
			if (x[1] == operator):
				return c
			c += 1
	return 0

def summarizeRow(parts):
	html = ''
	html += '<div class="step">'
	html += formatParts(parts)
	html += '</div>'
	return html

def formatParts(parts):
	html = ''; endSuper = False
	for x in parts:
		if (x == '^'):
			html += '<sup>'
			endSuper = True
		elif (endSuper):
			html += sexagesimal(x) + '</sup>'
			endSuper = False
		elif (x == '+'):
			html += ' <b>+</b> '
		elif (x == '*'):
			html += ' &times; '
		elif (x == ':'):
			html += ' <b>:</b> '
		elif (x == '-'):
			html += ' <b>&ndash;</b> '
		else:
			html += sexagesimal(x)

	return html

def createHTMLHeader(title):
	html = ''
	html += "<html><header><title>%s</title>" % (title)
	html += '<style type="text/css">'
	html += 'input {font-size:18px; width: 100%; height: 30px}'
	html += 'div.pageTitle{font-size: 30; color: white; text-align: left; background: #6685E0; padding: 12px; margin: 12; width: 500px}'
	html += 'div.step {font-size: 18; text-align: left; background: #D9D9D9; padding: 12px; margin: 12; width: 500px}'
	html += 'div.controls {color: white; font-size: 18; text-align: left; background: #555D73; padding: 12px; margin:12px; width: 500px}</style>'		
	html += "</header><body>"
	return html

def createHTMLFooter():
	return '</body></html>'

def createPage(bodyHTML, title, subhead):
	html = ''
	html += createHTMLHeader(title)
	html += '<div class="pageTitle"><em></em></br><small><small>%s</small></small></div>' % subhead
	html += bodyHTML
	html += createHTMLFooter()
	return html

def createAlert(kind, text):
	html = '<div class="%s">%s</div>' % (kind, text)
	return html

def printList(listy):
	html = "<ul>"
	for x in listy:
		html += '<li>%s</li>' % x
	html += '</ul>'
	return html