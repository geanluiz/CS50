#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //Prompt user for size of the Pyramids
    int size;
    do
    {
        size = get_int("Enter the desired size: ");
    }
    while (size < 1 || size > 8);

    //Prints the pyramids
    for (int a = 0; a < size; a++)
    {

        //Considers (input - current counting) to print " "
        for (int b = 1; b < (size - a); b++)
        {
            printf(" ");
        }

        //Prints the left "#"
        for (int c = 0; c <= a; c++)
        {
            printf("#");
        }

        //Prints the space between pyramids
        printf("  ");

        //Prints the right "#"
        for (int d = 0; d <= a; d++)
        {
            printf("#");
        }

        printf("\n");
    }
}
