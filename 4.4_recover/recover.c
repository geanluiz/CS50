#include <memory.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int block = 512;

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
    uint8_t cache[block];
    uint8_t id[] = {0xFF, 0xD8, 0xFF};
    uint8_t fourth = 0xE0;
    uint8_t end[] = {0x00, 0x00, 0x00};

    int count = 0;
    char name[8];

    FILE *img = NULL;

    while (fread(&cache, 1, block, card) == block)
    {
        // Create JPEG from the data
        sprintf(name, "%03i.jpg", count);

        if (memcmp(cache, &id, sizeof(id)) == 0 &&
            (cache[3] & 0xF0) == fourth) // Image header found
        {
            if (img != NULL) // If there is an opened image
            {
                fclose(img);
                count++;
                sprintf(name, "%03i.jpg", count);
                img = fopen(name, "w");
                fwrite(&cache, 1, block, img); // Write data to file
            }
            else
            {
                img = fopen(name, "w");
                fwrite(&cache, 1, block, img); // Write data to file
            }
        }
        else if (img != NULL)
        {
            fwrite(&cache, 1, block, img); // Write data to file
        }
    }
    fclose(img);
    fclose(card);
}
