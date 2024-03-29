# MCS Todo list

## Parser
  - [x] Rework ParserNode parent class
    - [x] Rework every parser node to fit new parent class
    - [x] Make sure everything still has the same functionality

  - [x] SetKeyNode
    - [x] Node
    - [x] Parser Implementation
  - [x] AttributeGetNode
    - [x] Node
    - [x] Parser implementation

## Interpreter
  - [x] SetKeyNode
    - [x] Iterable implementation
    - [x] Interpreter implementation

  - [x] Attributes/methods
    - [x] AttributeGetNode
    - [x] List
      - [x] .append()
      - [x] .length

## Compiler
  - [x] IfConditionNode
  - [x] ForLoopNode
  - [x] WhileLoopNode
  - [x] NullNode
  - [x] BooleanNode
  - [ ] GetKeyNode
  - [ ] SetKeyNode
  - [ ] AttributeGetNode
  - [ ] ReturnNode
  - [ ] UnaryOperationNode


  - [x] List implementation
    - [x] Data mcjson dict
    - [x] "length" (key) element for list length


  - [x] Builtin functions
    - [x] log() -> ``tellraw @a {"storage":"mcs_context_id", "nbt":"variable.name"}``
    - [x] command() function to run raw minecraft commands
    - [x] get_block() function to get block located at given x, y, z coordinates

## Documentation
  - [ ] Add page on customizing the language
    - [ ] Side note: make "true" keyword customizable in parser nodes (BooleanNode)
  - [ ] Revisit whole documentation
    - [ ] Remove obsolete/deprecated things
    - [ ] Add new features
    - [ ] Change "build" command to "compile"? -> Rework shell commands
