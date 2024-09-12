
from cs50 import get_string


def main():
    text = get_string("Text: ")

    grade_n = grade(text)
    if (grade_n < 1):
        print("Before Grade 1")
    elif (grade_n >= 16):
        print("Grade 16+")
    else:
        print(f"Grade {grade_n}")


def count_letters(text):
    letters = 0
    for i in text:
        if i.isalpha():
            letters += 1
    return letters


def count_sentences(text):
    sentences = 0
    end_char = ('!', '.', '?')
    for i in text:
        if i in end_char:
            sentences += 1
    return sentences


def count_words(text):
    words = 1
    for i in text:
        if i.isspace():
            words += 1
    return words


def grade(text):
    letters = count_letters(text)
    sentences = count_sentences(text)
    words = count_words(text)

    L = (letters / words) * 100
    S = (sentences / words) * 100
    index = round((0.0588 * L) - (0.296 * S) - 15.8)
    return index


main()
