//
// Created by bestc on 26. 10. 15..
//
#include <iostream>
using namespace std;

int x;  // 전역 변수

void sub(void) {
    double x;
    x = 3.14;
    ::x = 500;
    cout << "x = " << x << endl;
    cout << "::x = " << ::x << endl;
}

int main(void) {
    cout << "2026-10-15, 24117000, 차민규\n";
    cout << "슬라이드34) C++언어의 영역 구멍과 영역지정 연산자\n" << endl;

    x = 20;
    cout << "x = " << x << endl;
    sub();  // 함수 추출

    return 0;
}
