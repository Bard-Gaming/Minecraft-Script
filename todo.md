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
  - [ ] IfConditionNode
  - [ ] ForLoopNode
    - [ ] Make function macro file
    - [ ] Copy function macro file when building datapack
  - [ ] WhileLoopNode
    - [ ] Make function macro file
    - [ ] Copy function macro file when building datapack
  - [ ] SetKeyNode
  - [ ] AttributeGetNode


  - [ ] List implementation
    - [ ] Data mcjson dict
    - [ ] "length" (key) element for list length


  - [ ] Builtin functions
    - [x] log() -> ``tellraw @a {"storage":"mcs_context_id", "nbt":"variable.name"}``

## Documentation
  - [ ] Add page on customizing the language
    - [ ] Side note: make "true" keyword customizable in parser nodes (BooleanNode)
  - [ ] Revisit whole documentation
    - [ ] Remove obsolete/deprecated things
    - [ ] Add new features
    - [ ] Change "build" command to "compile"? -> Rework shell commands
