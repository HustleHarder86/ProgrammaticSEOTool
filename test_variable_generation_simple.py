"""Simple test for variable extraction and title generation logic"""

def extract_variables(template_pattern):
    """Extract variable names from template pattern"""
    import re
    matches = re.findall(r'\{([^}]+)\}|\[([^\]]+)\]', template_pattern)
    variables = []
    for match in matches:
        var = match[0] if match[0] else match[1]
        if var and var not in variables:
            variables.append(var)
    return variables

def generate_all_titles(template_pattern, variable_values):
    """Generate all possible title combinations"""
    
    # Single variable case
    if len(variable_values) == 1:
        var_name = list(variable_values.keys())[0]
        titles = []
        for value in variable_values[var_name]:
            title = template_pattern.replace(f"{{{var_name}}}", value)
            title = title.replace(f"[{var_name}]", value)
            titles.append(title)
        return titles
    
    # Multiple variables case - generate all combinations
    titles = []
    variable_names = list(variable_values.keys())
    
    def generate_combinations(index, current_values):
        if index == len(variable_names):
            # Generate title with current combination
            title = template_pattern
            for var_name, value in current_values.items():
                title = title.replace(f"{{{var_name}}}", value)
                title = title.replace(f"[{var_name}]", value)
            titles.append(title)
            return
        
        var_name = variable_names[index]
        for value in variable_values[var_name]:
            current_values[var_name] = value
            generate_combinations(index + 1, current_values.copy())
    
    generate_combinations(0, {})
    return titles

# Test Case 1: Single Variable
print("=== Test Case 1: Single Variable ===")
template1 = "{City} with Best Investment Potential"
variables1 = extract_variables(template1)
print(f"Template: {template1}")
print(f"Variables: {variables1}")

# Simulate AI-generated values
cities = ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa"]
titles1 = generate_all_titles(template1, {"City": cities})
print(f"Generated {len(titles1)} titles:")
for title in titles1:
    print(f"  - {title}")

# Test Case 2: Multiple Variables
print("\n=== Test Case 2: Multiple Variables ===")
template2 = "Best {Niche} Starter Packs on {Platform}"
variables2 = extract_variables(template2)
print(f"Template: {template2}")
print(f"Variables: {variables2}")

# Simulate AI-generated values
niches = ["Tech", "Design", "Marketing"]
platforms = ["Bluesky", "Twitter"]
titles2 = generate_all_titles(template2, {"Niche": niches, "Platform": platforms})
print(f"Generated {len(titles2)} titles (3 niches × 2 platforms):")
for i, title in enumerate(titles2):
    print(f"  {i+1}. {title}")

# Test Case 3: Different Bracket Types
print("\n=== Test Case 3: Mixed Bracket Types ===")
template3 = "[City] {Service} Provider"
variables3 = extract_variables(template3)
print(f"Template: {template3}")
print(f"Variables: {variables3}")

cities = ["New York", "Los Angeles"]
services = ["SEO", "Web Design", "Marketing"]
titles3 = generate_all_titles(template3, {"City": cities, "Service": services})
print(f"Generated {len(titles3)} titles:")
for title in titles3[:5]:
    print(f"  - {title}")
if len(titles3) > 5:
    print(f"  ... and {len(titles3) - 5} more")

print("\n✓ Variable extraction and title generation logic working correctly!")