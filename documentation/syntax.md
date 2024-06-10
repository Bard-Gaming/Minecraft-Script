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



## Operations

### Addition
### Subtraction
### Multiplication
### Division
### Boolean Not



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

if (false) {
    log("goodbye!");  // doesn't log anything since block is never executed
}
```