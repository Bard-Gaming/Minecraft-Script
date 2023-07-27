# Built-in Functions
## Logging / Printing outputs
The ``log()`` functions allows you to keep track of values in the console.
It is equivalent to **JavaScript**'s ``console.log()`` or **Python**'s ``print()`` function.
An indefinite amount of arguments is allowed, to which the arguments' values will be separated by a comma ('``,``').
```js
var hello1 = 500

log(400)  // logs "400" in console
log(hello1, 300)  // logs "500, 300" in console
```

## Adding / Appending values to a list
The ``append()`` appends any value to a list.
It takes a **list** as its first argument, and any other data type as its second.
Example as follows:
```js
var test = [3, 5, 4]

append(test, 2)  // append 2 to the list
append(test, [3, 4])  // append [3, 4] to the list

log(test)  // logs "[3, 5, 4, 2, [3, 4]]"
```

## Extending a list
The ``extend()`` function extends a list by another list.
As such, both the first and second arguments have to be lists.
Example as follows:
```js
var list_1 = [5, 2]
var list_2 = [2, 3]

extend(list_1, list_2)

log(list_1)  // logs "[5, 2, 2, 3]"
```