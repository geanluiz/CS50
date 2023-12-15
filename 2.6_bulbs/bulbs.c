#include <cs50.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);

int main(void)
{
    // Gets user input
    string text = get_string("Message: ");
    int length = strlen(text);

    // Converts letters to ASCII integers
    int decimal;
    int binary[BITS_IN_BYTE * length];

    for (int i = 0; i < length; i++)
    {
        decimal = text[i];

        // Converts ASCII to binary
        int bin_lenght = BITS_IN_BYTE;
        for (int j = 0; j < BITS_IN_BYTE; j++)
        {
            bin_lenght--;
            if ((decimal % 2) == 0)
            {
                binary[bin_lenght] = 0;
            }
            else
            {
                binary[bin_lenght] = 1;
            }
            decimal /= 2;
        }

        // Prints bulbs
        for (int x = 0; x < BITS_IN_BYTE; x++)
        {
            print_bulb(binary[x]);
        }
        printf("\n");
    }
}

void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}
