import sys
import os
import argparse
import subprocess
from copy import copy
from collections import defaultdict


""" Give a header and a source file, extract inner call graph """

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", "-f", nargs="+", help="input files")
    return parser.parse_args()

def split_source_header(files):
    headers, sources = [], []
    for file_ in files:
        assert os.path.exists(file_), "%s not exist" %(file_)
        if file_.endswith(".h"): headers.append(file_)
        else: sources.append(file_)
    return headers, sources
        
def process_header(header):
    content = open(header).read()
    content = ' '.join(content.split())
    content = content.split(';')

    tokens = []
    for line in content:
        line = line.strip()
        if line.startswith("//"): continue
        if line.startswith("/*"): continue
        if '#include' in line: continue
        if ' class ' in line: continue
        if 'operator' in line: continue
        if line.find('(') < 0 or line.find(')') < 0: continue
        
        line = line[:line.find('(')]
        if len(line.split()) != 2: continue
        tokens.append(line.split()[1])
    return tokens

def process_class(header):
    classes = []
    for line in open(header):
        if line.startswith('class '):
            classes.append(line.replace(':', ' ').split()[1])
    return classes

def extractCurrentFunction(line):
    line = line[:line.find('(')]
    pos = len(line) - 1
    while (line[pos].isalnum() or line[pos]=='_') and pos>=0: 
        pos-=1
    return line[pos+1:]


def process_source(source, tokens, classes):
    currentFunc = None
    my_tokens = set(copy(tokens))
    for line in open(source):
        if '//' in line: continue
        if not line.startswith(' ') and '(' in line:
            currentFunc = extractCurrentFunction(line)
            my_tokens.add(currentFunc)

    call_table = defaultdict(set)
    for _, line in enumerate(open(source), 1):
        if '//' in line: continue
        if not line.startswith(' ') and '(' in line:
            currentFunc = extractCurrentFunction(line)
        else:
            for token in my_tokens:
                if token in line and token!=currentFunc:
                    position = line.find(token)
                    if line[position-2:position] == "->": continue
                    if line[position + len(token)].isalnum(): continue
                    if currentFunc in  classes or token in classes: continue
                    call_table[currentFunc].add(token)
    return call_table

def update_call_table(call_table, other):
    for key, value in other.items():
        if key not in call_table:
            call_table[key] = value
        else:
            call_table[key] = call_table[key].union(value)
    return call_table


def generate_dot_file(name, call_table):
    s = "digraph %s {\n" %(name)
    s += "\tgraph [dpi=500]\n"
    for caller, callees in call_table.items():
        for callee in callees:
            s += "\t%s -> %s\n" %(callee, caller)
        s += "\n"
    s += "}"
    return s

def main():
    args = get_args()
    headers, sources = split_source_header(args.files)
    tokens = []
    classes = []
    for header in headers:
        tokens += process_header(header)
        classes += process_class(header)

    call_table = defaultdict(set)
    for source in sources:
        update_call_table(call_table, process_source(source, tokens, classes))

    name = os.path.basename(args.files[0])
    if '.' in name: name = name.rpartition('.')[0]

    dot_file = generate_dot_file(name, call_table)
    with open("%s.dot" % name, "w") as fp:
        fp.write(dot_file)
    # dot test.dot -Tpng -o test.png
    print("Saving %s.dot..." % name)
    print("Running `dot %s.dot -Tpng -o %s.png` to generate call graph" %(name, name))

if __name__ == '__main__':
    main()
