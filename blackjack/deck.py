# Carlos Patiño - cpatinoc

import tkinter as tk
import random

from card import Card
from hand import Hand

class Deck(Hand):
    """
    Extends the class Hand to represent a Deck of cards that can be shuffled and dealt
    """
    
    
    def __init__(self):

        # Initialize the arguments of the superclass
        super().__init__()

        # Loop through all possible cards for each suit, and add them to the Deck
        for i in range(1,13+1):
            for suit in Card.SUIT_LIST:
                super().add(Card(suit, Card.CARD_VALUES[i] , i))

        # Shuffle the initial deck of cards
        random.shuffle(self.cards)

        # Define a list to keep track of all the cards that have been dealt from this deck
        self.cardsDealt= []

    def deal(self):
        '''removes the top card on the deck and returns it'''
        
        self.cardsDealt.append(self.cards.pop())

        return self.cardsDealt[len(self.cardsDealt)-1]

    @property
    def size(self):
        '''returns the number of cards left in the deck'''
        return len(self.cards)

    def shuffle(self):
        '''randomly shuffles all the already dealt cards and places them at the bottom of the deck'''

        # Shuffle the dealt cards
        random.shuffle(self.cardsDealt)

        # Place the cards at the bottom of the deck using list concatenation
        self.cards= self.cardsDealt + self.cards

        # Reset cards dealt list
        self.cardsDealt= []