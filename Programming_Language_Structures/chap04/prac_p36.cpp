//
// Created by bestc on 26. 10. 15..
//
#include <iostream>
#define PI 3.14159

using namespace std;

int main() {
    float area, radius;
    cout << "반지름을 입력하세요: ";
    cin >> radius;
    area = PI * radius * radius;
    cout << "반지름 " << radius << "인 원의 면적= " << area << endl;
}

