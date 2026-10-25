# 1. Sum of digits
# Given a positive integer N, print the sum of its digits.
# Input: 472  →  Output: 13

# def sum_of_digits(num):
#     num = abs(num)
#     total_sum = 0

#     while num > 0:
#         total_sum += num % 10
#         num = num // 10

#     return total_sum

# print(sum_of_digits(1234))



# 2. Count even digits
# Given a positive integer N, count how many of its digits are even. The digit 0 is even.
# Input: 20481  →  Output: 3

# def count_digits(n):
#     n = abs(n)
#     count = 0

#     if n == 0:
#         count = 1
#     while n > 0:
#         n %= 10
#         count += 1

#         if n % 2 == 0:
#             return count

# print(count_digits(12450))

#reverse a number

n = int(input("Enter the num: "))

for i in range(1, 11):
    
    print(n*i)
        

