# Errors
## Common Errors
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
// not detected by parser, thus "No visit method" error
// still runs; logs "true, None" (Note that 'None' should not exist in mcs)
```

### Syntax Error
<span style="color: red; background-color: #00000040; padding: 5px 10px; border-radius: 4px;">
Syntax Error: Expected ")". Got '\n' instead.
</span>

Syntax errors are caused by incorrect provided syntax.
They originate in the parser, meaning that the code may never run after encountering such an error.

Example:
```js
function test = (num) => num + 1

log(test(5)  // ")" missing
```
