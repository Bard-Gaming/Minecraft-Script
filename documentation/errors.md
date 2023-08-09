# Errors
## Common Errors
### No visit method defined
<span style="color: red; background-color: #00000040; padding: 5px 10px; border-radius: 4px;">
No visit method defined for <u>NoneType</u>
</span>

This error originates in the interpreter.
It usually indicates a syntax error that hasn't
yet been accounted for in the language itself.

Example:
```js
function test = (num) => num + 1

log(test(5)  // parenthesis ")" missing; not detected by parser, thus "No visit method" error
```