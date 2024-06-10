# MCS Todo list


## Lexer
- [x] Add async while loop (keyword)
- [x] Make entity selector work in lexer instead of parser
- [x] Fix entity selector not supporting spaces


## Parser
- [x] Add async while loop (variant to normal while loop)
- [x] Update entity selector


## Interpreter
- [x] Add async while loop (exact same as normal while loop)


## Compiler
- [x] Add async while loop (uses a function subscribed to tick.mcfunction)


## Shell Commands
- [x] Update ``compile`` command
  - [x] Change args to \<path> \[\<datapack name>] \[\<output path>]
  - [x] Added errors in case a path doesn't exist
- [x] Add config for verbose option
- [x] Add config for default output path
- [x] Add ``config default`` command to reset config to default (needs confirmation)

## Documentation
- [x] Finish syntax documentation
  - [x] Special functions (main, init, kill)
  - [x] Code blocks (context)
  - [x] Conditionals
    - [x] If clause
    - [x] Else clause
  - [x] Loops
    - [x] For loop
    - [x] While loop
    - [x] Async while loop
  - [x] Operations
    - [x] Addition
    - [x] Subtraction
    - [x] Multiplication
    - [x] Division
    - [x] Modulus
    - [x] Equality
    - [x] Inequality (LESSER, LEQ, GEQ, GREATER)
    - [x] Boolean Not
  - [x] Entity selection


- [ ] Finish data types documentation