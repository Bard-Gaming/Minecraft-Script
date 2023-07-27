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

### Variables
The ``var`` keyword can be used to initialize new variables.
Use it by following it by the variable's name, then an equals sign and a value.

```js
var hello2 = 500  // initialized variable "hello2" with value 500

var hello2 = 300  // assigned new value 300 to variable hello2
var hello2 = hello2 + 500  // adds 500 to hello2
```

### Functions
Functions are defined with the ``function`` keyword. They can be anonymous,
or be attributed to a name. Parentheses around the parameters are required, even if there are none.

```js
function = (a) => a * 3  // anonymous function

function add = (a, b) => a + b  // define a simple add function
function log_5 = () => log(5)  // function without parameters

add(2, 7)  // call the function; returns 9
log_5()  // prints "5"
```


## Operations
Operations in MCS follow PEMDAS and not plain left-to-right computations.
Current operations are:
- ``+`` Summation
- ``-`` Substraction
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
Minecraft-script can only work with integers.
This is due to the fact that strings aren't a thing in minecraft,
and floating point numbers don't work in most cases, specifically scoreboards.
Current Data Types are:
- Numbers (integers)
- Lists
- Functions

```js
var number = 423  // number, has to be an integer

var array = [1, 2, 3, 4, 5]  // array of numbers

function func = () => log(80085)  // function

var diverse_list = [1, function = () => log(2), [3, 4]]  // list containing all data types
```

