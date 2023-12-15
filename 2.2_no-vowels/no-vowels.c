#include <cs50.h>
#include <stdio.h>
#include <string.h>

string replace(int N, string input);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Error: word not found!\n");
        printf("Usage: ./no-vowels word\n");
        return 1;
    }
    else
    {
        printf("%s\n", replace(strlen(argv[1]), argv[1]));
    }
}

string replace(int N, string input)
{
    for (int i = 0; i < N; i++)
    {
        char current = input[i];
        switch (current)
        {
            case 'a':
            case 'A':
                input[i] = '6';
                break;

            case 'e':
            case 'E':
                input[i] = '3';
                break;

            case 'i':
            case 'I':
                input[i] = '1';
                break;

            case 'o':
            case 'O':
                input[i] = '0';
                break;
        }
    }
    return input;
}
