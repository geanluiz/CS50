from cs50 import get_int


def main():
    while True:
        n = get_int("Height: ")
        if n > 0 and n < 9:
            construct(n)
            break
        else:
            print("Expected height between 1 and 8\n Try again")


def construct(h):
    for a in range(h):
        x = a + 1
        print(" " * (h - x), end="")

        print("#" * x, end="")

        print("  ", end="")

        print("#" * x)


main()
