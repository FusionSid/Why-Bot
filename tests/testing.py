def test_function():
    """
    This is a test function for me to check for help

    Help Info:
    ----------

    CATEGORY: Utilities
    USAGE: /calculate

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