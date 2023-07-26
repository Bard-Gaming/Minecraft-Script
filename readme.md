# Minecraft Script

Minecraft script is primarily a tool to make Minecraft Datapack creation easier.
Minecraft Script is an interpreted programming language which goes through the Python interpreter for output.
However, interpretation is not its main feature, and is rather more of a debugging tool, as its sole
purpose is to allow you to validate your code before building it into a full datapack.

# Commands
```cmd
python -m minecraft_script help
python -m minecraft_script run [files: optional, multiple allowed]
python -m minecraft_script build [file]
```

## Objects
### Variables
The var keyword can be used to initialize new variables.
Use it by following it by the variable's name, then an equals sign and a value.

```js
var hello2 = 500  // initialized variable "hello2" with value 500

var hello2 = 300  // assigned new value 300 to variable hello2
var hello2 = hello2 + 500  // adds 500 to hello2
```

### Functions
Functions are defined with the "function" keyword. They can be anonymous,
or be attributed a name. Parentheses around the arguments are required (currently, subject to change).

```js
function = (a) => a * 3  // anonymous function

function add = (a, b) => a + b  // define a simple add function
add(2, 7)  // call the function; returns 9
```

## Builtin Functions
### log
The log functions allows you to keep track of values in the console.
It is equivalent to JavaScript's console.log() or Python's print() function.

```js
var hello1 = 500

log(200 + 200)  // logs "400" in console
log(hello1, 300)  // logs "500, 300" in console
```