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

## Comparison Operators
Comparison Operators are used to compare different values.
How and if they can, be compared depends on the type of the values compared,
since some data types, like strings and numbers, aren't compatible with each-other.

The comparison operators are expressed as follows:
- ``==`` (Equality)
- ``<``  (Inferiority)
- ``<=`` (Inferiority or Equality)
- ``>``  (Superiority)
- ``>=`` (Superiority or Equality)

Example as follows:
```js
var value_1 = 15
var value_2 = 32

log(value_1 <= value_2)  // logs 'true'
log(true == !false)  // logs 'true'
log(true < false)  // logs 'false'
```

## Conditions
Conditions are expressed with the ``if`` and ``else`` statements.
They can also be combined to create a chain of conditions.
Conditions can be in any form, and will automatically be parsed to booleans.
This means that a truthy value like ``"hello"``, will count as ``true``.

Example as follows:
```js
if (true) log('hello')
else log('goodbye')
// logs "hello" since condition is true

var age = 17
if (age >= 18) {
    log('You are an adult.')
} else if (age < 18) {
    log('You are a minor.')
}
// logs 'You are a minor.'

function max = (value_1, value_2) => {
    if (value_1 > value_2) {
        return value_1
    } else return value_2
}

log(max(11, 5))  // logs '11'
```

## Loops
MCS currently supports ``for`` loops. These loops follow a python syntax,
allowing to loop over iterables instead of continually incrementing a variable
with the use of the ``in`` keyword.

Example as follows:
```js
for (number in [5, 7, 3, 1, 9, 4, 6]) {
    log(number)  // logs "5", then "7", then "3", etc...
}

// works with any iterable:
var string = "Hello"
for (character in string) {
    log(character)  // logs "H", then "e", then "l", etc...
}
```