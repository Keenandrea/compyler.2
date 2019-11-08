import sys, os
import collections

import node
import token
import utils
import scanner

tk = token.Token()
de_tokens = collections.deque()
node_list = []
line_list = collections.deque()

stat_list = [
    'IN_tk',
    'OUT_tk',
    'START_tk',
    'STOP_tk',
    'COND_tk',
    'ITER_tk'
    'ID_tk',
    'ASSIGN_tk',
]

def fetch_tokens(fn):
    line_number = 1
    with open(fn) as fp:
        while True:
            tk, line_number = scanner.driver(fp, line_number)
            #print tk.identity
            de_tokens.append(tk)
            #print tk.location
            line_list.append(line_number)
            if tk.identity == token.token_ids.token_names[35]: break
            if tk.identity == token.token_ids.token_names[36]: break  

def fetch_node(datum):
    this_node = node.Node()
    this_node.label = datum
    return this_node

# def fetch_terminal():

def printing(n):
    if n == None:
        print "<empty>"
    else:
        # indent
        print n.label, " ", n.token1.instance, " ", n.token2.instance
        if n.child1 != None:
            printing(n.child1)
        if n.child2 != None:
            printing(n.child2)

def error(expected, received):
    print "ERROR: expected", expected, "but received", received
    sys.exit(1)

def assign(tk):
    #print "assign passed:", tk.instance
    # make the node token to hold identifier
    print "terminal identifier:", tk.instance
    tk = de_tokens.popleft()
    print "assign popped:", tk.instance
    #print "assign popped:", tk.instance
    # np = fetch_node("<assign>")
    if tk.identity == "LT_tk":
        tk = de_tokens.popleft()
        print "assign popped:", tk.instance
        if tk.identity == "LT_tk":
            tk = de_tokens.popleft()
            print "from assign to expr with:", tk.instance
            expr(tk)
        else:
            error("LT_tk", tk.identity)
    else:
        error("LT_tk", tk.identity)

def cond(tk):
    #print "cond passed:", tk.instance
    tk = de_tokens.popleft()
    #print "cond popped:", tk.instance
    if tk.identity == "LPAREN_tk":
        tk = de_tokens.popleft()
        #print "cond popped:", tk.instance
        if tk.identity == "LPAREN_tk":
            tk = de_tokens.popleft()
            print "from cond to expr with:", tk.instance
            expr(tk)
            tk = de_tokens.popleft()
            print "from cond to RO with:", tk.instance
            RO(tk)
            tk = de_tokens.popleft()
            print "from cond to expr:", tk.instance
            expr(tk)
            tk = de_tokens.popleft()
            #print "cond popped:", tk.instance
            if tk.identity == "RPAREN_tk":
                tk = de_tokens.popleft()
                #print "cond popped:", tk.instance
                if tk.identity == "RPAREN_tk":
                    tk = de_tokens.popleft()
                    print "from cond to stat with:", tk.instance
                    stat(tk)
                else:
                    error("RPAREN_tk", tk.identity)
            else:
                error("RPAREN_tk", tk.identity)
        else:
            error("LPAREN_tk", tk.identity)
    else:
        error("LPAREN_tk", tk.identity)

def loop(tk):
    #print "loop passed:", tk.instance
    tk = de_tokens.popleft()
    #print "loop popped:", tk.instance
    if tk.identity == "LPAREN_tk":
        tk = de_tokens.popleft()
        #print "cond popped:", tk.instance
        if tk.identity == "LPAREN_tk":
            tk = de_tokens.popleft()
            print "from loop to first expr with:", tk.instance
            expr(tk)
            tk = de_tokens.popleft()
            print "from loop to RO with:", tk.instance
            RO(tk)
            tk = de_tokens.popleft()
            print "from loop to second expr with:", tk.instance
            expr(tk)
            tk = de_tokens.popleft()
            #print "cond popped:", tk.instance
            if tk.identity == "RPAREN_tk":
                tk = de_tokens.popleft()
                #print "cond popped:", tk.instance
                if tk.identity == "RPAREN_tk":
                    tk = de_tokens.popleft()
                    print "from loop to stat with:", tk.instance
                    stat(tk)
                else:
                    error("RPAREN_tk", tk.identity)
            else:
                error("RPAREN_tk", tk.identity)
        else:
            error("LPAREN_tk", tk.identity)
    else:
        error("LPAREN_tk", tk.identity)

def RO(tk):
    print "RO passed:", tk.instance
    tk = de_tokens.popleft()
    print "RO popped:", tk.instance
    if tk.identity == "LT_tk":
        tk = de_tokens.popleft()
        print "RO popped:", tk.instance
        if tk.identity == "LT_tk":
            print "< <"
        if tk.identity == "GT_tk":
            print "< >"
        else:
            error("LT_tk or GT_tk", tk.identity)
    elif tk.identity == "GT_tk":
        tk = de_tokens.popleft()
        print "RO popped:", tk.instance
        if tk.identity == "GT_tk":
            print "> >"
        else:
            error("GT_tk", tk.identity)
    elif tk.identity == "ASSIGN_tk":
        tk = de_tokens.popleft()
        print "RO popped:", tk.instance
    else:
        error("LT_tk or GT_tk or ASSIGN_tk", tk.identity)
    
def R(tk):
    #print "R passed:", tk.instance
    if tk.identity == "LBRACKET_tk":
        tk = de_tokens.popleft()
        print "from R to expr with:", tk.instance 
        expr(tk)
        if tk.identity == "RBRACKET_tk":
            # tk = de_tokens.popleft()
            # print "R popped:", tk.instance 
            print "[<expr>]"
        else:
            error("RBRACKET_tk", tk.identity)
    elif tk.identity == "ID_tk" or tk.identity == "INT_tk":
        #tk = de_tokens.popleft()
        print "terminal identifier:", tk.instance 
        #tk = de_tokens.popleft()
        #print "return out of R with:", tk.instance
        #return tk
    #elif tk.identity == "INT_tk":
        #tk = de_tokens.popleft()
        #print "terminal integer:", tk.instance 
        #tk = de_tokens.popleft()
        #print "return out of R with:", tk.instance
        #return tk
    else:
        error("LBRACKET_tk, ID_tk, or INT_tk", tk.identity) 

def M(tk):
    # print "M passed:", tk.instance 
    if tk.identity == "MINUS_tk":
        tk = de_tokens.popleft()
        print "from M to M with:", tk.instance
        M(tk)
    else:
        print "from M to R with:", tk.instance
        R(tk)    
        
def N(tk):
    print "from N to M with:", tk.instance 
    M(tk)
    print "N after M now has:", tk.instance
    #tk = de_tokens.popleft()
    #print "N after M popped:", tk.identity
    #print "N popped:", tk.instance
    if tk.identity == "FSLASH_tk":
        tk = de_tokens.popleft()
        print "from N to N with:", tk.instance
        N(tk)
        #tk = de_tokens.popleft()
    elif tk.identity == "ASTERISK_tk":
        tk = de_tokens.popleft()
        print "from N to N with:", tk.instance
        N(tk)
    else:
        # print "return out of N with:", tk.instance
        # return
        M(tk) 

def A(tk):
    print "from A to N with:", tk.instance
    N(tk)
    print "A after N now has:", tk.instance
    #tk = de_tokens.popleft()
    #print "A after N popped:", tk.instance
    if tk.identity == "MINUS_tk":
        tk = de_tokens.popleft()
        print "from A to A with:", tk.instance 
        A(tk)
    else:
    #    print "return out of A with:", tk.instance
    #     return tk
        N(tk)

def expr(tk):
    #print "expr passed:", tk.instance
    print "from expr to A with:", tk.instance
    A(tk)
    #print "expr after A popping..."
    #tk = de_tokens.popleft()
    #print "expr after A popped:", tk.instance
    #tk = de_tokens.popleft()
    #print "expr popped:", tk.instance
    if tk.identity == "PLUS_tk":
        tk = de_tokens.popleft()
        print "expr found '+' then popped:", tk.instance
        print "from expr to expr with:", tk.instance
        expr(tk)
    else:
        # print "return out of expr with:", tk.instance
        # return tk
        A(tk)

def out(tk):
    #print "out passed:", tk.instance
    tk = de_tokens.popleft()
    print "from out to expr with:", tk.instance
    #print "out popped:", tk.instance
    #np = fetch_node("<out>")
    #np.child1 = expr()
    expr(tk)

def ins(tk):
    #np = fetch_node("<in>")
    #print "ins passed:", tk.instance
    tk = de_tokens.popleft()
    #print "ins popped:", tk.instance
    if tk.identity == "ID_tk":
        #np.token1 = tk
        #tk = de_tokens.popleft()
        print "terminal ins with id:", tk.instance
        # fetch_terminal(tk)
        #return np
    else:
        error("ID_tk", tk.identity)

def stat(tk):
    #print "stat passed:", tk.instance
    #tk = de_tokens.popleft()
    #print "stat popped:", tk.identity
    #np = fetch_node("<stat>")
    if tk.identity == "IN_tk":
        #np.child1 = fetch_node("IN")
        #tk = de_tokens.popleft()
        print "from stat to ins with:", tk.instance
        #np.child2 = ins()
        ins(tk)
        #return np
    elif tk.identity == "OUT_tk":
        #np.child1 = fetch_node("OUT")
        #tk = de_tokens.popleft()
        print "from stat to out with:", tk.instance    
        #np.child2 = out()
        out(tk)
        #return np
    elif tk.identity == "START_tk" or tk.identity == "STOP_tk":
        #np.child1 = fetch_node("START")
        #tk = de_tokens.popleft()
        print "from stat to block with:", tk.instance  
        block(tk)  
        #np.child2 = block()
        #return np
    elif tk.identity == "COND_tk":
        #np.child1 = fetch_node("IF")
        #tk = de_tokens.popleft()
        print "from stat to cond with:", tk.instance    
        #np.child2 = cond()
        cond(tk)
        #return np
    elif tk.identity == "ITER_tk":
        #np.child1 = fetch_node("LOOP")
        #tk = de_tokens.popleft()
        print "from stat to loop with:", tk.instance    
        #np.child2 = loop()
        loop(tk)
        #return np
    elif tk.identity == "ID_tk":
        #np.token1 = tk
        #tk = de_tokens.popleft()
        print "from stat to assign with:", tk.instance    
        #np.child1 = assign()
        assign(tk)
        #return np
    else:
        error("IN_tk, OUT_tk, START_tk, COND_tk, ITER_tk, ID_tk, or STOP_tk", tk.identity)

def mstat(tk):
    # print "mstat passed:", tk.instance
    #tk = de_tokens.popleft()
    #np = fetch_node("<mstat>")
    if tk.identity in stat_list or tk.identity == "ID_tk":
        print "from mstat to stat with:", tk.instance
        #np.child1 = stat()
        #np.child2 = mstat()
        stat(tk)
        tk = de_tokens.popleft()
        if tk.identity == "SEMICOLON_tk":
            print "mstat semicolon"
            tk = de_tokens.popleft()
            mstat(tk)
        else:
            print "mstat semicolon error"
            error("SEMICOLON_tk", tk.identity)
    else:
        return None

def stats(tk):
    # print "stats passed:", tk.instance
    # tk = de_tokens.popleft()
    # print "stats popped:", tk.identity
    #np = fetch_node("<stats>")
    #np.child1 = stat()
    if tk.identity in stat_list or tk.identity == "ID_tk":
        print "from stats to stat with:", tk.instance
        stat(tk)
        tk = de_tokens.popleft()
        if tk.identity == "SEMICOLON_tk":
            print "stats semicolon"
            tk = de_tokens.popleft()
            # if tk.identity == "STOP_tk":
            #     print "from stats to block with:", tk.instance
            #     block(tk)
            # else:
            print "from stats to mstat with:", tk.instance
            mstat(tk)
            #np.child2 = mstat()
            #return np

def block(tk):
    if tk.identity == "STOP_tk":
        # if there is another to
        # ken after stop, pop it
        tk = de_tokens.popleft()
        print "stop popped:", tk.identity
        if tk.identity == "EOF_tk":
            print "program parsed!"
            sys.exit(1)
        elif tk.identity == "SEMICOLON_tk":
            tk = de_tokens.popleft()
            print "stop popped again:", tk.identity
            if tk.identity == "STOP_tk":
                block(tk)
            else:
                error("STOP_tk", tk.identity)
        else:
            error("EOF_tk or SEMICOLON_tk", tk.identity)
    elif tk.identity == "START_tk":
        tk = de_tokens.popleft()
        if tk.identity == "VAR_tk":
            print "from block to var with:", tk.instance        
            vars(tk)
            print "made it back to block with:", tk.instance
        elif tk.identity in stat_list:
            print "from block to stats with:", tk.instance 
            stats(tk)
            print "after stats call in block function:", tk.instance
        else:
            error("VAR_tk, IN_tk, OUT_tk, ITER_tk, COND_tk, or ID_tk", tk.identity) 
    else:
        error("START_tk or STOP_tk", tk.identity)

def vars(tk):
    #level = level + 1
    # print "var passed:", tk.identity
    # tk = de_tokens.popleft()
    # print "var popped:", tk.identity
    #np = fetch_node("<var>") 
    if tk.identity == "VAR_tk":
        tk = de_tokens.popleft()
        print "var var popped:", tk.instance
        if tk.identity == "ID_tk":
            #np.token1 = tk
            tk = de_tokens.popleft()
            print "var id popped:", tk.instance
            if tk.identity == "COLON_tk":
                tk = de_tokens.popleft()
                print "var colon popped:", tk.instance
                if tk.identity == "INT_tk":
                    tk = de_tokens.popleft()
                    print "var int popped:", tk.instance
                    # #np.token2 = tk
                    # #np.child1 = vars()
                    if tk.identity == "VAR_tk":
                        vars(tk)
                    elif tk.identity in stat_list:
                        stats(tk) 
                    else:
                        error("VAR_tk, IN_tk, OUT_tk, START_tk, COND_tk, ITER_tk, ID_tk", tk.identity)
                else:
                    error("INT_tk", tk.identity)
            else:
                error("COLON_tk", tk.identity)
        else:
            error("ID_tk", tk.identity)
    else:
        print "at return none:", tk.identity
        return None

def program(tk):
    #np = fetch_node("<program>")
    if tk.identity == "START_tk":
        #tk = de_tokens.popleft()
        print "from program to block with:", tk.instance
        block(tk)
    elif tk.identity == "VAR_tk":
        #tk = de_tokens.popleft()
        print "from program to vars with:", tk.instance    
        vars(tk)
    else:
        error("VAR_tk or START_tk", tk.identity)

def parser(fn):
    fetch_tokens(fn)
    #root = node.Node()
    #root = program()
    tk = de_tokens.popleft()
    print "from parser to program with:", tk.instance
    program(tk)
    if tk.identity == token.token_ids.token_names[35]:
        print "Parse success" 
    if tk.identity == token.token_ids.token_names[36]:     
        print "EOF expected"
        sys.exit(1)
    #return root


""" CLASS NOTES 10.31
token matches, non-terminal calls
use explicit returns when we build the tree
vars can be empty so start can be the first token in the program

CLASS NOTES 11.5

<expr> -> <A> <X>
<X> -> +<expr> | e

whenever a function is called, a node must be generated. 
although some functions may not need to generate nodes,
for example, a function that passes back an empty node
may not need a node, but have it generate a node instead
and have that node be an empty node. 

def expr(tk):
    create node labeled "<expr>"
    A(tk)
    if tk.identity == "PLUS_tk":
        store token in the node (if the token has to be stored)
        tk = de_tokens.popleft()
        attach node
        node.child# = expr(tk)
        return the node

tokens to be stored: identifiers, numbers, and operators

store two tokens in <RO> -> < | < < | > | = | < >
    < < will be two stored tokens 

def RO(tk):
    if tk.identity == <:
        tk = de_tokens.popleft()
        if tk.identity == <:
            store < < 
        else:
            store <

CLASS 11.6 QUESTIONS:

When we get to a terminal, say Identifier or Integer in <R>, 
where do we go from there?
"""


        
            

