// Returns the prime numbers in the range given by the user

#include <cs50.h>
#include <stdio.h>

bool prime(int number);

int main(void)
{
    // Prompts user for the first number
    int min;
    do
    {
        min = get_int("Minimum: ");
    }
    while (min < 1);

    // Prompts user for the last number
    int max;
    do
    {
        max = get_int("Maximum: ");
    }
    while (min >= max);

    // Loops between the numbers of the range
    for (int i = min; i <= max; i++)
    {
        if (prime(i))
        {
            printf("%i\n", i);
        }
    }
}

bool prime(int number)
{
    // TODO

    // Variable that will count the ammount of number i is divisible to
    int z = 0;

    // Checks if the given number is divisable by its precessors
    for (int y = 2; y < number; y++)
    {
        if ((number % y) == 0)
        {
            z++;
        }
    }

    // Checks how many numbers i is divisible to
    if (z == 0)
    {
        return true;
    }

    return false;
}
