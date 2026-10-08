//
// Created by bestc on 26. 10. 8..
//
#include <stdio.h>

int main() {
    printf("2026-10-08, 24117000, 차민규\n");
    printf("(예제 2) 블록의 중첩\n");
    int x = 1; {
        int y = 0;
        y = x + 2;
        printf("x = %d, y = %d\n", x, y); // (1)
    }
    {
        int x = 5;
        x += 1;
        printf("x = %d\n", x); // (2)
    }
    x *= 2;
    printf("x = %d", x);    // (3)
}
