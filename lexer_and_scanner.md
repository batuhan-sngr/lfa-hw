# **Lexer And Scanner**

### **Course: Formal Languages & Finite Automata**
### **Author: Emre Batuhan Sungur**

----

## **Theory**
In programming language theory and implementation, a lexer (lexical analyzer) serves as the first step in processing a text-based input file by breaking it down into tokens. Tokens represent the smallest units of meaning in a programming language, such as keywords, identifiers, numbers, and operators.

##  Objectives:

1. Understand what lexical analysis [1] is.
2. Get familiar with the inner workings of a lexer/scanner/tokenizer.
3. Implement a sample lexer and show how it works.

## **Implementation description**

### **Token Definition**
In the implementation, we define several token types using tuples. Each tuple contains a token name and its corresponding regular expression pattern. For example:

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
```
Each token type corresponds to a particular element of the programming language's syntax, such as keywords, identifiers, numbers, and operators.

### **Regular Expression Compilation**
The regular expressions defined for each token type are combined into a single pattern using the join function. This pattern is then compiled into a regular expression object using the `re.compile()` function. For example:

``` python
import re

lexer_pattern = re.compile('|'.join('(?P<%s>%s)' % pair for pair in tokens))
```

This compiled regular expression pattern is used by the lexer to match tokens in the input text.

### **Tokenization**
The `lexer()` function is responsible for tokenizing the input text. It iterates over matches of the compiled regular expression pattern in the input text and yields tuples containing the token type and its corresponding value. For example:

``` python
def lexer(input_text):
    for match in lexer_pattern.finditer(input_text):
        token_type = match.lastgroup
        token_value = match.group(token_type)
        if token_type == 'NUMBER':
            token_value = float(token_value)
        yield token_type, token_value
```

Inside the loop, `match.lastgroup` retrieves the name of the matched token type, and `match.group(token_type)` retrieves the corresponding value. Numeric values are converted to floats.

### **Example Usage**
The lexer function can be called with input text to tokenize it. For example:

``` python
input_text = '''
def foo(x)
  extern bar(y)
  {
  return x + y * 2.0;
  }
'''
for token in lexer(input_text):
    print(token)

```
# **Output**
``` terminal
('DEF', 'def')
('IDENTIFIER', 'foo')
('LPAREN', '(')
('IDENTIFIER', 'x')
('RPAREN', ')')
('EXTERN', 'extern')
('IDENTIFIER', 'bar')
('LPAREN', '(')
('IDENTIFIER', 'y')
('RPAREN', ')')
('IDENTIFIER', 'return')
('IDENTIFIER', 'x')
('PLUS', '+')
('IDENTIFIER', 'y')
('TIMES', '*')
('NUMBER', 2.0)
('SEMICOLON', ';')
```

## **Conclusions**
In conclusion, the implementation of the lexer offers a good foundation for processing text-based input in a programming language. By breaking down down the implementation into token definition, regular expression compilation, tokenization, and example usage, we obtain a thorough grasp of how the lexer operates.

The theoretical analysis of lexer implementation highlights essential concepts such as token enumeration, whitespace management, and error handling, all of which are required to efficiently process input text. These ideas are converted into real code in the Python implementation, which demonstrates how token types are defined, regular expressions are compiled, and input text is tokenized.

Overall, the lexer is an important component in language processing, establishing the framework for later phases such as parsing and interpretation. With a combination of theoretical understanding

### **References**

[1] [A sample of a lexer implementation](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html)

[2] [Lexical analysis](https://en.wikipedia.org/wiki/Lexical_analysis)