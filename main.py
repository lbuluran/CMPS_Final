import random
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from dataclasses import dataclass

# Hi-Lo card values used in the card counting system
HI_LO_VALUES = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'Jack': -1, 'Queen': -1, 'King': -1, 'Ace': -1
}

@dataclass
class Card:
    suit: str
    rank: str

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    # Standard card suits and ranks
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self, num_decks=1):
        self.num_decks = num_decks
        self.cards = [Card(suit, rank) for _ in range(num_decks) for suit in self.suits for rank in self.ranks]
        self.shuffle()

    # Shuffle the deck
    def shuffle(self):
        random.shuffle(self.cards)

    # Deal one card from the deck
    def deal_card(self):
        return self.cards.pop() if self.cards else None

class CardCounter:
    def __init__(self, num_decks=1):
        self.running_count = 0
        self.num_decks = num_decks
        self.cards_dealt = 0

    # Update running count based on dealt card
    def update_count(self, card: Card):
        self.running_count += HI_LO_VALUES.get(card.rank, 0)
        self.cards_dealt += 1

    # Reset the counter
    def reset(self):
        self.running_count = 0
        self.cards_dealt = 0

class CardCountingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Card Counting")
        self.root.geometry("800x600")
        self.root.configure(bg="#B2BEB5")  # Background color

        self.deck = Deck(num_decks=1)
        self.counter = CardCounter(num_decks=1)

        # Track game state
        self.attempts = []
        self.current_card = None
        self.mode = None
        self.user_quit = False

        # UI labels and elements
        self.correct_count_label = None
        self.incorrect_count_label = None
        self.instruction_label = None

        # Buttons for guide and restart
        self.guide_button = tk.Button(self.root, text="Show Explanation", command=self.show_guide_popup)
        self.guide_button.place(x=10, y=10)

        self.restart_button = tk.Button(self.root, text="Restart Game", command=self.restart_game)
        self.restart_button.place(x=680, y=10)
        self.restart_button.place_forget()

        # Canvas for card display
        self.canvas = tk.Canvas(self.root, width=400, height=300, bg="#8B0000")
        self.canvas.pack(pady=(40, 10))

        # Display for running count
        self.running_count_label = tk.Label(self.root, text="Running Count: 0", font=('Arial', 14), bg="#B2BEB5")
        self.running_count_label.pack()

        # Buttons for modes
        self.tutorial_button = tk.Button(self.root, text="Start Tutorial Mode", width=20, command=self.start_tutorial_mode)
        self.tutorial_button.pack(pady=5)

        self.automated_button = tk.Button(self.root, text="Start Automated Mode", width=20, command=self.start_automated_mode)
        self.automated_button.pack(pady=5)

        self.card_image_item = None
        self.card_photo = None

        # Keyboard bindings
        self.root.bind("<Return>", self.handle_enter_key)
        self.root.bind("<q>", self.quit_program)

    # Start the tutorial mode
    def start_tutorial_mode(self):
        self.cleanup_after_mode_switch()
        self.mode = "tutorial"
        self.reset_game_state()
        self.hide_mode_buttons()

        self.instruction_label = tk.Label(self.root, text="Tutorial Mode: Guess the running count.",
                                          font=('Arial', 12), fg="blue", bg="#B2BEB5")
        self.instruction_label.pack(pady=(10, 5))

        self.correct_count_label = tk.Label(self.root, text="Correct Guesses: 0", font=('Arial', 12), bg="#B2BEB5")
        self.correct_count_label.pack()

        self.incorrect_count_label = tk.Label(self.root, text="Incorrect Guesses: 0", font=('Arial', 12), bg="#B2BEB5")
        self.incorrect_count_label.pack()

        self.display_card()

    # Start the automated mode
    def start_automated_mode(self):
        self.cleanup_after_mode_switch()
        self.mode = "automated"
        self.reset_game_state()
        self.hide_mode_buttons()
        self.display_card()
        self.root.unbind("<Return>")  # Prevent tutorial Enter key handling
        self.root.bind("<Return>", self.handle_enter_key)

    # Hide mode selection buttons and show restart
    def hide_mode_buttons(self):
        self.tutorial_button.pack_forget()
        self.automated_button.pack_forget()
        self.restart_button.place(x=680, y=10)

    # Reset the game state variables and deck
    def reset_game_state(self):
        self.counter.reset()
        self.deck = Deck(num_decks=1)
        self.attempts = []
        self.correct_guesses = 0
        self.incorrect_guesses = 0

    # Restart game and reset UI
    def restart_game(self):
        self.cleanup_after_mode_switch()
        self.running_count_label.config(text="Running Count: 0")
        self.running_count_label.pack()
        self.tutorial_button.pack(pady=5)
        self.automated_button.pack(pady=5)
        self.restart_button.place_forget()
        self.mode = None
        self.root.unbind("<Return>")
        self.user_quit = False

    # Remove old widgets from previous mode
    def cleanup_after_mode_switch(self):
        for widget in self.root.winfo_children():
            if widget not in [self.canvas, self.guide_button, self.restart_button]:
                widget.pack_forget()
        self.canvas.delete("all")
        if hasattr(self, "info_label") and self.info_label is not None:
            self.info_label.destroy()
            self.info_label = None
        if hasattr(self, "guess_label"):
            self.guess_label.destroy()
        if hasattr(self, "guess_entry"):
            self.guess_entry.destroy()
        if hasattr(self, "submit_button"):
            self.submit_button.destroy()

    # Display the next card and animate
    def display_card(self, event=None):
        if len(self.deck.cards) == 0:
            if not self.user_quit:
                messagebox.showinfo("Game Over", "The deck is empty.")
            return

        self.current_card = self.deck.deal_card()
        self.counter.update_count(self.current_card)

        # Load card image based on card name
        image_path = f"cards/{self.current_card.rank}_{self.current_card.suit}.png"
        card_image = Image.open(image_path).resize((100, 150))
        self.card_photo = ImageTk.PhotoImage(card_image)

        # Animate card moving to center
        x_pos = 0
        target_x = 200
        y_pos = 150

        def animate():
            nonlocal x_pos
            if self.card_image_item:
                self.canvas.delete(self.card_image_item)
            self.card_image_item = self.canvas.create_image(x_pos, y_pos, image=self.card_photo)
            if x_pos < target_x:
                x_pos += 20
                self.canvas.after(10, animate)

        animate()

        # Update running count display
        if self.mode == "tutorial":
            self.running_count_label.config(text="Running Count Not Shown in Tutorial Mode")
            self.ask_for_guess()
        else:
            self.running_count_label.config(text=f"Running Count: {self.counter.running_count}")
            self.wait_for_input()

    # Ask user to input their guess
    def ask_for_guess(self):
        self.guess_label = tk.Label(self.root, text="Enter Running Count Guess:", font=('Arial', 12), bg="#B2BEB5")
        self.guess_label.pack()
        self.guess_entry = tk.Entry(self.root)
        self.guess_entry.pack()
        self.submit_button = tk.Button(self.root, text="Submit", command=self.check_guess)
        self.submit_button.pack()
        self.guess_entry.bind("<Return>", self.check_guess)
        self.guess_entry.focus_set()

    # Check user guess against actual count
    def check_guess(self, event=None):
        try:
            user_guess = int(self.guess_entry.get())
            is_correct = user_guess == self.counter.running_count
            if is_correct:
                self.correct_guesses += 1
            else:
                self.incorrect_guesses += 1
            self.correct_count_label.config(text=f"Correct Guesses: {self.correct_guesses}")
            self.incorrect_count_label.config(text=f"Incorrect Guesses: {self.incorrect_guesses}")
            self.guess_label.destroy()
            self.guess_entry.destroy()
            self.submit_button.destroy()
            self.display_card()
        except ValueError:
            messagebox.showinfo("Invalid Input", "Please enter a valid number.")

    # Prompt user for Enter key or quit in automated mode
    def wait_for_input(self):
        self.info_label = tk.Label(self.root, text="Press Enter for next card or 'q' to quit.", font=('Arial', 12), bg="#B2BEB5")
        self.info_label.pack()

    # Handle Enter key press in automated mode
    def handle_enter_key(self, event=None):
        if self.mode == "automated":
            if hasattr(self, "info_label"):
                self.info_label.destroy()
            self.display_card()

    # Handle quit key press
    def quit_program(self, event=None):
        self.user_quit = True
        messagebox.showinfo("Goodbye", "Thank you for playing!")
        self.root.quit()

    # Show popup with Hi-Lo explanation
    def show_guide_popup(self):
        guide_window = tk.Toplevel(self.root)
        guide_window.title("Hi-Lo Card Counting Guide")
        guide_window.geometry("600x400")
        guide_window.configure(bg="#B2BEB5")

        guide_text = (
            "What is the Hi-Lo System?\n\n"
            "The Hi-Lo system is a method used in Blackjack to track high and low cards.\n\n"
            "Card Values:\n"
            "- 2 to 6: +1\n"
            "- 7 to 9: 0\n"
            "- 10, J, Q, K, A: -1\n\n"
            "A positive count favors the player, a negative favors the dealer."
        )

        label = tk.Label(guide_window, text=guide_text, font=('Arial', 11), justify='left', wraplength=560, fg="darkgreen", bg="#B2BEB5")
        label.pack(padx=20, pady=20)

# Launch the application
def main():
    root = tk.Tk()
    app = CardCountingGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
