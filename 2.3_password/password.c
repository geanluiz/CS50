#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

bool valid(string password);

int main(void)
{
    string password = get_string("Enter your password: ");
    if (valid(password))
    {
        printf("Your password is valid!\n");
    }
    else
    {
        printf("Your password needs at least one uppercase letter, lowercase letter, number and symbol\n");
    }
}

bool valid(string password)
{
    int N = strlen(password);
    int upper = 0, lower = 0, num = 0, symbol = 0;
    for (int i = 0; i < N; i++)
    {
        int x = password[i];
        if (isupper(x))
        {
            upper++;
        }
        else if (islower(x))
        {
            lower++;
        }
        else if (isdigit(x))
        {
            num++;
        }
        else if (ispunct(x))
        {
            symbol++;
        }
    }
    if (upper * lower * num * symbol != 0)
    {
        return true;
    }
    return false;
}
