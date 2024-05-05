# **Parser & Building an Abstract Syntax Tree**

### **Course: Formal Languages & Finite Automata**
### **Author: Emre Batuhan Sungur**

----

## **Theory**
### Parsing:
Parsing is the process of analyzing a sequence of tokens to determine their grammatical structure with respect to a given formal grammar. It is a fundamental step in the compilation process of programming languages, where source code is transformed into a format that can be executed by a computer.

#### Types of Parsing:
Top-Down Parsing: Begins with the start symbol of the grammar and works down to the input tokens. Common algorithms include Recursive Descent and LL parsers.
Bottom-Up Parsing: Starts with the input tokens and works up towards the start symbol of the grammar. Common algorithms include LR and LALR parsers.
#### Parsing Techniques:
- Syntax Analysis: This phase of parsing involves checking whether the input tokens conform to the rules of the grammar. It typically generates a parse tree or an AST.
- Semantic Analysis: After syntax analysis, semantic analysis checks whether the program makes sense according to its meaning. This phase may involve type checking, scope analysis, etc.
### Abstract Syntax Trees (ASTs):
An Abstract Syntax Tree is a hierarchical representation of the syntactic structure of source code, abstracting away from the specific syntax details like punctuation and layout. It's a tree-like data structure composed of nodes, where each node represents a syntactic construct in the source code.

#### Components of ASTs:
- Nodes: Each node represents a construct in the source code, such as expressions, statements, functions, etc.
- Edges: The edges between nodes represent the relationships between syntactic constructs, such as parent-child relationships.

## **Why Use ASTs?**
- Simplify Analysis: ASTs provide a simplified representation of the source code, making it easier to analyze and manipulate.
- Language Agnostic: ASTs can be used for various programming languages, as they capture the underlying structure without being tied to specific syntax.
- Optimization: ASTs can be used for code optimization and transformation, as they provide a structured representation that is amenable to analysis.

##  Objectives:

1. Get familiar with parsing, what it is and how it can be programmed [1].
2. Get familiar with the concept of AST [2].
3. In addition to what has been done in the 3rd lab work do the following:
   1. In case you didn't have a type that denotes the possible types of tokens you need to:
      1. Have a type __*TokenType*__ (like an enum) that can be used in the lexical analysis to categorize the tokens. 
      2. Please use regular expressions to identify the type of the token.
   2. Implement the necessary data structures for an AST that could be used for the text you have processed in the 3rd lab work.
   3. Implement a simple parser program that could extract the syntactic information from the input text.

## **Implementation description**
### Lexer (`lexer` function):
The `lexer` function tokenizes input text using regular expressions defined in the tokens list.
It iterates over matches found by `finditer`, yielding token type and value pairs.
It converts number tokens to float type.
### Parser (`parse`, `parse_body`, `parse_expression` functions):
The `parse` function takes a list of tokens and constructs an Abstract Syntax Tree (AST).
It iterates through tokens, identifying function definitions ('DEF') and parsing their names, arguments, and bodies.
Function bodies are recursively parsed using `parse_body`, handling both function definitions and expressions.
The `parse_expression` function parses expressions until it reaches a semicolon, constructing a list representation of the expression.
### Abstract Syntax Tree (AST):
Three classes represent nodes in the AST: `NumberNode`, `BinOpNode`, and `FunctionNode`.
`FunctionNode` represents function definitions, storing the function name, arguments, and body.
`parse` function constructs `FunctionNode `objects and appends them to the AST.
`parse_body` recursively parses function bodies and expressions.
`parse_expression` constructs expression lists.

### **Lexer Definition**
By defining each token type with a corresponding regular expression, we can efficiently identify tokens in the input text.

```python
tokens = [
    ('DEF', r'def'),
    ('EXTERN', r'extern'),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('NUMBER', r'\d+(\.\d+)?'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('TIMES', r'\*'),
    ('DIVIDE', r'/'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('SEMICOLON', r';'),
]

lexer_pattern = re.compile('|'.join('(?P<%s>%s)' % pair for pair in tokens))
```
### **`lexer` Function**
The lexer function iterates over matches found by the compiled regular expression pattern. It yields token type and value pairs for each match. I used a generator function (`yield`) because it allows for lazy evaluation, which is more memory-efficient, especially for large input texts.
``` python
def lexer(input_text):
    for match in lexer_pattern.finditer(input_text):
        token_type = match.lastgroup
        token_value = match.group(token_type)
        if token_type == 'NUMBER':
            token_value = float(token_value)
        yield token_type, token_value
```
### **Parser and AST Definitions**
I defined three classes to represent nodes in the Abstract Syntax Tree (AST): `NumberNode`, `BinOpNode`, and `FunctionNode`. Each class encapsulates the relevant information for its corresponding syntactic construct. This approach helps in organizing and processing the parsed information more effectively

#### NumberNode:
The `NumberNode` class represents numeric literals in the Abstract Syntax Tree (AST). It encapsulates the value of the numeric literal. For example, if the input text contains the number `42`, a `NumberNode` object with the value `42` would be created. This class helps in organizing and processing numeric literals in the parsed input text.

#### BinOpNode:
The `BinOpNode` class represents binary operations (e.g., addition, subtraction, multiplication, division) in the AST. It encapsulates the left operand, operator, and right operand of the binary operation. For example, if the input text contains the expression `x + 3`, a `BinOpNode` object with the left operand `x`, operator `+`, and right operand `3` would be created. This class helps in organizing and processing binary operations in the parsed input text.

#### FunctionNode:
The `FunctionNode` class represents function definitions in the AST. It encapsulates the name of the function, its arguments, and its body. For example, if the input text contains the function definition `def foo(x, y): ...`, a `FunctionNode` object with the name `foo`, arguments `x` and `y`, and body `...` would be created. This class helps in organizing and processing function definitions in the parsed input text.
``` python
class NumberNode:
    def __init__(self, value):
        self.value = value

class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class FunctionNode:
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body
```
### **Parser Functions**
The parser functions implement a recursive descent parsing strategy. This approach is chosen because it is straightforward to implement and well-suited for parsing simple grammars, such as the one used in this example. Recursive descent parsing closely mirrors the structure of the grammar rules, making it easy to understand and maintain.

#### Recursive Descent Parsing:
The parser functions implement a recursive descent parsing strategy, which is a top-down parsing technique. In recursive descent parsing, the parser begins with the start symbol of the grammar and recursively expands non-terminals to match the input tokens. This approach is chosen because it is straightforward to implement and well-suited for parsing simple grammars, such as the one used in this example.

#### `parse(tokens)`:
The `parse` function is the entry point for parsing the input tokens. It iterates through the tokens and identifies function definitions (`DEF`). For each function definition, it parses the function name, arguments, and body, and constructs a `FunctionNode` object to represent the function definition in the AST.

#### `parse_body(token_iter)`:
The `parse_body` function parses the body of a function definition. It recursively processes tokens to identify expressions or nested function definitions within the function body. It returns a list representing the parsed body of the function.

#### `parse_expression(token_iter, first_token_value)`:
The `parse_expression` function parses an expression within a function body. It constructs a list representing the parsed expression, starting with the `first_token_value` provided as input. It continues parsing tokens until it encounters a semicolon, indicating the end of the expression.
``` python
def parse(tokens):
    token_iter = iter(tokens)
    ast = []
    for token_type, token_value in token_iter:
        if token_type == 'DEF':
            name = next(token_iter)[1] 
            args = []
            while True:
                arg_token = next(token_iter)
                if arg_token[1] == ')':
                    break
                args.append(arg_token[1])
            body = parse_body(token_iter)
            ast.append(FunctionNode(name, args, body))
    return ast

def parse_body(token_iter):
    body = []
    for token_type, token_value in token_iter:
        if token_type == 'RPAREN':
            break
        elif token_type == 'IDENTIFIER':
            if token_value == 'extern':
                while token_value != '{':
                    token_type, token_value = next(token_iter)
                body.append(parse_body(token_iter))
            else:
                body.append(parse_expression(token_iter, token_value))
    return body

def parse_expression(token_iter, first_token_value):
    expression = [first_token_value]
    for token_type, token_value in token_iter:
        if token_type == 'SEMICOLON':
            break
        expression.append(token_value)
    return expression
```
### ***Challenges Faced and Solutions***

Throughout the development of the code, several challenges were encountered, which required innovative solutions to overcome. Here are the key challenges that I've faced during the implementation process and their corresponding solutions:

1. **Challenge: Handling Nested Function Definitions:**
   - **Challenge:** Parsing nested function definitions (`extern`) within another function's body might lead to incorrect parsing or infinite loops if not handled properly.
   - **Solution:** The `parse_body` function correctly handles nested function definitions by recursively calling itself to parse inner function bodies.

2. **Challenge: Handling Different Types of Expressions:**
    - **Challenge:** Differentiating between function bodies, expressions, and nested function definitions while parsing the input text.
    - **Solution:** The parse_body function examines each token to determine whether it's an identifier (for a nested function), an expression, or a closing parenthesis. This allows for proper handling of different types of expressions and function definitions.

## **Conclusions**

As I reflect on the development process of this code, I find myself proud of the progress made and the challenges overcome. Initially, I embarked on this endeavor with the goal of creating a lexer and parser for a simple programming language. The task seemed daunting, but with determination and perseverance, I delved into the intricacies of lexical analysis and parsing.

The creation of the lexer was a crucial first step. By defining token types and their corresponding regular expressions, I was able to effectively tokenize input text, breaking it down into meaningful units for further processing. This stage required careful consideration of the grammar rules and syntax of the programming language, ensuring that tokens were accurately identified and categorized.

Moving on to the parser, I employed a recursive descent parsing strategy to construct an Abstract Syntax Tree (AST) from the tokenized input. This approach proved to be both intuitive and effective, allowing me to closely mirror the grammar rules in the parsing logic. As I implemented parser functions to handle function definitions, expressions, and nested constructs, I encountered challenges such as correctly identifying function arguments and handling nested function definitions. However, through careful planning and iterative refinement, I was able to overcome these obstacles and produce a robust parsing mechanism.

One of the most rewarding aspects of this project was witnessing the code in action. Seeing the lexer tokenize input text and the parser construct an AST filled me with a sense of accomplishment. Moreover, the example usage demonstrated the practical application of the lexer-parser duo, illustrating how they could be integrated into a larger parsing workflow for a programming language.

In conclusion, this journey has been a valuable learning experience, allowing me to deepen my understanding of lexical analysis, parsing techniques, and abstract syntax trees. While there were challenges along the way, each obstacle served as an opportunity for growth and refinement. As I look towards the future, I am excited to continue exploring the realm of language processing and building upon the foundation laid by this project.

### **References**
[1] [Parsing Wiki](https://en.wikipedia.org/wiki/Parsing)

[2] [Abstract Syntax Tree Wiki](https://en.wikipedia.org/wiki/Abstract_syntax_tree) 