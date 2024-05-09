# Builtin Functions

## Printing / Logging
The logging function ``log`` displays values in the Minecraft chat
using the ``/tellraw`` command. The benefit of using this function instead
of a standard Minecraft command, is that the values that are being printed
to the chat can be dynamic.

### Parameters:
- **value_1**: any -> value to be displayed
- **value_2**: any | optional -> value to be displayed
- ...
- **value_5**: any | optional -> value to be displayed

### Output:
- None

### Example:
```js
var test = " World!";
log("Hello", test);  // prints "Hello World!" in Minecraft chat
```



## Minecraft Command
The Minecraft command function ``command`` tries to run any Minecraft
command it receives (even if it's wrong). The input command can be a variable
that changes, allowing for dynamic command execution.

### Parameters
- **command**: string -> Minecraft command to be run

### Output:
- None

### Example:
```js
var cmd = "execute as @a at @s run say hi!";
@a command(cmd);  // redundant @a but this works; makes every player say "hi!"
```



## Get Block
The get block function ``get_block`` retrieves the id of the block
located at the given x, y, z coordinates as string. This is done using
The id is retrieved by getting the loot table of the block when
mined using a silk touch enchanted netherite pickaxe, so this does
not work on some blocks (such as bedrock).

### Parameters:
- **x**: string / number -> X coordinate of block to be retrieved
- **y**: string / number -> Y coordinate of block to be retrieved
- **z**: string / number -> Z coordinate of block to be retrieved

### Output:
- **block_id**: string -> id of block located at given X, Y, Z coordinates

### Example:
```js
@a var block = get_block("~", "~-1", "~");
log(block);  // logs whatever block the player is standing on
```



## Set Block
The set block function ``set_block`` places a given block
at specified x, y, z coordinates.

### Parameters:
- **x**: string / number -> X coordinate of block to be placed
- **y**: string / number -> Y coordinate of block to be placed
- **z**: string / number -> Z coordinate of block to be placed
- **block**: string -> block to be placed (e.g. "dirt" or "minecraft:dirt")

### Output:
- None

### Example:
```js
var block = "minecraft:white_concrete";
set_block(0, 64, 0, block);  // places white concrete at 0 64 0
```


raycast_block, raycast_entity,
give_item, concatenate, append,