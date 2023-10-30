#include <cs50.h>
#include <math.h>
#include <stdio.h>

int main(void)
{

    float minSize = 9;
    float initSize;
    float endSize;

    // TODO: Prompt for start size

    do
    {
        initSize = get_int("Insert initial population size: ");
    }
    while (initSize < minSize);

    // TODO: Prompt for end size

    do
    {
        endSize = get_int("Insert final population size: ");
    }
    while (endSize < initSize);

    // TODO: Calculate number of years until we reach threshold

    float born = truncf(initSize / 3);
    float deaths = truncf(initSize / 4);
    float years = 0;
    int totalPop = initSize;

    while (totalPop < endSize)
    {
        totalPop = totalPop + born - deaths;
        born = truncf(totalPop / 3);
        deaths = truncf(totalPop / 4);
        years++;
    }

    // TODO: Print number of years

    {
        printf("Years: %.0f\n", years);
    }
}
