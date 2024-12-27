import random
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class GameWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tallano Dungeon Battle")
        self.setGeometry(100, 100, 600, 400)

        self.game_state = "entrance"  # Initial game state
        self.previous_states = []  # Track visited states for looping functionality
        self.init_ui()

    def init_ui(self):
        # Main layout
        self.layout = QVBoxLayout()

        
        self.image_display = QLabel()
        self.image_display.setAlignment(Qt.AlignCenter)  
        self.layout.addWidget(self.image_display)

        # Game text display
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.layout.addWidget(self.text_display)

        # Button container layout
        self.button_layout = QVBoxLayout()
        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)
        self.update_game_state()

    def update_text(self, text):
        self.text_display.setText(text)

    def update_image(self, image_path):
        self.current_image_path = image_path  
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(
            self.image_display.width(), self.image_display.height(), Qt.KeepAspectRatio
        )
        self.image_display.setPixmap(scaled_pixmap)


    def add_button(self, text, function):
        button = QPushButton(text)
        button.clicked.connect(function)
        self.button_layout.addWidget(button)



    def clear_buttons(self):
        for i in reversed(range(self.button_layout.count())):
            widget = self.button_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def change_state(self, new_state):
        print(f"Changing state to: {new_state}") 
        self.previous_states.append(self.game_state)
        self.game_state = new_state
        self.update_game_state()



    def go_back(self):
        if self.previous_states:
            self.game_state = self.previous_states.pop()
            self.update_game_state()

    def update_game_state(self):
        print(f"Updating game state: {self.game_state}") 
        self.clear_buttons()
        if self.game_state == "entrance":
            self.entrance_screen()
        elif self.game_state == "left_room":
            self.left_room()
        elif self.game_state == "right_room":
            self.right_room()
        elif self.game_state == "maze":
            self.maze()
        elif self.game_state == "treasure_room":
            self.treasure_room()
        elif self.game_state == "exit":
            self.exit_game()


    def entrance_screen(self):
        self.update_text("You are at the entrance of a dark dungeon. Make your choice. WAHAHAHA (evil laugh)")
        self.update_image("evil.jpg")  
        self.add_button("Go to the left room", lambda: self.change_state("left_room"))
        self.add_button("Go to the right room", lambda: self.change_state("right_room"))
        self.add_button("Exit the dungeon", self.exit_game)

    def left_room(self):
        self.update_text("Oh no! A sleeping dragon.")
        self.update_image("sleeping drag.jpg")  
        self.add_button("Sneak past the dragon", self.sneak_past_dragon)
        self.add_button("Grab the box", self.grab_box)
        self.add_button("Go back", self.go_back)

    def sneak_past_dragon(self):
        self.update_text("You sneak past the dragon... but find another awake dragon! Go back to the entrance.")
        self.update_image("wakedrag.jpg") 
        self.clear_buttons()
        self.add_button("Go back to the entrance", lambda: self.change_state("entrance"))

    def grab_box(self):
        print("Grab box method called")
        self.update_text("The box contains a mysterious note: 'echo'. You return to the entrance.")
        self.update_image("echo.jpg")  
        self.clear_buttons()
        self.add_button("Go back to the entrance",lambda: self.change_state("entrance"))


    def right_room(self):
        self.update_text("You enter the right room.")
        self.update_image("rightroom.jpg")  
        self.add_button("Solve the riddle", self.solve_riddle)
        self.add_button("Enter the maze", lambda: self.change_state("maze"))
        self.add_button("Go back", self.go_back)

    def solve_riddle(self):
        self.update_text("I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?")
        self.update_image("riddle.jpg")
        self.clear_buttons() 

        self.answer_input = QLineEdit(self)
        self.layout.addWidget(self.answer_input)

        # Add the button to submit the answer
        self.add_button("Submit Answer", self.check_riddle_answer)

    def check_riddle_answer(self):
        
        user_answer = self.answer_input.text().lower()
        self.answer_input.deleteLater()  

        if user_answer == "echo":
            # If the answer is correct
            self.update_text("Correct! The riddle opens the path to the treasure room.")
            self.update_image("correct.jpg")  
            self.clear_buttons() 

            
            self.add_button("Go to the treasure room", lambda: self.change_state("treasure_room"))
        else:
            # If the answer is incorrect
            self.update_text("Incorrect answer. Try again.")
            self.update_image("incorrect.jpg") 
            self.clear_buttons()

            
            self.add_button("Go back to the entrance", lambda: self.change_state("entrance"))


    def maze(self):
        self.update_text("You are in the maze. Choose a path.")
        self.update_image("maze.jpg")  
        self.add_button("Go left", lambda: self.update_text("Dead end. Try again."))
        self.add_button("Go right", lambda: self.change_state("treasure_room"))
        self.add_button("Go straight", lambda: self.change_state("entrance"))
        self.add_button("Go back", self.go_back)

    def treasure_room(self):
        self.update_text("You find a treasure chest!")
        self.update_image("treasure_room.jpg")  
        self.add_button("Open the chest", self.open_chest)
        self.add_button("Ignore the chest", lambda: self.change_state("exit"))

    def open_chest(self):
        chest_outcome = random.randint(1, 2)
        if chest_outcome == 1:
            self.update_text("BOOM! The chest contains a bomb! You lose.")
            self.update_image("bomb.jpg")  
        else:
            self.update_text("Tallano golds! Congratulations, you won the game! Go and be the next president of the Philippines!")
            self.update_image("golds.jpg")  
        self.clear_buttons()
        self.add_button("Exit", lambda: self.change_state("exit"))

    def exit_game(self):
        self.update_text("Thank you for playing Tallano Dungeon Battle! Goodbye.")
        self.update_image("exit.jpg")  
        self.clear_buttons()
        self.add_button("Close", lambda: sys.exit())

# Start the application
def main():
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
