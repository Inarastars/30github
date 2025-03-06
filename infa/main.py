#import keyword
#print("Список ключевых слов в Python")
#print(keyword.kwlist)

#def add_numbers(a,b):
#    return a + b
#result = add_numbers(4,7)
#print(result)

def add_numbers(a,b):
    return a ** b
result = add_numbers(9,2)
print(result)

def is_even(n):
    return n % 2 == 0
print(is_even(8))
print(is_even(5))