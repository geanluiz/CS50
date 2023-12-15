// Checks the issuer of user's credit card by it's number
// And whether it's valid or not

#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    // Prompt user for a credit card number
    char number[15];
    printf("Insert your credit card number: ");
    scanf("%s", number);

    // Checks if the length of the number is even or odd
    int length = strlen(number);
    int even = (length % 2) == 0 ? 1 : 0;

    // If even, start from the first character, else starts with the second one
    int inv_even = even == 0 ? 1 : 0;

    int a, b, c, d;
    int sum1 = 0, sum2 = 0, sum_total = 0;

    // First sum
    for (int i = inv_even; i < length; i += 2)
    {
        int integer = (number[i] - '0') * 2;
        a = integer / 10;
        b = integer % 10;
        sum1 += a + b;
    }

    // Second sum
    for (int j = even; j < length; j += 2)
    {
        int integer = (number[j] - '0');
        c = integer / 10;
        d = integer % 10;
        sum2 += c + d;
    }

    // Returs whether final sum's last digit is '0'
    sum_total = sum1 + sum2;
    bool result = (sum_total % 10 == 0) ? true : false;

    // Stores the credit card issuer prefix
    int prefix = ((number[0] - '0') * 10) + (number[1] - '0');

    // Finds the credit card issuer
    if (result == true)
    {
        if (length == 15 && (prefix == 34 || prefix == 37))
        {
            printf("AMEX\n");
        }
        else if ((length == 13 || length == 16) && prefix >= 40 && prefix <= 49)
        {
            printf("VISA\n");
        }
        else if (length == 16 && prefix >= 51 && prefix <= 55)
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
        return 0;
    }
    else
    {
        printf("INVALID\n");
    }
    return 0;
}
