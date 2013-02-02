# -*- coding: utf-8 -*-
##
#This file is part of MegBot.
#
#   MegBot is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   MegBot is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with MegBot.  If not, see <http://www.gnu.org/licenses/>.
##

import cmath

base = 10 

class TypeError(Exception):
    pass
class MathsError(Exception):
    pass

class Elem():
    OPERAND = 0 # lets use this as an operand ID
    OPERATOR = 1 # lets use this as the operator ID
    MFUNC = 2 # this is used for maths functins (sqrt, log, etc...)
    def __init__(self, value, value_type):
        self.value = value

        # validate type
        if value_type == self.OPERATOR or value_type == self.OPERAND:
            self.type = value_type
        else:
            raise TypeError(value_type)
    def calculate(self, operand1, operand2):
        """ Calculates operand1 <self> operand2 """
        if self.value == "+":
            return operand1 + operand2
        elif self.value == "-":
            return operand1 - operand2
        elif self.value == "*":
            return operand1 * operand2
        elif self.value == "/":
            return operand1 / operand2
        elif self.value == "^":
            return operand1 ** operand2
        else:
            # what else?
            Channel.send("Something has gone wrong! Sorry. (%s %s %s)"
                    % (operand1, self.value, operand2))
            raise MathsError("%s %s %s" 
                        % (operand1, self.value, operand2))

def display(value):
    """ Displays the value """
    answer = value
    if int(value) == value:
        answer = int(value)
    Channel.send("Answer: %s" % answer)

def prefix(equation):
    """ Handles PN maths """
    Channel.send("Sorry, we don't currently support prefix (pn) notation")

def postfix(equation):
    """ Handles RPN maths """
    stack = []
    for elem in equation:
        # okay so if we've got two values in stack we expect
        # an operator, if not, we expect a value to add to
        # the stack
        slen = len(stack)
        if slen < 2 and elem.type == elem.OPERAND:
            stack.append(elem.value)
        elif slen == 2 and elem.type == elem.OPERATOR:
            try:
                stack = [elem.calculate(stack[0], stack[1])]
            except MathsError:
                return
        else:
            Channel.send("Maths error (Stack: %s, value: %s)" % (stack, elem.value))
            return
    display(stack[0])

def infix(equation):
    """ Handles infix notation """
    Channel.send("Sorry, we don't currently support infix notation.")

def main(conneciton, info):
    """ Calculates the answer to an equation """
    global base
    equation = []
    for item in Info.args:
        # okay it could be a number of things actually,
        # hex? 0x<val>
        # octal o<val> || º<value>
        # binary? 0<value> (not sure)
        # Senary? (fyfyh come on...)
        if item.startswith("0x"):
            # hex!
            val = Elem(int(item, 16), Elem.OPERAND)
            base = 16
        elif item.startswith("o") or item.startswith("º"):
            val = Elem(int(item, 8), Elem.OPERAND)
            base = 8
        elif item.startswith("0"):
            # assume binary?
            pass
        # okay we need to now look at operators and functions before
        # we look at base 10
        elif "+" == item:
            val = Elem(item, Elem.OPERATOR)
        elif "-" == item:
            val = Elem(item, Elem.OPERATOR)
        elif "*" == item:
            val = Elem(item, Elem.OPERATOR)
        elif "/" == item:
            val = Elem(item, Elem.OPERATOR)
        elif "^" == item:
            val = Elem(item, Elem.OPERATOR)
        # mathmatical functions?
        elif item.startswith("sqrt"):
            val = Elem(item, Elem.MFUNC)
        elif item.startswith("log"):
            val = Elem(item, Elem.MFUNC)
        elif item.startswith("lg"):
            # log to the base 2?
            val = Elem(item, Elem.MFUNC)
        elif item.startswith("ln"):
            # log the base e?
            val = Elem(item, Elem.MFUNC)
        elif item.startswith("tan"):
            val = Elem(item, Elem.MFUNC)
        elif item.startswith("cos"):
            val = Elem(item, Elem.MFUNC)
        elif item.startswith("sin"):
            val = Elem(item, Elem.MFUNC)
        # lets have a few constants eh?
        elif "pi" == item or "π" == item:
            val = Elem(cmath.pi, Elem.OPERAND)
        elif "e" == item:
            val = Elem(cmath.e, Elem.OPERAND)
        else:
            # base 10.
            val = Elem(float(item), Elem.OPERAND)

        # assume nothing has gone pair shaped.
        equation.append(val)

    if equation[0].type == Elem.OPERATOR:
        # pn
        prefix(equation)
    elif equation[-1].type == Elem.OPERATOR:
        # rpn
        postfix(equation)
    else:
        # assume infix
        infix(equation)
help = "Uses google to do calculations or conversions"
