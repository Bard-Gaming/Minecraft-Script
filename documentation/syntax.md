## General Syntax
MCS inherits its syntax from both Python and JavaScript.

Instructions are separated by newlines ('``\n``') and/or semicolons ('``;``').
Both newlines and semicolons are treated exactly the same on the lexer level,
so feel free to use whatever you prefer.

Comments are made using two forward-slashes ('``//``') and go up to the end of the line.
```js
// this
log(5);log(5);

// or this
log(5)
log(5)

// or even this
log(5);
log(5);
```

### Code Blocks
MCS supports code blocks. These blocks are independent of any other code, and have their own context.
This is especially useful when using functions (example in the Function section).
Code blocks are simply defined as being the instructions inside of **braces** ('``{}``').
Example as follows:
```js
var hello = 10
var hello2 = 15

{
    var hello = 5
    log(hello)  // logs "5"
    log(hello2)  // logs "15"
}

log(hello)  // logs "10"
```

### Variables
The ``var`` keyword can be used to initialize new variables.
Use it by following it by the variable's name, then an equals sign and a value.

```js
var hello2 = 500  // Assigned variable "hello2" with value 500

var hello2 = 300  // Reassign variable "hello2" to have the value 300
var hello2 = hello2 + 500  // Reassign variable "hello2" to 300 + 500
```
_Note: reassigning variables to new values works,
but it isn't the "main" way of changing a variable's value._


### Modifying variables
The ``set`` keyword can be used to change a variable's value. This is particularly
useful for debugging, since it raises a NameError when used with a name that wasn't defined
previously, as well as having more features.

```js
var variable = "hello"  // String variable
set variable = [1, 2, 3, 4]  // "variable" is now a List
log(variable)  // logs "[1, 2, 3, 4]"

set variable[2] = "hello again"  // change value at index 2 of variable
log(variable)  // logs '[1, 2, "hello again", 4]'
```

## Default Operations
Operations in MCS follow PEMDAS and **not** plain left-to-right computations.
Current operations are:
- ``+`` Summation
- ``-`` Subtraction
- ``*`` Multiplication
- ``/`` Euclidean Division (i.e. no floating point numbers)
- ``%`` Modulus Operations

Some types might not support certain operations, in which case a ``TypeError`` is raised.

Example as follows:
```js
var sum = 5 + 5  // normal sum. 5+5 = 10
var substraction = 5 - -5  // normal substraction. Unary operators work, so 5 - -5 = 10
var multiplication = 2 * 2  // normal multiplication. 2*2=4
var division = 5 / 2  // Euclidean divison. 5/2 = 2 (no support for floating point numbers)
var modulus = 5 % 2  // Modulus operation. 5%2 = 1

var expression = 3 + 5*2 + -4  // in a more "complex" operation, PEMDAS is applied.
log(expression)  // output is "9"
```
_Note: Depending on the data type, operations might do different things._
