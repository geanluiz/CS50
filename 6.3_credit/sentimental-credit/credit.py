
from re import match


def main():
    # Prompt user for a credit card number
    n = input("Number: ")

    # Returns the result
    if is_valid(n):
        check_issuer(n)
    else:
        print("INVALID")


# Luhn’s Algorithm to check if card number is valid as per week 1
def is_valid(n):
    n_is_even = len(n) % 2 == 0

    sum1 = 0
    sum2 = 0
    for i in range(len(n)):
        a = int(n[i])
        if (n_is_even and i % 2 == 0) or not n_is_even and i % 2 != 0:
            a *= 2
            b = a // 10
            c = a % 10
            sum1 += b + c
        else:
            b = a // 10
            c = a % 10
            sum2 += b + c

    if (sum1 + sum2) % 10 != 0 or len(n) < 13:
        return False
    else:
        return True

# Checks what's the card issuer using regular expressions match
def check_issuer(n):
    if match(r"^(34|37)", n):  # If n starts with 34 or 37
        print("AMEX")
    elif match(r"^4[0-9]", n):  # If n starts with a number between 40 and 49
        print("VISA")
    elif match(r"5[1-5]", n):  # If n starts with a number between 51 and 55
        print("MASTERCARD")
    else:
        print("INVALID")


main()
