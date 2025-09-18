# 실습결과보고서 문제 1번

"""
1. 사용자로부터 세 개의 정수를 입력받고, 이 중에서 모두 다른 값이면 “True”,
 하나라도 중복된 값이면 “False”를 출력하는 프로그램을 작성하시오.
"""

print("세 개의 정수를 입력하세요.")

a = int(input("첫 번째 정수: "))
b = int(input("두 번째 정수: "))
c = int(input("세 번째 정수: "))

result = (a != b) and (a != c) and (b != c)
print(result)
