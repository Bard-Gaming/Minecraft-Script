# MCS Todo list


## Lexer
- [ ] Add async while loop (keyword)
- [x] Make entity selector work in lexer instead of parser
- [x] Fix entity selector not supporting spaces


## Parser
- [ ] Add async while loop (variant to normal while loop)
- [x] Update entity selector


## Interpreter
- [ ] Add async while loop (exact same as normal while loop)


## Compiler
- [ ] Add async while loop (uses a function subscribed to tick.mcfunction)


## Shell Commands
- [x] Update ``compile`` command
  - [x] Change args to \<path> \[\<datapack name>] \[\<output path>]
  - [x] Added errors in case a path doesn't exist
- [x] Add config for verbose option
- [x] Add config for default output path
- [x] Add ``config default`` command to reset config to default (needs confirmation)

## Documentation
- [ ] Finish syntax documentation
  - [ ] Special functions (main, init, kill)
  - [x] Code blocks (context)
  - [ ] Conditionals
    - [x] If clause
    - [ ] Else clause
  - [ ] Loops
    - [x] For loop
    - [ ] While loop
    - [ ] Async while loop
  - [ ] Operations
    - [ ] Addition
    - [ ] Subtraction
    - [ ] Multiplication
    - [ ] Division
    - [ ] Modulus
    - [ ] Equality
    - [ ] Inequality (LESSER, LEQ, GEQ, GREATER)
    - [ ] Boolean Not
  - [ ] Entity selection


- [ ] Finish data types documentation