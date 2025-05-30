import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter import messagebox
import random

from config import (
    WORD_LIST, COMMON_SEPARATORS_DISPLAY, CAPITALIZATION_OPTIONS_DISPLAY,
    PLACEMENT_OPTIONS_DISPLAY, TIPS
)
from logic import generate_passphrase_logic, estimate_strength_logic

class PassphraseApp:
    def __init__(self, root):
        self.root = root
        root.title("Secure Phrase Architect")
        root.geometry("600x700")
        root.configure(bg="#F0F0F0")

        self.default_font = tkfont.Font(family="Helvetica", size=10)
        self.label_font = tkfont.Font(family="Helvetica", size=10)
        self.header_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        self.result_font = tkfont.Font(family="Courier New", size=12)
        self.button_font = tkfont.Font(family="Helvetica", size=10, weight="bold")
        self.tip_font = tkfont.Font(family="Helvetica", size=9, slant="italic")

        style = ttk.Style()
        style.theme_use('clam')

        style.configure(".", font=self.default_font, background="#F0F0F0", foreground="#333333")
        style.configure("TFrame", background="#F0F0F0")
        style.configure("TLabel", background="#F0F0F0", foreground="#333333", font=self.label_font)
        style.configure("TLabelframe", background="#F0F0F0", bordercolor="#CCCCCC")
        style.configure("TLabelframe.Label", background="#F0F0F0", foreground="#222222", font=self.header_font)
        
        style.configure("TCheckbutton", background="#F0F0F0", foreground="#333333", font=self.label_font)
        style.map("TCheckbutton",
                  background=[('active', '#E0E0E0')])
        
        style.configure("TSpinbox", fieldbackground="#FFFFFF", foreground="#333333", borderwidth=1)
        style.configure("TCombobox", fieldbackground="#FFFFFF", foreground="#333333", selectbackground='#E0E0E0', selectforeground='#333333')
        style.map("TCombobox",
                  fieldbackground=[('readonly', '#FFFFFF')])

        style.configure("Accent.TButton",
                        font=self.button_font,
                        background="#007AFF",
                        foreground="white",
                        borderwidth=1,
                        padding=(10, 5))
        style.map("Accent.TButton",
                  background=[('active', '#0056B3'), ('pressed', '#004085')],
                  relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

        style.configure("Copy.TButton",
                        font=self.default_font,
                        background="#6c757d",
                        foreground="white",
                        padding=(5,3))
        style.map("Copy.TButton",
                  background=[('active', '#5a6268')])

        main_frame = ttk.Frame(root, padding="15")
        main_frame.pack(expand=True, fill=tk.BOTH)

        config_frame = ttk.LabelFrame(main_frame, text="Configuration Options", padding="15")
        config_frame.pack(fill=tk.X, pady=10)
        
        config_frame.columnconfigure(1, weight=1)

        r = 0
        ttk.Label(config_frame, text="Number of Words:").grid(row=r, column=0, sticky=tk.W, padx=5, pady=5)
        self.num_words_var = tk.IntVar(value=4)
        self.num_words_spinbox = ttk.Spinbox(config_frame, from_=2, to_=len(WORD_LIST), textvariable=self.num_words_var, width=7, font=self.default_font)
        self.num_words_spinbox.grid(row=r, column=1, sticky=tk.EW, padx=5, pady=5)
        r+=1

        ttk.Label(config_frame, text="Separator:").grid(row=r, column=0, sticky=tk.W, padx=5, pady=5)
        self.separator_var = tk.StringVar(value=list(COMMON_SEPARATORS_DISPLAY.keys())[0])
        self.separator_combo = ttk.Combobox(config_frame, textvariable=self.separator_var, values=list(COMMON_SEPARATORS_DISPLAY.keys()), state="readonly", width=20, font=self.default_font)
        self.separator_combo.grid(row=r, column=1, sticky=tk.EW, padx=5, pady=5)
        r+=1

        ttk.Label(config_frame, text="Capitalization:").grid(row=r, column=0, sticky=tk.W, padx=5, pady=5)
        self.capitalization_var = tk.StringVar(value=list(CAPITALIZATION_OPTIONS_DISPLAY.keys())[0])
        self.capitalization_combo = ttk.Combobox(config_frame, textvariable=self.capitalization_var, values=list(CAPITALIZATION_OPTIONS_DISPLAY.keys()), state="readonly", width=28, font=self.default_font)
        self.capitalization_combo.grid(row=r, column=1, sticky=tk.EW, padx=5, pady=5)
        r+=1

        self.add_numbers_var = tk.BooleanVar(value=False)
        self.add_numbers_check = ttk.Checkbutton(config_frame, text="Add Numbers", variable=self.add_numbers_var, command=self.toggle_number_options)
        self.add_numbers_check.grid(row=r, column=0, columnspan=2, sticky=tk.W, padx=5, pady=(10,2))
        r+=1

        self.num_numbers_label = ttk.Label(config_frame, text="Quantity:")
        self.num_numbers_label.grid(row=r, column=0, sticky=tk.W, padx=25, pady=2)
        self.num_numbers_var = tk.IntVar(value=1)
        self.num_numbers_spinbox = ttk.Spinbox(config_frame, from_=1, to_=5, textvariable=self.num_numbers_var, width=7, font=self.default_font)
        self.num_numbers_spinbox.grid(row=r, column=1, sticky=tk.EW, padx=5, pady=2)
        r+=1

        self.number_placement_label = ttk.Label(config_frame, text="Placement:")
        self.number_placement_label.grid(row=r, column=0, sticky=tk.W, padx=25, pady=2)
        self.number_placement_var = tk.StringVar(value=list(PLACEMENT_OPTIONS_DISPLAY.keys())[1])
        self.number_placement_combo = ttk.Combobox(config_frame, textvariable=self.number_placement_var, values=list(PLACEMENT_OPTIONS_DISPLAY.keys()), state="readonly", width=20, font=self.default_font)
        self.number_placement_combo.grid(row=r, column=1, sticky=tk.EW, padx=5, pady=2)
        r+=1
        
        self.add_special_var = tk.BooleanVar(value=False)
        self.add_special_check = ttk.Checkbutton(config_frame, text="Add Special Characters", variable=self.add_special_var, command=self.toggle_special_options)
        self.add_special_check.grid(row=r, column=0, columnspan=2, sticky=tk.W, padx=5, pady=(10,2))
        r+=1

        self.num_special_label = ttk.Label(config_frame, text="Quantity:")
        self.num_special_label.grid(row=r, column=0, sticky=tk.W, padx=25, pady=2)
        self.num_special_var = tk.IntVar(value=1)
        self.num_special_spinbox = ttk.Spinbox(config_frame, from_=1, to_=5, textvariable=self.num_special_var, width=7, font=self.default_font)
        self.num_special_spinbox.grid(row=r, column=1, sticky=tk.EW, padx=5, pady=2)
        r+=1

        self.special_placement_label = ttk.Label(config_frame, text="Placement:")
        self.special_placement_label.grid(row=r, column=0, sticky=tk.W, padx=25, pady=2)
        self.special_placement_var = tk.StringVar(value=list(PLACEMENT_OPTIONS_DISPLAY.keys())[1])
        self.special_placement_combo = ttk.Combobox(config_frame, textvariable=self.special_placement_var, values=list(PLACEMENT_OPTIONS_DISPLAY.keys()), state="readonly", width=20, font=self.default_font)
        self.special_placement_combo.grid(row=r, column=1, sticky=tk.EW, padx=5, pady=2)

        self.toggle_number_options()
        self.toggle_special_options()

        self.generate_button = ttk.Button(main_frame, text="Generate Secure Phrase", command=self.generate_and_display, style="Accent.TButton")
        self.generate_button.pack(pady=20, fill=tk.X, padx=20)

        result_frame = ttk.LabelFrame(main_frame, text="Generated Passphrase", padding="10")
        result_frame.pack(fill=tk.X, pady=10)

        self.passphrase_result_var = tk.StringVar()
        self.passphrase_result_entry = ttk.Entry(result_frame, textvariable=self.passphrase_result_var, state="readonly", font=self.result_font, justify='center')
        self.passphrase_result_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0,10), ipady=5)
        
        self.copy_button = ttk.Button(result_frame, text="Copy", command=self.copy_to_clipboard, width=8, style="Copy.TButton")
        self.copy_button.pack(side=tk.RIGHT)

        info_frame = ttk.Frame(main_frame, padding="10")
        info_frame.pack(fill=tk.X, pady=10)

        self.strength_label_var = tk.StringVar(value="Strength: N/A")
        self.strength_label = ttk.Label(info_frame, textvariable=self.strength_label_var, font=self.label_font)
        self.strength_label.pack(side=tk.LEFT, padx=5)

        self.tip_label_var = tk.StringVar(value="Click 'Generate' for a new passphrase and security tip!")
        ttk.Label(info_frame, textvariable=self.tip_label_var, wraplength=550, justify=tk.LEFT, font=self.tip_font, foreground="#555555").pack(side=tk.RIGHT, padx=5, expand=True, fill=tk.X)

    def set_strength_color(self, strength_text):
        color = "#333333"
        if "Weak" in strength_text: color = "#D9534F"
        elif "Fair" in strength_text: color = "#F0AD4E"
        elif "Good" in strength_text: color = "#5CB85C"
        elif "Strong" in strength_text: color = "#0275D8"
        elif "Very Strong" in strength_text: color = "#01579B"
        self.strength_label.configure(foreground=color)

    def toggle_number_options(self):
        state = tk.NORMAL if self.add_numbers_var.get() else tk.DISABLED
        for widget in [self.num_numbers_label, self.num_numbers_spinbox, self.number_placement_label, self.number_placement_combo]:
            widget.configure(state=state)

    def toggle_special_options(self):
        state = tk.NORMAL if self.add_special_var.get() else tk.DISABLED
        for widget in [self.num_special_label, self.num_special_spinbox, self.special_placement_label, self.special_placement_combo]:
            widget.configure(state=state)

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
            self.set_strength_color("Error")
            return

        self.passphrase_result_var.set(generated_pass)
        strength = estimate_strength_logic(generated_pass)
        self.strength_label_var.set(f"Strength: {strength}")
        self.set_strength_color(strength)
        self.tip_label_var.set(random.choice(TIPS))

    def copy_to_clipboard(self):
        passphrase = self.passphrase_result_var.get()
        if passphrase:
            self.root.clipboard_clear()
            self.root.clipboard_append(passphrase)
            original_text = self.copy_button.cget("text")
            self.copy_button.configure(text="Copied!")
            self.root.after(1500, lambda: self.copy_button.configure(text=original_text))
        else:
            messagebox.showwarning("Nothing to Copy", "Generate a passphrase first.")