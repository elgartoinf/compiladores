# ----------------------------------------------------------------------

# Las siguientes clases para visitar y reescribir el AST se toman del 
# módulo ast de Python.

# NO MODIFIQUE
class NodeVisitor(object):
	'''
	Clase para visitar los nodos del árbol de análisis sintáctico. 
	Esto se modela después de una clase similar en la biblioteca estándar 
	ast.NodeVisitor. Para cada nodo, el método de visit(node) llama a 
	un método visit_NodeName(node) que debe implementarse en subclases. 
	El método generic_visit() se llama para todos los nodos donde no hay 
	ningún método de matching_NodeName() coincidente.
	
	Este es un ejemplo de un visitante que examina un operador binario:
	
	class VisitOps(NodeVisitor):
		visit_BinOp(self,node):
			print('Binary operator', node.op)
			self.visit(node.left)
			self.visit(node.right)
			visit_UnaryOp(self,node):
			print('Unary operator', node.op)
			self.visit(node.expr)
	
	tree = parse(txt)
	VisitOps().visit(tree)
	'''
	def visit(self, node):
		'''
		Enecuta un metodo de la forma visit_NodeName(node) donde
		NodeName es el nombre de la clase de un nodo particular.
		'''
		if isinstance(node, list):
			for item in node:
				self.visit(item)
		elif isinstance(node, AST):
			method = 'visit_' + node.__class__.__name__
			visitor = getattr(self, method, self.generic_visit)
			visitor(node)
			
	def generic_visit(self,node):
		'''
		Metodo ejecutado si no se encuentra el metodo visit_.
		Este examina el nodo para ver si tiene _fields, una lista,
		o puede ser atravesado.
		'''
		for field in getattr(node, '_fields'):
			value = getattr(node, field, None)
			self.visit(value)
			
	@classmethod
	def __init_subclass__(cls):
		'''
		Revision de sanidad. Se asegura que las clases visitor usen los
		nombres adecuados.
		'''
		for key in vars(cls):
			if key.startswith('visit_'):
				assert key[6:] in globals(), f"{key} no coincide con nodos AST"
				
# NO MODIFICAR
def flatten(top):
	'''
	Aplana todo el árbol de análisis sintáctico en una lista para 
	depurar y probar.  Esto devuelve una lista de tuplas de la 
	forma (depth, node) donde depth es un entero que representa 
	la profundidad y node es el nodo AST asociado.
	'''
	class Flattener(NodeVisitor):
		def __init__(self):
			self.depth = 0
			self.nodes = []
		def generic_visit(self, node):
			self.nodes.append((self.depth, node))
			self.depth += 1
			NodeVisitor.generic_visit(self, node)
			self.depth -= 1
			
	d = Flattener()
	d.visit(top)
	return d.nodes