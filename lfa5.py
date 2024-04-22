class Grammar:
    def __init__(self):
        self.VN = set()  
        self.VT = set()  
        self.P = {}      
        self.S = ''      

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

    def remove_unit(self):
        # Step 2: Eliminate unit productions
        unit_productions = {key: value for key, value in self.P.items() if len(value) == 1 and value[0] in self.VN}
        while unit_productions:
            for A, B in unit_productions.items():
                self.P[A].remove(B[0])
                self.P[A].extend(self.P[B[0]])
                self.P[A] = list(set(self.P[A]))
            unit_productions = {key: value for key, value in self.P.items() if len(value) == 1 and value[0] in self.VN}

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

    def print_grammar(self):
        print("VN:", self.VN)
        print("VT:", self.VT)
        print("P:")
        for key, value in self.P.items():
            for prod in value:
                print(key, "->", prod)
        print("S:", self.S)

# Define the grammar string
grammar_str = """
S -> aB | bA
A -> B | b | aD | AS | bAAB | 
B -> b | bS
C -> AB
D -> BB
"""
grammar = Grammar()

productions = grammar_str.strip().split('\n')
for prod in productions:
    grammar.add_production(prod)

grammar.convert_to_cnf()

grammar.print_grammar()
