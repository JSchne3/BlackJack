#!/usr/bin/env python3
#Objects for Blackjack program go here.
from decimal import Decimal, ROUND_HALF_UP
import random

#Card Class
class Card:
    def __init__(self, rank="", suit="", value=0):
        self.rank = rank
        self.suit = suit
        self.value = value

    def printCard(self):
        strrank = self.rank
        strof = " of "
        strsuit = self.suit
        print(strrank + strof + strsuit)

    def getValue(self):
        return self.value

    def getRank(self):
        return str(self.rank)


#Deck Class
class Deck:
    def __init__(self, value=0):
        self.list = []
        self.value = value

    def addCard(self, card):
        self.list.append(card)

    def shuffleDeck(self):
        random.shuffle(self.list)

    def getCard(self):
        card = self.list.pop(0)
        return card
    
    def totalValue(self):
        self.value = 0
        for card in self.list:
            self.value += int(card.getValue())
        return self.value

    def listCards(self):
        for card in self.list:
            card.printCard()


#the Hand Class inherits from the Deck class so that it can store cards much like a deck does, and can use the methods that add and remove cards
#The Dealer and Player objects in the main module are both Hand Classes.
class Hand(Deck):
    def __init__(self):
        Deck.__init__(self)

    def countCards(self):
        count=0
        for card in self.list:
            count += 1
        return i

    def cardList(self):
        cardlist = ""
        for card in self.list:
            cardlist = cardlist + " " + card.getRank()
        return cardlist
