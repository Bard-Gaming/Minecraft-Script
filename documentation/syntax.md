# Minecraft-Script Syntax
Minecraft-Script's syntax is heavily inspired by both the Python, and JavaScript
programming languages. This is done so that the syntax is simple to learn (which
is necessary since this language is exclusively made to make Minecraft Datapacks).

Note: in the following document, "context" will be used synonymously with "scope".

## General
Unlike Python, in most cases, whitespaces and newlines are ignored.
Statements are separated by semicolons (``;``), and indentation is irrelevant,
so feel free to structure your code however you desire.

### Grammatical priorities
Grammatical classes have a given priority, which defines which
element gets treated first when parsing a program.
These priorities are as follows (descending order):

- Statement
- Code Block
- Expression
- Logical Comparison
- Term
- Factor
- Atom

### Code blocks
Code blocks are used to isolate part of a program within its own context.
They are most often used with other structures, such as functions,
[conditions](#conditions), and [loops](#loops), but they can be
used on their own.

#### Grammar
- "{" [statement]* "}"

_Note that the semicolon ``;`` after a code block is implicit, and thus not required._

#### Grammatical class: Code Block

#### Examples
```js
var text = "Hello World!";

{
    log(text);  // code blocks inherit variables from their parents
}
```



## Variables

### Defining a variable
Defining a variable means attributing a value to a variable that can be accessed
from the current context and all its children. This also means that defining a variable
also overrides any definition that originates from parent contexts.

#### Grammar
- "var" [name] "=" [expression]

#### Grammatical class: Statement

#### Examples
```js
var bob = 5;  // define the variable bob to correspond to the value 5.
log(bob);  // logs "bob" to the console.
```

```js
{
  var bob = 5; 
}

log(bob);  // Error: bob is not defined in current context.
```

```js
var bob = 5;

{
    var bob = 6;
    log(bob);  // logs 6
}

log(bob);  // logs 5
```



### Changing a variable's value
This implementation of variable definition means that it's impossible
to change a variable that has been defined in a parent's context just by redefining it.
As such, the ``set`` keyword allows the changing of a variable's value, such that
it also changes its value in any parent's context.

#### Grammar
- "set" [name] "=" [expression]
- "set" [name] "[" [expression] "]" = [expression]

#### Grammatical class: Statement

#### Examples
```js
var bob = 5;
set bob = 2;  // sets value of bob to 2

log(bob);  // logs 2
```

```js
var bob = 5;

{
    set bob = 6;
    log(bob);  // logs 6
}

log(bob);  // logs 6 since bob was also changed in parent scope
```

```js
var bob = [1, 2, 3];
set bob[1] = 4;

log(bob[1]);  // logs 4, since bob is now [1, 4, 3]
```



## Functions
### User-defined functions
Functions allow for organizing and optimizing a program/datapack
by isolating bits of code into their own objects. These functions
can then be called in-game with the following syntax:
``/function [datapack name]:user_functions/[function name]``.

#### Grammar
- "function" [name] "(" [name]* ")" [code block]

#### Grammatical Class: Statement

#### Examples
```js
function do_stuff() {
    log("doing stuff...");
}

do_stuff();
```

```js
function do_thing(thing) {
    var msg = concatenate("doing ", thing);
    log(msg);
}

do_thing("stuff");
```

### Special functions
Minecraft-Script has some functions that allow for special
interaction with Minecraft. These functions are constructed
like any normal function.

The "main" function is called every tick (configured in the
datapack's tick.json file).

The "init" function is called when the world is
loaded or when the ``/reload`` function is called
(configured in the datapack's load.json file).

The "kill" function is called when the datapack's
main "kill" function called with the command
``/function [datapack name]:kill``. The kill function
adds a way to disable/uninstall the datapack in such a
way that all used storages (``/data get storage ...``),
all used scoreboards, and in general all data associated with
the datapack is removed.

#### Grammar
- "function" "main" "(" ")" [code block]
- "function" "init" "(" ")" [code block]
- "function" "kill" "(" ")" [code block]

#### Grammatical Class: Statement

#### Example
```js
function main() {
    log("hello!");  // logs "hello!" every tick.
}

function init() {
    log("starting greetings...");
    // logs "starting greetings..."
    // when the world is first loaded (before main function)
}

function kill() {
    log("stopping greetings...");
    // logs "stopping greetings..."
    // when the datapack is disabled using the kill function.
}
```


### Builtin-Functions
See [builtin-functions](builtin-functions.md) for reference.




## Operations

### Addition
Simple integer addition. Using a string in an addition
does an integer addition with the string's length
(default Minecraft behaviour).

#### Grammar
- [factor] "+" [factor]

#### Grammatical class: Term

#### Example
```js
var bob = 1;
log(bob + 5);  // logs 6
```


### Subtraction
Simple integer subtraction.

#### Grammar
- [factor] "-" [factor]

#### Grammatical class: Term

#### Example
```js
var bob = 5;
log(bob - 4);  // logs 1
```


### Multiplication
Simple integer multiplication.

#### Grammar
- [atom] "*" [atom]

#### Grammatical class: Factor

#### Example
```js
var bob = 5;
log(1 + bob * 2);  // logs 11 (follows mathematical order)
```


### Division
Euclidean division. This is the same as
applying a normal division and then flooring the result
down to its nearest integer.

#### Grammar
- [atom] "/" [atom]

#### Grammatical class: Factor

#### Example
```js
var bob = 5;
log(bob / 2);  // logs 2
```


### Modulus
Modulus operation. This is the same as getting
the remainder of the Euclidean division of two integers.

#### Grammar
- [atom] "%" [atom]

#### Grammatical class: Factor

#### Example
```js
var bob = 5;
log(bob % 2);  // logs 1 (5 = 2*2 + 1, with 1 being the remainder)
```


### Equality
The equality operation checks whether two operands are
equal in value.

#### Grammar
- [term] "==" [term]

#### Grammatical class: Logical Comparison

#### Example
```js
var bob = 5;
log(bob == 5);  // logs 1 (integer representation of true)
```

### Inequality
The inequality operations compare two operands
relative to each other.

#### Grammar
- [term] "<" [term]
- [term] "<=" [term]
- [term] ">" [term]
- [term] ">=" [term]

#### Grammatical Class: Logical Comparison

### Boolean Not
The boolean not operation inverts a
given boolean value. An inverted ``true`` is
``false``, and an inverted ``false`` is ``true``.

#### Grammar
- "!" [atom]

#### Grammatical Class: Atom

#### Example
```js
var bob = true;
log(!bob);  // logs 0 (integer representation of false)
```



## Loops

### For Loops
In Minecraft-Script, for loops are equivalent to Python loops,
or JavaScript forEach loops. This means that for loops
require an iterable to function, hence the existence of
the ``range()`` function.

#### Grammar
- "for" "(" [name] "in" [expression] ")" [code block]

#### Grammatical class: Statement

#### Examples
```js
// Log all integers between 0 and 5 (exclusive):
for (i in range(5)) {
    log(i);
}
```

```js
// set dirt at current position, then grass_block, then stone
var blocks = ["dirt", "grass_block", "stone"];
for (block in blocks) {
    set_block(block, "~", "~", "~");
}
```

### While Loops
While loops are a way of repeating a code block
until a given condition is false. Normal while loops
are compiled in a recursive manner, meaning they execute
all commands in a single tick, and are bound by the
maxCommandChainLength game rule (by default 65,536 commands),
meaning that the loop will forcefully stop if it doesn't end before
the limit.


#### Grammar
- "while" "(" [expression] ")" [code block]

#### Grammatical class: Statement

#### Examples
```js
// Log all integers between 0 and 5 (exclusive):
var i = 0;
while (i < 5) {
    log(i);
}
```

```js
// Say "hi!" 65,536 times in a single tick
while (true) {
    command("say hi!")
}
```

### Async While Loops
Asynchronous while loops are a way of repeating
a code block until a given condition is false. Whilst normal
while loops are bound by the maxCommandChainLength and end in
a single tick, asynchronous while loops can run indefinitely
and are only repeated once every tick.

#### Grammar
- "async" "while" "(" [expression] ")" [code block]

#### Grammatical class: Statement

#### Examples
```js
// Log all integers between 0 and 5 (exclusive):
var i = 0;
async while (i < 5) {
    log(i);
}
```

```js
// Say "hi!" every single tick
async while (true) {
    command("say hi!")
}
```


## Conditions

### If Clause
In Minecraft-Script, if clauses are syntactically equal
to their JavaScript counterparts. The code block that
follows a given boolean expression will only execute if the
expression is evaluated to being true.

#### Grammar
- "if" "(" [expression] ")" [code block]

#### Grammatical class: Statement

#### Examples
```js
if (true) {
    log("hello!");  // logs "hello!" in the chat
}
```

```js
if (false) {
    log("goodbye!");  // doesn't log anything since block is never executed
}
```


### Else Clause
Else clauses execute if all previous conditions are false.

#### Grammar
- "else" "if" "(" [expression] ")" [code block]
- "else" [code block]

#### Grammatical class: Statement

#### Examples
```js
if (false) {
    log("goodye!");
} else {
    log("hello!);  // logs "hello! since all previous conditions are false
}
```

```js
var bob = 3;

if (bob == 1) {
    log("bob is 1!");  // doesn't log
} else if (bob == 2) {
    log("bob is 2!");  // doesn't log
} else {
    log("bob is not 1 or 2!");  // logs, since bob != 2 and bob != 3
}
```



## Minecraft-related syntax
### Entity Selection
In order to specify which entities should execute what commands,
MCS uses a custom syntax to allow for entity selection in a seamless way.
The selectors themselves are simply taken as granted and passed onto the
datapack, which means they follow exactly the same syntax as Minecraft's
entity selectors.

The debugger won't check the selectors themselves, and will simply
execute the attached statement as if no selector was present
(since it can't access anything within Minecraft).

Selectors allow for spaces and quotation marks, as well as brackets,
since it uses a counting-based system to determine if all brackets
were closed to determine when the selector ends.

#### Grammar
- @ \[selector] [statement]

#### Grammatical Class: Statement

#### Examples
```js
@e[type=cow, name="Bob"] command("kill @s");  // kills all cows named "Bob".
@a[nbt={Inventory:[{id:"minecraft:stick"}]}] command("say hi!");  // makes all players with sticks say hi.

// set a diamond block under every player and give them dirt
@a {
    give_item("minecraft:dirt");
    set_block("~", "~-1", "~", "minecraft:diamond_block");
}
```