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

    def to_finite_automaton(self):
        # Implement conversion to Finite Automaton
        pass

class FiniteAutomaton:
    def __init__(self, terminals, non_terminals, transitions, start_state, accept_states):
        self.terminals = terminals  # Set of terminal symbols
        self.non_terminals = non_terminals  # Set of non-terminal symbols
        self.transitions = transitions  # Dictionary representing transitions: {(state, symbol): next_state}
        self.start_state = start_state  # Initial state
        self.accept_states = accept_states  # Set of accept states

    def string_belongs_to_language(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if (current_state, symbol) in self.transitions:
                current_state = self.transitions[(current_state, symbol)]
            else:
                return False
        return current_state in self.accept_states


class Main:
    def __init__(self):
        self.grammar = Grammar()
        self.terminals = self.grammar.VT
        self.non_terminals = self.grammar.VN
        self.transitions = {}  # Initialize transitions based on grammar
        self.start_state = 'S'  # Set start state
        self.accept_states = {'S'}  # Set accept states
        self.build_transitions()

    def build_transitions(self):
        for variable in self.grammar.P:
            for production in self.grammar.P[variable]:
                if len(production) == 2:  # Binary production rule
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
