import random
import string
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

WORD_LIST = [
    "apple", "banana", "cloud", "dolphin", "forest", "guitar", "mountain", "ocean",
    "puzzle", "robot", "shadow", "galaxy", "wizard", "mystery", "journey", "crystal",
    "village", "spirit", "quasar", "nebula", "planet", "comet", "aurora", "eclipse",
    "volcano", "canyon", "meadow", "island", "lagoon", "harbor", "beacon", "cipher"
]
COMMON_SEPARATORS_DISPLAY = {
    "Hyphen (-)": "-",
    "Underscore (_)": "_",
    "Period (.)": ".",
    "Space ( )": " ",
    "Tilde (~)": "~"
}
SPECIAL_CHARACTERS = "!@#$%^&*()_+-=[]{}|;:,.<>?"

CAPITALIZATION_OPTIONS_DISPLAY = {
    "None (all lowercase)": "n",
    "Title Case (Like This)": "t",
    "Sentence case (First word capitalized)": "s",
    "Random word FULLY capitalized": "r"
}

PLACEMENT_OPTIONS_DISPLAY = {
    "Beginning": "b",
    "End": "e",
    "Intersperse (Simplified)": "i"
}

TIPS = [
    "Tip: Longer passphrases are generally stronger and harder to crack.",
    "Tip: Using a mix of uppercase, lowercase, numbers, and symbols increases complexity.",
    "Tip: Avoid common words or easily guessable patterns.",
    "Tip: For critical accounts, consider using a unique passphrase for each.",
    "Tip: Store your passphrases securely using a password manager."
]

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

class PassphraseApp:
    def __init__(self, root):
        self.root = root
        root.title("Secure Phrase Architect")
        root.geometry("550x650")

        style = ttk.Style()
        style.theme_use('clam')

        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(config_frame, text="Number of Words:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.num_words_var = tk.IntVar(value=4)
        self.num_words_spinbox = ttk.Spinbox(config_frame, from_=2, to_=len(WORD_LIST), textvariable=self.num_words_var, width=5)
        self.num_words_spinbox.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Label(config_frame, text="Separator:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.separator_var = tk.StringVar(value=list(COMMON_SEPARATORS_DISPLAY.keys())[0])
        self.separator_combo = ttk.Combobox(config_frame, textvariable=self.separator_var, values=list(COMMON_SEPARATORS_DISPLAY.keys()), state="readonly", width=18)
        self.separator_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Label(config_frame, text="Capitalization:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.capitalization_var = tk.StringVar(value=list(CAPITALIZATION_OPTIONS_DISPLAY.keys())[0])
        self.capitalization_combo = ttk.Combobox(config_frame, textvariable=self.capitalization_var, values=list(CAPITALIZATION_OPTIONS_DISPLAY.keys()), state="readonly", width=25)
        self.capitalization_combo.grid(row=2, column=1, columnspan=2, sticky=tk.W, padx=5, pady=2)

        self.add_numbers_var = tk.BooleanVar(value=False)
        self.add_numbers_check = ttk.Checkbutton(config_frame, text="Add Numbers", variable=self.add_numbers_var, command=self.toggle_number_options)
        self.add_numbers_check.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)

        self.num_numbers_label = ttk.Label(config_frame, text="Quantity:")
        self.num_numbers_label.grid(row=4, column=0, sticky=tk.W, padx=25, pady=2)
        self.num_numbers_var = tk.IntVar(value=1)
        self.num_numbers_spinbox = ttk.Spinbox(config_frame, from_=1, to_=5, textvariable=self.num_numbers_var, width=5)
        self.num_numbers_spinbox.grid(row=4, column=1, sticky=tk.W, padx=5, pady=2)

        self.number_placement_label = ttk.Label(config_frame, text="Placement:")
        self.number_placement_label.grid(row=5, column=0, sticky=tk.W, padx=25, pady=2)
        self.number_placement_var = tk.StringVar(value=list(PLACEMENT_OPTIONS_DISPLAY.keys())[0])
        self.number_placement_combo = ttk.Combobox(config_frame, textvariable=self.number_placement_var, values=list(PLACEMENT_OPTIONS_DISPLAY.keys()), state="readonly", width=18)
        self.number_placement_combo.grid(row=5, column=1, sticky=tk.W, padx=5, pady=2)
        
        self.add_special_var = tk.BooleanVar(value=False)
        self.add_special_check = ttk.Checkbutton(config_frame, text="Add Special Characters", variable=self.add_special_var, command=self.toggle_special_options)
        self.add_special_check.grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)

        self.num_special_label = ttk.Label(config_frame, text="Quantity:")
        self.num_special_label.grid(row=7, column=0, sticky=tk.W, padx=25, pady=2)
        self.num_special_var = tk.IntVar(value=1)
        self.num_special_spinbox = ttk.Spinbox(config_frame, from_=1, to_=5, textvariable=self.num_special_var, width=5)
        self.num_special_spinbox.grid(row=7, column=1, sticky=tk.W, padx=5, pady=2)

        self.special_placement_label = ttk.Label(config_frame, text="Placement:")
        self.special_placement_label.grid(row=8, column=0, sticky=tk.W, padx=25, pady=2)
        self.special_placement_var = tk.StringVar(value=list(PLACEMENT_OPTIONS_DISPLAY.keys())[0])
        self.special_placement_combo = ttk.Combobox(config_frame, textvariable=self.special_placement_var, values=list(PLACEMENT_OPTIONS_DISPLAY.keys()), state="readonly", width=18)
        self.special_placement_combo.grid(row=8, column=1, sticky=tk.W, padx=5, pady=2)

        self.toggle_number_options()
        self.toggle_special_options()

        self.generate_button = ttk.Button(main_frame, text="Generate Passphrase", command=self.generate_and_display, style="Accent.TButton")
        self.generate_button.pack(pady=15)
        style.configure("Accent.TButton", font=("Helvetica", 10, "bold"))

        result_frame = ttk.LabelFrame(main_frame, text="Generated Passphrase", padding="10")
        result_frame.pack(fill=tk.X, pady=5)

        self.passphrase_result_var = tk.StringVar()
        self.passphrase_result_entry = ttk.Entry(result_frame, textvariable=self.passphrase_result_var, state="readonly", font=("Courier", 11))
        self.passphrase_result_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0,5))
        
        self.copy_button = ttk.Button(result_frame, text="Copy", command=self.copy_to_clipboard, width=8)
        self.copy_button.pack(side=tk.RIGHT)

        info_frame = ttk.Frame(main_frame, padding="5")
        info_frame.pack(fill=tk.X, pady=5)

        self.strength_label_var = tk.StringVar(value="Strength: N/A")
        ttk.Label(info_frame, textvariable=self.strength_label_var, font=("Helvetica", 10, "italic")).pack(side=tk.LEFT, padx=5)

        self.tip_label_var = tk.StringVar(value="Tip: Click 'Generate' for a new passphrase and tip!")
        ttk.Label(info_frame, textvariable=self.tip_label_var, wraplength=500, justify=tk.LEFT, font=("Helvetica", 9)).pack(side=tk.RIGHT, padx=5, expand=True, fill=tk.X)


    def toggle_number_options(self):
        state = tk.NORMAL if self.add_numbers_var.get() else tk.DISABLED
        self.num_numbers_label.config(state=state)
        self.num_numbers_spinbox.config(state=state)
        self.number_placement_label.config(state=state)
        self.number_placement_combo.config(state=state)

    def toggle_special_options(self):
        state = tk.NORMAL if self.add_special_var.get() else tk.DISABLED
        self.num_special_label.config(state=state)
        self.num_special_spinbox.config(state=state)
        self.special_placement_label.config(state=state)
        self.special_placement_combo.config(state=state)

    def generate_and_display(self):
        try:
            num_words = self.num_words_var.get()
        except tk.TclError:
            messagebox.showerror("Input Error", "Number of words must be a valid integer.")
            return

        separator_display = self.separator_var.get()
        separator = COMMON_SEPARATORS_DISPLAY[separator_display]
        
        capitalization_display = self.capitalization_var.get()
        capitalization_style = CAPITALIZATION_OPTIONS_DISPLAY[capitalization_display]

        add_numbers = self.add_numbers_var.get()
        num_numbers = self.num_numbers_var.get() if add_numbers else 0
        number_placement_display = self.number_placement_var.get()
        number_placement = PLACEMENT_OPTIONS_DISPLAY[number_placement_display] if add_numbers else ''

        add_special = self.add_special_var.get()
        num_special = self.num_special_var.get() if add_special else 0
        special_placement_display = self.special_placement_var.get()
        special_placement = PLACEMENT_OPTIONS_DISPLAY[special_placement_display] if add_special else ''

        generated_pass = generate_passphrase_logic(
            num_words, separator,
            add_numbers, num_numbers, number_placement,
            add_special, num_special, special_placement,
            capitalization_style
        )
        
        if generated_pass is None:
            self.passphrase_result_var.set("")
            self.strength_label_var.set("Strength: Error")
            return

        self.passphrase_result_var.set(generated_pass)
        strength = estimate_strength_logic(generated_pass)
        self.strength_label_var.set(f"Strength: {strength}")
        self.tip_label_var.set(random.choice(TIPS))

    def copy_to_clipboard(self):
        passphrase = self.passphrase_result_var.get()
        if passphrase:
            self.root.clipboard_clear()
            self.root.clipboard_append(passphrase)
            messagebox.showinfo("Copied", "Passphrase copied to clipboard!")
        else:
            messagebox.showwarning("Nothing to Copy", "Generate a passphrase first.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PassphraseApp(root)
    root.mainloop()