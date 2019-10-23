'''
topdown.py

Analizador descendente recursivo.
'''
from sly.lex import Lexer
import re

# -------------------------------------------
# Analizador Lexico

class Tokenizer(Lexer):
	
	tokens = { IDENT, NUM, ASSIGN,}
	literals = '();+-*/='

	ignore = ' \t\n'
	
	NUM = r'\d+(\.\d+)?(E[-+]?\d+)?'
	IDENT  = r'[a-zA-Z][a-zA-Z0-9]*'

	def NUM(self, t):
		t.value = float(t.value)
		return t

	def error(self, t):
		print("Entrada errada %r" % t.value[0])
		self.index += 1

# -------------------------------------------
# Nodos Abstract Syntax Tree (AST)
class AST(object):
	_nodes = { }
	
	@classmethod
	def __init_subclass__(cls):
		AST._nodes[cls.__name__] = cls
		
		if not hasattr(cls, '__annotations__'):
			return
			
		fields = list(cls.__annotations__.items())
		
		def __init__(self, *args, **kwargs):
			if len(args) != len(fields):
				raise TypeError(f'{len(fields)} argumentos esperados')
			for (name, ty), arg in zip(fields, args):
				if isinstance(ty, list):
					if not isinstance(arg, list):
						raise TypeError(f'{name} debe ser una lista')
					if not all(isinstance(item, ty[0]) for item in arg):
						raise TypeError(f'Todos los tipos de {name} deben ser {ty[0]}')
				elif not isinstance(arg, ty):
					raise TypeError(f'{name} debe ser {ty}')
				setattr(self, name, arg)
				
			for name, val in kwargs.items():
				setattr(self, name, val)
				
		cls.__init__ = __init__
		cls._fields = [name for name,_ in fields]
		
	def __repr__(self):
		vals = [ getattr(self, name) for name in self._fields ]
		argstr = ', '.join(f'{name}={type(val).__name__ if isinstance(val, AST) else repr(val)}'
		for name, val in zip(self._fields, vals))
		return f'{type(self).__name__}({argstr})'

# Nodos Abstract del AST
class Statement(AST):
	pass
	
class Expression(AST):
	pass
	
class Literal(Expression):
	'''
	Un valor literal como 2, 2.5, o "dos"
	'''
	pass

class Location(AST):
	pass

# Nodos Reales del AST

class NumLiteral(Literal):
	value : float
		
class Binop(Expression):
	'''
	Un operador binario como 2 + 3 o x * y
	'''
	op    : str
	left  : Expression
	right : Expression

class SimpleLocation(Location):
	name : str
	
class ReadLocation(Expression):
	location : Location

class WriteLocation(Statement):
	location : Location
	value    : Expression


# -------------------------------------------
# Recursive Descent Parser.
#
# You must modify the methods of this class to build the parse tree
class RecursiveDescentParser(object):
	'''
	Implementacion de un Analizador descendente
	recursivo.  cada metodo implementa una sola
	regla de la gramatica.  Use el metodo
	._accept() para probar y aceptar el token
	actualmente leido.  use el metodo
	._expect() para coincidir y descartar
	exactamente el token siguiente en la 
	
	 entrada (o levantar un SystemError si no
	coincide).
	
	El atributo .tok contiene el untimo
	token aceptado. El atributo .nexttok 
	contiene el siguiente token leido.
	'''
	def assignment(self):
		'''
		assignment : IDENT = expression ;
		'''
		if self._accept('IDENT'):
			name = self.tok.value
			self._expect('=')
			expr = self.expression()
			self._expect(';')
			return WriteLocation(
				SimpleLocation(name),
				expr,
				lineno=1)
		else:
			raise SyntaxError('Esperando un identificador')
			
	def expression(self):
		'''
		expression : term { ('+'|'-') term }          # EBNF
		'''
		# You need to complete
		expr = self.term()
		while self._accept('+') or self._accept('-'):
			operator = self.tok.value
			right = self.term()
			expr = Binop(operator,
				expr,
				right, 
				lineno=1)
		return expr
		
	def term(self):
		'''
		term : factor { ('*'|'/') factor }            # EBNF
		'''
		term = self.factor()
		while self._accept('*') or self._accept('/'):
			operator = self.tok.value
			right = self.factor()
			term = Binop(operator,
				term,
				right,
				lineno=1)
		return term
		
	def factor(self):
		'''
		factor : IDENT
				| NUMBER
				| ( expression )
		'''
		if self._accept('IDENT'):
			return ReadLocation(self.tok.value)
		elif self._accept('NUM'):
			return NumLiteral(self.tok.value)
		elif self._accept('('):
			expr = self.expression()
			self._expect(')')
			return expr
		else:
			raise SyntaxError('Esperando IDENT, NUM o (')
			
	# -----------------------------------------
	# Gunciones de Itilidad.  No cambie nada
	# 
	def _advance(self):
		'Advanced the tokenizer by one symbol'
		self.tok, self.nexttok = self.nexttok, next(self.tokens, None)
		
	def _accept(self,toktype):
		'Consume the next token if it matches an expected type'
		if self.nexttok and self.nexttok.type == toktype:
			self._advance()
			return True
		else:
			return False
			
	def _expect(self,toktype):
		'Consume and discard the next token or raise SyntaxError'
		if not self._accept(toktype):
			raise SyntaxError("Expected %s" % toktype)
			
	def start(self):
		'Entry point to parsing'
		self._advance()              # Load first lookahead token
		return self.assignment()
		
	def parse(self,tokens):
		'Entry point to parsing'
		self.tok = None         # Last symbol consumed
		self.nexttok = None     # Next symbol tokenized
		self.tokens = tokens
		return self.start()
		
if __name__ == '__main__':
	text = "a = 2 + 3 * (4 + 5);"
	lexer = Tokenizer()
	parser = RecursiveDescentParser()
	ast = parser.parse(lexer.tokenize(text))
	
	for depth, node in flatten(ast):
			print('%s: %s%s' % (getattr(node, 'lineno', None), ' '*(2*depth), node))

