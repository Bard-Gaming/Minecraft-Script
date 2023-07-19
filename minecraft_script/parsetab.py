
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'left+-left*/CONST_DEFINE LOG LOGTYPE NAME NUMBER VAR_DEFINEstatement : VAR_DEFINE NAME "=" expression\n                 | CONST_DEFINE NAME "=" expressionstatement : VAR_DEFINE NAME\n                 | CONST_DEFINE NAMEstatement : NAME "=" expressionstatement : LOG expressionstatement : LOGTYPE NAME\n                 | LOGTYPE NUMBERstatement : expressionexpression : expression \'+\' expressionexpression : expression \'-\' expressionexpression : expression \'*\' expressionexpression : expression \'/\' expressionexpression : \'(\' expression \')\'expression : NUMBERexpression : NAME'
    
_lr_action_items = {'VAR_DEFINE':([0,],[2,]),'CONST_DEFINE':([0,],[5,]),'NAME':([0,2,5,6,7,9,11,12,13,14,15,22,28,],[3,10,16,18,19,18,18,18,18,18,18,18,18,]),'LOG':([0,],[6,]),'LOGTYPE':([0,],[7,]),'(':([0,6,9,11,12,13,14,15,22,28,],[9,9,9,9,9,9,9,9,9,9,]),'NUMBER':([0,6,7,9,11,12,13,14,15,22,28,],[8,8,20,8,8,8,8,8,8,8,8,]),'$end':([1,3,4,8,10,16,17,18,19,20,23,24,25,26,27,29,30,31,],[0,-16,-9,-15,-3,-4,-6,-16,-7,-8,-5,-10,-11,-12,-13,-14,-1,-2,]),'=':([3,10,16,],[11,22,28,]),'+':([3,4,8,17,18,21,23,24,25,26,27,29,30,31,],[-16,12,-15,12,-16,12,12,-10,-11,-12,-13,-14,12,12,]),'-':([3,4,8,17,18,21,23,24,25,26,27,29,30,31,],[-16,13,-15,13,-16,13,13,-10,-11,-12,-13,-14,13,13,]),'*':([3,4,8,17,18,21,23,24,25,26,27,29,30,31,],[-16,14,-15,14,-16,14,14,14,14,-12,-13,-14,14,14,]),'/':([3,4,8,17,18,21,23,24,25,26,27,29,30,31,],[-16,15,-15,15,-16,15,15,15,15,-12,-13,-14,15,15,]),')':([8,18,21,24,25,26,27,29,],[-15,-16,29,-10,-11,-12,-13,-14,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'statement':([0,],[1,]),'expression':([0,6,9,11,12,13,14,15,22,28,],[4,17,21,23,24,25,26,27,30,31,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement","S'",1,None,None,None),
  ('statement -> VAR_DEFINE NAME = expression','statement',4,'p_statement_declare_value','parser.py',15),
  ('statement -> CONST_DEFINE NAME = expression','statement',4,'p_statement_declare_value','parser.py',16),
  ('statement -> VAR_DEFINE NAME','statement',2,'p_statement_declare','parser.py',24),
  ('statement -> CONST_DEFINE NAME','statement',2,'p_statement_declare','parser.py',25),
  ('statement -> NAME = expression','statement',3,'p_statement_assign','parser.py',37),
  ('statement -> LOG expression','statement',2,'p_statement_log','parser.py',48),
  ('statement -> LOGTYPE NAME','statement',2,'p_statement_log_type','parser.py',52),
  ('statement -> LOGTYPE NUMBER','statement',2,'p_statement_log_type','parser.py',53),
  ('statement -> expression','statement',1,'p_statement_expr','parser.py',67),
  ('expression -> expression + expression','expression',3,'p_expression_add','parser.py',76),
  ('expression -> expression - expression','expression',3,'p_expression_subtract','parser.py',81),
  ('expression -> expression * expression','expression',3,'p_expression_multiply','parser.py',86),
  ('expression -> expression / expression','expression',3,'p_expression_divide','parser.py',91),
  ('expression -> ( expression )','expression',3,'p_expression_group','parser.py',100),
  ('expression -> NUMBER','expression',1,'p_expression_number','parser.py',105),
  ('expression -> NAME','expression',1,'p_expression_name','parser.py',110),
]
