## Changes

##### [2013-09-23a](https://github.com/senecando/ptolemy/commit/2445bf77cf2e8ea23f7e60acb9e7e1eee3af2870)

* Switched from `Pesto` to `Flask` to run on Heroku.
* Switched some variables to snake_case. Will be doing more of this where needed.
* Started using templates for html generation.
* Started work on moving code into objects.
* Changed the CSS and HTML a bit.
* Added instructions to the home page.
* Created a way to display warnings and errors to the user.


##### 2013-09-15

* Added exponents. Use `^`.
* Added evaluation of a single number. Can now be used as a simple decimal to sexagesimal converter.
* Added an optional argument to `sexagesimal()` for number of places. Defaults to 2.
* Cleaned up display of expressions.
* Fixed Bug: Calculations with just two numbers give an error. Oops.
* Initial commit.