
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'left+-left*/CONST_DEFINE FUNCTION_ARROW FUNCTION_BLOCK FUNCTION_DEFINE FUNCTION_PARAMETER LEFT_PARENTHESIS LOG LOGTYPE NAME NUMBER RIGHT_PARENTHESIS VAR_DEFINEstatement : VAR_DEFINE NAME "=" expression\n                 | CONST_DEFINE NAME "=" expression\n                 | FUNCTION_DEFINE NAME "=" functionstatement : VAR_DEFINE NAME\n                 | CONST_DEFINE NAMEstatement : NAME "=" expressionstatement : LOG expressionstatement : LOGTYPE NAME\n                 | LOGTYPE NUMBERstatement : expressionexpression : expression \'+\' expressionexpression : expression \'-\' expressionexpression : expression \'*\' expressionexpression : expression \'/\' expressionexpression : LEFT_PARENTHESIS expression RIGHT_PARENTHESISexpression : NUMBERexpression : NAMEexpression_repeat :\n                         | expression expression_repeatstatement : function LEFT_PARENTHESIS expression_repeat RIGHT_PARENTHESISfunction : FUNCTION_PARAMETER FUNCTION_ARROW FUNCTION_BLOCK'
    
_lr_action_items = {'VAR_DEFINE':([0,],[2,]),'CONST_DEFINE':([0,],[5,]),'FUNCTION_DEFINE':([0,],[6,]),'NAME':([0,2,5,6,8,9,10,11,14,15,16,17,18,21,23,28,30,31,32,33,34,37,38,],[3,13,19,20,23,24,-16,23,23,23,23,23,23,23,-17,23,-11,-12,-13,-14,23,23,-15,]),'LOG':([0,],[8,]),'LOGTYPE':([0,],[9,]),'LEFT_PARENTHESIS':([0,7,8,10,11,14,15,16,17,18,21,23,28,30,31,32,33,34,37,38,39,],[11,21,11,-16,11,11,11,11,11,11,11,-17,11,-11,-12,-13,-14,11,11,-15,-21,]),'NUMBER':([0,8,9,10,11,14,15,16,17,18,21,23,28,30,31,32,33,34,37,38,],[10,10,25,-16,10,10,10,10,10,10,10,-17,10,-11,-12,-13,-14,10,10,-15,]),'FUNCTION_PARAMETER':([0,35,],[12,12,]),'$end':([1,3,4,10,13,19,22,23,24,25,29,30,31,32,33,38,39,40,41,42,43,],[0,-17,-10,-16,-4,-5,-7,-17,-8,-9,-6,-11,-12,-13,-14,-15,-21,-1,-2,-3,-20,]),'=':([3,13,19,20,],[14,28,34,35,]),'+':([3,4,10,22,23,26,29,30,31,32,33,37,38,40,41,],[-17,15,-16,15,-17,15,15,-11,-12,-13,-14,15,-15,15,15,]),'-':([3,4,10,22,23,26,29,30,31,32,33,37,38,40,41,],[-17,16,-16,16,-17,16,16,-11,-12,-13,-14,16,-15,16,16,]),'*':([3,4,10,22,23,26,29,30,31,32,33,37,38,40,41,],[-17,17,-16,17,-17,17,17,17,17,-13,-14,17,-15,17,17,]),'/':([3,4,10,22,23,26,29,30,31,32,33,37,38,40,41,],[-17,18,-16,18,-17,18,18,18,18,-13,-14,18,-15,18,18,]),'RIGHT_PARENTHESIS':([10,21,23,26,30,31,32,33,36,37,38,44,],[-16,-18,-17,38,-11,-12,-13,-14,43,-18,-15,-19,]),'FUNCTION_ARROW':([12,],[27,]),'FUNCTION_BLOCK':([27,],[39,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'statement':([0,],[1,]),'expression':([0,8,11,14,15,16,17,18,21,28,34,37,],[4,22,26,29,30,31,32,33,37,40,41,37,]),'function':([0,35,],[7,42,]),'expression_repeat':([21,37,],[36,44,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement","S'",1,None,None,None),
  ('statement -> VAR_DEFINE NAME = expression','statement',4,'p_statement_declare_value','parser.py',63),
  ('statement -> CONST_DEFINE NAME = expression','statement',4,'p_statement_declare_value','parser.py',64),
  ('statement -> FUNCTION_DEFINE NAME = function','statement',4,'p_statement_declare_value','parser.py',65),
  ('statement -> VAR_DEFINE NAME','statement',2,'p_statement_declare','parser.py',77),
  ('statement -> CONST_DEFINE NAME','statement',2,'p_statement_declare','parser.py',78),
  ('statement -> NAME = expression','statement',3,'p_statement_assign','parser.py',90),
  ('statement -> LOG expression','statement',2,'p_statement_log','parser.py',104),
  ('statement -> LOGTYPE NAME','statement',2,'p_statement_log_type','parser.py',109),
  ('statement -> LOGTYPE NUMBER','statement',2,'p_statement_log_type','parser.py',110),
  ('statement -> expression','statement',1,'p_statement_expr','parser.py',128),
  ('expression -> expression + expression','expression',3,'p_expression_add','parser.py',137),
  ('expression -> expression - expression','expression',3,'p_expression_subtract','parser.py',142),
  ('expression -> expression * expression','expression',3,'p_expression_multiply','parser.py',147),
  ('expression -> expression / expression','expression',3,'p_expression_divide','parser.py',152),
  ('expression -> LEFT_PARENTHESIS expression RIGHT_PARENTHESIS','expression',3,'p_expression_group','parser.py',161),
  ('expression -> NUMBER','expression',1,'p_expression_number','parser.py',166),
  ('expression -> NAME','expression',1,'p_expression_name','parser.py',171),
  ('expression_repeat -> <empty>','expression_repeat',0,'p_expression_repeat','parser.py',179),
  ('expression_repeat -> expression expression_repeat','expression_repeat',2,'p_expression_repeat','parser.py',180),
  ('statement -> function LEFT_PARENTHESIS expression_repeat RIGHT_PARENTHESIS','statement',4,'p_statement_function_call','parser.py',198),
  ('function -> FUNCTION_PARAMETER FUNCTION_ARROW FUNCTION_BLOCK','function',3,'p_function_anonymous_define','parser.py',202),
]
