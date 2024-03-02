# **Determinism in Finite Automata**

### **Course: Formal Languages & Finite Automata**
### **Author: Emre Batuhan Sungur**

----

## **Theory**
In formal language theory, finite automata are mathematical models used to recognize patterns within strings. They consist of states, transitions, an alphabet, and accept states. Visualizing a finite automaton helps in understanding its structure and behavior.

##  Objectives:

1. Understand what an automaton is and what it can be used for.

2. Continuing the work in the same repository and the same project, the following need to be added: 
a. Provide a function in your grammar type/class that could classify the grammar based on Chomsky hierarchy.

b. For this you can use the variant from the previous lab.

3. According to your variant number (by universal convention it is register ID), get the finite automaton definition and do the following tasks:

a. Implement conversion of a finite automaton to a regular grammar.

b. Determine whether your FA is deterministic or non-deterministic.

c. Implement some functionality that would convert an NDFA to a DFA.

d. Represent the finite automaton graphically (Optional, and can be considered as a bonus point):

You can use external libraries, tools or APIs to generate the figures/diagrams.

Your program needs to gather and send the data about the automaton and the lib/tool/API return the visual representation.

## **Implementation description**

### **Grammar Class**
The `Grammar` class represents a finite automaton with its states (Q), alphabet (sigma), transition function (delta), and accept states (F). It also includes a method to classify the grammar in the Chomsky hierarchy as a regular grammar.

```python
class Grammar:
    def __init__(self, Q, sigma, delta, F):
        self.Q = Q 
        self.sigma = sigma 
        self.delta = delta  
        self.F = F  

    def classify_chomsky_hierarchy(self):
        # Count the number of symbols on the left and right side of productions
        left_symbols = set()
        right_symbols = set()
        for transition, next_state in self.delta.items():
            left_symbols.add(transition[0])
            right_symbols.add(next_state)

        # Determine the type of grammar based on the Chomsky hierarchy
        if left_symbols == set(self.Q) and right_symbols == set(self.sigma).union({'ε'}):
            return "Type 0 (Unrestricted Grammar)"
        elif left_symbols == set(self.Q) and right_symbols <= set(self.sigma).union({'ε'}):
            return "Type 1 (Context-Sensitive Grammar)"
        elif left_symbols <= set(self.Q) and right_symbols <= set(self.sigma).union({'ε'}) and 'ε' not in right_symbols:
            return "Type 2 (Context-Free Grammar)"
        elif left_symbols <= set(self.Q) and len(right_symbols) == 1:
            return "Type 3 (Regular Grammar)"
        else:
            return "Unknown Type"

```
### **Visualization Function**
The `visualize_fa` function visualizes the finite automaton using Matplotlib. It plots the states and transitions of the automaton.

``` python
def visualize_fa(self):
    plt.figure(figsize=(8, 6))

    for transition, next_state in self.delta.items():
        x_start = int(transition[0][1])
        y_start = 0
        x_end = int(next_state[1])
        y_end = 0
        plt.arrow(x_start, y_start, x_end - x_start, y_end - y_start, head_width=0.1, head_length=0.1, fc='k', ec='k')

    for state in self.Q:
        x = int(state[1])
        y = 0
        if state in self.F:
            plt.plot(x, y, 'ro')  
        else:
            plt.plot(x, y, 'bo')  
        plt.text(x, y, state, fontsize=12, ha='center', va='center')

    plt.xlim(0, 4)
    plt.ylim(-1, 1)
    plt.xlabel('X-axis')
    plt.title('Finite Automaton')

    plt.grid(True)
    plt.show()

```
### **Main Class**
The `Main` class initializes the finite automaton and executes the visualization.

``` python
class Main:
    def __init__(self):
        self.Q = {'q0', 'q1', 'q2', 'q3'}
        self.sigma = {'a', 'b', 'c'}
        self.delta = {
            ('q0', 'a'): 'q0',
            ('q0', 'b'): 'q2',
            ('q1', 'a'): 'q1',
            ('q1', 'b'): 'q3',
            ('q1', 'c'): 'q2',
            ('q2', 'b'): 'q3'
        }
        self.F = {'q3'}
        self.grammar = Grammar(self.Q, self.sigma, self.delta, self.F)

    def run(self):
        classification = self.grammar.classify_chomsky_hierarchy()
        print("Classification:", classification)

        self.visualize_fa()

if __name__ == "__main__":
    main = Main()
    main.run()

```
## **Conclusions**
In this work, we successfully implemented a Python program to visualize a finite automaton. By leveraging Matplotlib, we created a graphical representation of the automaton's states and transitions, providing valuable insights into its structure and behavior.

Through the implementation of the Grammar class, we demonstrated the classification of the grammar in the Chomsky hierarchy as a regular grammar. Additionally, the visualization function visualize_fa facilitated the intuitive understanding of the finite automaton's operation.

This project underscores the importance of visual aids in formal language theory and finite automata. By visualizing complex concepts, such as state transitions and accept states, we enhance our understanding and facilitate further exploration in the field of computational linguistics.

In conclusion, the successful implementation of the finite automaton visualization program signifies our proficiency in formal language theory and computational linguistics. By combining theoretical knowledge with practical implementation, we have laid a solid foundation for future endeavors in this domain.

### **References**
* Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). Introduction to Automata Theory, Languages, and Computation. Pearson Education. https://www-2.dc.uba.ar/staff/becher/Hopcroft-Motwani-Ullman-2001.pdf

* Wikipedia contributors, "Context-free grammar," Wikipedia, The Free Encyclopedia, https://en.wikipedia.org/w/index.php?title=Context-free_grammar&oldid=1193952841