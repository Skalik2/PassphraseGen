import random
import string

WORD_LIST = [
    "apple", "banana", "cloud", "dolphin", "forest", "guitar", "mountain", "ocean",
    "puzzle", "robot", "shadow", "galaxy", "wizard", "mystery", "journey", "crystal",
    "village", "spirit", "quasar", "nebula", "planet", "comet", "aurora", "eclipse",
    "volcano", "canyon", "meadow", "island", "lagoon", "harbor", "beacon", "cipher"
]
COMMON_SEPARATORS = ["-", "_", ".", " ", "~"]
SPECIAL_CHARACTERS = "!@#$%^&*()_+-=[]{}|;:,.<>?"

def get_user_choice(prompt, options_map, default_key=None):
    print(prompt)
    for key, desc in options_map.items():
        print(f"  {key}) {desc}")
    
    while True:
        choice = input(f"Enter your choice ({'/'.join(options_map.keys())}" + (f", default: {default_key}" if default_key else "") + "): ").strip().lower()
        if not choice and default_key:
            return default_key
        if choice in options_map:
            return choice
        print(f"Invalid choice. Please select from: {', '.join(options_map.keys())}")

def generate_passphrase(num_words, separator,
                        add_numbers, num_numbers, number_placement,
                        add_special, num_special, special_placement,
                        capitalization_style):

    if num_words < 2 or num_words > len(WORD_LIST):
        print(f"Warning: Number of words should be between 2 and {len(WORD_LIST)}. Using {min(max(2, num_words), len(WORD_LIST))}.")
        num_words = min(max(2, num_words), len(WORD_LIST))
        
    chosen_words_list = random.sample(WORD_LIST, k=num_words)

    if capitalization_style == 't':
        chosen_words_list = [word.capitalize() for word in chosen_words_list]
    elif capitalization_style == 'r':
        if chosen_words_list:
            idx_to_capitalize = random.randrange(len(chosen_words_list))
            chosen_words_list[idx_to_capitalize] = chosen_words_list[idx_to_capitalize].upper()
    elif capitalization_style == 's':
        if chosen_words_list:
            chosen_words_list[0] = chosen_words_list[0].capitalize()

    passphrase_core = separator.join(chosen_words_list)
    final_passphrase_parts = [passphrase_core]

    if add_numbers == 'y':
        numbers_str = "".join(random.choice(string.digits) for _ in range(num_numbers))
        if number_placement == 'b':
            final_passphrase_parts.insert(0, numbers_str)
        elif number_placement == 'e':
            final_passphrase_parts.append(numbers_str)
        elif number_placement == 'i':
            if random.choice([True, False]):
                 final_passphrase_parts.insert(0, numbers_str)
            else:
                 final_passphrase_parts.append(numbers_str)

    if add_special == 'y':
        special_str = "".join(random.choice(SPECIAL_CHARACTERS) for _ in range(num_special))
        if special_placement == 'b':
            final_passphrase_parts.insert(0, special_str)
        elif special_placement == 'e':
            final_passphrase_parts.append(special_str)
        elif special_placement == 'i':
            if random.choice([True, False]):
                 final_passphrase_parts.insert(0, special_str)
            else:
                 final_passphrase_parts.append(special_str)

    return "".join(final_passphrase_parts)

def estimate_strength(passphrase):
    score = 0
    length = len(passphrase)

    if length < 8:
        score -= 2
    elif length >= 12:
        score += 1
    if length >= 16:
        score += 1
    if length >= 20:
        score +=1

    if any(c.islower() for c in passphrase):
        score += 1
    if any(c.isupper() for c in passphrase):
        score += 1
    if any(c.isdigit() for c in passphrase):
        score += 1
    if any(c in SPECIAL_CHARACTERS for c in passphrase):
        score += 1
    
    num_separators = sum(1 for char in passphrase if char in COMMON_SEPARATORS)
    if num_separators >= 2:
        score +=1
    if num_separators >=3:
        score +=1

    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Fair"
    elif score <= 6:
        return "Good"
    elif score <= 8:
        return "Strong"
    else:
        return "Very Strong"

if __name__ == "__main__":
    print("Welcome to Secure Phrase Architect!")

    while True:
        while True:
            try:
                num_words_input = input("Number of words (e.g., 3-6, default: 4): ")
                num_words = int(num_words_input) if num_words_input else 4
                if num_words < 2:
                    print("Minimum 2 words required.")
                    continue
                break
            except ValueError:
                print("Invalid number.")

        print("Available separators:", " ".join(COMMON_SEPARATORS))
        separator = input(f"Choose a separator (default: '{COMMON_SEPARATORS[0]}'): ")
        if not separator:
            separator = COMMON_SEPARATORS[0]
        elif separator not in COMMON_SEPARATORS and len(separator) > 1:
            print("Using only the first character of your custom separator.")
            separator = separator[0]
        elif not separator.strip() and separator in COMMON_SEPARATORS:
             pass
        elif not separator.strip():
            print("Separator cannot be empty, using default.")
            separator = COMMON_SEPARATORS[0]

        capitalization_options = {
            'n': "None (all lowercase)",
            't': "Title Case (Like This)",
            's': "Sentence case (First word capitalized)",
            'r': "Random word FULLY capitalized"
        }
        capitalization_style = get_user_choice("Capitalization style:", capitalization_options, 'n')

        add_numbers = get_user_choice("Add numbers? (y/n):", {'y': "Yes", 'n': "No"}, 'n')
        num_numbers = 0
        number_placement = ''
        if add_numbers == 'y':
            while True:
                try:
                    num_numbers_input = input("How many numbers (e.g., 1-3, default: 1): ")
                    num_numbers = int(num_numbers_input) if num_numbers_input else 1
                    if num_numbers < 1: num_numbers = 1
                    break
                except ValueError:
                    print("Invalid number.")
            number_placement = get_user_choice("Place numbers:", {'b': "Beginning", 'e': "End", 'i': "Intersperse (simplified for console)"}, 'e')

        add_special = get_user_choice("Add special characters? (y/n):", {'y': "Yes", 'n': "No"}, 'n')
        num_special = 0
        special_placement = ''
        if add_special == 'y':
            while True:
                try:
                    num_special_input = input(f"How many special characters (e.g., 1-2, from '{SPECIAL_CHARACTERS}', default: 1): ")
                    num_special = int(num_special_input) if num_special_input else 1
                    if num_special < 1: num_special = 1
                    break
                except ValueError:
                    print("Invalid number.")
            special_placement = get_user_choice("Place special characters:", {'b': "Beginning", 'e': "End", 'i': "Intersperse (simplified for console)"}, 'e')

        generated_passphrase = generate_passphrase(
            num_words, separator,
            add_numbers, num_numbers, number_placement,
            add_special, num_special, special_placement,
            capitalization_style
        )

        print("\n" + "="*30)
        print("Generated Passphrase:", generated_passphrase)
        
        strength = estimate_strength(generated_passphrase)
        print("Estimated Strength:", strength)
        print("="*30)
        
        tips = [
            "Tip: Longer passphrases are generally stronger and harder to crack.",
            "Tip: Using a mix of uppercase, lowercase, numbers, and symbols increases complexity.",
            "Tip: Avoid common words or easily guessable patterns.",
            "Tip: For critical accounts, consider using a unique passphrase for each.",
            "Tip: Store your passphrases securely using a password manager."
        ]
        print("\n" + random.choice(tips))

        if input("\nGenerate another passphrase? (y/n, default: n): ").strip().lower() != 'y':
            break
    
    print("\nThank you for using Secure Phrase Architect!")