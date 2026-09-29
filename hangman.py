import argparse
import random
from english_words import english_words_lower_set


def load_words(filename):
    if filename:
        with open(filename, "r", encoding="utf-8") as file:
            return [line.strip().lower() for line in file]

    return list(english_words_lower_set)


def choose_word(words, word_length):
    available_words = [
        word
        for word in words
        if word.isalpha()
        and (
            len(word) == word_length
            if word_length
            else 5 <= len(word) <= 10
        )
    ]

    if not available_words:
        print("No suitable words found.")
        quit()

    return random.choice(available_words)


def display_word(secret_word, guessed_letters):
    return " ".join(
        letter.upper() if letter in guessed_letters else "_"
        for letter in secret_word
    )


def play_hangman(max_penalties, word_length, filename):
    words = load_words(filename)
    secret_word = choose_word(words, word_length)

    guessed_letters = set()
    penalties = 0

    while penalties < max_penalties:
        print()
        print(display_word(secret_word, guessed_letters))
        print(
            penalties,
            "penalty" if penalties == 1 else "penalties"
        )

        guess = input("$> ").strip().lower()

        if not guess.isalpha():
            print("Please enter letters only.")
            continue

        if len(guess) > 1:
            if guess == secret_word:
                print(
                    guess.upper(),
                    ": correct guess -",
                    penalties,
                    "penalties"
                )
                return

            penalties += 5
            print(guess.upper() + ": incorrect guess")

        else:
            if guess in guessed_letters:
                print("You already tried this letter.")
                continue

            guessed_letters.add(guess)
            occurrences = secret_word.count(guess)

            if occurrences > 0:
                print(
                    "Found",
                    occurrences,
                    "'" + guess.upper() + "'"
                )
            else:
                penalties += 1
                print("No '" + guess.upper() + "' found")

        if all(letter in guessed_letters for letter in secret_word):
            print()
            print(secret_word.upper() + ": correct guess")
            print("You win with", penalties, "penalties!")
            return

    print()
    print("You lose!")
    print("The word was:", secret_word.upper())


parser = argparse.ArgumentParser(description="Play Hangman")

parser.add_argument(
    "--penalties",
    type=int,
    default=12,
    help="Maximum number of penalties"
)

parser.add_argument(
    "--length",
    type=int,
    help="Length of the hidden word"
)

parser.add_argument(
    "--word-file",
    help="File containing one word per line"
)

arguments = parser.parse_args()

play_hangman(
    arguments.penalties,
    arguments.length,
    arguments.word_file
)
