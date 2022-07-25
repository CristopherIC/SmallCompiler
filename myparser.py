import ply.yacc as yacc
import mylexer

tokens = mylexer.tokens

class Node:

    def __init__(self, type, value, childs=[], parent=None):
        self.type = type
        self.value = value
        self.childs = childs
        self.parent = parent

    def addChilds(self, nodes):
        for node in nodes:
            self.childs.append(node)

    def __str__(self, level = 0):
        ret = "\t" * level + (self.type + ':' + str(self.value))+"\n"
        for child in self.childs:
            ret += child.__str__(level+1)
        return ret

    def print(self, level = 0):
        s = '\t'*level
        print( s + self.type + ":" + str(self.value))
        for c in self.childs:
            c.print(level+1)
        return s

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)

# Dictionary of names
names = {}

def p_program(p):
    '''
    program : block
    '''
    p[0] = p[1]

def p_block(p):
    '''
    block : statements block
          |
    '''
    #Caso 1
    if len(p) > 2:
        p[0] = Node('block', 'block', [p[1], p[2]], None)
        p[1].parent = p[0]
        p[0].addChilds(p[2].childs)
    else:
       p[0] = Node('block', 'λ')

def p_statements(p):
    '''
    statements : basicstmt ';' 
               | printstmt ';'   
    '''
    p[0] = p[1]

#---- basicstmt ----
def p_basicstmt_dcl(p):
    '''
    basicstmt : INT ID
              | FLOAT ID
              | STRING ID
    '''
    if p[1] == 'int':
        node = Node('int', 0)
    elif p[1] == 'float':
        node = Node('float', 0.0)
    elif p[1] == 'string':
        node = Node('string', '')

    p[0] = Node("dcl " + p[1], p[2], [node])
    node.parent = p[0]

def p_basicstmt_dclass(p):
    '''
    basicstmt : INT ID '=' num_expr
              | FLOAT ID '=' num_expr
              | STRING ID '=' alph_expr
    '''
    p[0] = Node("dcl "+p[1], p[2], [p[4]])
    p[4].parent = p[0]

def p_basicstmt_ass(p):
    '''
    basicstmt : ID '=' num_expr
              | ID '=' alph_expr
    '''
    p[0] = Node('ID', p[1], [p[3]])
    p[3].parent = p[0]

#--- num_expr ---
def p_num_expr(p):
    '''
    num_expr : num_val
    '''
    p[0] = p[1]

def p_num_expr_grp(p):
    '''
    num_expr : '(' num_val ')'
             | '(' num_expr ')'
    '''
    p[0] = p[2]

def p_num_expr_ops(p):
    '''
    num_expr : num_expr '+' num_expr
             | num_expr '-' num_expr
             | num_expr '*' num_expr
             | num_expr '/' num_expr
             | num_expr '^' num_expr
    '''

    p[0] = Node('Operation', p[2], [[p[1], p[3]]])
    p[1].parent = p[0]
    p[3].paren = p[0]

def p_num_expr_uminus(p):
    '''
    num_expr : '-' num_expr %prec UMINUS
    '''
    p[0] = -p[2]

#--- num_val ---

def p_num_val(p):
    '''
    num_val : number
    '''
    p[0] = p[1]

#--- number ---
def p_number_int(p):
    '''
    number : INUMBER
    '''
    p[0] = Node('int', p[1])

def p_number_float(p):
    '''
    number : FNUMBER
    '''
    p[0] = Node('float', p[1])

def p_number_id(p):
    '''
    number : ID
    '''
    p[0] = Node('id', p[1])

#--- printstmt ---
def p_printstmt(p):
    '''
    printstmt : PRINT '(' print_expr ')'
    '''

def p_print_expr(p):
    #Agregar el resto de casos luego
    '''
    print_expr : num_expr
    '''

#--- alph_expr ---
def p_alph_expr(p):
    #Agregar el resto de casos luego
    '''
    alph_expr : STRING
    '''

# ----- -----
def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

yacc.yacc()

while 1:
    try:
        s = input('> ')
    except EOFError:
        break
    if not s:
        continue
    tree = yacc.parse(s)
    tree.print()