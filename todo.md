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
  - [ ] Add ``MCSObject`` parent class
  - [ ] ``get_value()``


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