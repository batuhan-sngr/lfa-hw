import re

# Define token types
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

# Combine the regular expressions into a single pattern
lexer_pattern = re.compile('|'.join('(?P<%s>%s)' % pair for pair in tokens))

# Tokenize input text
def lexer(input_text):
    for match in lexer_pattern.finditer(input_text):
        token_type = match.lastgroup
        token_value = match.group(token_type)
        if token_type == 'NUMBER':
            token_value = float(token_value)
        yield token_type, token_value

# Example usage
if __name__ == "__main__":
    input_text = '''
    def foo(x)
      extern bar(y)
      {
      return x + y * 2.0;
      }
    '''
    for token in lexer(input_text):
        print(token)
