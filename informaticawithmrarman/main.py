for i in range(1,11):
    print(f" 5* {i}")

for i in range(1,11):
    for j in range(1, 11):
         print(f" {j}* {i}")

for i in range(1,11):
    for j in range(1, 11):
         print(f" {j}** {i}")

a = 456
i = 3
while True:
    b = int(input("введите пароль"))
    i -= 1
    if a == b:
        print("доступ разрешен")
        break
    else:
        print("доступ запрешен")
    print(f"у вас осталось {i} попыток")
        