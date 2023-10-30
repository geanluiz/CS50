// Calculate your half of a restaurant bill
// Data types, operations, type casting, return value

#include <cs50.h>
#include <stdio.h>

float half(float bill, float tax, float tip);

int main(void)
{
    float bill_amount = get_float("Bill before tax and tip: ");
    float tax_percent = 1 + get_float("Sale Tax Percent: ") / 100;
    float tip_percent = 1 + get_float("Tip percent: ") / 100;

    printf("You will owe $%.2f each!\n", half(bill_amount, tax_percent, tip_percent));
}

// TODO: Complete the function
float half(float bill, float tax, float tip)
{
    float total = ((bill * tax) * tip) / 2;
    return total;
}
