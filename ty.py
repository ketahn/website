import time
import random
import customtkinter as ctk
from tkinter import messagebox

class TypingSpeedTester:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Tester")
        self.root.geometry("800x600")

        # Configure theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Sample texts categorized by difficulty
        self.texts = {
            "Easy": [
                "The quick brown fox jumps over the lazy dog.",
                "Practice makes perfect.",
                "There are both good and bad."
            ],
            "Medium": [
                "Blue whale is the largest animal in the world as well as aquatic.",
                "Those who never know failure will never know success.",
                "Python is an interpreted, high-level, general-purpose programming language."
            ],
            "Hard": [
                "Programming is the art of telling another human what one wants the computer to do.",
                "The best way to predict the future is to invent it.",
                "If a thing has to be remained as a secret, it should never be exposed."
            ]
        }

        # Variables
        self.start_time = None
        self.test_active = False
        self.current_text = ""
        self.results_history = []
        self.remaining_time = 60
        self.timer_id = None

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(
            self.main_frame, text="Typing Speed Test", font=("Arial", 24, "bold")
        )
        self.title_label.pack(pady=(10, 20))

        # Difficulty selection
        self.difficulty_menu = ctk.CTkOptionMenu(
            self.main_frame,
            values=["Easy", "Medium", "Hard"],
            command=self.set_difficulty
        )
        self.difficulty_menu.set("Medium")
        self.difficulty_menu.pack(pady=10)

        self.text_frame = ctk.CTkFrame(self.main_frame)
        self.text_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.sample_text = ctk.CTkLabel(
            self.text_frame,
            text="Click 'Start Test' to begin",
            font=("Arial", 16),
            wraplength=700,
            justify="left"
        )
        self.sample_text.pack(pady=20, padx=10)

        self.typing_entry = ctk.CTkEntry(
            self.main_frame,
            font=("Arial", 16),
            width=600,
            height=40,
            state="disabled"
        )
        self.typing_entry.pack(pady=10)
        self.typing_entry.bind("<Return>", self.check_typing)

        self.timer_label = ctk.CTkLabel(
            self.main_frame,
            text="Time Left: 60s",
            font=("Arial", 14)
        )
        self.timer_label.pack(pady=5)

        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(pady=20)

        self.start_button = ctk.CTkButton(
            self.button_frame,
            text="Start Test",
            command=self.start_test,
            width=120,
            height=40
        )
        self.start_button.pack(side="left", padx=10)

        self.results_button = ctk.CTkButton(
            self.button_frame,
            text="Show Results",
            command=self.show_results,
            width=120,
            height=40,
            state="disabled"
        )
        self.results_button.pack(side="left", padx=10)

        self.results_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Arial", 14)
        )
        self.results_label.pack(pady=10)

    def set_difficulty(self, choice):
        self.selected_difficulty = choice

    def start_test(self):
        self.test_active = True
        self.start_time = time.time()
        self.remaining_time = 60
        self.current_text = random.choice(self.texts[self.difficulty_menu.get()])

        self.sample_text.configure(text=self.current_text)
        self.typing_entry.configure(state="normal")
        self.typing_entry.delete(0, "end")
        self.typing_entry.focus()

        self.start_button.configure(state="disabled")
        self.results_button.configure(state="disabled")
        self.results_label.configure(text="")
        self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0 and self.test_active:
            self.timer_label.configure(text=f"Time Left: {self.remaining_time}s")
            self.remaining_time -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.check_typing()

    def check_typing(self, event=None):
        if not self.test_active:
            return

        self.root.after_cancel(self.timer_id)
        typed_text = self.typing_entry.get().strip()
        if not typed_text:
            messagebox.showwarning("Warning", "Please type the text before submitting.")
            return

        end_time = time.time()
        time_taken = end_time - self.start_time

        word_count = len(typed_text.split())
        wpm = (word_count / time_taken) * 60 if time_taken > 0 else 0

        typed_words = typed_text.split()
        sample_words = self.current_text.split()
        correct_words = sum(1 for tw, sw in zip(typed_words, sample_words) if tw == sw)
        accuracy = (correct_words / len(sample_words)) * 100 if sample_words else 0

        result_text = (
            f"Time: {time_taken:.2f} seconds | "
            f"WPM: {wpm:.2f} | "
            f"Accuracy: {accuracy:.2f}%"
        )
        self.results_label.configure(text=result_text)
        self.results_history.append(result_text)

        self.test_active = False
        self.typing_entry.configure(state="disabled")
        self.start_button.configure(state="normal")
        self.results_button.configure(state="normal")
        self.timer_label.configure(text="Time Left: 60s")

    def show_results(self):
        if not self.results_history:
            messagebox.showinfo("Results", "No test results available yet.")
            return

        history = "\n".join(self.results_history[-5:])
        messagebox.showinfo("Recent Results", history)

if __name__ == "__main__":
    root = ctk.CTk()
    app = TypingSpeedTester(root)
    root.mainloop()