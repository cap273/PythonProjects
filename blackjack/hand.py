# Carlos Patiño - cpatinoc

from card import Card
import tkinter as tk

class Hand():
    '''Holds a collection of cards'''

    def __init__(self):

        # Define a list of Card objects as the collection of cards
        # This list will be treated as a stack (LIFO)
        self.cards= []

    def reset(self):
        '''Clears the collection of cards'''
        self.cards= []

    def add(self, card):
        '''Takes a Card object and adds the card to the collection of cards'''
        self.cards.append(card)

    @property
    def total(self):
        '''Returns the sum of the values of the cards in the hand'''
        
        sumValues= 0
        for card in self.cards:
            sumValues+= card.value
        
        return sumValues

    def draw(self, canvas, start_x, start_y, canvas_width, canvas_height):
        '''Draws the hand of cards on to the canvas starting at the location specified (i.e., start_x and start_y). 
        Draw the cards horizontally along the x-axis.  The method takes in the canvas_width and canvas_height but you may not 
        need to use them in your implementation.'''

        OFFSET_IN_PIXELS= 5

        this_x= start_x

        for card in self.cards:

            # Place card image in canvas
            canvas.create_image(this_x, start_y, anchor=tk.NW, image=card.image)

            # Move x coordinate to the right
            this_x+= (Card.IMAGE_WIDTH_IN_PIXELS + OFFSET_IN_PIXELS)


