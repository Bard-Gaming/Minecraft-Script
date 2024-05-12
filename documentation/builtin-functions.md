# Utility Functions

## Printing / Logging
The ``log`` function displays values in the Minecraft chat
using the ``/tellraw`` command. The benefit of using this function instead
of a standard Minecraft command, is that the values that are being printed
to the chat can be dynamic.

### Parameters
- **value_1**: any -> value to be displayed
- **value_2**: any | optional -> value to be displayed
- ...
- **value_5**: any | optional -> value to be displayed

### Output
- None

### Example
```js
var test = " World!";
log("Hello", test);  // prints "Hello World!" in Minecraft chat
```



# World Manipulation

## Get Block
The ``get_block`` function retrieves the id of the block
located at the given x, y, z coordinates as string. This is done using
The id is retrieved by getting the loot table of the block when
mined using a silk touch enchanted netherite pickaxe, so this does
not work on some blocks (such as bedrock).

### Parameters
- **x**: string / number -> X coordinate of block to be retrieved
- **y**: string / number -> Y coordinate of block to be retrieved
- **z**: string / number -> Z coordinate of block to be retrieved

### Output
- **block_id**: string -> id of block located at given X, Y, Z coordinates

### Example
```js
@a var block = get_block("~", "~-1", "~");
log(block);  // logs whatever block the player is standing on
```



## Set Block
The ``set_block`` function places a given block
at specified x, y, z coordinates.

### Parameters
- **x**: string / number -> X coordinate of block to be placed
- **y**: string / number -> Y coordinate of block to be placed
- **z**: string / number -> Z coordinate of block to be placed
- **block**: string -> block to be placed (e.g. "dirt" or "minecraft:dirt")

### Output
- None

### Example
```js
var block = "minecraft:white_concrete";
set_block(0, 64, 0, block);  // places white concrete at 0 64 0
```



## Give Item
The ``give_item`` function gives the person executing the function a given
item with specified properties.

### Parameters
- **item**: string -> Item to be given (e.g. "stick" or "minecraft:stick")
- **components**: string | optional -> component(s) that apply to the item (e.g. "item_name=bob, damage=5")
- **count**: number | optional -> quantity of given item (defaults to 1)

### Output
- None

### Example
```js
@a give_item("minecraft:diamond", "", 64);  // give 64 diamonds to all players in the server
```



## Give Clickable Item
The ``give_clickable_item`` function give the person executing the function
an item that, when right-clicked, executes a function on the person who used it. The item itself
is always a Carrot on a Stick, but using a custom model data with a texture pack can make the item
look custom-made.

### Parameters
- **click_function**: function -> Function that executes on click
- **item_name**: str | optional -> Specifies the item's name ("Carrot on a Stick" by default)
- **custom_model_data**: str / number | optional -> Specifies the item's custom model data

### Output
- None

### Example
```js
function hello = () => {
    command("say Hello World!");
}

// give everyone an item that makes them say "Hello World!" on click:
@a give_clickable_item(hello, "Hello Stick");
```



## Minecraft Command
The ``command`` function tries to run any Minecraft
command it receives (even if it's wrong). The input command can be a variable
that changes, allowing for dynamic command execution.

### Parameters
- **command**: string -> Minecraft command to be run

### Output
- None

### Example
```js
var cmd = "execute as @a at @s run say hi!";
@a command(cmd);  // redundant @a but this works; makes every player say "hi!"
```



# Ray-casting functions

## Block Raycast
The ``raycast_block`` function makes the entity executing
the function cast a ray that travels for a given amount of blocks and runs
any function when it reaches a block.

### Parameters
- **end_function**: function -> function to run when the endpoint is reached
- **travel_distance**: number -> maximum number of blocks the ray travels before stopping
- **ray_function**: function | optional -> function to run at every ray travel tick

### Output
- None

### Example
```js
function place_block = () => {
    set_block("~", "~", "~", "diamond_block");
}

function display_particle = () => {
    command("particle end_rod ~ ~ ~ 0 0 0 0 1 force");
}

// Make every player cast a ray that travels 10 blocks,
// displays an end rod particle along the way,
// and places a diamond block at the destination.
@a raycast_block(place_block, 10, display_particle);
```



## Entity Raycast
The ``raycast_entity`` function makes the entity executing
the function cast a ray that travels for a given amount of blocks and that runs
any function when it reaches an entity (on the entity).

### Parameters
- **end_function**: function -> function to run on the entity when it is reached
- **travel_distance**: number -> maximum number of blocks the ray travels before stopping
- **ray_function**: function | optional -> function to run at every ray travel tick

### Output
- None

### Example
```js
function kill_mob = () => {
    command("kill @s");
}

function display_particle = () => {
    command("particle end_rod ~ ~ ~ 0 0 0 0 1 force");
}

// Make every player cast a ray that travels 10 blocks,
// displays an end rod particle along the way,
// and kills the mob it hit (if it hits one).
@a raycast_block(kill_mob, 10, display_particle);
```



# Data Manipulation

## Appending to a list
The ``append`` function inserts a new value to the end of the list.

### Parameters
- **append_list**: list -> list to append a value to
- **value**: any -> value to append to the list

### Output
- None

### Example
```js
var values = [1, 2, 3, 4];
append(values, 5);
log(values[4]);  // logs "5"
```



## Range of integers
The ``range`` function creates a list containing values ranging from 0 to the
specified bounding value (excluded).

### Parameters
- **bounding_value**: (positive) number -> range boundary

### Output
- **range**: list -> all values from 0 to bounding_value - 1

### Example
```js
for (i in range(5)) {
    log(i);  // logs "0", then "1", ..., then "4"
}
```

## String concatenation
The ``concatenate`` function creates a new string by concatenating
two existing strings. This is especially useful when creating dynamic
commands.

### Parameters
- **string_1**: string -> string to concatenate with string_2 (can't include quotes)
- **string_2**: string -> string to concatenate with string_1 (can't include quotes)

### Output
- **concat_string**: string -> result of string concatenation between string_1 (left)
and string_2 (right)

### Example
```js
function give_nice_item = (name) => {
    var components = concatenate("custom_data={cool: 1}, item_name=", name);
    give_item("diamond", components);
}

@a give_nice_item("Bob");  // gives everyone a diamond named "Bob" with custom data {cool: 1}
```
