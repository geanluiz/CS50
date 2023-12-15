// This program takes an text from the user and encrypts it by rotating
// Each letter a number of times given by the user via command-line argument

#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int n_key;
bool only_digits(string text);
char rotate(char letter, int key);

int main(int argc, string argv[])
{
    // Checks if there is only one argument in argv
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
        exit(EXIT_FAILURE);
    }

    string k = argv[1];
    n_key = strlen(k);

    // Checks if argv contains only digits
    if (only_digits(k) == false)
    {
        printf("Usage: ./caesar key\n");
        return 1;
        exit(EXIT_FAILURE);
    }

    // Prompts user for a text
    string text = get_string("text: ");
    int K = atoi(k);
    int n = strlen(text);

    // Prints result
    printf("Ciphertext: ");
    for (int i = 0; i < n; i++)
    {
        printf("%c", rotate(text[i], K));
    }
    printf("\n");
    return 0;
}

bool only_digits(string text)
{
    int count = 0;
    for (int i = 0; i < n_key; i++)
    {
        if (!isdigit(text[i]))
        {
            count++;
        }
    }
    if (count != 0)
    {
        return false;
    }
    else
    {
        return true;
    }
}

char rotate(char letter, int key)
{
    // Handles key previously if it is greater than 26
    if (key > 26)
    {
        key -= 26;
    }

    // Handles non-alphabetical characteres
    if (!isalpha(letter))
    {
        return letter;
    }
    else
    {
        // Rotates letter
        int x = letter + key;

        // Handles overflow of characters
        if (islower(letter))
        {
            while (!isalpha(x) || x > 'z')
            {
                x -= 26;
            }
        }
        else if (isupper(letter))
        {
            while (!isalpha(x) || x > 'z')
            {
                x -= 26;
            }
        }
        return x;
    }
}
