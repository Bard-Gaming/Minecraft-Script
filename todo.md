# MCS Todo List

## Emergencies
- [x] Fix everything breaking after function call | Resolved: forgot to .advance()

## Yet to be done
- [ ] **Update binary operations**
  - [ ] change it so the left expr is unchanged (doesn't auto-convert to number)
  - [ ] make strings concatenable
  - [ ] exception handling


- [ ] Update Variables
  - [x] Once declared, ~~don't need keyword~~ use 'set' keyword
  - [ ] actually make use of 'const' keyword (or remove it entirely)


- [ ] Types restructure
  - [ ] Make Functions & BuiltinFunctions inherit from ``MCSObject``
  - [x] Add ``MCSObject`` parent class
  - [x] ``get_value()``


- [ ] Add attributes
  - [ ] Lexer ``.`` (``tt_type``=``TT_ATTRIBUTE_DOT``)
  - [ ] Parser attribute
    - [ ] grammar: ``atom`` ``.`` ``name``
    - [ ] loop back to atom (i.e. attribute is atom)
  - [ ] Interpreter attribute
    - [ ] Context stuff
    - [ ] Errors


- [ ] Add conditions
  - [ ] Add truth checks
    - [ ] ``==``
    - [ ] ``<`` & ``>``
    - [ ] ``<=`` & ``>=``
  - [ ] ``if`` condition
  - [ ] ``else`` condition
    - [ ] ``else if`` support


- [ ] Add loops
  - [ ] ``for`` loop
  - [ ] ``while`` loop


- [ ] **Add 'Entity' type**
  - [ ] Add dict to cross-check what current entities are being selected
  - [ ] Add tags (delimited with '\[' and '\]')


- [ ] Make return statements throw error when not in function / code block (to be decided)

## Completed
- [x] Rework Iterables
  - [x] Rework ``ListGetNode`` to support strings (and other iterables in the future)
  - [x] ``IterableSetNode``
  - [x] Make Strings Iterable


- [x] implement ``set`` keyword
  - [x] for iterables
  - [x] for non-iterables


- [x] Restructure Statements
  - [x] ``.statement()`` --> ``.statement_list()``
  - [x] new ``.statement()`` = ``.expression()`` without ``var``, ``set``