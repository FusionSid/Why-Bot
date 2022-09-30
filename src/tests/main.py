import ctypes

lib = ctypes.CDLL("e.so")
lib.run()

# `gcc -fPIC -shared`
