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
from src.vccompiler.lexical.parser import preprocess

print(preprocess(content).encode())
