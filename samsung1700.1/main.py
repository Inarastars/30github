n = int(input())
num = 1
for i in range(0,n,1):
    row = []
    for j in range(n, 0, -1):
        row.append(num)
        num += 1
    if i % 2 == 1:
        row.reverse()
    print("  ".join(map(str, row)))

#n = input("Enter the integer:")
#if n == n[:: -1]:
 #   print("this is number-polyndrom")
#else:
 #   print("this is not number-polyndrom")

#correct_answer = 32
#tries = 0
#print("Guess a number between 1 to 100")
#while True:
 #   n = int(input("Enter the number:"))
  #  tries += 1
   # if n < correct_answer:
    #    print("Higher!")
    #elif n > correct_answer:
     #   print("Lower")
 #   else:
  #      print(f"Congratulations. Total try = {tries}")
   #     break