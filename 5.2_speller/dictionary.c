// Implements a dictionary's functionality

#include <ctype.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Stores the number of words in dictionary
static int w_count = 0;

// Number of buckets in hash table
const unsigned int N = 1200;

// Hash table
node *table[N]; // Array of pointers

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    char w[LENGTH + 1];
    char *d = w;
    while (*word != '\0')
    {
        *d++ = (isupper(*word))? tolower(*word++): *word++;
    }
    *d = '\0';

    int index = hash(w); // Try to compare hashes instead to see if it is faster
    node *tmp = table[index];

    while (tmp != NULL)
    {
        if (strcmp(w, tmp->word) == 0)
        {
            return true;
        }
        tmp = tmp->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hash = 4993;
    char c;
    while ((c = *word++))
    {
        hash = ((hash << 2) + hash) + c;
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *dict_file = fopen(dictionary, "r");
    if (dict_file == NULL)
    {
        return false;
    }

    errno = 0;
    char word[LENGTH + 1];
    while (fgets(word, sizeof(word), dict_file) != NULL)
    {
        if (word[0] == '\n')
            continue;

        word[strcspn(word, "\n")] = '\0';
        int i = hash(word);

        node *new = malloc(sizeof(node));
        strcpy(new->word, word);
        new->next = NULL;

        w_count++;
        if (table[i] == NULL)
        {
            table[i] = new;
            continue;
        }

        new->next = table[i];
        table[i] = new;
    }
    if (errno != 0)
        return false;

    fclose(dict_file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return w_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    errno = 0;
    for (int i = 0; i < N; i++)
    {
        if (table[i] == NULL) continue;

        node *tmp = table[i]->next;
        node *prev = table[i];
        free(prev);

        while (tmp != NULL)
        {
            prev = tmp;
            tmp = tmp->next;
            free(prev);
        }
    }
    w_count = 0;
    return (errno == 0);
}
