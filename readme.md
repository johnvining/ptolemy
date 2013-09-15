# Ptolemy
## A Sexagesimal Calculator for Ancient Astronomy

This is not at all done. At the moment, it converts sexagesimal numbers to decimal, performs the calculation, and converts them back. For numbers like `0;2`, this is a real problem.

#### What it does and doesn't do

Takes a query like `3;0+2;30*4;45;45` and returns a value in sexagesimal. Order of operations is <strike>PE</strike>MDAS. The most obvious errors at this point come from the conversion to decimal. For example, `1;0+1;0+1;01` returns `3;0;59`.

#### Todo and bugs

Here is a very preliminary todo list:

* Bug: Calculations with just two numbers given an error. Oops.
* Rewrite sexagesimal addition and subtraction methods. Maybe, add multiplcation and division as well. 
* Allow whole numbers without `;` or `.`
* Support for parentheses
* Import Ptolemy's values for chord values


#### Requirements

Ptolemy just requires [Pesto](http://www.ollycope.com/software/pesto/).