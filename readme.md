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
It can either be simply followed by a variable name, in which case it will default to 0,
or you can directly assign a value to it.

```js
var hello1;  // initalized variable "hello1" with value 0 (default)
var hello2 = 500;  // initialized variable "hello2" with value 500

hello2 = 300;  // assigned new value 300 to variable hello2
hello2 = hello2 + 500;  // adds 500 to hello2

logtype hello2; // logs "var" in the console
log hello2;  // logs "800" in the console
```

### Constants
The const keyword can be used to initialize and define new constants.
Unlike vars, these cannot be reassigned new values. Trying to initialize
a new constant without a value brings raises a Syntax Error.

```js
const hello1;  // raises 'Syntax Error: Missing value in const declaration'
const hello1 = 500;
hello1 = 300;  // raises 'Type Error: Tried to assign new value to const "hello1"'

logtype hello1;  // logs "const" in the console
log hello1;  // logs "500" in the console
```

## Functions

```js

function add = (a, b) => a + b  // define a simple add function
add(2, 7)  // call the function; returns 9

```

## Console logging
### Console logging values with log
Logging values in MCS is as simple as typing "log", followed by an expression.
Example:
```js
var hello1 = 500;
const hello2 = 600;

log 200 + 200;  // logs 400 in console
log hello1;  // logs 500 in console
log hello2;  // logs 600 in console
```

### Console logging types with logtype
Logging types in MCS is equally as simple. To log an object's type, simply type "logtype" followed by the object.
Example:
```js
var hello1 = 500;
const hello2 = 600;

logtype 400;  // logs "number" in console
logtype hello1;  // logs "var" in console
logtype hello2;  // logs "const" in console
```