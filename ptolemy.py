from flask import Flask, url_for, render_template, request, Markup
from calculator import *
from sexagesimal import Expression
from utils import Logger, Error

app = Flask(__name__)
app.debug = True
l = Logger('ptol')

@app.route('/', methods = ['GET','POST'])
def evaluate_query():
	errors = []

	if request.method == 'GET':
		l.l('request.method = GET')
		# If there is no query, display the basic page with instructions
		return render_template('pt.html', instructions=True)
	
	elif request.method == 'POST':
		l.l('request.method = POST')
		# If method = Post, parse the query
		calc = Calculator()

		query_expression, query_errors = Expression.from_string(request.form['query'])
		for x in query_errors: errors.append(x)

		q_e_html = query_expression.to_html()
		
		# TODO: The following is destructive and should not be.
		result, steps, eval_errors = calc.evaluate_expression(query_expression)
		for x in eval_errors: errors.append(x)

		if (errors==[]): 
			return render_template('pt.html', steps=steps, query=q_e_html, result=str(result), warning='')
		else:
			return render_template('pt.html', errors=errors, instructions=True)