en c parse en 

@_("BOOL_LIT")
def expr(self,p):
	return BoolLiteral(p.BOOL_LIT,lineo=p.lineo)




#TODO: para float e int lo anterior


#TODO: operaciones binarias
expr OR expr
expr AND expr
expr EQ expr | expr NE expr
expr LE expr | expr '<' expr | expr GE expr | expr > expr
expr + expr | expr - expr
expr * expr | expr / expr | expr % expr
! expr | - expr | + expr
( expr )
IDENT | IDENT[ expr ] | IDENT( args ) | IDENT . size
BOOL_LIT | INT_LIT | FLOAT_LIT | NEW type_spec [ expr ]
@_("")
def expr(self,p):
	return BinOp(p[1],p.expr0,p.expr1,lineo=p.lineo)