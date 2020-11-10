# Carlos Patiño - cpatinoc

import tkinter as tk

class Card():

    # Constant class attributes
    CLUBS= "clubs"
    DIAMONDS= "diamonds"
    HEARTS= "hearts"
    SPADES= "spades"
    SUIT_LIST= [CLUBS, DIAMONDS, HEARTS, SPADES]

    # Class attribute to define card values for each card number
    CARD_VALUES= {
        1: 11, #Ace is worth 11 points
        2: 2,
        3: 3,
        4: 4,
        5: 5,
        6: 6,
        7: 7,
        8: 8,
        9: 9,
        10: 10,
        11: 10, # Face cards are all woth 10 points
        12: 10,
        13: 10,
    }

    IMAGE_WIDTH_IN_PIXELS= 75
    IMAGE_HEIGHT_IN_PIXELS= 109

    # Class attribute to hold image objects
    card_images= {}

    def __init__(self, suit, value, cardNumber):
        """
        Attributes:
            suit: Card.CLUBS, Card.DIAMONDS, Card.HEARTS, or Card.SPADES
            value: an int, this card's value for Blackjack (between 2 to 11)
            cardNumber: an int, this card's number to identify this card (1-13)
        """

        # Verify that value matches with the cardNumber. If not, raise exception
        if value != Card.CARD_VALUES[cardNumber]:
            raise ValueError("Card value does not match Card number")

        self.suit= suit
        self.__cardValue= value
        self.cardNumber= cardNumber

    @classmethod
    def load_images(cls):
        """
        Class method that loads all images inside the images/ directory as tk.PhotoImage objects.
        The images are loaded in a dictionary where:
            - each key is a string that is the name of the image, in the form of '<cardNumber>-<cardSuit>' (e.g. '12-spades')
            - each value is the corresponding tk.PhotoImage object.
        """

        # Reset class attribute to an empty dictionary
        cls.card_images= {}

        # Specify the folder where all the card images are stored.
        path= "images/"
        
        # Loop through all possible cards for each suit, and add them to the dictionary of names-images key-value pairs
        for i in range(1,13+1):
            for suit in cls.SUIT_LIST:
                cls.card_images[str(i) + '-' + suit]= tk.PhotoImage(file= path + str(i) + "_of_" + suit + ".gif")

    @property
    def value(self):
        '''Returns the card value'''

        return self.__cardValue

    @property
    def image(self):
        '''Returns the tk.PhotoImage object from the Card.card_images dictionary'''

        return Card.card_images[str(self.cardNumber) + '-' + self.suit]