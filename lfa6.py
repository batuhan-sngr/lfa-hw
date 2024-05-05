import re

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

def lexer(input_text):
    for match in lexer_pattern.finditer(input_text):
        token_type = match.lastgroup
        token_value = match.group(token_type)
        if token_type == 'NUMBER':
            token_value = float(token_value)
        yield token_type, token_value

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

class FunctionNode:
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body

    def __str__(self):
        return f"Function: {self.name}, Args: {self.args}, Body: {self.body}"

if __name__ == "__main__":
    input_text = '''
    def foo(x, y)
      extern bar(y)
      {
      return x + y * 2.0;
      }
    '''
    tokens = list(lexer(input_text))
    ast = parse(tokens)
    for node in ast:
        print(node)
