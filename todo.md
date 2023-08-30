# MCS Todo List

## Emergencies
- [x] Fix everything breaking after function call | Resolved: forgot to .advance()

## Yet to be done
- [ ] Update Variables
  - [x] Once declared, ~~don't need keyword~~ use 'set' keyword
  - [ ] actually make use of 'const' keyword (or remove it entirely)


- [ ] Add loops
  - [x] ``for`` loop
    - [x] structure: ``for`` ``(`` ``name token`` ``in`` ``iterable`` ``)`` ``statement``
    - [x] ``in`` keyword
    - [x] fix return
    - [ ] fix body node doing weird stuff when not in code block
    - [x] documentation
  - [ ] ``while`` loop
    - [ ] structure: ``while`` ``(`` ``atom (parsed to bool)`` ``)``  ``statement``
    - [ ] fix return
    - [ ] documentation


- [ ] Add attributes
  - [ ] Lexer ``.`` (``tt_type``=``TT_ATTRIBUTE_DOT``)
  - [ ] Parser attribute
    - [ ] grammar: ``atom`` ``.`` ``name``
    - [ ] loop back to atom (i.e. attribute is atom)
  - [ ] Interpreter attribute
    - [ ] Context stuff
    - [ ] Errors
  - [ ] Make ``extend()`` & ``append()`` attributes of list


- [ ] **Add 'Entity' type**
  - [ ] Add dict to cross-check what current entities are being selected
  - [ ] Add tags (delimited with '\[' and '\]')


- [ ] Make return statements throw error when not in function / code block (to be decided)

## Completed
- [x] Add conditions
  - [x] Add truth checks
    - [x] ``==``
    - [x] ``<`` & ``>``
    - [x] ``<=`` & ``>=``
  - [x] ``if`` condition
  - [x] ``else`` condition
    - [x] ``else if`` support


- [x] **Update binary operations**
  - [x] change it so the left expr is unchanged (doesn't auto-convert to number)
  - [x] make strings concatenable
  - [x] exception handling


- [x] Types restructure
  - [x] Make Functions & BuiltinFunctions inherit from ``MCSObject``
  - [x] Add ``MCSObject`` parent class
  - [x] ``get_value()``


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