import re

def _find_mathematical_expressions(query: str):
    options = []
    print(query)
    # Define a regular expression pattern to match mathematical expressions
    pattern = r"(?:\d+(\.\d+)?|\((?:\d+(\.\d+)?\s*([-+*/]\s*\d+(\.\d+)?)*?)\))\s*([-+*/]\s*(?:\d+(\.\d+)?|\((?:\d+(\.\d+)?\s*([-+*/]\s*\d+(\.\d+)?)*)\))\s*)*"

    # Find all matches of the pattern in the input string
    matches = re.findall(pattern, query)

    print(matches)

    # Extract the matched expressions and append them to the options list
    for match in matches:
        options.append(match[0])

    return options

strin = "2+2"
options = _find_mathematical_expressions(strin)
print(options)
