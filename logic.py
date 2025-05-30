import random
import string
from tkinter import messagebox # Still used here for simplicity, though could be refactored out
from config import WORD_LIST, SPECIAL_CHARACTERS, COMMON_SEPARATORS_DISPLAY

def generate_passphrase_logic(num_words, separator,
                        add_numbers, num_numbers, number_placement,
                        add_special, num_special, special_placement,
                        capitalization_style):

    if not isinstance(num_words, int) or num_words < 2 or num_words > len(WORD_LIST):
        messagebox.showwarning("Input Error", f"Number of words should be an integer between 2 and {len(WORD_LIST)}.")
        return None
        
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

    if add_numbers:
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

    if add_special:
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

def estimate_strength_logic(passphrase):
    if not passphrase: return "N/A"
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
    
    num_separators = sum(1 for char in passphrase if char in COMMON_SEPARATORS_DISPLAY.values())
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