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
var hello2 = 500  // initialized variable "hello2" with value 500

var hello2 = 300  // assigned new value 300 to variable hello2
var hello2 = hello2 + 500  // adds 500 to hello2
```


## Operations
Operations in MCS follow PEMDAS and **not** plain left-to-right computations.
Current operations are:
- ``+`` Summation
- ``-`` Subtraction
- ``*`` Multiplication
- ``/`` Euclidean Division
- ``%`` Modulus Operations

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

## Data Types
Minecraft-script doesn't currently support floating point numbers,
although this will probably change in the future.
This is because it can cause issues with operations
(scoreboards don't support floating-point numbers).


### Numbers / Integers
Numbers are integers. They are the building blocks of many functionalities.
They can be manipulated in operations, as seen above.
```js
var number = 423  // number, has to be an integer
```

### Character Strings
Strings are a data type used for storing characters or chains of characters.
The following symbols are used to indicate the presence of a variable:
- ``'`` (Apostrophe)
- ``"`` (Quotation mark)
- `` ` `` (Grave Accent)

*Note: Strings are broken up by newlines,
and not matching a starting quote with an end quote will result in a Syntax Error.*
```js
var string1 = 'this'
var string2 = "is a"
var string3 = `string`

log(string1, string2, string3)  // logs "'this', 'is a', 'string'"
```

### Lists / Arrays
Lists are groups storing all kinds of data.
```js
var list = [1, 2, 3]  // list
extend(list, [4, false, 6])

log(list)  // prints "[1, 2, 3, 4, false, 6]"
```

### Booleans
Booleans are used for logical expressions. They are unique in that they only
have 2 values: ``true`` and ``false``.
```js
var bool = false  // boolean "false"

log(bool)  // logs "false"
```

Booleans also possess unique operations that accept any truthy or faulty values. These are the following:
- ``!`` Logical not (goes before the bool)
- ``&&`` Logical and
- ``||`` Logical or

Example as follows:
```js
var and_operation = !true && true
var or_operation = false || true

log(and_operation)  // logs "false" since !true is false
log(or_operation)  // logs "true" since either one of "false or true" is true
```
However, these operations don't only accept true or false values per se.
For instance, the number 0 counts as being faulty, meaning that ``0 && true`` results in ``false``.
Any number value above 0 is considered truthy.<br>
Expanding on this, booleans can also be used in number operations,
in which case ``true`` will be interpreted as ``1``,
and ``false`` will be interpreted as ``0``.

### Functions
Functions are defined with the ``function`` keyword. They can be anonymous,
or be attributed to a name. Parentheses around the parameters are required, even if there are none.
For simple, single-line functions, the expression is returned.
For more complex, multi-line functions using code blocks, the ``return`` statement is needed.

```js
function = (a) => a * 3  // anonymous function
[function = () => log(5), 2][0]()  // an anonymous function in a list being called

function add = (a, b) => a + b  // define a simple add function; implicit return
function log_5 = () => log(5)  // function without parameters

add(2, 7)  // call the function; returns 9
log_5()  // prints "5"
```

Functions also work with code blocks. This allows you to have functions with multiple instructions.
Example as follows:
```js
function increment_log = (num) => {
    var num = num + 1
    log(num)
}

log(increment_log(5))  // prints "false" (since no return)


function increment = (num) => {
    var num = num + 1
    return num  // return statement
}

log(increment(7))  // prints "8"
```