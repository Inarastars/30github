#game_score =  int(input("Enter Score: "))
#if game_score >= 1000:
 #   print("Congratulations, you are a master!")
#else:
 #   print("Sorry, you are not a master!")

#x = int(input())
#if x > 0 and x <= 100 and x >= -100:
 #   print("натуральное число")
#else:
 #   print(" x =", x)

age =list(map(int, input("Enter your age: ").split()))
if age >= 20:
   print("adult")
elif age >= 10:
   print("YOUTH")
else:
   print("kid")
