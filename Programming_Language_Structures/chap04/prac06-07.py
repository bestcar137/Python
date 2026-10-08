print("2026-10-08, 24117000, 차민규\n")
print("동적타입언어 변수 값 변경")

percent = 20


def salePrice(price):
    global percent  # global 변수 (지역 변수)가 없으면 아래에서 오류 발생 예정
    percent += 10  # 이 문장에서 오류 발생 예정
    result = price * (1 - percent / 100)
    return result


salePrice(50000)
