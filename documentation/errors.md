# Errors
## Syntax Error
<span style="color: red; background-color: #00000040; padding: 5px 10px; border-radius: 4px;">
Syntax Error: Expected ")". Got '\n' instead.
</span>

Syntax errors are caused by incorrect provided syntax.
They originate in the parser, meaning that the code may never run after encountering such an error.

Example:
```js
function test = (num) => num + 1

log(test(5)  // ")" missing -> results in Syntax Error
```
<br>

## Name Error
<span style="color: red; background-color: #00000040; padding: 5px 10px; border-radius: 4px;">
Name Error: Name 'e' is not defined
</span>

Name Errors originate in the parser. This type of error is raised when the attempt
to access or modify an unassigned variable is made. The error is also raised
if the variable is assigned in a lower context.


Example:
```js
var hello2 = "hello!"
log(hello)  // "hello" wasn't defined prior to this call -> results in Name Error


(function a = () => {
    var bob = 3  // assign variable "bob" in lower context
    log(bob)  // logs "3"
})()

log(bob)  // "bob" only assigned in lower context -> results in Name Error
```
<br>

## Unhandled Errors
### No visit method defined
<span style="color: red; background-color: #00000040; padding: 5px 10px; border-radius: 4px;">
No visit method defined for <u>NoneType</u>
</span>

This error originates in the interpreter.
It usually indicates a syntax error that hasn't
yet been accounted for in the language itself.
The code might or might not continue running as per usual afterward.

Example:
```js
// Unaccounted "," followed by ")":
log(any([1, 0]),)
// not (yet) detected by parser, thus "No visit method" error
// still runs; logs "true, None" (Note that 'None' should not exist in mcs)
```
<br>
