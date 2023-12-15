#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

string l_alpha;
string u_alpha;
bool only_alpha(string key);
bool unique(string key);
string ciphertext(string text, string key);

int main(int argc, string argv[])
{
    string key = argv[1];
    if (argc != 2 || argc > 2 || !only_alpha(key))
    {
        printf("Usage: ./substitution key\n");
        return 1;
        exit(EXIT_FAILURE);
    }

    int key_size = strlen(key);
    if (key_size != 26 || !unique(key))
    {
        printf("Key must contain 26 unique characters.\n");
        return 1;
        exit(EXIT_FAILURE);
    }

    l_alpha = "abcdefghijklmnopqrstuvwxyz";
    u_alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    string text = get_string("plaintext: ");
    printf("ciphertext: %s\n", ciphertext(text, key));
    return 0;
}

bool only_alpha(string key)
{
    int count = 0;
    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(key[i]))
        {
            count++;
            printf("%i\n", count);
        }
    }
    if (count == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}

bool unique(string key)
{
    int count = 0;
    for (int i = 0; i < 26; i++)
    {
        for (int K = 0; K < 26; K++)
        {
            if (key[i] == key[K])
            {
                count++;
            }
        }
    }
    if (count == 26)
    {
        return true;
    }
    else
    {
        return false;
    }
}

string ciphertext(string text, string key)
{
    int n = strlen(text);
    string output = text;
    for (int t = 0; t < n; t++)
    {
        if (islower(text[t]))
        {
            char x = text[t];
            for (int K = 0; K < 26; K++)
            {
                if (x == l_alpha[K])
                {
                    output[t] = tolower(key[K]);
                }
            }
        }
        else if (isupper(text[t]))
        {
            char x = text[t];
            for (int K = 0; K < 26; K++)
            {
                if (x == u_alpha[K])
                {
                    output[t] = toupper(key[K]);
                }
            }
        }
        else
        {
            output[t] = text[t];
        }
    }
    return output;
}
