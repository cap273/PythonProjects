from tkinter import font
import tkinter as tk
from abc import ABC, abstractmethod

from deck import Deck
from hand import Hand
from card import Card

class GameGUI(ABC):

    def __init__(self, window):
        self._window = window
        self._canvas_width = 1024
        self._canvas_height = 400
        self._canvas = tk.Canvas(window, width=self._canvas_width, height=self._canvas_height)
        self._canvas.pack()
        window.bind("<Key>", self._keyboard_event)

    def _keyboard_event(self, event):
        key = str(event.char)

        if key == 'h':
            self.player_hit()
        elif key == 's':
            self.player_stand()
        elif key == 'r':
            self.reset()

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def player_hit(self):
        pass

    @abstractmethod
    def player_stand(self):
        pass

class BlackJack(GameGUI):
    '''implements a simple version of the cardgame  and  displays  the  game  state  to  the  player'''


    # In pixels, specify the vertical separation between different elements in the canvas.
    SMALL_VERTICAL_OFFSET= 20
    MEDIUM_VERTICAL_OFFSET= 30

    # Specify where to put the game status axis
    GAME_STATUS_TEXT_X_AXIS= Card.IMAGE_WIDTH_IN_PIXELS*3 + 10


    def __init__(self, window):
        '''
        Attributes (not already defined in the superclass):
        numPlayerWins: an int, keep track of times the player has won
        numDealerWins: an int, keep track of times the dealer has won
        gameStatusText: a str, game status text indicating the current state of the game
        gameStatusColor: a str, the color of the game status text
        playerHand: a Hand object, representing the player's hand
        dealerHand: a Hand object, representing the dealer's hand
        deck: a Deck object, representing the current deck of cards
        '''

        super().__init__(window)

        self.reset()

    def reset(self):
        '''Restarts the game.  This method is automatically called whenever the user hits the “r” key.'''


        # Initialize game situation
        self.numPlayerWins= 0
        self.numDealerWins= 0
        self.gameStatusText= "In Progress..."
        self.gameStatusColor= "green"

        # Initialize (empty) player and dealer hands
        self.playerHand= Hand()
        self.dealerHand= Hand()

        # Initialize deck
        self.deck= Deck()

        # Load images
        Card.load_images()

        # Draw canvas
        self.draw_canvas()

    def player_hit(self):
        '''
        The user is requesting to perform a hit on their hand.  
        This means that the method must draw acard from the deck and add it to the player’s hand.
        '''

        # Is this the first hit in a new game? If so, clear the player and dealer hands, and reset the game status
        self.new_game_check()

        # Deal a new card to the player
        self.playerHand.add(self.deck.deal())
        self.reshuffle_check()

        # Did the player bust?
        if self.playerHand.total > 21:
            self.gameStatusColor= "red"
            self.gameStatusText= "Dealer WINS... Press 'r' to start a new game"
            self.numDealerWins+= 1

        # Update GUI
        self.draw_canvas()

    def player_stand(self):
        '''
        The user is requesting to perform a stand on their hand.  This means that the method must
        continuously add cards to the dealer’s hand until their hand is greater than or equal to 17.
        '''

        # Is this the first stand in a new game? If so, clear the player and dealer hands, and reset the game status
        self.new_game_check()
        
        # Add cards to the dealer's hand until the dealer's hand is greater than or equal to 17
        while self.dealerHand.total < 17:
            self.dealerHand.add(self.deck.deal())
            self.reshuffle_check()

        self.gameStatusColor= "red"
        # Did the dealer bust OR did the player's total exceed the dealer's score?
        if (self.dealerHand.total > 21) or (self.dealerHand.total < self.playerHand.total):
            self.gameStatusText= "Player WINS... Press 'r' to start a new game"
            self.numPlayerWins+= 1

        # Was there a tie?    
        elif (self.dealerHand.total == self.playerHand.total):
            self.gameStatusText= "TIE Game...Press 'r' to start a new game"

        # Did the dealer win?
        elif (self.dealerHand.total > self.playerHand.total):
            self.gameStatusText= "Dealer WINS... Press 'r' to start a new game"
            self.numDealerWins+= 1

        # Update GUI
        self.draw_canvas()

    def reshuffle_check(self):
        '''Check if the deck has 13 cards remaining. If so, reschuffle the deck.'''

        if self.deck.size <= 13:
            self.deck.shuffle()

    def new_game_check(self):
        '''
        If this is a new game, clear the player and dealer hands, and reset the game status
        '''
        
        if self.gameStatusText != "In Progress...":
            self.gameStatusText= "In Progress..."
            self.gameStatusColor= "green"
            self.playerHand.reset()
            self.dealerHand.reset()

    def draw_canvas(self):
        ''' Update the GUI and redraw everything '''

        # Initial coordinates
        current_x= 10
        current_y= 10

        # Define the font for everything
        REGULAR_FONT= font.Font(family='Helvetica', size=10, weight='bold')

        # Time to update the GUI
        self._canvas.delete(tk.ALL)

        # Text with the current player hand total
        self._canvas.create_text(current_x, current_y, 
                                            anchor=tk.NW, 
                                            font=REGULAR_FONT, 
                                            text=f'Player Hand Total: {self.playerHand.total}')

        # The images of the player's current hand
        current_y+= BlackJack.SMALL_VERTICAL_OFFSET
        self.playerHand.draw(self._canvas, current_x, current_y, None, None)

        # The text of the dealer's current hand total
        current_y+= (BlackJack.MEDIUM_VERTICAL_OFFSET + Card.IMAGE_HEIGHT_IN_PIXELS)
        self._canvas.create_text(current_x, current_y, 
                                            anchor=tk.NW, 
                                            font=REGULAR_FONT, 
                                            text=f'Dealer Hand Total: {self.dealerHand.total}')

        # The images of the dealer's current hand total
        current_y+= BlackJack.SMALL_VERTICAL_OFFSET
        self.dealerHand.draw(self._canvas, current_x, current_y, None, None)

        # The game status
        current_y+= (BlackJack.MEDIUM_VERTICAL_OFFSET + Card.IMAGE_HEIGHT_IN_PIXELS)
        self._canvas.create_text(BlackJack.GAME_STATUS_TEXT_X_AXIS, current_y, 
                                            anchor=tk.NW, 
                                            font=REGULAR_FONT,
                                            fill= self.gameStatusColor,
                                            text=f'Game Status: {self.gameStatusText}')

        # The text with the dealer wins and the player wins
        current_y+= BlackJack.SMALL_VERTICAL_OFFSET
        self._canvas.create_text(current_x, current_y, 
                                            anchor=tk.NW, 
                                            font=REGULAR_FONT, 
                                            text=f'Dealer Wins: {self.numDealerWins}')
                                            
        current_y+= BlackJack.SMALL_VERTICAL_OFFSET
        self._canvas.create_text(current_x, current_y, 
                                            anchor=tk.NW, 
                                            font=REGULAR_FONT, 
                                            text=f'Player Wins: {self.numPlayerWins}')
        

def main():
    window = tk.Tk()
    window.title("Blackjack")
    # Uncomment this out when you are ready to implement BlackJack
    game= BlackJack(window)
    window.mainloop()

if __name__ == "__main__":
    main()