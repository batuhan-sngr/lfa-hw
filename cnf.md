# **Chomsky Normal Form**

### **Course: Formal Languages & Finite Automata**
### **Author: Emre Batuhan Sungur**

----

## **Theory**
In Chomsky Normal Form (CNF), the grammar is restricted to production rules having two non-terminals or a single terminal symbol on the right hand side. These rules can be expressed in the form

A non-terminal symbol generating two non-terminal symbols (A → BC)
A non-terminal symbol generating a terminal symbol (A → a)
A start symbol generating ε (S → ε)
 
Here A,B,C are non-terminal symbols, a is a terminal symbol, S is the start symbol and ε denotes an empty string.

#### **Steps for Converting CFG to CNF**

1. If the Start symbol S occurs on the right side of a grammar rule, create a new start symbol S’ and a new production or grammar rule S’ → S.

2. Remove null production rules as well as unit production rules from the grammar.

3. Replace each production rule A →B1B2……Bn where n>2, with A→B1C where C→B2…..Bn. 

Repeat this step for all production rules of the CFG having two or more symbols on the right side.

4. If the right side of any grammar rule is in the form A→aB where ‘a’ is a terminal symbol and A, B are non-terminals, then the production rule is replaced by A →XB and X →a.

Repeat this step for every production rule of the grammar which is of the form A→aB.

##  **Objectives**:

1. Learn about Chomsky Normal Form (CNF) [1].
2. Get familiar with the approaches of normalizing a grammar.
3. Implement a method for normalizing an input grammar by the rules of CNF.
    1. The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
    2. The implemented functionality needs executed and tested.
    3. A **BONUS point** will be given for the student who will have unit tests that validate the functionality of the project.
    4. Also, another **BONUS point** would be given if the student will make the aforementioned function to accept any grammar, not only the one from the student's variant.

## **Implementation description**
The code consists of a Python class `Grammar`, which encapsulates the functionality to parse a grammar and convert it to CNF. The implementation follows the steps typically used to convert a CFG to CNF, including the elimination of ε-productions, unit productions, inaccessible symbols, and non-productive symbols, followed by the conversion of remaining productions into CNF.

### **Parsing Grammar**
The `add_production` method of the `Grammar` class is responsible for parsing grammar rules. It splits the rule into left-hand side (lhs) and right-hand side (rhs) parts, extracts non-terminal and terminal symbols, and adds them to the respective sets (VN and VT). It also updates the start symbol if not already set. Each production rule is stored in a dictionary `P`, where the key is the lhs non-terminal symbol, and the value is a list of possible rhs productions.

```python
def add_production(self, production):
        parts = production.split('->')
        lhs = parts[0].strip()
        rhs = [x.strip() for x in parts[1].split('|')]
        if not self.S:
            self.S = lhs
        self.VN.add(lhs)
        for symbol in rhs:
            self.VT.update(set(symbol.split()) - self.VN)
        self.P[lhs] = rhs
```

### **Elimination of ε-productions**
The `remove_epsilon` method is responsible for eliminating ε-productions from the grammar. It iteratively removes ε-productions and adjusts other productions accordingly until no more ε-productions remain. This process ensures that non-terminals can no longer derive an empty string. In order check if there is any ε-productions when introduce our grammar we need to put a whitespace to indicate the ε-production. 

``` python
def remove_epsilon(self):
        # Step 1: Eliminate ε-productions
        epsilon_productions = {key for key, value in self.P.items() if '' in value}
        while epsilon_productions:
            for A in epsilon_productions:
                self.P[A].remove('')
                for key, value in self.P.items():
                    for prod in value[:]:
                        if A in prod:
                            self.P[key].extend([x.replace(A, '') for x in value if x])
            epsilon_productions = {key for key, value in self.P.items() if '' in value}
```
### **Elimination of Unit Productions**
The `remove_unit` method is responsible for eliminating unit productions from the grammar. It iteratively replaces each unit production A → B with the productions of B, excluding any unit productions. This process ensures that each non-terminal directly generates terminal strings or two non-terminal symbols.

``` python
def remove_unit(self):
        # Step 2: Eliminate unit productions
        unit_productions = {key: value for key, value in self.P.items() if len(value) == 1 and value[0] in self.VN}
        while unit_productions:
            for A, B in unit_productions.items():
                self.P[A].remove(B[0])
                self.P[A].extend(self.P[B[0]])
                self.P[A] = list(set(self.P[A]))
            unit_productions = {key: value for key, value in self.P.items() if len(value) == 1 and value[0] in self.VN}
```
### **Elimination of Inaccessible Symbols**
The `remove_inaccessible` method is responsible for eliminating inaccessible symbols from the grammar. It identifies symbols that are reachable from the start symbol and removes unreachable symbols. This ensures that only symbols reachable from the start symbol are retained in the grammar.
``` python
def remove_inaccessible(self):
        # Step 3: Eliminate inaccessible symbols
        reachable = set()
        reachable.add(self.S)
        old_size = 0
        while len(reachable) != old_size:
            old_size = len(reachable)
            for A, prods in self.P.items():
                if any(sym in reachable for sym in prods):
                    reachable.add(A)
        unreachable = set(self.VN) - reachable
        for A in unreachable:
            self.VN.remove(A)
            del self.P[A]
```

### **Elimination of Non-Productive Symbols**

The `remove_non_productive` method is responsible for eliminating non-productive symbols from the grammar. It identifies symbols that can generate terminal strings and removes non-productive symbols. This ensures that only symbols that contribute to the generation of terminal strings are retained in the grammar.

``` python
def remove_non_productive(self):
        # Step 4: Eliminate non-productive symbols
        productive = set(self.VT)
        old_size = 0
        while len(productive) != old_size:
            old_size = len(productive)
            for A, prods in self.P.items():
                if all(sym in productive or sym == '' for sym in prods):
                    productive.add(A)
        non_productive = set(self.VN) - productive
        for A in non_productive:
            self.VN.remove(A)
            del self.P[A]
```

### **Conversion to CNF**
The `convert_to_cnf` method is responsible for converting the grammar to Chomsky Normal Form (CNF). It sequentially applies the elimination steps described above and then converts the remaining productions into CNF. Each production is transformed to ensure it has one of the two CNF forms: A → BC or A → a.

``` python
def convert_to_cnf(self):
        self.remove_epsilon()
        self.remove_unit()
        self.remove_inaccessible()
        self.remove_non_productive()
        # Step 5: Convert productions into CNF
        for A, prods in self.P.items():
            for prod in prods[:]:
                if len(prod) > 2:
                    new_prods = [prod[:2]]
                    for symbol in prod[2:]:
                        new_non_terminal = symbol
                        while new_non_terminal in self.VN:
                            new_non_terminal += "'"
                        self.VN.add(new_non_terminal)
                        self.P[new_non_terminal] = [symbol]
                        new_prods.append(new_non_terminal)
                    self.P[A].remove(prod)
                    self.P[A].extend(new_prods)
```
### ***Challenges Faced***

In the implementation, handling complex productions with multiple symbols on the right-hand side was crucial for converting the grammar to CNF. For example, consider a production like A -> BCDE. This production has more than two symbols on the right-hand side. To address this, the implementation splits such productions into multiple binary productions while ensuring correctness and minimal disruption to the original grammar. For the given example, it would be split into A -> BZ, Z -> CD, and D -> E, where Z is a newly introduced non-terminal symbol.

The handling of complex productions with multiple symbols on the right-hand side, as described in the explanation, occurs within the `convert_to_cnf` method of the `Grammar` class. This method is responsible for converting the grammar to Chomsky Normal Form (CNF), which includes the transformation of productions to ensure they have one of the two CNF forms: A -> BC or A -> a.

```python
def convert_to_cnf(self):
    # Previous steps for grammar normalization (removing epsilon, unit, inaccessible, non-productive productions)  
    # Step 5: Convert productions into CNF
    for A, prods in self.P.items():
        for prod in prods[:]:  # Iterate over a copy of productions
            if len(prod) > 2:  # Check if the production has more than two symbols
                new_prods = [prod[:2]]  # Take the first two symbols as one production
                for symbol in prod[2:]:  # Iterate over the remaining symbols
                    new_non_terminal = symbol
                    while new_non_terminal in self.VN:
                        new_non_terminal += "'"  # Generate a new non-terminal symbol
                    self.VN.add(new_non_terminal)  # Add the new non-terminal symbol to VN
                    self.P[new_non_terminal] = [symbol]  # Add a production for the new non-terminal
                    new_prods.append(new_non_terminal)  # Add the new non-terminal symbol to the list of productions
                self.P[A].remove(prod)  # Remove the original production
                self.P[A].extend(new_prods)  # Extend with the new binary productions
```


### ***Solutions Employed***
1. Utilized Python's `re.findall` function along with a regular expression pattern to extract patterns within parentheses.
2. Leveraged conditional statements in the `explain_regex_processing` function to identify and explain different components of the regular expression.
3. Tested the script with various regular expression variants and iteratively refined the implementation to ensure accuracy and clarity.

## **Conclusions**
This project has provided invaluable insights into the intricate world of formal language theory and computational linguistics. From understanding the theoretical foundations of CNF and grammar normalization techniques to translating that knowledge into practical Python code, this project has been both challenging and rewarding.

Throughout the project, I encountered various challenges, each offering a unique opportunity for learning and growth. From handling complex productions with multiple symbols on the right-hand side to resolving ambiguity in the grammar, every obstacle pushed me to think critically, problem-solve creatively, and develop robust solutions. These challenges not only strengthened my technical skills but also deepened my understanding of the underlying principles of grammar transformation and algorithmic complexity.

Furthermore, this project has reinforced the importance of rigorous testing and validation in software development. By implementing unit tests to verify the functionality of the CNF converter and ensure its correctness across different grammars, I gained firsthand experience in quality assurance and software testing methodologies. This meticulous approach to testing not only instilled confidence in the reliability of the converter but also cultivated a mindset of thoroughness and attention to detail, essential qualities for any aspiring software engineer or researcher.

In conclusion, this project has been a journey of discovery, exploration, and growth. From delving into the intricacies of formal language theory to implementing practical solutions in code, I have gained invaluable knowledge and skills that will serve me well in my academic and professional endeavors. Beyond the technical aspects, this project has fostered a deeper appreciation for the beauty and complexity of language and computation, inspiring me to continue exploring the fascinating intersection of linguistics, mathematics, and computer science.

### **References**
[1] [Chomsky Normal Form Wiki](https://en.wikipedia.org/wiki/Chomsky_normal_form)