//
// Created by bestc on 26. 10. 15..
//
#include <stdio.h>

int func(void) {
    static int count = 0;
    count++;
    return count;
}

int main(void) {
    printf("2026-10-15, 24117000, 차민규\n");
    printf("슬라이드 23) C언어와 static 변수\n");
    int i;
    for (i = 0; i < 10; i++)
        printf("%d ", func());
    return 0;
}
