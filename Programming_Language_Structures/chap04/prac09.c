//
// Created by bestc on 26. 10. 8..
//
#include <stdio.h>

int x = 1;

int f(int x) { return x * x; }

int main() {
    int y = 2;
    x = f(y);
    printf("%d %d\n", x, y);
    return 0;
}
