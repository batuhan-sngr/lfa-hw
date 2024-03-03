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
