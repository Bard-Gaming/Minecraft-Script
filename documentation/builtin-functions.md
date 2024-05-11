# Utility Functions

## Printing / Logging
The logging function ``log`` displays values in the Minecraft chat
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
The get block function ``get_block`` retrieves the id of the block
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
The set block function ``set_block`` places a given block
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
The give item function ``give_item`` gives the person executing the function a given
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
The give clickable item function ``give_clickable_item`` give the person executing the function
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
The Minecraft command function ``command`` tries to run any Minecraft
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
The block ray-casting function ``raycast_block`` makes the entity executing
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
The entity ray-casting function ``raycast_entity`` makes the entity executing
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

## Range of integers

## String concatenation

