# **Regular Grammars**

### **Course: Formal Languages & Finite Automata**
### **Author: Emre Batuhan Sungur**

----

## **Theory**
In formal language theory, a context-free grammar (CFG) is a set of production rules that define the syntax of a language. A finite automaton is a mathematical model of computation used to recognize patterns within strings. The relationship between CFGs and finite automata lies in their ability to describe the same set of languages, making them interchangeable in certain contexts.

##  Objectives:

1. Discover what a language is and what it needs to have in order to be considered a formal one;

2. Provide the initial setup for the evolving project that you will work on during this semester. You can deal with each laboratory work as a separate task or project to demonstrate your understanding of the given themes, but you also can deal with labs as stages of making your own big solution, your own project. Do the following:

    a. Create GitHub repository to deal with storing and updating your project;

    b. Choose a programming language. Pick one that will be easiest for dealing with your tasks, you need to learn how to solve the problem itself, not everything around the problem (like setting up the project, launching it correctly and etc.);

    c. Store reports separately in a way to make verification of your work simpler (duh)

3. According to your variant number, get the grammar definition and do the following:

    a. Implement a type/class for your grammar;

    b. Add one function that would generate 5 valid strings from the language expressed by your given grammar;

    c. Implement some functionality that would convert and object of type Grammar to one of type Finite Automaton;

    d. For the Finite Automaton, please add a method that checks if an input string can be obtained via the state transition from it;

## **Implementation description**

### **Grammar Class**
The `Grammar` class initializes with a set of non-terminal symbols (VN), terminal symbols (VT), and production rules (P). It also provides a method `generate_string()` to generate strings following the grammar rules. As well as `to_finite_automaton` to convert and object of type Grammar to one of type Finite Automaton. The function `classify_grammar()` in the Grammar class serves to categorize a given grammar based on the Chomsky hierarchy. It systematically examines the structure of productions to infer the grammar's type, providing valuable insights into its generative power and complexity.

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
        generated_string = ""
        current_symbol = 'S'

        while any(symbol in self.VN for symbol in current_symbol):
            for symbol in current_symbol:
                if symbol in self.VT:
                    generated_string += symbol
                else:
                    production = random.choice(self.P[symbol])
                    generated_string += production

            current_symbol = generated_string
            generated_string = ""  

        return current_symbol

    def classify_grammar(self):
        if all(len(p) == 2 for p_list in self.P.values() for p in p_list):
            return "Type 2: Context-Free Grammar"
        elif all(len(p) <= 2 for p_list in self.P.values() for p in p_list):
            return "Type 3: Regular Grammar"
        else:
            return "Other types of grammar (Not Type 3 or Type 2)"

    def to_finite_automaton(self):
        terminals = self.VT
        non_terminals = self.VN
        transitions = {}  
        start_state = 'S' 
        accept_states = {'FINAL'}  

        for variable, productions in self.P.items():
            for production in productions:
                source_state = variable
                if len(production) == 1 :
                    transitions.setdefault((source_state, production[0]), set()).add('FINAL')
                else:
                    t, nt = "", ""
                    for symbol in production:
                        if symbol in non_terminals:
                            nt = symbol
                        else:
                            t = symbol
                    transitions.setdefault((source_state, t), set()).add(nt)

        print("Finite Automaton:")
        print("Terminals:", terminals)
        print("Non-terminals:", non_terminals)
        print("Transitions:")
        for transition, next_state in transitions.items():
            print(f"  {transition[0]} --({transition[1]})-> {next_state}")
        print("Start State:", start_state)
        print("Accept States:", accept_states)

        return FiniteAutomaton(terminals, non_terminals, transitions, start_state, accept_states)
```
### **FiniteAutomaton Class**
The `FiniteAutomaton` class represents a finite automaton with its terminals, non-terminals, transitions, start state, and accept states. It provides a method `string_belongs_to_language()` to check if a given string belongs to the language accepted by the automaton.

``` python
class FiniteAutomaton:
    def __init__(self, terminals, non_terminals, transitions, start_state, accept_states):
        self.terminals = terminals 
        self.non_terminals = non_terminals  
        self.transitions = {} 
        for key, value in transitions.items():
            self.transitions[tuple(key)] = value
        self.start_state = start_state  
        self.accept_states = accept_states  

    def string_belongs_to_language(self, input_string):
        current_states = {self.start_state}
        def get_next_states(state, symbol, visited):
            visited.add(state)
            next_states = set()
            for s in self.transitions.get((state, symbol), []):
                if s not in visited:
                    next_states.add(s)
                    next_states |= get_next_states(s, symbol, visited)
            for s in self.transitions.get((state, ''), []):
                if s not in visited:
                    next_states |= get_next_states(s, symbol, visited)
            return next_states

        for symbol in input_string:
            next_states = set()
            for state in current_states:
                next_states |= get_next_states(state, symbol, set())
            current_states = next_states

        for state in current_states:
            if state in self.accept_states:
                return True
        return False
```
### **Main Class**
The `Main` class initializes a grammar instance, extracts terminals and non-terminals, builds transitions for the finite automaton, and executes by generating strings and checking their acceptance.

``` python
class Main:
    def __init__(self):
        self.grammar = Grammar()
        self.finite_automaton = self.grammar.to_finite_automaton()
        self.terminals = self.grammar.VT
        self.non_terminals = self.grammar.VN
        self.transitions = {}  # Initialize transitions based on grammar
        self.start_state = 'S'  # Set start state
        self.accept_states = {'S'}  # Set accept states
        self.build_transitions()

    def build_transitions(self):
        # Initialize transitions with empty transitions for all states
        for state in self.grammar.VN:
            self.transitions[(state, '')] = state
        # Build transitions based on grammar productions
        for variable in self.grammar.P:
            for production in self.grammar.P[variable]:
                source_state = variable
                target_state = production
                symbol = ''
                self.transitions[(source_state, symbol)] = target_state

    def execute(self):
        print("The 5 random strings that have been created by the grammar:")
        for _ in range(5):
            generated_string = self.grammar.generate_string()
            print(f'{generated_string}')
        fa = self.grammar.to_finite_automaton()
        print(fa.string_belongs_to_language("abaabb"))
        print(fa.string_belongs_to_language("a"))
        print("Grammar Classification:", self.grammar.classify_grammar())


if __name__ == "__main__":
    main = Main()
    main.execute()
```
## **Conclusions**
In this lab work, I've successfully implemented a Python program that generates strings based on context-free grammar rules and converts these grammars into finite automata. This project delves into the fundamental concepts of formal language theory, offering valuable insights into computational linguistics.

Through this implementation, I've gained a deeper understanding of how context-free grammars describe the syntax of languages, and how finite automata can recognize patterns within strings. By seamlessly transitioning between these two formalisms, I've demonstrated their interchangeability in capturing the same set of languages, showcasing their complementary roles in language theory. And by also employing the Chomsky hierarchy function, I can efficiently determine the type of grammar represented, aiding in linguistic analysis and understanding. It forms an essential component of grammar analysis tools and contributes to research in formal language theory.

Our exploration of context-free grammars and finite automata exemplifies the intricate relationship between language structures and computational models. By rigorously analyzing and implementing these concepts, we uncovered the underlying principles governing formal languages and computation.

Furthermore, this project highlighted the practical application of theoretical concepts in computational linguistics. Through hands-on implementation and examination, I've navigated through complex language structures, paving the way for a deeper understanding of language recognition and processing algorithms.

In conclusion, this lab work not only showcases our proficiency in implementing formal language theory concepts but also underscores our comprehensive grasp of the subject matter. By delving into the nuances of context-free grammars and finite automata, we have laid a solid foundation for further exploration and research in computational linguistics.

### **References**
* Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). Introduction to Automata Theory, Languages, and Computation. Pearson Education. https://www-2.dc.uba.ar/staff/becher/Hopcroft-Motwani-Ullman-2001.pdf

* Wikipedia contributors, "Context-free grammar," Wikipedia, The Free Encyclopedia, https://en.wikipedia.org/w/index.php?title=Context-free_grammar&oldid=1193952841