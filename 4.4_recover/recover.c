#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <memory.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{

    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Could not open file.\n");
        return 2;
    }

    // While there's still data left to read from the memory card
    BYTE cache[512];
    BYTE id[] = {255, 216, 255};
    BYTE end[] = {0, 0, 0};

    int count = 0;
    char name[8];
    sprintf(name, "%03i.jpg", count);

    while (1)
    {
        fread(&cache, sizeof(BYTE), 512, card);

        if (feof(card))
        {
            break;
        }

        // Create JPEG from the data
        if (memcmp(cache, &id, sizeof(id)) == 0 && cache[3] >= 224) // Image header found
        {
            FILE *img = fopen(name, "w");
            while(memcmp(cache, &end, sizeof(end)) != 0) // While not the end of image
            {
                fwrite(&cache, sizeof(BYTE), 512, img); // Write data to file
            }
            fclose(img);
            count++;
        }
    }
    fclose(card);
}
