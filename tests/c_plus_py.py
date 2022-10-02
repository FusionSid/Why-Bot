import ctypes

lib = ctypes.CDLL("e.so")
lib.run()

print(5 + 5)

# `gcc -fPIC -shared`
