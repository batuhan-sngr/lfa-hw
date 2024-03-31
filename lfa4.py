import re
import itertools

def generate_combinations(regex):
    patterns = re.findall(r'\((.*?)\)', regex)  # Extract patterns within parentheses
    combinations = []

    for pattern in patterns:
        options = pattern.split('|')
        combinations.append(options)

    valid_combinations = list(itertools.product(*combinations))
    return [''.join(combo) for combo in valid_combinations]

def explain_regex_processing(regex):
    # Split the regular expression into components
    components = regex.split(' ')

    explanation = []
    for component in components:
        if component.startswith('(') and component.endswith(')'):
            explanation.append(f"Match one of: {component[1:-1].split('|')}")
        elif component.endswith('*'):
            explanation.append(f"Match zero or more occurrences of: {component[:-1]}")
        elif component.endswith('?'):
            explanation.append(f"Match zero or one occurrence of: {component[:-1]}")
        elif component.endswith('^+'):
            explanation.append(f"Match one or more occurrences of: {component[:-2]}")
        elif component.startswith('^') and component.endswith('+'):
            explanation.append(f"Match exactly 5 occurrences of: {component[1:-2]}")
        else:
            explanation.append(f"Match: {component}")

    return explanation

# Variant 1
variant1_regex = "(a|b)(c|d)E*G? p(Q|R|S)T(uv|w|x)*Z^+ 1(0|1)*2(3|4)^5 36"
variant1_combinations = generate_combinations(variant1_regex)
variant1_processing_sequence = explain_regex_processing(variant1_regex)

print("Variant 1:")
print("Generated Combinations:", variant1_combinations)
print("Processing Sequence:")
for step, explanation in enumerate(variant1_processing_sequence, 1):
    print(f"Step {step}: {explanation}")
print()

# Variant 2
variant2_regex = "M?N^2 (O|P)^3 Q^* R^+ (X|Y|Z)^3 8^+ (9|0) (H|I) (J|K) L*N?"
variant2_combinations = generate_combinations(variant2_regex)
variant2_processing_sequence = explain_regex_processing(variant2_regex)

print("Variant 2:")
print("Generated Combinations:", variant2_combinations)
print("Processing Sequence:")
for step, explanation in enumerate(variant2_processing_sequence, 1):
    print(f"Step {step}: {explanation}")
print()

# Variant 3
variant3_regex = "O(P|Q|R)^+ 2(3|4) A*B(C|D|E) F(G|H|I)^2 J^+ K(L|M|N)*O? (P|Q)^3"
variant3_combinations = generate_combinations(variant3_regex)
variant3_processing_sequence = explain_regex_processing(variant3_regex)

print("Variant 3:")
print("Generated Combinations:", variant3_combinations)
print("Processing Sequence:")
for step, explanation in enumerate(variant3_processing_sequence, 1):
    print(f"Step {step}: {explanation}")
print()

# Variant 4
variant4_regex = "(S|T) (U|V) w*y^+ 24 L(M|N)O^3 P*Q (2|3) R*S(T|U|V) W(X|Y|Z)^2"
variant4_combinations = generate_combinations(variant4_regex)
variant4_processing_sequence = explain_regex_processing(variant4_regex)

print("Variant 4:")
print("Generated Combinations:", variant4_combinations)
print("Processing Sequence:")
for step, explanation in enumerate(variant4_processing_sequence, 1):
    print(f"Step {step}: {explanation}")
print()
