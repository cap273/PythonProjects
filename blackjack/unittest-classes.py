import unittest
import tkinter as tk

from deck import Deck
from hand import Hand
from card import Card


class TestBlackjackClasses(unittest.TestCase):

    def test_card(self):
        window= tk.Tk()
        window.title('test')
        
        # Check proper instantiation of 10 of clubs
        thisCard= Card(Card.CLUBS, 10, 10)
        self.assertEqual(thisCard.value, 10)
        self.assertEqual(thisCard.suit, Card.CLUBS)
        self.assertEqual(thisCard.cardNumber, 10)

        # Check proper instantiation of Jack of clubs (value of 10, but cardNumber of 11)
        anotherCard= Card(Card.CLUBS, 10, 11)
        self.assertEqual(anotherCard.value, 10)
        self.assertEqual(anotherCard.suit, Card.CLUBS)
        self.assertEqual(anotherCard.cardNumber, 11)

        # Ensure that trying to instantiate a Jack of clubs with the wrong value raises an exception
        # Format: self.assertRaises(ExpectedException, afunction, arg1, arg2)
        self.assertRaises(ValueError, Card, Card.CLUBS, 11, 11)

        # Check that all images have been loaded into the class attribute class_images, after calling the function load_images()
        self.assertEqual(len(Card.card_images), 0)
        Card.load_images()
        self.assertEqual(len(Card.card_images), 52)

    def test_hand(self):
        window= tk.Tk()
        window.title('test')

        thisCard= Card(Card.SPADES, 10, 10)
        anotherCard= Card(Card.SPADES, 5, 5)
        thirdCard= Card(Card.CLUBS, 11, 1)

        thisHand= Hand()
        thisHand.add(thisCard)
        thisHand.add(anotherCard)
        thisHand.add(thirdCard)

        self.assertEqual(len(thisHand.cards), 3)
        self.assertEqual(thisHand.total, 26)

        thisHand.reset()
        self.assertEqual(len(thisHand.cards), 0)

    def test_deck(self):
        window= tk.Tk()
        window.title('test')

        thisDeck= Deck()
        self.assertEqual(len(thisDeck.cards), 52)
        self.assertEqual(len(thisDeck.cardsDealt), 0)

        firstDealtCard= thisDeck.deal()
        secondDealtCard= thisDeck.deal()

        self.assertEqual(len(thisDeck.cards), 50)
        self.assertEqual(len(thisDeck.cardsDealt), 2)
        self.assertEqual(thisDeck.cardsDealt[0], firstDealtCard)
        self.assertEqual(thisDeck.cardsDealt[1], secondDealtCard)

        thisDeck.shuffle()
        self.assertEqual(len(thisDeck.cards), 52)
        self.assertEqual(len(thisDeck.cardsDealt), 0)
        self.assertTrue(firstDealtCard in thisDeck.cards[0:2])
        self.assertTrue(secondDealtCard in thisDeck.cards[0:2])

        # The next card dealt cannot be either firstDealtCard or secondDealtCard, which are on the bottom
        anotherCardDealt= thisDeck.deal()
        self.assertFalse(firstDealtCard is anotherCardDealt)
        self.assertFalse(secondDealtCard is anotherCardDealt)

if __name__ == '__main__':
    unittest.main()
