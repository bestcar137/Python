# 실습결과보고서 문제 2번

"""
2. 함수 testPrime(n)을 작성하여 n이 소수인지 판정하고,
해당 함수를 이용해 2부터 100까지의 모든 소수를 한 줄로 출력하시오.
(입력 없음, 출력은 공백으로 구분된 소수 나열)
"""

# [함수] testPrime(n): 소수 판정
# - 예외/기저 처리: 2는 소수, 2 미만은 합성/무의미 처리
# - 짝수 배제: n이 짝수면(2 제외) 합성수
# - 나눗셈 검사는 3부터 √n까지의 홀수만 확인하여 연산량 감소
def testPrime(n):
    if n < 2:
        return False              # 0, 1은 소수 아님
    if n == 2:
        return True               # 2는 유일한 짝수 소수
    if n % 2 == 0:
        return False              # 2를 제외한 모든 짝수는 합성수

    i = 3
    while i * i <= n:             # i가 √n을 넘으면 더 볼 필요 없음
        if n % i == 0:            # 나누어떨어지면 약수가 있으므로 합성수
            return False
        i += 2                    # 홀수만 검사(3,5,7, ...)
    return True                   # 위 조건에 걸리지 않으면 소수

# [처리] 2~100을 순회하며 소수만 수집
primes = []
for k in range(2, 101):
    if testPrime(k):
        primes.append(k)

# [출력] 한 줄에 공백으로 구분하여 소수들을 나열
print(*primes)
