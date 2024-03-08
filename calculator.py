from sexagesimal import *
from utils import Logger, Error

l = Logger('calc')


class Calculator:
    def __init__(self, order_of_operations='PEMDAS'):
        if order_of_operations == 'PEMDAS':
            self.order_of_operations = 'PEMDAS'
        elif order_of_operations == 'LEFT TO RIGHT':
            self.order_of_operations = 'LEFT TO RIGHT'
        l.v('New Calculator: ' + self.order_of_operations)

    def evaluate_expression(self, expression):
        l.v('evaluate_expression: ' + str(expression))
        steps = []
        errors = []
        result = None
        query_expression = expression.pieces

        # Check for expressions within the expression, evaluate those
        query_expression_temp = []
        c = 0
        for x in query_expression:
            if isinstance(x, Expression):
                result_from_parenthetical, steps_for_parenthetical, eval_errors = self.evaluate_expression(x)
                result_from_parenthetical.is_new = True
                for y in eval_errors:
                    errors.append(y)
                beginning_string = Expression(query_expression_temp).to_html()
                query_expression_temp.append(result_from_parenthetical)
                end_string = Expression(query_expression[c + 1:]).to_html()

                for y in steps_for_parenthetical:
                    steps.append(beginning_string + "(" + y + ")" + end_string)
                steps.append(beginning_string + result_from_parenthetical.to_html() + end_string)

            else:
                query_expression_temp.append(x)
            c += 1
        query_expression = query_expression_temp

        # And now, for Unary Operators
        query_expression_temp = []
        c = 0
        for x in query_expression:
            if isinstance(x, Sexagesimal) and x.has_unary:
                x_un_unarized = x.evaluate_unary()
                query_expression_temp.append(x_un_unarized)
                beginning_string = Expression(query_expression_temp[:c]).to_html()
                end_string = Expression(query_expression[c + 1:]).to_html()
                steps.append(beginning_string + x_un_unarized.to_html() + end_string)
            else:
                query_expression_temp.append(x)
            c += 1
        query_expression = query_expression_temp



        # General order of operations
        cont = True
        while cont:
            try:
                if len(query_expression) == 1:
                    # If the query is a single number
                    result = query_expression[0]
                    cont = False
                elif len(query_expression) == 2:
                    errors.append(Error('Only two items in the expression.'))
                    cont = False
                elif len(query_expression) == 3:
                    # If the query has been solved down the last triplet, evaluate and set result
                    result = self.evaluate(query_expression[0], query_expression[2], query_expression[1])
                    cont = False
                else:
                    c = 0
                    triplets = []
                    length = len(query_expression) - 2
                    while c < length:
                        triplets.extend([query_expression[c:c + 3]])
                        c += 1

                    d = self.next_to_evaluate(triplets)
                    sub_result = self.evaluate(query_expression[d], query_expression[d + 2], query_expression[d + 1])
                    sub_result.is_new = True
                    l.l('new sub result: ' + str(sub_result))
                    query_expression.pop(d)
                    query_expression.pop(d + 1)
                    query_expression[d] = sub_result
                    try:
                        steps.append(Expression(query_expression).to_html())
                    except Exception as e:
                        l.e('Could not append step.')
                        l.e('   ' + str(e))
                        errors.append(Error('Could not append step.', python_error=e))
            except Exception as e:
                errors.append(Error('There was a problem with the query:', expression, e))
                l.e('Problem with query. Py: ' + str(e))
                cont = False

        return result, steps, errors

    def next_to_evaluate(self, triplets):
        l.v('next_to_evaluate')
        if self.order_of_operations == 'PEMDAS':
            order = ['^', '*', ':', '+', '-']
            for operator in order:
                c = 0
                for x in triplets:
                    if x[1] == operator:
                        return c
                    c += 1
            return 0
        elif self.order_of_operations == 'LEFT TO RIGHT':
            return 0

    def evaluate(self, a, b, operator):
        l.v('evaluate')
        if operator == "*":
            return a * b
        elif operator == "+":
            return a + b
        elif operator == ':':
            return a / b
        elif operator == '-':
            return a - b
        elif operator == '^':
            return a ** b
        else:
            raise Exception(str(operator) + ' is not a valid operator.')