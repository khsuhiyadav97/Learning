def isPalindrome(x):
    real_num = x
    reverse = 0

    while x > 0:
        num = 0
        num = x % 10
        reverse = reverse * 10 + num
        x = x // 10

    if real_num == reverse:
        return True
    return False

a = isPalindrome(12321)
b = isPalindrome(1234)
print(a, b)
