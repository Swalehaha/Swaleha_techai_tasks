import random

# Step 1: Select a random secret word
def select_secret_word():
    """
    #Chooses a random word from the words.txt file.
    #Words in the file must be one per line.
    """
    with open(r"D:\Swaleha\Coding\TechAI Tasks\Task 1 - Wordle\words.txt", "r") as f:
        words = f.readlines()  # Read all words
        return random.choice(words).lower().strip()  # Pick one, lowercase, strip newline

SECRET_WORD = select_secret_word()
# print(SECRET_WORD)  # Uncomment to test/debug

# Step 2: Function to check guess
def check_guess(secret, guess):
    """
    Compares the guess with the secret word.
    Returns a list of feedback for each letter: 'correct', 'present', or 'absent'.
    """
    feedback = []
    for i in range(len(guess)):
        if guess[i] == secret[i]:
            feedback.append('correct')  # Right letter, right position
        elif guess[i] in secret:
            feedback.append('present')  # Right letter, wrong position
        else:
            feedback.append('absent')   # Letter not in the word
    return feedback

# Step 3: Function to display feedback in colors
def display_feedback(guess, feedback):
    """
    Displays the guess letters with colors according to feedback:
    Green = correct, Yellow = present, Gray = absent
    """
    for i in range(len(guess)):
        if feedback[i] == 'correct':
            print(f"\033[42m{guess[i].upper()}\033[0m", end=" ")  # Green background
        elif feedback[i] == 'present':
            print(f"\033[43m{guess[i].upper()}\033[0m", end=" ")  # Yellow background
        else:
            print(f"\033[100m{guess[i].upper()}\033[0m", end=" ")  # Gray background
    print()  # New line after the word

# Step 4: Main game loop
MAX_ATTEMPTS = 6  # Player has 6 tries

print("Welcome to Command-Line Wordle!")
print(f"You have {MAX_ATTEMPTS} attempts to guess the 5-letter word.\n")

for attempt in range(1, MAX_ATTEMPTS + 1):
    while True:
        guess = input(f"Attempt {attempt}/{MAX_ATTEMPTS}: Enter your guess: ").lower()
        try:
            if len(guess) != 5:
                raise Exception("Word length must be exactly 5 letters. Try again.")
            break  # Exit loop if valid input
        except Exception as e:
            print(e)

    feedback = check_guess(SECRET_WORD, guess)
    display_feedback(guess, feedback)

    # Check if the player guessed correctly
    if guess == SECRET_WORD:
        print(f"Congratulations! You guessed the word '{SECRET_WORD.upper()}' correctly in {attempt} attempts!")
        break
else:
    # Executed if loop completes without break (player ran out of attempts)
    print(f"Sorry! You've used all {MAX_ATTEMPTS} attempts. The secret word was '{SECRET_WORD.upper()}'.")
