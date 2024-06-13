#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float sum = 0;

            RGBTRIPLE temp = image[i][j];
            sum += temp.rgbtBlue;
            sum += temp.rgbtGreen;
            sum += temp.rgbtRed;

            int cache = round(sum / 3);

            image[i][j].rgbtBlue = cache;
            image[i][j].rgbtGreen = cache;
            image[i][j].rgbtRed = cache;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float originalBlue = image[i][j].rgbtBlue;
            float originalGreen = image[i][j].rgbtGreen;
            float originalRed = image[i][j].rgbtRed;

            float sepiaBlue = .272 * originalRed + .534 * originalGreen + .131 * originalBlue;
            float sepiaGreen = .349 * originalRed + .686 * originalGreen + .168 * originalBlue;
            float sepiaRed = .393 * originalRed + .769 * originalGreen + .189 * originalBlue;

            (sepiaBlue > 255) ? sepiaBlue = 255 : sepiaBlue;
            (sepiaGreen > 255) ? sepiaGreen = 255 : sepiaGreen;
            (sepiaRed > 255) ? sepiaRed = 255 : sepiaRed;

            image[i][j].rgbtBlue = round(sepiaBlue);
            image[i][j].rgbtGreen = round(sepiaGreen);
            image[i][j].rgbtRed = round(sepiaRed);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2); j++)
        {
            int x = j + 1;
            RGBTRIPLE temp = image[i][width - x];
            image[i][width - x] = image[i][j];
            image[i][j] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    int x_min, x_max, y_min, y_max;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // First row
            if (i == 0)
            {
                if (j == 0)
                {
                    x_min = i;
                    x_max = i + 1;
                    y_min = j;
                    y_max = j + 1;
                }

                else if (j == (width - 1))
                {
                    x_min = i;
                    x_max = i + 1;
                    y_min = j - 1;
                    y_max = j;
                }

                else
                {
                    x_min = i;
                    x_max = i + 1;
                    y_min = j - 1;
                    y_max = j + 1;
                }
            }

            // Last row
            else if (i == (height - 1))
            {
                if (j == 0)
                {
                    x_min = i - 1;
                    x_max = i;
                    y_min = j;
                    y_max = j + 1;
                }

                else if (j == (width - 1))
                {
                    x_min = i - 1;
                    x_max = i;
                    y_min = j - 1;
                    y_max = j;
                }

                else
                {
                    x_min = i - 1;
                    x_max = i;
                    y_min = j - 1;
                    y_max = j + 1;
                }
            }

            // First and last columns
            else if (j == 0)
            {
                x_min = i - 1;
                x_max = i + 1;
                y_min = j;
                y_max = j + 1;
            }

            else if (j == (width - 1))
            {
                x_min = i - 1;
                x_max = i + 1;
                y_min = j - 1;
                y_max = j;
            }

            // Other pixels
            else
            {
                x_min = i - 1;
                x_max = i + 1;
                y_min = j - 1;
                y_max = j + 1;
            }

            // Calculation
            int count = 0;
            float sumBlue = 0;
            float sumGreen = 0;
            float sumRed = 0;

            for (int x = x_min; x <= x_max; x++)
            {
                for (int y = y_min; y <= y_max; y++)
                {
                    sumBlue += copy[x][y].rgbtBlue;
                    sumGreen += copy[x][y].rgbtGreen;
                    sumRed += copy[x][y].rgbtRed;
                    count++;
                }
            }
            image[i][j].rgbtBlue = round(sumBlue / count);
            image[i][j].rgbtGreen = round(sumGreen / count);
            image[i][j].rgbtRed = round(sumRed / count);
        }
    }
    return;
}

// TODO: Refactoring
