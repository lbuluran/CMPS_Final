import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from dataclasses import dataclass

HI_LO_VALUES = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

@dataclass
class Card:
    suit: str
    rank: str

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self, num_decks=1):
        self.num_decks = num_decks
        self.cards = []
        for _ in range(num_decks):
            for suit in self.suits:
                for rank in self.ranks:
                    self.cards.append(Card(suit, rank))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        if len(self.cards) == 0:
            return None
        return self.cards.pop()

class CardCounter:
    def __init__(self, num_decks=1):
        self.running_count = 0
        self.num_decks = num_decks
        self.cards_dealt = 0

    def update_count(self, card: Card):
        if card.rank in ['2', '3', '4', '5', '6']:
            self.running_count += 1
        elif card.rank in ['10', 'Jack', 'Queen', 'King', 'Ace']:
            self.running_count -= 1
        self.cards_dealt += 1

    #def true_count(self, remaining_cards: int) -> float:
        #remaining_decks = remaining_cards / 52.0
        #if remaining_decks == 0:
            #return self.running_count
        #return self.running_count / remaining_decks

    def reset(self):
        self.running_count = 0
        self.cards_dealt = 0

class CardCountingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Card Counting")
        self.root.geometry("800x600")
        self.root.configure(bg="#B2BEB5")  # Sage Green

        self.deck = Deck(num_decks=1)
        self.counter = CardCounter(num_decks=1)
        self.running_count = 0
        self.attempts = []
        self.current_card = None
        self.mode = None

        self.correct_count_label = None
        self.incorrect_count_label = None
        self.instruction_label = None

        self.guide_button = tk.Button(self.root, text="Show Explanation", command=self.show_guide_popup)
        self.guide_button.place(x=10, y=10)

        self.restart_button = tk.Button(self.root, text="Restart Game", command=self.restart_game)
        self.restart_button.place(x=680, y=10)
        self.restart_button.place_forget()

        self.canvas = tk.Canvas(self.root, width=400, height=300, bg="#8B0000")  # Velvet Red
        self.canvas.pack(pady=(40, 10))

        self.running_count_label = tk.Label(self.root, text="Running Count: 0", font=('Arial', 14), bg="#B2BEB5")
        self.running_count_label.pack()

        #self.true_count_label = tk.Label(self.root, text="True Count: 0.00", font=('Arial', 14), bg="#B2BEB5")
        #self.true_count_label.pack()

        self.tutorial_button = tk.Button(self.root, text="Start Tutorial Mode", width=20, command=self.start_tutorial_mode)
        self.tutorial_button.pack(pady=5)

        self.automated_button = tk.Button(self.root, text="Start Automated Mode", width=20, command=self.start_automated_mode)
        self.automated_button.pack(pady=5)

        self.card_image_item = None
        self.card_photo = None

        self.root.bind("<Return>", self.handle_enter_key)
        self.root.bind("<q>", self.quit_program)
        self.user_quit = False  # Track if user pressed 'q'


    def start_tutorial_mode(self):
        self.mode = "tutorial"
        self.reset_game_state()
        self.hide_mode_buttons()

        self.instruction_label = tk.Label(
            self.root,
            text="📘 Tutorial Mode:\nTry to keep a running count and enter your guess after each card is shown.",
            font=('Arial', 12),
            fg="blue",
            bg="#B2BEB5",
            justify="center"
        )
        self.instruction_label.pack(pady=(10, 5))

        self.correct_count_label = tk.Label(self.root, text="✅ Correct Guesses: 0", font=('Arial', 12), bg="#B2BEB5")
        self.correct_count_label.pack()

        self.incorrect_count_label = tk.Label(self.root, text="❌ Incorrect Guesses: 0", font=('Arial', 12), bg="#B2BEB5")
        self.incorrect_count_label.pack()

        self.display_card()

    def start_automated_mode(self):
        self.mode = "automated"
        self.reset_game_state()
        self.hide_mode_buttons()
        self.display_card()
        self.root.unbind("<Return>")  # Prevent tutorial Enter key handling
        self.root.bind("<Return>", self.handle_enter_key)


    def hide_mode_buttons(self):
        self.tutorial_button.pack_forget()
        self.automated_button.pack_forget()
        self.restart_button.place(x=680, y=10)

    def reset_game_state(self):
        self.counter.reset()
        self.deck = Deck(num_decks=1)
        self.attempts = []
        self.correct_guesses = 0
        self.incorrect_guesses = 0

    def restart_game(self):
        for widget in self.root.winfo_children():
            if widget not in [self.canvas, self.guide_button, self.restart_button]:
                widget.pack_forget()
        self.canvas.delete("all")
        self.card_image_item = None
        self.running_count_label.config(text="Running Count: 0")
        #self.true_count_label.config(text="True Count: 0.00")
        self.running_count_label.pack()
        #self.true_count_label.pack()
        self.tutorial_button.pack(pady=5)
        self.automated_button.pack(pady=5)
        self.restart_button.place_forget()
        self.mode = None
        self.root.unbind("<Return>")
        self.user_quit = False



    def display_card(self, event=None):
        if len(self.deck.cards) == 0:
            if not self.user_quit:
                messagebox.showinfo("Game Over", "The deck is empty.")
            self.root.quit()
            return


        self.current_card = self.deck.deal_card()
        self.counter.update_count(self.current_card)
        #remaining_cards = len(self.deck.cards)
        #true_count = self.counter.true_count(remaining_cards)

        image_path = f"cards/{self.current_card.rank}_{self.current_card.suit}.png"
        card_image = Image.open(image_path).resize((100, 150))
        self.card_photo = ImageTk.PhotoImage(card_image)

        if self.card_image_item is not None:
            self.canvas.delete(self.card_image_item)

        # Start animation: move from left to center
        x_pos = 0
        target_x = 200
        y_pos = 150

        def animate():
            nonlocal x_pos
            # Clear old image
            if self.card_image_item is not None:
                self.canvas.delete(self.card_image_item)
    # Draw new image at updated x
            self.card_image_item = self.canvas.create_image(x_pos, y_pos, image=self.card_photo)
            if x_pos < target_x:
                x_pos += 20
                self.canvas.after(10, animate)
            else:
                self.canvas.itemconfig(self.card_image_item, image=self.card_photo)


        animate()

        if self.mode != "tutorial":
            self.running_count_label.config(text=f"Running Count: {self.counter.running_count}")
        else:
            self.running_count_label.config(text="Running Count Not Shown in Tutorial Mode")

        #self.true_count_label.config(text=f"True Count: {true_count:.2f}")

        if self.mode == "tutorial":
            self.ask_for_guess()
        elif self.mode == "automated":
            self.wait_for_input()

    def ask_for_guess(self):
        self.guess_label = tk.Label(self.root, text="Enter Running Count Guess:", font=('Arial', 12), bg="#B2BEB5")
        self.guess_label.pack()

        self.guess_entry = tk.Entry(self.root)
        self.guess_entry.pack()

        self.submit_button = tk.Button(self.root, text="Submit", command=self.check_guess)
        self.submit_button.pack()

        self.guess_entry.bind("<Return>", self.check_guess)
        self.guess_entry.focus_set()

    def check_guess(self, event=None):
        try:
            user_guess = int(self.guess_entry.get())
            is_correct = user_guess == self.counter.running_count
            if is_correct:
                self.correct_guesses += 1
            else:
                self.incorrect_guesses += 1

            if self.correct_count_label:
                self.correct_count_label.config(text=f"✅ Correct Guesses: {self.correct_guesses}")
            if self.incorrect_count_label:
                self.incorrect_count_label.config(text=f"❌ Incorrect Guesses: {self.incorrect_guesses}")

            self.guess_label.destroy()
            self.guess_entry.destroy()
            self.submit_button.destroy()
            self.display_card()

        except ValueError:
            messagebox.showinfo("Invalid Input", "❌ Invalid input. Please enter a number.")

    def wait_for_input(self):
        if not hasattr(self, "info_label"):
            self.info_label = tk.Label(self.root, text="Press Enter for the next card or 'q' to quit.",
                                       font=('Arial', 12), bg="#B2BEB5")
            self.info_label.pack()

    def handle_enter_key(self, event=None):
        if self.mode == "automated":
            if hasattr(self, "info_label") and self.info_label is not None:
                self.info_label.destroy()
                self.info_label = None
            self.display_card()

    def quit_program(self, event=None):
            self.user_quit = True
            messagebox.showinfo("Goodbye", "Thank you for playing!")
            self.root.quit()



    def show_guide_popup(self):
        guide_window = tk.Toplevel(self.root)
        guide_window.title("Hi-Lo Card Counting Guide")
        guide_window.geometry("600x400")
        guide_window.configure(bg="#B2BEB5")

        guide_text = (
            "What is the Hi-Lo System?\n\n"
            "The Hi-Lo system is a simple method used to keep a running count of cards in Blackjack.\n"
            "Why? Because small cards (2–6) help the dealer more, and big cards (10–A) help the player.\n"
            "This helps inform your betting strategy.\n\n"
            "How it works:\n"
            "- Cards 2–6: Count +1\n"
            "- Cards 7–9: Count 0\n"
            "- Cards 10, J, Q, K, A: Count -1\n\n"
            "Add the values as cards are revealed. A high positive count means the deck is rich in high cards "
            "and more likely to favor the player in upcoming hands."
        )

        label = tk.Label(guide_window, text=guide_text, font=('Arial', 11), justify='left',
                         wraplength=560, fg="darkgreen", bg="#B2BEB5")
        label.pack(padx=20, pady=20)

def main():
    root = tk.Tk()
    app = CardCountingGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()