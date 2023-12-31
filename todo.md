# MCS Todo List

## Emergencies
- [x] Fix everything breaking after function call | Resolved: forgot to .advance()
- [ ] Fix for/while loop body node doing weird stuff when not in code block

## Yet to be done
- [ ] Minecraft datapack
  - [x] NumberNode
  - [x] StringNode
  - [x] ListNode
  - [x] IterableGetNode
  - [ ] IterableSetNode
  - [ ] BooleanNode
  - [ ] UnaryBooleanNode
  - [x] VariableAssignNode
  - [ ] VariableSetNode
  - [x] VariableAccessNode
  - [x] FunctionAssignNode
  - [x] FunctionCallNode
  - [ ] BinaryOperationNode (good luck)
  - [ ] UnaryOperationNode
  - [ ] IfConditionNode
  - [ ] ForLoopNode
  - [ ] WhileLoopNode
  - [x] MultipleStatementsNode
  - [x] CodeBlockNode
  - [ ] ReturnNode


- [ ] Update Variables
  - [x] Once declared, ~~don't need keyword~~ use 'set' keyword
  - [ ] actually make use of 'const' keyword (or remove it entirely)


- [ ] Add attributes
  - [ ] Lexer ``.`` (``tt_type``=``TT_ATTRIBUTE_DOT``)
  - [ ] Parser attribute
    - [ ] grammar: ``atom`` = ``atom`` ``.`` ``name``
    - [ ] loop back to atom (i.e. attribute is atom)
  - [ ] Interpreter attribute
    - [ ] Context stuff
    - [ ] Errors
  - [ ] Make ``extend()`` & ``append()`` attributes of list


- [ ] **Add 'Entity' type**
  - [ ] Add dict to cross-check what current entities are being selected
  - [ ] Add tags (delimited with '\[' and '\]')
  - [ ] Structure ``@`` ``name``


- [x] Make return statements throw error when not in function / code block (to be decided)

## Completed
- [x] Update type structure
  - [x] "private" variable mangling
  - [x] add "value" variable to MCSObject class (super().\_\_init\_\_() it)


- [x] Add loops
  - [x] ``for`` loop
    - [x] structure: ``for`` ``(`` ``name token`` ``in`` ``iterable`` ``)`` ``statement``
    - [x] ``in`` keyword
    - [x] fix return
    - [x] documentation
  - [x] ``while`` loop
    - [x] structure: ``while`` ``(`` ``atom (parsed to bool)`` ``)``  ``statement``
    - [x] fix return
    - [x] documentation


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