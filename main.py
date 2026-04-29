import json
import random
import os
from tkinter import *
from tkinter import ttk, messagebox

HISTORY_FILE = "quotes_history.json"
QUOTES_FILE = "quotes_data.json"

DEFAULT_QUOTES = [
    {"text": "Гений и злодейство — две вещи несовместные", "author": "Александр Пушкин", "theme": "Мораль"},
    {"text": "Береги честь смолоду", "author": "Александр Пушкин", "theme": "Мудрость"},
    {"text": "Весь мир — театр, а люди в нём — актёры", "author": "Уильям Шекспир", "theme": "Жизнь"},
    {"text": "Человек создан для счастья, как птица для полёта", "author": "Владимир Короленко", "theme": "Счастье"},
    {"text": "Кто много живёт, тот много видит", "author": "Михаил Лермонтов", "theme": "Жизнь"},
    {"text": "Сила в правде", "author": "Александр Невский", "theme": "Мораль"},
    {"text": "Ум без книги, как птица без крыльев", "author": "Русская пословица", "theme": "Знания"},
    {"text": "Век живи — век учись", "author": "Русская пословица", "theme": "Знания"},
    {"text": "Лучше один раз увидеть, чем сто раз услышать", "author": "Русская пословица", "theme": "Мудрость"},
    {"text": "Счастье — это когда тебя понимают", "author": "Александр Грин", "theme": "Счастье"},
    {"text": "Не бойся медленного пути — бойся стоять на месте", "author": "Китайская мудрость", "theme": "Мотивация"},
    {"text": "Терпение и труд всё перетрут", "author": "Русская пословица", "theme": "Мотивация"},
]

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор цитат")
        self.root.geometry("700x600")
        self.root.resizable(True, True)

        self.quotes = self.load_quotes()
        self.history = self.load_history()

        self.setup_ui()

        self.update_filters()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_quotes(self):
        if os.path.exists(QUOTES_FILE):
            with open(QUOTES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        else:

            with open(QUOTES_FILE, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_QUOTES, f, ensure_ascii=False, indent=4)
            return DEFAULT_QUOTES.copy()

    def save_quotes(self):
        with open(QUOTES_FILE, "w", encoding="utf-8") as f:
            json.dump(self.quotes, f, ensure_ascii=False, indent=4)

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_history(self):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def setup_ui(self):
        main_frame = Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=BOTH, expand=True)

        quote_frame = LabelFrame(main_frame, text="Случайная цитата", padx=10, pady=10, font=("Arial", 12, "bold"))
        quote_frame.pack(fill=X, pady=(0, 10))

        self.quote_text_label = Label(quote_frame, text="Нажмите кнопку \"Сгенерировать\"", 
                                      wraplength=650, font=("Arial", 11, "italic"), justify=LEFT, fg="gray")
        self.quote_text_label.pack(fill=X, pady=5)

        self.quote_author_label = Label(quote_frame, text="", font=("Arial", 10), fg="darkblue")
        self.quote_author_label.pack(fill=X)

        self.quote_theme_label = Label(quote_frame, text="", font=("Arial", 9), fg="green")
        self.quote_theme_label.pack(fill=X)

        self.generate_btn = Button(quote_frame, text="Сгенерировать цитату", command=self.generate_random_quote,
                                   bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), cursor="hand2")
        self.generate_btn.pack(pady=10)

        filter_frame = LabelFrame(main_frame, text="Фильтрация истории", padx=10, pady=10)
        filter_frame.pack(fill=X, pady=(0, 10))

        filter_row = Frame(filter_frame)
        filter_row.pack(fill=X)

        Label(filter_row, text="Автор:").pack(side=LEFT, padx=(0, 5))
        self.author_filter = ttk.Combobox(filter_row, state="readonly", width=20)
        self.author_filter.pack(side=LEFT, padx=(0, 15))
        self.author_filter.bind("<<ComboboxSelected>>", lambda e: self.update_history_display())

        Label(filter_row, text="Тема:").pack(side=LEFT, padx=(0, 5))
        self.theme_filter = ttk.Combobox(filter_row, state="readonly", width=20)
        self.theme_filter.pack(side=LEFT)
        self.theme_filter.bind("<<ComboboxSelected>>", lambda e: self.update_history_display())

        Button(filter_row, text="Сбросить фильтры", command=self.reset_filters, cursor="hand2").pack(side=LEFT, padx=(15, 0))

        add_frame = LabelFrame(main_frame, text="Добавить новую цитату", padx=10, pady=10)
        add_frame.pack(fill=X, pady=(0, 10))

        Label(add_frame, text="Текст цитаты:").pack(anchor=W)
        self.new_text = Text(add_frame, height=3, width=70)
        self.new_text.pack(fill=X, pady=(0, 5))

        row1 = Frame(add_frame)
        row1.pack(fill=X, pady=2)
        Label(row1, text="Автор:").pack(side=LEFT, padx=(0, 5))
        self.new_author = Entry(row1, width=30)
        self.new_author.pack(side=LEFT, padx=(0, 15))
        Label(row1, text="Тема:").pack(side=LEFT, padx=(0, 5))
        self.new_theme = Entry(row1, width=20)
        self.new_theme.pack(side=LEFT)

        Button(add_frame, text="➕ Добавить цитату", command=self.add_quote, bg="#2196F3", fg="white", cursor="hand2").pack(pady=5)

        history_frame = LabelFrame(main_frame, text="История сгенерированных цитат", padx=10, pady=10)
        history_frame.pack(fill=BOTH, expand=True)

        scrollbar = Scrollbar(history_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.history_listbox = Listbox(history_frame, yscrollcommand=scrollbar.set, font=("Arial", 9), 
                                       height=10, selectmode=SINGLE)
        self.history_listbox.pack(fill=BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)

        self.info_label = Label(main_frame, text="", font=("Arial", 8), fg="gray")
        self.info_label.pack()

    def update_filters(self):
        authors = sorted(set(q["author"] for q in self.quotes))
        themes = sorted(set(q["theme"] for q in self.quotes))

        self.author_filter['values'] = ["Все"] + authors
        self.theme_filter['values'] = ["Все"] + themes

        if not self.author_filter.get():
            self.author_filter.set("Все")
        if not self.theme_filter.get():
            self.theme_filter.set("Все")
    
    def reset_filters(self):
        self.author_filter.set("Все")
        self.theme_filter.set("Все")
        self.update_history_display()
    
    def generate_random_quote(self):
        if not self.quotes:
            messagebox.showwarning("Нет цитат", "Список цитат пуст. Добавьте несколько цитат.")
            return

        random_quote = random.choice(self.quotes)

        self.quote_text_label.config(text=f"❝ {random_quote['text']} ❞", fg="black")
        self.quote_author_label.config(text=f"— {random_quote['author']}")
        self.quote_theme_label.config(text=f"Тема: {random_quote['theme']}")

        from datetime import datetime
        quote_entry = {
            "text": random_quote['text'],
            "author": random_quote['author'],
            "theme": random_quote['theme'],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.insert(0, quote_entry)
        self.save_history()
        self.update_history_display()

        self.info_label.config(text=f"Всего в истории: {len(self.history)} цитат")

    def update_history_display(self):
        self.history_listbox.delete(0, END)

        author_filter = self.author_filter.get()
        theme_filter = self.theme_filter.get()

        filtered_history = []
        for item in self.history:
            if author_filter != "Все" and item['author'] != author_filter:
                continue
            if theme_filter != "Все" and item['theme'] != theme_filter:
                continue
            filtered_history.append(item)

        if not filtered_history:
            self.history_listbox.insert(END, "Нет цитат в истории с выбранными фильтрами")
        else:
            for item in filtered_history:
                display_text = f"{item['timestamp']} — {item['author']}: «{item['text'][:50]}»"
                if len(item['text']) > 50:
                    display_text += "..."
                display_text += f" (Тема: {item['theme']})"
                self.history_listbox.insert(END, display_text)

        self.info_label.config(text=f"Показано: {len(filtered_history)} из {len(self.history)} цитат")

    def add_quote(self):
        text = self.new_text.get("1.0", END).strip()
        author = self.new_author.get().strip()
        theme = self.new_theme.get().strip()

        if not text:
            messagebox.showerror("Ошибка", "Текст цитаты не может быть пустым!")
            return
        if not author:
            messagebox.showerror("Ошибка", "Автор не может быть пустым!")
            return
        if not theme:
            messagebox.showerror("Ошибка", "Тема не может быть пустой!")
            return

        new_quote = {
            "text": text,
            "author": author,
            "theme": theme
        }
        self.quotes.append(new_quote)
        self.save_quotes()

        self.new_text.delete("1.0", END)
        self.new_author.delete(0, END)
        self.new_theme.delete(0, END)

        self.update_filters()
        
        messagebox.showinfo("Успех", f"Цитата от {author} добавлена!")
    
    def on_closing(self):
        self.save_history()
        self.save_quotes()
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    app = QuoteGenerator(root)
    root.mainloop()
