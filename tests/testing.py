import inspect


def test_function():
    """
    This is a test function for me to check for help

    Help Info:
    ----------

    CATEGORY: Utilities\n
    USAGE: /calculate\n\n

    """
    print("hi")


doc = test_function.__doc__.split("\n")
doc = [i.strip() for i in doc]

help_str = doc[1]
category, usage = None, None

for line in doc:
    if line.startswith("CATEGORY:"):
        category = line.replace("CATEGORY:", "").strip()
    elif line.startswith("USAGE:"):
        usage = line.replace("USAGE:", "").strip()


print(f"Help: {help_str}\nCategory: {category}\nUsage: {usage}")

first_line = test_function.__code__.co_firstlineno
function_length = len(
    inspect.getsource(test_function).replace("\\n", "").split("\n")[:-1]
)
lines_count = function_length + first_line
last_line = function_length + first_line - 1
print(f"{first_line}-{last_line}")
print(first_line, function_length, lines_count)
