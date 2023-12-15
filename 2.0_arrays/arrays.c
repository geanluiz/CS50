#include <cs50.h>
#include <stdio.h>

int N = 3;
float average(int lenght, int scores[]);

int main(int argc, string argv[])
{
    int entry[N];
    for (int i = 0; i < N; i++)
    {
        entry[i] = get_int("Score #%i: ", i + 1);
    }

    printf("%f\n", average(N, entry));
}

float average(int lenght, int scores[])
{
    float sum = 0;
    for (int i = 0; i < lenght; i++)
    {
        sum += scores[i];
    }
    return sum / lenght;
}
