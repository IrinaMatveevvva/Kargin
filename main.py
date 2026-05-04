import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
from datetime import datetime

HISTORY_FILE = 'password_history.json'

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("600x550")

        self.history = self.load_history()
        self.setup_ui()

    def setup_ui(self):
        # --- Настройки пароля ---
        frame_settings = ttk.LabelFrame(self.root, text="Настройки пароля", padding=15)
        frame_settings.pack(padx=10, pady=10, fill="x")

        # Длина пароля
        ttk.Label(frame_settings, text="Длина пароля:").grid(row=0, column=0, sticky="w")
        self.length_var = tk.IntVar(value=12)
        self.scale_length = tk.Scale(frame_settings, from_=4, to=32, orient="horizontal", variable=self.length_var)
        self.scale_length.grid(row=0, column=1, padx=5, sticky="ew")
        
        self.lbl_length_num = ttk.Label(frame_settings, textvariable=self.length_var)
        self.lbl_length_num.grid(row=0, column=2, padx=5)

        # Чекбоксы символов
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=False)

        ttk.Checkbutton(frame_settings, text="Цифры (0-9)", variable=self.use_digits).grid(row=1, column=0, sticky="w", pady=5)
        ttk.Checkbutton(frame_settings, text="Буквы (a-z, A-Z)", variable=self.use_letters).grid(row=1, column=1, sticky="w")
        ttk.Checkbutton(frame_settings, text="Спецсимволы (!@#$)", variable=self.use_special).grid(row=1, column=2, sticky="w")

        # Кнопка генерации
        self.btn_generate = ttk.Button(frame_settings, text="Сгенерировать пароль", command=self.generate_password)
        self.btn_generate.grid(row=2, column=0, columnspan=3, pady=15)

        # Поле вывода результата
        self.entry_result = ttk.Entry(self.root, font=("Courier", 14), justify="center")
        self.entry_result.pack(padx=10, pady=5, fill="x")

        # --- История ---
        frame_hist = ttk.LabelFrame(self.root, text="История генераций", padding=10)
        frame_hist.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(frame_hist, columns=("date", "pass", "len"), show="headings")
        self.tree.heading("date", text="Дата и время")
        self.tree.heading("pass", text="Пароль")
        self.tree.heading("len", text="Длина")
        
        self.tree.column("len", width=50, anchor="center")
        self.tree.pack(fill="both", expand=True)

        self.refresh_table()

    def generate_password(self):
        length = self.length_var.get()
        
        # Валидация выбора типов символов
        chars = ""
        if self.use_digits.get(): chars += string.digits
        if self.use_letters.get(): chars += string.ascii_letters
        if self.use_special.get(): chars += string.punctuation

        if not chars:
            messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов!")
            return

        # Генерация
        password = "".join(random.choice(chars) for _ in range(length))
        
        # Отображение
        self.entry_result.delete(0, tk.END)
        self.entry_result.insert(0, password)

        # Сохранение в историю
        new_entry = {
            "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "password": password,
            "length": length
        }
        self.history.append(new_entry)
        self.save_history()
        self.refresh_table()

    def load_history(self):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_history(self):
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for h in reversed(self.history):
            self.tree.insert("", "end", values=(h['date'], h['password'], h['length']))

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()