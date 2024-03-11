#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    /*
    int m = 300;
    float fx = 300.600006;
    char cht = 'z';

    printf("\nPointer : Demonstrate the use of & and * operator :\n");
    printf("--------------------------------------------------------\n");
    printf("m = %i\n", m);
    printf("fx = %f\n", fx);
    printf("cht = %c\n\n", cht);

    printf("Using & operator :\n");
    printf("-----------------------\n");
    printf("address of m = %p\n", &m);
    printf("address of fx = %p\n", &fx);
    printf("address of cht = %p\n", &cht);;

    int *pt_m = &m;
    float *pt_fx = &fx;
    char *pt_cht = &cht;
    printf("Using & and * operator :\n");
    printf("-----------------------------\n");
    printf("value at address of m = %i\n", *(&m));
    printf("value at address of fx= %f\n", *(&fx));
    printf("value at address of cht= %c\n\n", *(&cht));

    printf("Using only pointer variable :\n");
    printf("----------------------------------\n");
    printf("address of m = %p\n", pt_m);
    printf("address of fx = %p\n", pt_fx);
    printf("address of cht = %p\n\n", pt_cht);

    printf("Using only pointer operator :\n");
    printf("----------------------------------\n");
    printf("value at address of m = %i\n", *pt_m);
    printf("value at address of fx = %f\n", *pt_fx);
    printf("value at address of cht = %c\n\n", *pt_cht);
    */


    int n1, n2;
    int *p1 = &n1;
    int *p2 = &n2;

    printf("Insert #1: ");
    scanf("%i", &n1);

    printf("Insert #2: ");
    scanf("%i", &n2);

    char op;

    printf("Choose the operation: ");
    scanf(" %c", &op);

    int result;

    switch(op)
    {
        case '+':
            result = *p1 + *p2;
            printf("The sum of the entered numbers is : %i\n", result);
            break;

        case '-':
            result = *p1 - *p2;
            printf("The first number minus the second one is : %i\n", result);
            break;

        default:
            printf("Error");
    }

    return 0;
}
