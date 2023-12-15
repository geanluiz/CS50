#include <cs50.h>
#include <stdio.h>

int get_cents(void);
int calculate_quarters(int cents);
int calculate_dimes(int cents);
int calculate_nickels(int cents);
int calculate_pennies(int cents);

int main(void)
{
    // Ask how many cents the customer is owed
    int cents = get_cents();

    // Calculate the number of quarters to give the customer
    int quarters = calculate_quarters(cents);
    cents = cents - quarters * 25;

    // Calculate the number of dimes to give the customer
    int dimes = calculate_dimes(cents);
    cents = cents - dimes * 10;

    // Calculate the number of nickels to give the customer
    int nickels = calculate_nickels(cents);
    cents = cents - nickels * 5;

    // Calculate the number of pennies to give the customer
    int pennies = calculate_pennies(cents);
    cents = cents - pennies * 1;

    // Sum coins
    int coins = quarters + dimes + nickels + pennies;

    // Print total number of coins to give the customer
    printf("%i\n", coins);
}

int get_cents(void)
{
    // TODO
    return 0;
}

int calculate_quarters(int cents)
{
    // TODO
    return 0;
}

int calculate_dimes(int cents)
{
    // TODO
    return 0;
}

int calculate_nickels(int cents)
{
    // TODO
    return 0;
}

int calculate_pennies(int cents)
{
    // TODO
    return 0;
}

/*
https://cs50.harvard.edu/x/2023/psets/1/cash/

        Implementation Details
In cash.c, we’ve implemented most (but not all!) of a program that prompts the user for the number of cents
that a customer is owed and then prints the smallest number of coins with which that change can be made.
Indeed, main is already implemented for you. But notice how main calls several functions that aren’t yet implemented!
One of those functions, get_cents, takes no arguments (as indicated by void) and returns an int.
The rest of the functions all take one argument, an int, and also return an int. All of them currently return 0 so that the code will compile.
But you’ll want to replace every TODO and return 0; with your own code. Specifically, complete the implementation of those functions as follows:

Implement get_cents in such a way that the function prompts the user for a number of cents using get_int and then returns that number as an int.
If the user inputs a negative int, your code should prompt the user again.
(But you don’t need to worry about the user inputting, e.g., a string, as get_int will take care of that for you.)
Odds are you’ll find a do while loop of help, as in mario.c!

Implement calculate_quarters in such a way that the function calculates (and returns as an int) how many quarters a customer should be given
if they’re owed some number of cents. For instance, if cents is 25, then calculate_quarters should return 1.
If cents is 26 or 49 (or anything in between, then calculate_quarters should also return 1.
If cents is 50 or 74 (or anything in between), then calculate_quarters should return 2. And so forth.

Implement calculate_dimes in such a way that the function calculates the same for dimes.
Implement calculate_nickels in such a way that the function calculates the same for nickels.
Implement calculate_pennies in such a way that the function calculates the same for pennies.
Note that, unlike functions that only have side effects, functions that return a value should do so explicitly with return!
Take care not to modify the distribution code itself, only replace the given TODOs and the subsequent return value! Note too that,
recalling the idea of abstraction, each of your calculate functions should accept any value of cents ,
not just those values that the greedy algorithm might suggest. If cents is 85, for example, calculate_dimes should return 8.
*/
