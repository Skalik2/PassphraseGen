import random

word_list = ["apple", "banana", "cloud", "dance", "eagle", "forest", "guitar", "happy", "island", "journey"]
separators = ["-", "_", ".", " "]

def generate_passphrase(num_words=4):
    if num_words < 2:
        print("Number of words must be at least 2.")
        return None

    k_words = min(num_words, len(word_list))
    chosen_words = random.sample(word_list, k=k_words)
    separator = random.choice(separators)
    passphrase = separator.join(chosen_words)

    if random.choice([True, False]):
        passphrase += str(random.randint(0, 9))

    return passphrase

if __name__ == "__main__":
    print("Welcome to the 'Secure Phrase Weaver' passphrase generator!")
    try:
        count = int(input("How many words should your passphrase have (e.g., 3, 4, 5)? "))
        
        new_passphrase = generate_passphrase(count)
        if new_passphrase:
            print("\nYour generated passphrase is:")
            print(new_passphrase)
            print("\nRemember to memorize it and not share it with anyone!")
            
    except ValueError:
        print("Please enter a valid number.")