#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_sentences(string text);
int count_words(string text);

int grade(string text);

int main(void)
{
    // Prompt the user for a string of text using get_string
    string text = get_string("Text: ");

    // Prints the given text and the result
    printf("Text: %s\n", text);

    if (grade(text) < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade(text) >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade(text));
    }
}

// Counts the amount of lettes are in the text
int count_letters(string text)
{
    int letters = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }
    return letters;
}

// Counts the amount of sentences are in the text
int count_sentences(string text)
{
    int sentences = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == '!' || text[i] == '.' || text[i] == '?')
        {
            sentences++;
        }
    }
    return sentences;
}

// Counts the amount of words are in the text
int count_words(string text)
{
    int words = 1;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isspace(text[i]))
        {
            words++;
        }
    }
    return words;
}

// Calculates the grade using Coleman-Liau formula
int grade(string text)
{
    // Casts the countings results to float
    float n_letters = count_letters(text);
    float n_sentences = count_sentences(text);
    float n_words = count_words(text);

    float L = (n_letters / n_words) * 100;
    float S = (n_sentences / n_words) * 100;
    int index = round((0.0588 * L) - (0.296 * S) - 15.8);
    return index;
}
