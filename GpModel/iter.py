import itertools

def find_combinations(numbers):
    # Generate all combinations of the numbers
    combinations = []
    for r in range(1, len(numbers) + 1):
        combinations.extend(itertools.combinations(numbers, r))
    return combinations

# Example usage:
numbers = [1, 5, 2, 3]
numbers = set(numbers)
all_combinations = find_combinations(numbers)

for combi in all_combinations:
    for val in combi:
        print(val)
print("All possible combinations:", all_combinations)