from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
# Attempt to read the CSV file with words to learn; if not found, load from original data
try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("./data/english_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

# Function to display the next flashcard
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer) # Cancel any existing flip timer
    current_card = random.choice(to_learn) # Pick a random card from the to_learn list
    canvas.itemconfigure(card_title, text="English", fill="black")
    canvas.itemconfigure(card_word, text=current_card["English"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card) # Set timer to flip the card after 3 seconds

# Function to flip the card to display the translation
def flip_card():
    canvas.itemconfigure(card_title, text="Hindi",fill="white")
    canvas.itemconfigure(card_word, text=current_card["Hindi"], fill="white")
    canvas.itemconfigure(card_background, image=card_back_image)

# Function to handle when the word is known
def is_known():
    to_learn.remove(current_card) # Remove the current card from the to_learn list
    print(len(to_learn)) # Print remaining cards count (for debugging)
    data = pd.DataFrame(to_learn)
    data.to_csv("./data/words_to_learn.csv", index=False) # Save updated list to CSV
    next_card() # Display the next card


# Function to center the window on the screen
def center_window(window):
    # Update the window to calculate the dimensions accurately
    window.update_idletasks()

    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the window width and height
    window_width = window.winfo_width()
    window_height = window.winfo_height()

    # Calculate the coordinates for centering the window
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Set the window position
    window.geometry(f"+{x}+{y}")


# UI Set-Up
window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

# Canvas for displaying flashcard
canvas = Canvas(height=526, width=800, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_image = PhotoImage(file= "./images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Buttons for marking known or unknown
cross_img = PhotoImage(file="./images/wrong.png")
unknown_button = Button(image=cross_img, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_img = PhotoImage(file="./images/right.png")
known_button = Button(image=check_img, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

# Load initial card
next_card()

# Center the window on the screen
center_window(window)

# Start the main event loop
window.mainloop()
