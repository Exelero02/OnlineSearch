import tkinter as tk
from tkinter import scrolledtext, messagebox
import wikipediaapi
import pymongo
import datetime
from datetime import timezone
from pymongo import MongoClient


class WikipediaSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wikipedia Searcher")
        self.root.geometry("1000x800")
        self.day_mode = True
        self.setup_gui()
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['wikipedia_search_history']
        self.collection = self.db['searches']

    def setup_gui(self):

        self.day_mode_colors = {
            "bg_main_frame": "#303030",
            "bg_search_frame": "#f0f0f0",
            "bg_label": "#f0f0f0",
            "fg_label": "#333333",
            "bg_entry": "white",
            "fg_entry": "black",
            "bg_button": "#4caf50",
            "fg_button": "white",
            "bg_result_frame": "#f0f0f0",
            "fg_result_text": "#333333",
            "highlight_bg": "#000000",
            "text_bg": "#f0f0f0",
            "text_fg": "#333333"
        }

        self.night_mode_colors = {
            "bg_main_frame": "#000000",
            "bg_search_frame": "#333333",
            "bg_label": "#333333",
            "fg_label": "white",
            "bg_entry": "#333333",
            "fg_entry": "white",
            "bg_button": "#333333",
            "fg_button": "white",
            "bg_result_frame": "#333333",
            "fg_result_text": "white",
            "highlight_bg": "#ffffff",
            "text_bg": "#000000",
            "text_fg": "white"
        }

        self.main_frame = tk.Frame(self.root, bg=self.day_mode_colors["bg_main_frame"], bd=10,
                                   highlightbackground=self.day_mode_colors["highlight_bg"], highlightthickness=1)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.search_frame = tk.Frame(self.main_frame, bg=self.day_mode_colors["bg_search_frame"], pady=20, padx=30,
                                     bd=0, highlightbackground=self.day_mode_colors["highlight_bg"],
                                     highlightthickness=1)
        self.search_frame.pack(pady=(30, 20), padx=20, fill=tk.BOTH)

        self.label = tk.Label(self.search_frame, text="Online Searcher", font=("Arial", 24, "bold"),
                              fg=self.day_mode_colors["fg_label"], bg=self.day_mode_colors["bg_label"])
        self.label.grid(row=0, column=0, columnspan=3, padx=(20, 10), pady=(10, 20), sticky="n")  # Adjusted padx

        self.entry = tk.Entry(self.search_frame, width=50, font=("Arial", 14), bg=self.day_mode_colors["bg_entry"],
                              fg=self.day_mode_colors["fg_entry"])
        self.entry.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), ipady=10, sticky="ew")
        self.entry.bind('<Return>', lambda event: self.search_wikipedia())  # Bind Enter key press to search function

        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search_wikipedia,
                                       font=("Arial", 14, "bold"),
                                       bg=self.day_mode_colors["bg_button"], fg=self.day_mode_colors["fg_button"],
                                       padx=20, bd=0, relief=tk.FLAT, activebackground="#666666",
                                       activeforeground="white")
        self.search_button.grid(row=1, column=2, padx=10, pady=(0, 10), ipady=7, sticky="w")

        self.mode_button = tk.Button(self.search_frame, text="Night Mode", command=self.toggle_mode,
                                     font=("Arial", 14, "bold"),
                                     bg=self.day_mode_colors["bg_button"], fg=self.day_mode_colors["fg_button"],
                                     bd=0, relief=tk.FLAT, width=10)
        self.mode_button.grid(row=0, column=2, padx=(5, 20), pady=(10, 20), sticky="e")

        self.result_frame = tk.Frame(self.main_frame, bg=self.day_mode_colors["bg_result_frame"], padx=20, pady=20,
                                     bd=0, highlightbackground=self.day_mode_colors["highlight_bg"],
                                     highlightthickness=1)
        self.result_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.text = scrolledtext.ScrolledText(self.result_frame, wrap=tk.WORD, font=("Arial", 14),
                                              bg=self.day_mode_colors["bg_result_frame"],
                                              fg=self.day_mode_colors["fg_result_text"], bd=0)
        self.text.pack(fill=tk.BOTH, expand=True)

        self.text.bind("<Up>", lambda event: self.scroll_text(-1))
        self.text.bind("<Down>", lambda event: self.scroll_text(1))

        self.text.config(state=tk.DISABLED)

        self.history_button = tk.Button(self.search_frame, text="Show History", command=self.show_search_history,
                                        font=("Arial", 14, "bold"),
                                        bg=self.day_mode_colors["bg_button"], fg=self.day_mode_colors["fg_button"],

                                        bd=0, relief=tk.FLAT, width=10)
        self.history_button.grid(row=2, column=2, padx=(5, 20), pady=(10, 20), sticky="e")

    def toggle_mode(self):
        if self.day_mode:
            self.apply_night_mode()
        else:
            self.apply_day_mode()
        self.update_history_button_color()
        self.day_mode = not self.day_mode

    def update_history_button_color(self):
        current_bg_color = self.night_mode_colors["bg_button"] if self.day_mode else self.day_mode_colors["bg_button"]
        current_fg_color = self.night_mode_colors["fg_button"] if self.day_mode else self.day_mode_colors["fg_button"]
        self.history_button.config(bg=current_bg_color, fg=current_fg_color)

    def apply_day_mode(self):
        self.main_frame.config(bg=self.day_mode_colors["bg_main_frame"],
                               highlightbackground=self.day_mode_colors["highlight_bg"])
        self.mode_button.config(text="Night Mode", bg=self.day_mode_colors["bg_button"],
                                fg=self.day_mode_colors["fg_button"])
        self.label.config(fg=self.day_mode_colors["fg_label"], bg=self.day_mode_colors["bg_label"])
        self.search_frame.config(bg=self.day_mode_colors["bg_search_frame"],
                                 highlightbackground=self.day_mode_colors["highlight_bg"])
        self.entry.config(bg=self.day_mode_colors["bg_entry"], fg=self.day_mode_colors["fg_entry"])
        self.search_button.config(bg=self.day_mode_colors["bg_button"], fg=self.day_mode_colors["fg_button"])
        self.result_frame.config(bg=self.day_mode_colors["bg_result_frame"],
                                 highlightbackground=self.day_mode_colors["highlight_bg"])
        self.text.config(bg=self.day_mode_colors["bg_result_frame"], fg=self.day_mode_colors["fg_result_text"])

    def apply_night_mode(self):
        self.main_frame.config(bg=self.night_mode_colors["bg_main_frame"],
                               highlightbackground=self.night_mode_colors["highlight_bg"])
        self.mode_button.config(text="Day Mode", bg=self.night_mode_colors["bg_button"],
                                fg=self.night_mode_colors["fg_button"])
        self.label.config(fg=self.night_mode_colors["fg_label"], bg=self.night_mode_colors["bg_label"])
        self.search_frame.config(bg=self.night_mode_colors["bg_search_frame"],
                                 highlightbackground=self.night_mode_colors["highlight_bg"])
        self.entry.config(bg=self.night_mode_colors["bg_entry"], fg=self.night_mode_colors["fg_entry"])
        self.search_button.config(bg=self.night_mode_colors["bg_button"], fg=self.night_mode_colors["fg_button"])
        self.result_frame.config(bg=self.night_mode_colors["bg_result_frame"],
                                 highlightbackground=self.night_mode_colors["highlight_bg"])
        self.text.config(bg=self.night_mode_colors["bg_result_frame"], fg=self.night_mode_colors["fg_result_text"])

    def scroll_text(self, lines):
        self.text.yview_scroll(lines, "units")

    def search_wikipedia(self, event=None):
        query = self.entry.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search term.")
            return

        user_agent = "Python GUI App/1.0 (testacc@gmail.com)"
        wiki_wiki = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent=user_agent
        )
        page = wiki_wiki.page(query)

        search_entry = {
            'query': query,
            'timestamp': datetime.datetime.now(timezone.utc)
        }
        self.collection.insert_one(search_entry)

        if page.exists():
            self.text.config(state=tk.NORMAL)
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, page.text[:100000])
            self.text.config(state=tk.DISABLED)
        else:
            self.text.config(state=tk.NORMAL)
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, "Page not found.")
            self.text.config(state=tk.DISABLED)

    def show_search_history(self):
        search_history = self.collection.find().sort('timestamp', pymongo.DESCENDING)
        history_text = "Search History:\n\n"
        for entry in search_history:
            if 'timestamp' in entry:
                history_text += f"{entry['timestamp']} - {entry['query']}\n"
        if history_text == "Search History:\n\n":
            history_text += "No search history found."
        messagebox.showinfo("Search History", history_text)

    def __del__(self):
        self.client.close()


def main():
    root = tk.Tk()
    app = WikipediaSearchApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
