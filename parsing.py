import sys, os

import utils
import node
import token
import scanner

def get_node(title):
    this_node = node.Node()
    this_node.label = title
    return this_node

# def stats(f, t, level, line):
#     level = level + 1
#     n = node.Node("<stats>", level)
#     n.child1 = stat(f, t, level, line)
#     n.child2 = mstat(f, t, level, line)
#     return n

# def mstat(f, t, level, line):
#     level = level + 1
#     n = node.Node("<mstat>", level)
#     if t.identity == "IN_tk" or t.identity == "OUT_tk" or t.identity == "START_tk" or t.identity == "COND_tk" or t.identity == "ITER_tk" or t.identity == "ID_tk":
#         n.child1 = stat(f, t, level, line)
#         n.child2 = mstat(f, t, level, line)
#         return n
#     else:
#         return None

# def stat(f, t, level, line):
#     level = level + 1
#     n = node.Node("<stat>", level)
#     if t.identity == "IN_tk":
#         n.child1 = ins(f, t, level, line)
#         return n
#     elif t.identity == "OUT_tk":
#         n.child1 = out(f, t, level, line)
#         return n
#     elif t.identity == "START_tk":
#         n.child1 = block(f, t, level, line)
#         return n
#     elif t.identity == "COND_tk":
#         n.child1 = cond(f, t, level, line)
#         return n
#     elif t.identity == "ITER_tk":
#         n.child1 = loop(f, t, level, line)
#         return n
#     elif t.identity == "ID_tk":
#         n.child1 = assign(f, t, level, line)
#         return n
#     else:
#         statement_error(t)


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

def block(fp, tk, level, line):
    level = level + 1
    n = node.Node("<block>", level)
    print "Block function:", tk.identity
    if tk.identity == "START_tk":
        print "Got start"
        tk, line = scanner.driver(fp, line)
        n.child1 = vars(fp, tk, level, line)
        #n.child2 = stats(f, t, level, line)
        if tk.identity == "STOP_tk":
            print "Got stop"
            tk, line = scanner.driver(fp, line)
            return n 
        else:
            error("STOP_tk", tk.identity)
    else:
        error("START_tk", tk.identity)

def vars(fp, tk, level, line):
    print "Made it to vars function with", tk.identity
    level = level + 1
    n = node.Node("<vars>", level)
    if tk.identity == "VAR_tk":
        print "Got var"
        tk, line = scanner.driver(fp, line)
    else:
        print "Return None", tk.identity
        return None

    if tk.identity == "ID_tk":
        print "Got id"
        n.token1 = tk
        tk, line = scanner.driver(fp, line)
    else:
        error("ID_tk", tk.identity)

    if tk.identity == "COLON_tk":
        print "Got Colon"
        tk, line = scanner.driver(fp, line)
    else:
        error("COLON_tk", tk.identity) 

    if tk.identity == "INT_tk":
        print "Got Int"
        n.token2 = tk
        tk, line = scanner.driver(fp, line)
        n.child1 = vars(fp, tk, level, line)
        print "In INT conditional", tk.identity
        return n
    else:
        error("INT_tk", tk.identity)

def program(fp, tk, line):
    level = 0
    print "In Program function"
    n = node.Node("<program>", level)
    if tk.identity == "VAR_tk":
        n.child1 = vars(fp, tk, level, line)
        n.child2 = block(fp, tk, level, line)
        return n
    else:
        error("VAR_tk", tk.identity)

def parser(fn):
    tk = token.Token()
    root = node.Node()
    line = 1
    with open(fn) as fp:
        while True:
            tk, line = scanner.driver(fp, line)
            root = program(fp, tk, line)
            if tk.identity == token.token_ids.token_names[36]: break
            if tk.identity == token.token_ids.token_names[35]: 
                return root
                break



