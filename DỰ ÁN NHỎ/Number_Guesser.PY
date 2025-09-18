import random
print("Chao ban den voi tro choi Number Guesser " )
print("Luat choi : Người chơi sẽ cố gắng đoán một con số ngẫu nhiên do máy tính tạo ra (1 - 100).\n Máy tính sẽ đưa ra gợi ý cho biết số người chơi đoán là lớn hơn hay nhỏ hơn con số bí mật.")
lc = input("Bạn muốn chơi nó không (Y/N) : ")
while True:
    top_range = input("Phạm vi bạn muốn đoán: ")
    if top_range.isdigit():
        top_range = int(top_range)
    else:
        print("Hãy nhập vào 1 số nguyên để chọn.")
        continue
    a = random.randint(1,top_range)
    if lc.lower() != "y":
        break 
    minp = top_range
    maxt = 1
    A=[maxt,minp]
    while True:
        print(A)
        so = input("Đoán số :  ")
        if so.isdigit() and int(so) < top_range:
            so = int(so)
        else:
            print("Vui lòng nhập số hợp lệ!")
        if so > a :
            minp = so
            print("Lon hon dap an")
        elif     so < a :
            maxt = so
            print("Nho hon dap an")
        else:
            print("Chinh xac !")
            again = input("Bạn có muốn chơi tiếp không (Y/N)")
            if again.lower() == "Y":
                top_range = input("Phạm vi bạn muốn đoán: ")
                continue
            else:
                break
        A=[maxt,minp]
        