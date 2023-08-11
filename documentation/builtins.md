# Built-in Functions
## Logging / Printing outputs
The ``log()`` functions allows you to keep track of values in the console.
It is equivalent to **JavaScript**'s ``console.log()`` or **Python**'s ``print()`` function.
An indefinite amount of arguments is allowed, to which the arguments' values will be separated by a comma ('``,``').

**Parameters:** &nbsp; _log_value:_ ``*any`` <br>
**Returns:** &nbsp; ``false``

Example as follows:
```js
var hello1 = 500

log(400)  // logs "400" in console
log(hello1, 300)  // logs "500, 300" in console
```

## Adding / Appending values to a list
The ``append()`` appends any value to a list.
It takes a **list** as its first argument, and any other data type as its second.

**Parameters:** &nbsp; _base_list:_ ``list``, _append_value:_ ``any`` <br>

**Returns:** &nbsp; _appended_list:_ ``list``

Example as follows:
```js
var list = [3, 5, 4]

append(list, 2)  // append 2 to the list
var list2 = append(list, [3, 4])  // append [3, 4] to the list and put result in list2

log(list)  // logs "[3, 5, 4, 2, [3, 4]]"
log(list2)  // logs "[3, 5, 4, 2, [3, 4]]"
```

## Extending a list
The ``extend()`` function extends a list by another list.
As such, both the first and second arguments have to be lists.

**Parameters:** &nbsp; _base_list:_ ``list``, _extend_list:_ ``list`` <br>

**Returns:** &nbsp; _extended_list_: ``list``

Example as follows:
```js
var list_1 = [5, 2]
var list_2 = [2, 3]

extend(list_1, list_2)
var list_3 = extend(list_1, list_2)

log(list_1)  // logs "[5, 2, 2, 3]"
log(list_3)  // logs "[5, 2, 2, 3]"
```

## Number Ranges
The ``range()`` function creates a list of numbers starting at 0 by default
and going up to, but not including, the end input value.
It behaves exactly like python's ``range()`` function.

**Parameters:** &nbsp; _end:_&nbsp; ``number`` <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
_start:_ ``number``, _end:_ ``number`` <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
_start:_ ``number``, _end:_ ``number``, _step:_ ``number`` <br><br>
**Returns:** &nbsp; _range:_ ``list``

Example as follows:
```js
var num_range = range(10)
var num_range_1 = range(0, 10, 2)

log(num_range)  // logs "[0, 1, 2]"
log(num_range_1)  // logs "[0, 2, 4, 6, 8]"
```

## Any of List
The ``any()`` function checks a list of elements and tries to find a single truthy value.
If it succeeds, true is returned, else false.

**Parameters:** &nbsp; _compare_list:_ ``list`` <br>
**Returns:** &nbsp; _contains_truthy:_ ``boolean``

Example as follows:
```js
var false_list = [0, false, 0]
var normal_list = [false, 52, 0]
var contains_truthy = any([0, 0, 0, 1, 0])

log(any(false_list))  // logs "false", since 0 and false are considered faulty
log(any(normal_list))  // logs "true", since 52 is truthy
log(contains_truthy)  // logs "true", since 1 is truthy
```