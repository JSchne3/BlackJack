#!/usr/bin/env python3
#This module stores the code for the user interface

#Classes and Modules from Python
import sys
import locale as lc
from decimal import Decimal, ROUND_HALF_UP

#Classes and Modules created for this game.
from objects import Card, Deck, Hand
from db import Session
import db
import programtime

#global
result = lc.setlocale(lc.LC_ALL, "")
if result == "C":
    lc.setlocale(lc.LC_ALL, "en_US")
line = "{} {}"





#This method checks the wallet amount at the start of the game.
#if below a certain threshold, asks if you'd like to buy more chips.
#if the wallet amount is valid, gets the bet amount and starts the game.
def checkFunds(wallet, deck, player, dealer):
    if wallet <= 5:
        print()
        buyMore = input("You are out of chips, would you like to buy some more? (y/n): ")
        if buyMore != 'y':
            sys.exit("See you another time!")
        else:
            wallet = wallet + 100
            print(line.format("Money:", lc.currency(wallet, grouping=True)))
    else: pass

    if wallet > 5:
        betAmount = getBet(wallet)
        wallet = gameLoop(wallet, betAmount, deck, player, dealer)
    return wallet



#This method gets the bet amount from the user and validates it. 
def getBet(wallet):
    validbet = False
    while validbet == False:
        try:
            betAmount = float(input("Bet amount: "))
            print()
            if betAmount <= wallet and betAmount >= 5 and betAmount <= 1000:
                validbet = True
            else:
                raise exception
        except:
            print("Bet must not exceed your total funds, and must be between 5 and 1000.")
            print("Please enter a valid bet.")
    return betAmount



#This method is the main game loop, which plays after the wallet and bet have been verified.
def gameLoop(wallet, betAmount, deck, player, dealer):
    #The first move
    dealerHit(deck, dealer)
    playerHit(deck, player)
    playerHit(deck, player)
    print("DEALER'S SHOW CARDS: ")
    dealer.listCards()
    print()
    print("YOUR CARDS: ")
    player.listCards()
    print()
    playerMove = input("Hit or Stand? (hit/stand): ")

    #The game Loop
    while playerMove != 'exit':
        if playerMove.lower() == 'hit':
            dealerHit(deck, dealer)
            playerHit(deck, player)
            print("YOUR CARDS: ")
            player.listCards()
            print()
            playerMove = input("Hit or Stand? (hit/stand): ")
        elif playerMove.lower() == 'stand':
            wallet = stand(deck, player, dealer, betAmount, wallet)
            playerMove = "exit"
        else:
            print("Something went wrong.")
    return wallet




#Create and shuffle Deck at start of game.
def createDeck(deck):
    cardDict = {"suits":['Clubs', 'Diamonds', 'Hearts', 'Spades'],
                "ranks":['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King'],
                "values":[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]}
    suits = cardDict["suits"]
    ranks = cardDict["ranks"]
    values = cardDict["values"]
    for suit in suits:
        i = 0
        for rank in ranks:
            card = Card(rank, suit, values[i])
            deck.addCard(card)
            i += 1
    deck.shuffleDeck()
    return deck


#this method is used for all dealer hits
def dealerHit(deck, dealer):
    if dealer.totalValue() <= 17:
        card = deck.getCard()
        dealer.addCard(card)
    else:
        pass
    

#this method is used for all player hits
def playerHit(deck, player):
    card = deck.getCard()
    player.addCard(card)
    

#if the player decides to stand, this will compare the point values between the Dealer and the Player.
def stand(deck, player, dealer, betAmount, wallet):
    print()
    print("DEALER'S CARDS:")
    dealer.listCards()
    print()
    print("YOUR POINTS: {}".format(player.totalValue()))
    print("DEALER'S POINTS: {}".format(dealer.totalValue()))
    print()
    if player.totalValue() > 21:
        difference = 99
    elif player.totalValue() < 21:
        difference = 21 - player.totalValue()
    elif player.totalValue() == 21:
        difference = 0
    else:
        print("Error Calculating Player Score")

    if dealer.totalValue() > 21:
        difference2 = dealer.totalValue() - 21
    elif dealer.totalValue() < 21:
        difference2 = 21 - dealer.totalValue()
    elif dealer.totalValue() == 21:
        difference2 = 0
    else:
        print("Error Calculating Dealer Score")

    if difference > difference2:
        wallet = playerLoss(wallet, betAmount)
        print("Sorry. You lose.")
        print(line.format("Money:", lc.currency(wallet, grouping=True)))
    elif difference < difference2:
        wallet = playerWin(wallet, betAmount)
        print("Yay! The dealer busted. You win!")
        print(line.format("Money:", lc.currency(wallet, grouping=True)))
    elif difference == difference2:
        print("It's a tie...")
    else:
        print("There was an error comparing the scores")
    return wallet





#Money Methods 
def getStart():
    return db.loadWallet()

def getAddedMoney(startMoney, wallet):
    addedMoney = Decimal(wallet) - Decimal(startMoney)
    return addedMoney

def playerLoss(wallet, betAmount):
    wallet = Decimal(wallet)
    wallet = wallet.quantize(Decimal("1.00"))
    betAmount = Decimal(betAmount)
    betAmount = betAmount.quantize(Decimal("1.00"))
    
    wallet = wallet - betAmount
    wallet = wallet.quantize(Decimal("1.00"), ROUND_HALF_UP)
    return wallet

def playerWin(wallet, betAmount):
    payout = 1.5
    wallet = Decimal(wallet)
    wallet = wallet.quantize(Decimal("1.00"))
        
    betAmount = Decimal(betAmount)
    betAmount = betAmount.quantize(Decimal("1.00"))

    payout = Decimal(payout)
    payout = payout.quantize(Decimal("1.00"))
        
    wallet = wallet + (betAmount * payout)
    wallet = wallet.quantize(Decimal("1.00"), ROUND_HALF_UP)
    return wallet




#Main Method
def main():
    startMoney = 0.0
    startMoney = getStart(startMoney)
    wallet = startMoney
    playAgain = "y"
    while playAgain.lower() == 'y':
        print("BLACKJACK!")
        print("Blackjack payout is 3:2")

        startTime = ""
        startTime = programtime.getStartTime()
        
        print()
        print(line.format("Money:", lc.currency(wallet, grouping=True)))
        
        deck = Deck()
        player = Hand()
        dealer = Hand()
        deck = createDeck(deck)
        
        wallet = checkFunds(wallet, deck, player, dealer)
        print()
        playAgain = input("Play Again? (y/n): ")
        print()

    stopTime = ""
    stopTime = programtime.getEndTime()
    programtime.getElapsedTime(stopTime, startTime)
    addedMoney = float(getAddedMoney(startMoney, wallet))
    stopMoney = float(wallet)

    session = Session(startTime, startMoney, addedMoney, stopTime, stopMoney)
    session.recordSession()
    
    print()
    print("Come back soon!")
    
if __name__ == "__main__":
    main()


#The Below methods were added to be used by the GUI version program specifically. 
#They do not affect and are not used by the console version of the game.
def getDeck():
    deck = Deck()
    cardDict = {"suits":['Clubs', 'Diamonds', 'Hearts', 'Spades'],
                "ranks":['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King'],
                "values":[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]}
    suits = cardDict["suits"]
    ranks = cardDict["ranks"]
    values = cardDict["values"]
    for suit in suits:
        i = 0
        for rank in ranks:
            card = Card(rank, suit, values[i])
            deck.addCard(card)
            i += 1
    deck.shuffleDeck()
    return deck

