print("2026-10-08, 24117000, 차민규\n")
print("동적타입언어 변수 참조")

persent = 20


def salePrice(price):
    result = price * (1 - persent / 100)
    print(f"지불 금액 = {result}")
    return result


salePrice(50000)
