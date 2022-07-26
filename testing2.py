import ply.yacc as yacc
import mylexer

tokens = mylexer.tokens

class Node:

    def __init__(self, type, childs=[], parent=None):
        self.type = type
        self.childs = childs
        self.parent = parent

    def addChilds(self, nodes):
        for node in nodes:
            self.childs.append(node)
    
precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', '^'),
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
          | statements
    '''
    #Caso 1
    if len(p) > 2:
        p[0] = Node('block', [p[1], p[2]])
        p[1].parent = p[0]
        p[0].addChilds(p[2].childs)
    else:
       p[0] = p[1]

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
    '''
    p[1] = Node(p[1])
    p[2] = Node(p[2])
    p[0] = Node('dcl', [p[1], p[2]], None)
    p[1].parent = p[0]
    p[2].parent = p[0]
    

def p_basicstmt_dclass(p):
    '''
    basicstmt : INT ID '=' num_expr
              | FLOAT ID '=' num_expr
    '''
    p[1] = Node(p[1])
    p[2] = Node(p[2])
    dclNode = Node('dcl', [p[1], p[2]])
    p[1].parent = dclNode
    p[2].parent = dclNode
    
    p[4] = Node(p[4])
    p[0] = Node('asg', [dclNode, p[4]])
    p[4].parent = p[0]

def p_basicstmt_asg(p):
    '''
    basicstmt : ID '=' num_expr                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    '''
    p[0] = Node('asg', [Node(p[1],None,p[0]), p[3]])

    p[3].parent = p[0]

#--- num_expr ---
def p_num_expr(p):
    '''
    num_expr : num_val
    '''
    p[0] = p[1]

def p_num_expr_grp(p):
    '''
    num_expr : '(' num_expr ')'
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
    p[0] = Node(p[2], [p[1], p[3]])
  
    p[1].parent = p[0]
    p[3].parent = p[0]

def p_num_expr_uminus(p):
    '''
    num_expr : '-' num_expr %prec UMINUS
    '''
    p[0] = -p[2]

#--- number ---
def p_number_int(p):
    '''
    num_val : INUMBER
    '''
    p[0] = Node(p[1])

def p_number_float(p):
    '''
    num_val : FNUMBER
    '''
    p[0] = Node(p[1])

def p_number_id(p):
    '''
    num_val : ID
    '''
    p[0] = Node(p[1])

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

# ----- -----
def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

yacc.yacc()

def printChilds(node,level=0):
        print(('\t' * level) + node.type)
        if node.childs:
            for i in node.childs:
             printChilds(i, level+1)

while 1:
    try:
        s = input('> ')
    except EOFError:
        break
    if not s:
        continue
    root = yacc.parse(s)
    printChilds(root)
    