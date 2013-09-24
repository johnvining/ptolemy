import os, sys, string, re
from flask import Flask, url_for, render_template, request, Markup


app = Flask(__name__)
app.debug = True

@app.route('/')
def ptolemy():
	return render_template('pt.html', title="Ptolemy", instructions=True)

@app.route('/query/', methods=['POST'])
def evaluate_query():
	html = ''
	error = ''

	if request.method == 'POST':
		query = request.form['query']
		parts = re.split('([\*\+\-\/\:\^])', query)	

	if (len(parts) == 1):
		html += '<div class="controls"><small>QUERY</small><br/>%s</div>' % query
	else:
		html += '<div class="controls"><small>QUERY</small><br/>%s</div>' % formatParts(parts)

	while True:
		if (len(parts) == 1):
			result = sexagesimal(parts[0])
			break
		elif (len(parts) < 4):
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

	return render_template('pt.html', export=Markup(html), result=Markup(sexagesimal(result)), error=error)

def decimal(s):
	if (';' in str(s)):
		whole_and_frac = string.split(s, ";")
		numInDec = float(whole_and_frac[0])
		fracs = string.split(whole_and_frac[1], ",")
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
		i, d = divmod(float(n), 1)
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

def createAlert(kind, text):
	html = '<div class="%s">%s</div>' % (kind, text)
	return html

def printList(listy):
	html = "<ul>"
	for x in listy:
		html += '<li>%s</li>' % x
	html += '</ul>'
	return html

# class Number:
# 	def __init__(self, s): 
# 		if (';' in str(s)):
# 			self.base = 60
# 			whole_and_frac = string.split(s, ";")
# 			self.whole = int(whole_and_frac[0])
# 			if (',' in str(whole_and_frac[1])):
# 				fracs = string.split(whole_and_frac[1], ",")
# 				y = 1
# 				self.parts = []
# 				for x in fracs:
# 					self.parts.extend([int(x)])
# 			else:
# 				self.parts = [int(whole_and_frac[1])]
# 		elif ('.' in str(s)):
# 			self.base = 10
# 			self.decfloat = float(s)
# 		else:
# 			self.whole = int(s)


# 	def print_number(self, places=4):
# 		if (self.base == 60):
# 			s  = str(self.whole) + ";"
# 			places = min(places, len(self.parts))
# 			for x in self.parts:
# 				if (places > 1):
# 					s += str(x) + ","
# 				elif (places == 1):
# 					s += str(x)
# 				places -= 1
# 		elif (self.base == 10):
# 			s = str(self.decfloat)

# 		return s

# 	# TODO: Switch to: Print natural (b60 or b10 based on number), and specific
# 	# methods to force the conversion.