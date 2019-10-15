# clexer.py
# coding: utf-8
r'''
Proyecto 1 - Escribir un Lexer
==============================

En este primer proyecto, usted debe escribir un lexer sencillo para 
un lenguaje de instrucciones: MiniC. 

El proyecto es basado en código que usted debe leer (en este archivo) 
y completar. Por favor, lea el contenido completo de este archivo y 
cuidadosamente complete los pasos indicados como comentarios.

Revisión:
---------
El proceso del analizador léxico es la de tomar el texto de entrada y 
descomponerlo en un flujo de símbolos (tokens). Cada token es como una 
palabra válida del diccionario.  Escencialmente, el papel del lexer es 
simplemente asegurarse de que el texto de entrada se compone de símbolos 
válidos antes de cualquier procesamiento adicional relacionado con el 
análisis sintático.

Cada token es definido por una expresion regular. Por lo tanto, su 
principal tarea en este primer proyecto es definir un conjunto de 
expresiones regulares para el lenguaje. El trabajo actual del análisis 
léxico deberá ser manejado por SLY.

Especificación:
---------------
Su lexer debe reconocer los siguientes tokens (símbolos). El nombre a la 
izquierda es el nombre del token, el valor en la derecha es el texto de 
coincidencia.

Palabras Reservadas:
    INT      : 'int'
    IF       : 'if'
    WHILE    : 'while'

Identificadores: (Las mismas reglas como para Python)
    IDENT    : El texto inicia con una letra o '_', seguido por 
                         cualquier número de letras, digitos o guión bajo.

Operadores y Delimitadores:
    PLUS    : '+'
    MINUS   : '-'
    TIMES   : '*'
    DIVIDE  : '/'
    ASSIGN  : '='
    SEMI    : ';'
    LPAREN  : '('
    RPAREN  : ')'
    COMMA   : ','

Literales:
    INTEGER : '123' (decimal)
                        '0123'  (octal)
                        '0x123' (hex)

    FLOAT   : '1.234'
                        '1.234e1'
                        '1.234e+1'
                        '1.234e-1'
                        '1e2'
                        '.1234'
                        '1234.'

Comentarios: Para ser ignorados por el lexer
    //             Ignora el resto de la línea
    /* ... */      Omite un bloque (sin anidamiento permitido)

Errores: Su lexer debe reportar los siguientes mensajes de error:
    lineno: Caracter ilegal 'c' 
    lineno: Cadena sin terminar
    lineno: Comentario sin terminar
    lineno: Cadena de código de escape malo '\..'

Pruebas
-------
Para el desarrollo inicial, trate de correr el lexer sobre un 
archivo de entrada de ejemplo, como:

    bash % python minic.tokenizer.py nibless.c

Estudie cuidadosamente la salida del lexer y asegúrese que tiene 
sentido. Una vez que este rasonablemente contento con la salida, 
intente ejecutar alguna de las pruebas mas difíciles:

    bash % python minic.tokenizer.py testlex1.c
    bash % python minic.tokenizer.py testlex2.c

Bono: ¿Cómo haría usted para convertir estas pruebas en pruebas 
unitarias adecuadas?
'''
import re
from colors import bcolors
# ----------------------------------------------------------------------
# El siguiente import carga una función error(lineno,msg) que se debe
# utilizar para informar de todos los mensajes de error emitidos por su
# lexer. Las pruebas unitarias y otras caracteristicas del compilador
# confiarán en esta función. Ver el archivo errors.py para más documentación
# acerca del mecanismo de manejo de errores.
from errors import error, errors_reported

# ----------------------------------------------------------------------
# El paquete SLY. https://github.com/dabeaz/sly
from sly import Lexer as SLYLexer

from SLYToken import Token

class Lexer(SLYLexer):
    # -------
    # Conjunto de palabras reservadas.  Este conjunto enumera todos los
    # nombres especiales utilizados en el lenguaje, como 'if', 'else',
    # 'while', etc.
    keywords = {
        #type_spec
        'float',
        'integer',
        'string',
        'char',
        'true',
        'false',
        'null',

        #conditions
        'if',
        'else',
        
        #cycles
        'while',

        #comparations
        'eqeq',
        'not_eqeq',
        'eq_greater',
        'greater',
        'eq_less',
        'less',
        'eq_add',
        'eq_sub',
        
        #basic operations
        'plus',
        'minus',
        'times',
        'divide',
        'assign',
        'semi',
        'comma',
        'lparen',
        'rparen',
        'lbracket',
        'rbracket',
        'return',
        'muleq',
        'diveq',
        'modeq',
        'or',
        'and',
    }

    # ----------------------------------------------------------------------
    # Conjunto de token. Este conjunto identifica la lista completa de 
    # nombres de tokens que reconocerá su lexer. No cambie ninguno de estos
    # nombres.
    tokens = {
        # keywords
        * { kw.upper() for kw in keywords },

        # Identificador
        IDENT,
    }

    literals = {
        "+",
        "-",
        "*",
        "/",
        "|",
        "&",
        "!",
        "(",
        ")",
        "{",
        "}",
        ";",
        ",",
        ":",
        "[",
        "]",
    }
    # ----------------------------------------------------------------------
    # Caracteres ignorados (whitespace)
    #
    # Los siguientes caracteres son ignorados completamente por el lexer.
    # No lo cambie.

    ignore = ' \t\r'
    ignore_comment = r'(\/\/.*|/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|/\*'
    ignore_newline = r'\n+'
    # ----------------------------------------------------------------------
    # Patrones ignorados.  Complete las expresiones regulares a continuación 
    # para ignorar los comentarios
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    ASSIGN  = r'='
    SEMI = r';'
    COMMA = r','
    LPAREN  = r'\('
    RPAREN  = r'\)' 
    EQEQ = r"=="
    NOT_EQEQ = r"!="
    GREATER = r">"
    EQ_GREATER = r"=>"
    EQ_LESS = r"=<"
    LESS = r"<"
    EQ_ADD = r"\+="
    EQ_SUB = r"-="
    MULEQ    = r'\*='
    DIVEQ    = r'\/='
    MODEQ    = r'\%='
    OR       = r'\|\|'
    AND      = r'\&\&'
    LBRACKET = r'\{'
    RBRACKET = r'\}'
    ID["true"] = TRUE
    ID["false"] = FALSE
    ID["while"] = WHILE
    ID["if"] = IF
    ID["else"] = ELSE
    ID["null"] = NULL
    ID["return"] = RETURN


    #/*  */
    @_(r'/\*(.|\n)*\*/')
    def COMMENT(self, t):
        self.lineno += t.value.count('\n')

    # //
    @_(r'//.*?')
    def CPPCOMMENT(self, t):
        self.lineno += 1

    @_(r'/\*[^/\*]*')
    def COMMENT_UNTERM(self, t):
        error(self.lineno, "Comentario sin terminar")
        
    # ----------------------------------------------------------------------
    #                           *** DEBE COMPLETAR ***
    #
    # escriba las expresiones regulares que se indican a continuación.
    #
    # Tokens para símbolos simples: + - * / = ( ) ; < >, etc.
    # 
    # Precaución: El orden de las definiciones es importante. Los símbolos 
    # más largos deben aparecer antes de los símbolos más cortos que son 
    # una subcadena (por ejemplo, el patrón para <= debe ir antes de <).

    # ----------------------------------------------------------------------
    #                           *** DEBE COMPLETAR ***
    #
    # escriba las expresiones regulares y el código adicional a continuación
    #
    # Tokens para literales, INTEGER, FLOAT, STRING.
    #
    @_(r'\".*\"(,var|,\".*\")*|\'.*\'(,var|,\'.*\')*')
    def STRING(self, t):
        t.value = t.value[1:-1]
        return t
    # Constante de punto flotante. Debe reconocer los números de punto 
    # flotante en los siguientes formatos:
    #
    #   1.23
    #   123.
    #   .123
    #
    # Bonificación: reconocer números flotantes en notación científica
    #
    #   1.23e1
    #   1.23e+1
    #   1.23e-1
    #   1e1
    #
    # El valor debe ser convertir en un float de Python cuando se lea
    @_(r'[-+]?[0-9]*\.[0-9]+(?:[eE][-+]?[0-9]+)?|[-+]?[0-9][eE][0-9]+|[+-]?\d*[.]')
    def FLOAT(self, t):
        if(not("e" in t.value)):
            t.value = float(t.value)
        return t

    # Constante entera
    #s
    #     1234             (decimal)
    #
    # El valor debe ser convertido a un int de Python cuando se lea.
    #
    # Bonificación. Reconocer enteros en diferentes bases tales como 
    # 0x1a, 0o13 o 0b111011.
    
    @_(r'0[xX][0-9a-fA-F]+|0[oO][0-9a-fA-F]+|[0-9a-fA-F]+|\d+')
    def INTEGER(self, t):
        if(not("b" in t.value or "o" in t.value or "x" in t.value)):
            t.value = int(t.value)
        return t

    # ----------------------------------------------------------------------
    #                           *** DEBE COMPLETAR ***
    #
    # escribir la expresión regular y agregar palabras reservadas
    #
    # Identificadores y palabras reservadas
    #
    # Concuerde con un identificador. Los identificadores siguen las mismas 
    # reglas que Python. Es decir, comienzan con una letra o un guión bajo (_)
    # y pueden contener una cantidad arbitraria de letras, dígitos o guiones
    # bajos después de eso.
    # Las palabras reservadas del lenguaje como "if" y "while" también se 
    # combinan como identificadores. Debe capturar estos y cambiar su tipo 
    # de token para que coincida con la palabra clave adecuada.
    
    @_(r'[a-zA-Z][a-zA-Z]*\d*_*|[_][a-zA-Z]*\d*_*')
    def ID(self, t):
        if t.value == 'const':
            t.type = 'CONST'

        elif t.value == 'print':
            t.type = 'PRINT'

        elif t.value == 'func':
            t.type = 'FUNC'

        elif t.value=='return':
            t.type='RETURN'

        elif t.value=='while':
            t.type='WHILE'

        elif t.value=='else':
            t.type='ELSE'
        
        return t

    # ----------------------------------------------------------------------
    # Manejo de errores de caracteres incorrectos
    def error(self, t):
        if re.match(r'(\/\/.*|/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|/\*',t.value):
            error(self.lineno, "Comentario sin terminar {}".format(t.value))
        elif re.match(r'(\"|\')', t.value):
            error(self.lineno, "Cadena sin terminar {}"(t.value.rstrip()))
        elif t.value.__contains__("\\"):
            error(self.lineno, "Cadena de código de escape malo {}".format(t.value.rstrip()))
        else:
            error(self.lineno, "Caracter Ilegal {}".format(t.value[0]))
        self.index += 1

    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')


    def ignore_comment(self,t):
        if not re.match(r'(\/\/.*|/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)',t.value):
            errorToken = Token()
            errorToken.type = 'ERROR'
            errorToken.value = t.value
            raise self.error(errorToken)

# ----------------------------------------------------------------------
#                   NO CAMBIE NADA POR DEBAJO DE ESTA PARTE
#
# Use este programa principal para probar/depurar su Lexer. Ejecutelo 
# usando la opción -m
#
#    bash% python3 -m clexer filename.c
#
# ----------------------------------------------------------------------
def main():
    '''
    main. Para propósitos de depuracion
    '''
    import sys

    if len(sys.argv) != 2:
        sys.stderr.write('Uso: python3 -m clexer filename.c\n')
        raise SystemExit(1)

    lexer = Lexer()
    text = open(sys.argv[1]).read()
    try:
        for tok in lexer.tokenize(text):
            print("{} {} {}".format(bcolors.OKGREEN,tok,bcolors.ENDC))
    except:
        pass
    print("total errors: {}".format(errors_reported()))

if __name__ == '__main__':
    main()
