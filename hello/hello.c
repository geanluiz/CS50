#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //Prompts user for his name and prints out a greeting
    string x = get_string("What's your name? ");
    {
        printf("Hello, %s!\n", x);
    }
}
