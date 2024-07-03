# State pattern implementation for a game menu

# State interface
class State:
    def __init__(self):
        pass
    
    def update(self):
        pass

    def display(self):
        pass

# Concrete States
class MainMenuState(State):
    def display(self):
        print("Main Menu")
        print("1. Start Game")
        print("2. Load Game")
        print("3. Options")
        print("4. Exit")

class GameMenuState(State):
    def display(self):
        print("Game Menu")
        print("1. Save Game")
        print("2. Resume Game")
        print("3. Options")
        print("4. Quit to Main Menu")

# Context
class Menu:
    def __init__(self):
        self.state = MainMenuState()

    def change_state(self, state):
        self.state = state

    def display(self):
        self.state.display()

# Example usage
if __name__ == "__main__":
    game_menu = Menu()
    
    # Display initial main menu
    game_menu.display()
    
    # Change state to game state
    game_menu.change_state(GameMenuState())
    
    # Display game menu
    game_menu.display()
