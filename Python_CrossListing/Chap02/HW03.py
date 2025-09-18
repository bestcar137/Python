# 실습보고서 문제 3번

"""
사용자로부터 문자열과 반복 횟수를 입력받아서
해당 문자열을 입력받은 횟수만큼 반복하여 출력하는 프로그램을 작성하시오.
"""

repeat_String = input("반복할 문자열을 입력하세요: ")
repeat_Time = input("반복할 횟수를 입력하세요: ")

print(f"결과: {repeat_String * int(repeat_Time)}")