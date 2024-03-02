import matplotlib.pyplot as plt

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

def fa_to_regular_grammar(fa):
    # Regular grammar rules: A -> aB or A -> a
    regular_grammar = {}
    for state in fa.Q:
        regular_grammar[state] = []
        for transition, next_state in fa.delta.items():
            if transition[0] == state:
                symbol = transition[1]
                if next_state == state:
                    regular_grammar[state].append(symbol)
                else:
                    regular_grammar[state].append(symbol + next_state)
    return regular_grammar

def is_deterministic(fa):
    # Check if the FA is deterministic
    for state in fa.Q:
        transitions = [transition[1] for transition in fa.delta if transition[0] == state]
        if len(transitions) != len(set(transitions)):
            return False
    return True

def convert_ndfa_to_dfa(ndfa):
    dfa_states = set()
    dfa_delta = {}
    dfa_final_states = set()

    initial_state = frozenset({next_state for state in ndfa.Q if state == 'q0' for transition, next_state in ndfa.delta.items() if transition[0] == state})
    unmarked_states = {initial_state}
    
    while unmarked_states:
        current_dfa_state = unmarked_states.pop()
        dfa_states.add(current_dfa_state)
        
        for symbol in ndfa.sigma:
            next_states = {next_state for state in current_dfa_state for transition, next_state in ndfa.delta.items() if transition[0] == state and transition[1] == symbol}
            if next_states:
                next_dfa_state = frozenset(next_states)
                dfa_delta[(current_dfa_state, symbol)] = next_dfa_state
                if next_dfa_state not in dfa_states:
                    unmarked_states.add(next_dfa_state)
        
        for state in current_dfa_state:
            if state in ndfa.F:
                dfa_final_states.add(current_dfa_state)
                break

    dfa_sigma = ndfa.sigma
    dfa = Grammar(dfa_states, dfa_sigma, dfa_delta, dfa_final_states)
    return dfa

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
        self.grammar = Grammar({'q0', 'q1', 'q2', 'q3'}, {'a', 'b', 'c'}, {
            ('q0', 'a'): 'q0',
            ('q0', 'b'): 'q2',
            ('q1', 'a'): 'q1',
            ('q1', 'b'): 'q3',
            ('q1', 'c'): 'q2',
            ('q2', 'b'): 'q3'
        }, {'q3'})

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

        # Show plot
        plt.grid(True)
        plt.show()

    def run(self):
        classification = self.grammar.classify_chomsky_hierarchy()
        print("Classification:", classification)

        regular_grammar = fa_to_regular_grammar(self.grammar)
        print("Regular Grammar:", regular_grammar)

        is_dfa = is_deterministic(self.grammar)
        print("Is Deterministic FA:", is_dfa)

        dfa = convert_ndfa_to_dfa(self.grammar)
        print("DFA:", dfa.Q, dfa.sigma, dfa.delta, dfa.F)

        self.visualize_fa()

# Example Usage
if __name__ == "__main__":
    main = Main()
    main.run()