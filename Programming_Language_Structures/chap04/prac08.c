//
// Created by bestc on 26. 10. 15..
//
#include <stdio.h>

void swap(int a, int b) {
    int temp;

    temp = a;
    a = b;
    b = temp;
    printf("swap(): a = %d, b = %d\n", a, b);
}


int main() {
    printf("2026-10-15, 24117000, 차민규\n");
    printf("예제 8) 파스칼 프로그램을 C 언어로 변환\n");

    int x = 5, y = -3; // 변수의 선언과 초기화를 동시에 작업 가능
    swap(x, y); // 함수 호출 (매개 변수 전달-값)

    printf("main(): x = %d, y = %d\n", x, y); // (x = 5, y = -3), (x = -3, y = 5)
}
