# CMPS_Final
This is the Finals Repository for CMPS1100 Spring '25

# Blackjack Card Counting Trainer (Hi-Lo System)

This project is a Python-based GUI application that teaches and trains users to use the Hi-Lo card counting system in Blackjack. It offers two interactive modes: a tutorial mode where users guess the running count, and an automated mode where the count is displayed. The GUI is built using `tkinter` and includes animated card dealing, a performance tracker, and an instructional guide.

## Features

- Tutorial Mode: Users manually input the running count after each card to test accuracy.
- Automated Mode: Cards are shown, and the running count is updated automatically.
- Visual feedback for correct and incorrect guesses.
- Animated card dealing within the GUI canvas.
- Pop-up guide explaining the Hi-Lo counting system.
- Restart button for replaying the session without restarting the program.

## Requirements

- Python 3.8 or higher
- `tkinter` (usually included with Python installations)
- `Pillow` for image processing

To install required packages:
```bash
pip install pillow
How to Run the Application


Clone the repository:

git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
Ensure the cards/ folder is in the same directory as main.py and contains all 52 properly named card image files.


Run the GUI:

python main.py

Running the Tests
To verify that the deck and counting logic are functioning correctly:

python test_card_counting.py
Hi-Lo System Summary
The Hi-Lo system assigns point values to cards to keep a running count:

Card Value	Count
2 to 6	+1
7 to 9	0
10 to Ace	-1

As each card is revealed, its value is added to the running count. A higher count indicates a deck favorable to the player.

Controls and Interaction
Enter key: Deal next card (automated mode)

q key: Quit the application

Buttons in GUI:

Start Tutorial Mode

Start Automated Mode

Restart Game

Show Explanation (Hi-Lo guide)

Notes
All card image files must be named using the format: Rank_Suit.png, e.g., 2_Hearts.png, Queen_Spades.png.

The application automatically closes once all cards in the deck are dealt.

If card images are missing or incorrectly named, the program may encounter errors when displaying cards.
