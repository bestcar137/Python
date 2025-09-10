# 실습결과보고서 문제 1번

"""
1. 사용자로부터 두 개의 정수를 받아서 정수의 합, 정수의 차, 정수의 곱,
정수의 평균, 큰 수, 작은 수를 계산하여 화면에 출력하는 프로그램을 작성하시오.
파이썬이 제공하는 내장 함수 sum(), max(), min()을 사용해도 됨.
 """

a = int(input("첫 번째 정수를 입력하세요: "))
b = int(input("두 번째 정수를 입력하세요: "))

sum = a + b
dif = a - b
mul = a * b
avg = (a + b) / 2
max = max(a, b)
min = min(a, b)

print(f"정수의 합: {sum}")
print(f"정수의 차: {dif}")
print(f"정수의 곱: {mul}")
print(f"정수의 평균: {avg}")
print(f"큰 수: {max}")
print(f"작은 수: {min}")