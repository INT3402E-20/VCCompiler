# vccompiler

Efficient lexer & parser for VC language

## Install

```shell
$ git clone https://github.com/INT3402E-20/VCCompiler.git
$ python3 -m pip install .
```

In order to draw the parse tree, the following dependencies are required:
- [networkx](https://github.com/networkx/networkx) and [pydot](https://github.com/pydot/pydot)
```shell
$ python3 -m pip install networkx pydot
```
- [graphviz](https://www.graphviz.org/download/): follow the link for guided installation; also available in conda
```shell
$ conda install graphviz
```

## Usage

```shell
$ vclexer -h
usage: vclexer [-h] [-v] [-o OUTPUT] [-r RULE] input

positional arguments:
  input                 source file

options:
  -h, --help            show this help message and exit
  -v, --verbose         default: WARN; (-v): INFO; (-vv): DEBUG
  -o OUTPUT, --output OUTPUT
                        output file
  -r RULE, --rule RULE  rules file
```

```shell
$ vcparser -h
usage: vcparser [-h] [-v] [-o OUTPUT] [--tab TAB] [--eol EOL] [--draw PATH] [--disable-pruning] [--disable-left] input

positional arguments:
  input                 source file

options:
  -h, --help            show this help message and exit
  -v, --verbose         default: WARN; (-v): INFO; (-vv): DEBUG
  -o OUTPUT, --output OUTPUT
                        output file
  --tab TAB             tab character
  --eol EOL             end of line character
  --draw PATH           draw parse tree to dot file
  --disable-pruning     disable parse tree pruning
  --disable-left        disable left associative transformation
```

Use graphviz to convert dot files into your preferred format:
```shell
$ dot -Tsvg cst.dot -o cst.svg
```

## Structure

- `tokenize(source, dfa)`
  - Tokenize the input source using a given DFA (Deterministic Finite Automaton).

- class `DFA`
  - This class represents a Deterministic Finite Automaton (DFA).
  - method:
    - `search(content)`
      - Search for a valid token in the given string using the DFA.

- class `State`
  - This class represents a state in a Deterministic Finite Automaton (DFA).
  - method:
    - `add(pattern, state, skip_check=False)`
      - Add a transition from the current state to another state based on a pattern.
    - `default(state, skip_check=False)`
      - Set the default transition state when no specific transition is defined.
    - `copy(new_id=-1)`
      - Clone the current state with an optional new identifier.
    - `consume(ch)`
      - Determine the next state based on the input character.
    - `insert_keyword(keyword, index, hook)`
      - Insert a keyword into the DFA by creating transitions and updating hooks.
    - `is_end_state()`
      - Check if the current state is an end state (has an associated hook).

- `EndState(index, hook)`
  - Create an end state with the specified index and hook.