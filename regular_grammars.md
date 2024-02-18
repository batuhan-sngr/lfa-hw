# **Generating Strings with Context-Free Grammars and Converting to Finite Automata**

### **Course: Formal Languages & Finite Automata**
### **Author: Emre Batuhan Sungur**

----

## **Theory**
In formal language theory, a context-free grammar (CFG) is a set of production rules that define the syntax of a language. A finite automaton is a mathematical model of computation used to recognize patterns within strings. The relationship between CFGs and finite automata lies in their ability to describe the same set of languages, making them interchangeable in certain contexts.

## **Objectives:**
* **Implement a Python class representing a context-free grammar.**
* **Develop a method to generate strings based on the grammar rules.**
* **Convert the generated grammar into a finite automaton.**

## **Implementation description**

### **Grammar Class**
The `Grammar` class initializes with a set of non-terminal symbols (VN), terminal symbols (VT), and production rules (P). It also provides a method `generate_string()` to generate strings following the grammar rules.

```python
class Grammar:
    def __init__(self):
        self.VN = {'S', 'A', 'B', 'C'}
        self.VT = {'a', 'b'}
        self.P = {
            'S': ['aA'],
            'A': ['bS', 'aB'],
            'B': ['bC', 'aB'],
            'C': ['aA', 'b']
        }

    def generate_string(self):
        import random
        max_length = 10  # Maximum length of generated string to avoid infinite loop
        string = ''
        current_symbol = 'S'
        while len(string) < max_length:
            if current_symbol in self.VT:
                string += current_symbol
                break
            else:
                production = random.choice(self.P[current_symbol])
                for symbol in production:
                    if symbol in self.VT:
                        string += symbol
                    else:
                        current_symbol = symbol
        return string
```
### **FiniteAutomaton Class**
The FiniteAutomaton class represents a finite automaton with its terminals, non-terminals, transitions, start state, and accept states. It provides a method string_belongs_to_language() to check if a given string belongs to the language accepted by the automaton.

``` python
Copy code
class FiniteAutomaton:
    def __init__(self, terminals, non_terminals, transitions, start_state, accept_states):
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def string_belongs_to_language(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if (current_state, symbol) in self.transitions:
                current_state = self.transitions[(current_state, symbol)]
            else:
                return False
        return current_state in self.accept_states
```
### **Main Class**
The Main class initializes a grammar instance, extracts terminals and non-terminals, builds transitions for the finite automaton, and executes by generating strings and checking their acceptance.

``` python
Copy code
class Main:
    def __init__(self):
        self.grammar = Grammar()
        self.terminals = self.grammar.VT
        self.non_terminals = self.grammar.VN
        self.transitions = {}  
        self.start_state = 'S'  
        self.accept_states = {'S'}  
        self.build_transitions()

    def build_transitions(self):
        for variable in self.grammar.P:
            for production in self.grammar.P[variable]:
                if len(production) == 2:  
                    source_state = variable
                    target_state = production[1]
                    symbol = production[0]
                    self.transitions[(source_state, symbol)] = target_state

    def execute(self):
        finite_automaton = FiniteAutomaton(self.terminals, self.non_terminals, self.transitions, self.start_state, self.accept_states)
        for _ in range(5):
            generated_string = self.grammar.generate_string()
            print("Generated String:", generated_string)
            print("Belongs to Language:", finite_automaton.string_belongs_to_language(generated_string))
            print()


if __name__ == "__main__":
    main = Main()
    main.execute()
```
## **Conclusions**
The implemented code demonstrates the generation of strings based on context-free grammar rules and the conversion of these grammars into finite automata. This approach allows for the exploration of language recognition within a computational framework.

### **References**
Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). Introduction to Automata Theory, Languages, and Computation. Pearson Education. https://www-2.dc.uba.ar/staff/becher/Hopcroft-Motwani-Ullman-2001.pdf
Wikipedia contributors, "Context-free grammar," Wikipedia, The Free Encyclopedia, https://en.wikipedia.org/w/index.php?title=Context-free_grammar&oldid=1193952841