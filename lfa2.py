import graphviz

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def is_deterministic(self):
        for state in self.states:
            for symbol in self.alphabet:
                if len(self.transitions.get((state, symbol), [])) > 1:
                    return False
        return True

    def to_regular_grammar(self):
        dfa = self.to_dfa()
        if not dfa.is_deterministic():
            raise ValueError("Cannot convert non-deterministic finite automaton to regular grammar")

        grammar = {}
        for state in dfa.states:
            for symbol in dfa.alphabet:
                next_state = dfa.transitions.get((state, symbol), '')
                if next_state:
                    grammar.setdefault(state, []).append(symbol + next_state)

        return grammar

    def to_dfa(self):
        if self.is_deterministic():
            return self

        dfa_states = set()
        dfa_transitions = {}
        dfa_final_states = set()

        def epsilon_closure(states):
            closure = set(states)
            for state in states:
                for next_state in self.transitions.get((state, ''), []):
                    if next_state not in closure:
                        closure.add(next_state)
                        closure.update(epsilon_closure([next_state]))
            return closure

        initial_state_closure = epsilon_closure([self.initial_state])
        dfa_states.add(tuple(sorted(initial_state_closure)))
        queue = [initial_state_closure]

        while queue:
            current_states = queue.pop(0)
            current_states_tuple = tuple(sorted(current_states))

            for symbol in self.alphabet:
                next_states = set()
                for state in current_states:
                    next_states.update(self.transitions.get((state, symbol), []))
                next_states_closure = epsilon_closure(next_states)
                next_states_closure_tuple = tuple(sorted(next_states_closure))

                if next_states_closure_tuple:
                    if next_states_closure_tuple not in dfa_states:
                        dfa_states.add(next_states_closure_tuple)
                        queue.append(next_states_closure)
                    dfa_transitions[(current_states_tuple, symbol)] = next_states_closure_tuple

        for state in dfa_states:
            if any(final_state in state for final_state in self.final_states):
                dfa_final_states.add(state)

        return FiniteAutomaton(dfa_states, self.alphabet, dfa_transitions, initial_state_closure, dfa_final_states)

    def draw_graph(self):
        dot = graphviz.Digraph()

        for state in self.states:
            state_label = ', '.join(state) if isinstance(state, tuple) else state
            if state in self.final_states:
                dot.node(state_label, shape='doublecircle')
            else:
                dot.node(state_label)

        for transition, next_states in self.transitions.items():
            current_states, symbol = transition
            current_states_label = ', '.join(current_states) if isinstance(current_states, tuple) else current_states
            for next_state in next_states:
                next_state_label = ', '.join(next_state) if isinstance(next_state, tuple) else next_state
                dot.edge(current_states_label, next_state_label, label=symbol)

        try:
            dot.render('finite_automaton_graph', format='png', cleanup=True)
            print("Finite automaton graph saved as finite_automaton_graph.png")
        except Exception as e:
            print("Error rendering graph:", e)

        return dot


def main():
    states = {'q0', 'q1', 'q2', 'q3'}
    alphabet = {'a', 'b', 'c'}
    transitions = {
        ('q0', 'a'): {'q0', 'q1'},
        ('q0', 'b'): {'q2'},
        ('q1', 'a'): {'q1'},
        ('q1', 'b'): {'q3'},
        ('q1', 'c'): {'q2'},
        ('q2', 'b'): {'q3'}
    }
    initial_state = 'q0'
    final_states = {'q3'}

    fa = FiniteAutomaton(states, alphabet, transitions, initial_state, final_states)

    if fa.is_deterministic():
        print("The finite automaton is deterministic.")
    else:
        print("The finite automaton is non-deterministic.")
        dfa = fa.to_dfa()
        print("Converted to DFA.")

    try:
        regular_grammar = fa.to_regular_grammar()
        print("Regular Grammar:")
        for state, productions in regular_grammar.items():
            for production in productions:
                print(f"{state} -> {production}")
    except ValueError as e:
        print(e)

    fa.draw_graph()

if __name__ == "__main__":
    main()
