#include <stdio.h>

int fib(n) {
    if (n <= 1) {
        return n;
    };
    return fib(n - 1) + fib(n - 2);
}

void run() {
    for (int i = 0; i < 42; i++)
    {
        int res = fib(i);
        printf("%i\n", res);
    }
}

