import argparse
import string


parser = argparse.ArgumentParser("vc")
parser.add_argument("input_file")

args = parser.parse_args()

content = ""
with open(args.input_file, "r") as f:
    content = f.read()


import logging
logging.basicConfig(level=logging.DEBUG)
from src.vccompiler import lexer

source = content
source = lexer.preprocess(source)

tokens = lexer.evaluate(source)
for token, evaluated, kind in tokens:
    print(f"Kind = {kind.value}, token = {repr(token)}, evaluated = {repr(evaluated)}")