import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter import messagebox
import random
import webbrowser # For opening URLs

from config import (
    WORD_LIST, COMMON_SEPARATORS_DISPLAY, CAPITALIZATION_OPTIONS_DISPLAY,
    PLACEMENT_OPTIONS_DISPLAY, TIPS
)
from logic import generate_passphrase_logic, estimate_strength_logic
import storage # Import the new storage module

class PassphraseApp:
    def __init__(self, root):
        self.root = root
        root.title("Secure Phrase Architect")
        root.geometry("750x850") # Increased size for new elements
        root.configure(bg="#F0F0F0")

        self.default_font = tkfont.Font(family="Helvetica", size=10)
        self.label_font = tkfont.Font(family="Helvetica", size=10)
        self.header_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        self.result_font = tkfont.Font(family="Courier New", size=12)
        self.button_font = tkfont.Font(family="Helvetica", size=10, weight="bold")
        self.tip_font = tkfont.Font(family="Helvetica", size=9, slant="italic")
        self.treeview_font = tkfont.Font(family="Helvetica", size=9)


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

        style.configure("Save.TButton",
                        font=self.button_font,
                        background="#28a745", # Green for save
                        foreground="white",
                        borderwidth=1,
                        padding=(10, 5))
        style.map("Save.TButton",
                  background=[('active', '#218838'), ('pressed', '#1e7e34')],
                  relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

        style.configure("Action.TButton",
                        font=self.default_font,
                        background="#6c757d",
                        foreground="white",
                        padding=(5,3))
        style.map("Action.TButton",
                  background=[('active', '#5a6268')])

        main_frame = ttk.Frame(root, padding="15")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # --- Configuration Frame (Top Left) ---
        top_left_frame = ttk.Frame(main_frame)
        top_left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10), anchor='nw')
        
        config_frame = ttk.LabelFrame(top_left_frame, text="Configuration Options", padding="15")
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

        self.generate_button = ttk.Button(top_left_frame, text="Generate Secure Phrase", command=self.generate_and_display, style="Accent.TButton")
        self.generate_button.pack(pady=(15,5), fill=tk.X, padx=20)

        result_frame = ttk.LabelFrame(top_left_frame, text="Generated Passphrase", padding="10")
        result_frame.pack(fill=tk.X, pady=5, padx=20)
        self.passphrase_result_var = tk.StringVar()
        self.passphrase_result_entry = ttk.Entry(result_frame, textvariable=self.passphrase_result_var, state="readonly", font=self.result_font, justify='center')
        self.passphrase_result_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0,10), ipady=5)
        self.copy_button = ttk.Button(result_frame, text="Copy", command=self.copy_to_clipboard, width=8, style="Action.TButton")
        self.copy_button.pack(side=tk.RIGHT)

        self.strength_label_var = tk.StringVar(value="Strength: N/A")
        self.strength_label = ttk.Label(top_left_frame, textvariable=self.strength_label_var, font=self.label_font)
        self.strength_label.pack(pady=(5,0), padx=20, anchor='w')
        self.tip_label_var = tk.StringVar(value="Click 'Generate' for a new passphrase and security tip!")
        ttk.Label(top_left_frame, textvariable=self.tip_label_var, wraplength=300, justify=tk.LEFT, font=self.tip_font, foreground="#555555").pack(pady=5, padx=20, anchor='w')


        # --- Storage Association Frame (Below Result) ---
        storage_input_frame = ttk.LabelFrame(top_left_frame, text="Store with Website", padding="10")
        storage_input_frame.pack(fill=tk.X, pady=10, padx=20)

        ttk.Label(storage_input_frame, text="Website Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.website_name_var = tk.StringVar()
        self.website_name_entry = ttk.Entry(storage_input_frame, textvariable=self.website_name_var, width=30)
        self.website_name_entry.grid(row=0, column=1, sticky=tk.EW, pady=2)

        ttk.Label(storage_input_frame, text="Website URL (Optional):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.website_url_var = tk.StringVar()
        self.website_url_entry = ttk.Entry(storage_input_frame, textvariable=self.website_url_var, width=30)
        self.website_url_entry.grid(row=1, column=1, sticky=tk.EW, pady=2)
        storage_input_frame.columnconfigure(1, weight=1)

        self.save_button = ttk.Button(storage_input_frame, text="Save Passphrase", command=self.save_passphrase_entry, style="Save.TButton")
        self.save_button.grid(row=2, column=0, columnspan=2, pady=(10,0), sticky=tk.EW)


        # --- Stored Passphrases Display (Right Side) ---
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, anchor='ne')

        stored_frame = ttk.LabelFrame(right_frame, text="Stored Passphrases", padding="10")
        stored_frame.pack(expand=True, fill=tk.BOTH, pady=10)

        tree_cols = ("Website Name", "URL") # Not showing passphrase directly in tree
        self.passphrase_tree = ttk.Treeview(stored_frame, columns=tree_cols, show="headings", height=15)
        self.passphrase_tree.heading("Website Name", text="Website Name")
        self.passphrase_tree.heading("URL", text="Website URL")
        self.passphrase_tree.column("Website Name", width=150, anchor='w')
        self.passphrase_tree.column("URL", width=200, anchor='w')
        
        ysb = ttk.Scrollbar(stored_frame, orient=tk.VERTICAL, command=self.passphrase_tree.yview)
        self.passphrase_tree.configure(yscrollcommand=ysb.set)
        self.passphrase_tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        ysb.pack(side=tk.RIGHT, fill=tk.Y)

        self.passphrase_tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        # --- Action Buttons for Stored Passphrases ---
        stored_actions_frame = ttk.Frame(right_frame)
        stored_actions_frame.pack(fill=tk.X, pady=5)

        self.load_stored_button = ttk.Button(stored_actions_frame, text="Refresh List", command=self.load_and_display_stored, style="Action.TButton")
        self.load_stored_button.pack(side=tk.LEFT, padx=2)
        
        self.copy_stored_button = ttk.Button(stored_actions_frame, text="Copy Pwd", command=self.copy_selected_stored_passphrase, style="Action.TButton", state=tk.DISABLED)
        self.copy_stored_button.pack(side=tk.LEFT, padx=2)

        self.open_url_button = ttk.Button(stored_actions_frame, text="Open URL", command=self.open_selected_url, style="Action.TButton", state=tk.DISABLED)
        self.open_url_button.pack(side=tk.LEFT, padx=2)

        self.delete_entry_button = ttk.Button(stored_actions_frame, text="Delete Entry", command=self.delete_selected_entry, style="Action.TButton", state=tk.DISABLED)
        self.delete_entry_button.pack(side=tk.LEFT, padx=2)

        self.load_and_display_stored() # Initial load

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
            self.root.after(1500, lambda: self.copy_button.configure(text="Copy"))
        else:
            messagebox.showwarning("Nothing to Copy", "Generate a passphrase first.")

    def save_passphrase_entry(self):
        name = self.website_name_var.get().strip()
        url = self.website_url_var.get().strip()
        passphrase = self.passphrase_result_var.get()

        if not name:
            messagebox.showerror("Input Error", "Website Name is required to save.")
            return
        if not passphrase:
            messagebox.showerror("Input Error", "Generate a passphrase first to save.")
            return
        
        # SECURITY WARNING
        warn_msg = "SECURITY WARNING:\nPassphrases will be stored in a plain text JSON file (passphrases_store.json) in the application directory. This is NOT secure for real-world use.\n\nDo you want to proceed with saving?"
        if not messagebox.askyesno("Plaintext Storage Confirmation", warn_msg, icon='warning'):
            return

        if storage.add_passphrase_entry(name, url, passphrase):
            messagebox.showinfo("Success", f"Passphrase for '{name}' saved.")
            self.website_name_var.set("")
            self.website_url_var.set("")
            self.load_and_display_stored()
        else:
            messagebox.showerror("Save Error", f"Could not save passphrase for '{name}'. Name might already exist or file error.")

    def load_and_display_stored(self):
        for i in self.passphrase_tree.get_children():
            self.passphrase_tree.delete(i)
        
        entries = storage.load_passphrases()
        for entry in entries:
            # We store the full entry data (including passphrase) with the item ID in the tree
            # but only display name and URL.
            self.passphrase_tree.insert("", tk.END, iid=entry.get("name"), # Using name as IID (assumes unique)
                                        values=(entry.get("name", ""), entry.get("url", "")), 
                                        tags=(entry.get("passphrase", ""),)) # Store passphrase in tags

    def on_tree_select(self, event):
        selected_item = self.passphrase_tree.focus() # Gets the IID of the selected item
        if selected_item:
            self.copy_stored_button.config(state=tk.NORMAL)
            self.delete_entry_button.config(state=tk.NORMAL)
            values = self.passphrase_tree.item(selected_item, "values")
            if values and values[1]: # If URL column has a value
                self.open_url_button.config(state=tk.NORMAL)
            else:
                self.open_url_button.config(state=tk.DISABLED)
        else:
            self.copy_stored_button.config(state=tk.DISABLED)
            self.open_url_button.config(state=tk.DISABLED)
            self.delete_entry_button.config(state=tk.DISABLED)

    def copy_selected_stored_passphrase(self):
        selected_item_iid = self.passphrase_tree.focus()
        if not selected_item_iid:
            messagebox.showwarning("Selection Error", "No entry selected.")
            return
        
        # Retrieve passphrase from tags
        tags = self.passphrase_tree.item(selected_item_iid, "tags")
        if tags and tags[0]:
            passphrase_to_copy = tags[0]
            self.root.clipboard_clear()
            self.root.clipboard_append(passphrase_to_copy)
            messagebox.showinfo("Copied", "Stored passphrase copied to clipboard!")
        else:
            messagebox.showerror("Error", "Could not retrieve passphrase for selected item.")


    def open_selected_url(self):
        selected_item_iid = self.passphrase_tree.focus()
        if not selected_item_iid:
            messagebox.showwarning("Selection Error", "No entry selected.")
            return
        
        item_values = self.passphrase_tree.item(selected_item_iid, "values")
        url = item_values[1] if len(item_values) > 1 else None

        if url:
            if not (url.startswith("http://") or url.startswith("https://")):
                url = "http://" + url # Basic protocol addition
            try:
                webbrowser.open_new_tab(url)
            except Exception as e:
                messagebox.showerror("URL Error", f"Could not open URL: {url}\nError: {e}")
        else:
            messagebox.showinfo("No URL", "No URL associated with this entry.")
            
    def delete_selected_entry(self):
        selected_item_iid = self.passphrase_tree.focus() # This is the 'name'
        if not selected_item_iid:
            messagebox.showwarning("Selection Error", "No entry selected.")
            return

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the entry for '{selected_item_iid}'?"):
            if storage.delete_passphrase_entry(selected_item_iid):
                messagebox.showinfo("Deleted", f"Entry '{selected_item_iid}' deleted.")
                self.load_and_display_stored()
                # Disable buttons again after deletion as selection is lost
                self.copy_stored_button.config(state=tk.DISABLED)
                self.open_url_button.config(state=tk.DISABLED)
                self.delete_entry_button.config(state=tk.DISABLED)
            else:
                messagebox.showerror("Delete Error", f"Could not delete entry '{selected_item_iid}'.")