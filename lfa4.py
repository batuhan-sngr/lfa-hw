import re
import itertools
import random

def generate_combinations(regex):
    patterns = re.findall(r'\((.*?)\)', regex)  # Extract patterns within parentheses
    combinations = []
    chosen_options = []

    while len(combinations) < 4:  # Ensure at least 4 combinations are generated
        combinations.clear()
        chosen_options.clear()

        for pattern in patterns:
            options = pattern.split('|')
            chosen_option = random.choice(options)  # Choose a random option in each group
            chosen_options.append(chosen_option)
            combinations.append([chosen_option])

    valid_combinations = list(itertools.product(*combinations))
    return [''.join(combo) for combo in valid_combinations], chosen_options

def explain_regex_processing(regex, chosen_options):
    components = regex.split(' ')
    explanation = []

    for component, chosen_option in zip(components, chosen_options):
        if component.startswith('(') and component.endswith(')'):
            options = component[1:-1].split('|')
            explanation.append(f"I choose '{chosen_option}' from options: {options}")
        elif component.endswith('*'):
            explanation.append(f"Match zero to five occurrences of: {chosen_option}")
        elif component.endswith('?'):
            explanation.append(f"Match zero or one occurrence of: {chosen_option}")
        elif component.endswith('^+'):
            explanation.append(f"Match one or more occurrences of: {chosen_option}")
        elif component.startswith('^') and component.endswith('+'):
            explanation.append(f"Match exactly 5 occurrences of: {chosen_option}")
        else:
            explanation.append(f"Match: {component}")

    return explanation

# Variant 1
variant1_regex = "(a|b)(c|d)E*G? p(Q|R|S)T(uv|w|x)*Z^+ 1(0|1)*2(3|4)^5 36"
variant1_combinations, chosen_options = generate_combinations(variant1_regex)
variant1_processing_sequence = explain_regex_processing(variant1_regex, chosen_options)

print("Variant 1:")
print("Generated Combinations:", variant1_combinations)
print("Processing Sequence:")
for step, explanation in enumerate(variant1_processing_sequence, 1):
    print(f"Step {step}: {explanation}")
