from ply import lex

tokens = [
        'SYMBOL',
        'TEXT',
        'NODESTART',
        'LPAREN',
        'RPAREN',
        'ENDL'
        ]

t_TEXT   = r'\w+'
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore_comment = r'\/\/[^\n]*'
t_ignore = ' \t'

def t_NODESTART(t): 
    r'>+'
    t.value = len(t.value)  # count the number of >
    return t

def t_SYMBOL(t):
    r'\$\w+'
    t.value = t.value[1:]
    return t

def t_ENDL(t):
    r';'
    t.value = '\n'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character {}".format(t.value[0]))
    t.lexer.skip(1)

lexer = lex.lex()

##############################   Yacc   ############################## 
from ply import yacc
from node import Node, Symbol

#TODO: parentheses matching

def p_nodes(p):
    '''nodes : node nodes
             | empty'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_empty(p):
    'empty :'
    pass

def p_node(p):
    'node : NODESTART content'
    p[0] = Node(p[1],         # depth within the tree
                p.lineno(1),  # line where node is defined
                p[2])

def p_content(p):
    '''content : term content
               | empty'''
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = ""

def p_term(p):
    '''term : TEXT
            | LPAREN
            | RPAREN
            | ENDL'''
    p[0] = p[1]

def p_term_symbol(p):
    'term : SYMBOL'
    p[0] = Symbol(p[1]).get_symbol()

def p_error(p):
    raise(SyntaxError(p))

parser = yacc.yacc()

    
