import inspect


def test_function():
    """
    This is a test function for me to check for help
    eeee
    eeeeee

    Help Info:
    ----------

    CATEGORY: Utilities

    USAGE: /calculate

    """
    print("hi")


doc = test_function.__doc__.split("\n")
doc = [i.strip() for i in doc]

help_str = doc[1]
for i in doc:
    if i.startswith("Help Info:"):
        break
    help_str += f" {i}"
category, usage = None, None

for line in doc:
    if line.startswith("Category:"):
        category = line.replace("Category:", "", 1).strip()
    elif line.startswith("Usage:"):
        usage = line.replace("Usage:", "", 1).strip()


print(f"Help: {help_str}\nCategory: {category}\nUsage: {usage}")

first_line = test_function.__code__.co_firstlineno
function_length = len(
    inspect.getsource(test_function).replace("\\n", "").split("\n")[:-1]
)
lines_count = function_length + first_line
last_line = function_length + first_line - 1
print(f"{first_line}-{last_line}")
print(first_line, function_length, lines_count)


"""


Help Info:
----------
Category: 

Usage: 
"""