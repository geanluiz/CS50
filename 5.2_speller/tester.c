#include "dictionary.c"

int main (void)
{
    char *w = "pneumoultramicroscopicsilicovolcanocoliosis";
    unsigned int x = hash(w);
    int expected = 3534;

    load("dictionaries/small");
    char *s = (unload() == 1)? "ok": "err";
    printf("%s\n", s);
}
