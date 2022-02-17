#!/usr/bin/env python3
                        #GUI for blackjack game.
import tkinter as tk
from tkinter import ttk
import sys, traceback

import ui
import programtime
import db
from db import Session
from objects import Card, Deck, Hand

class BlackjackFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.parent = parent

        #String Variables for the Entry Fields.
        self.money = tk.StringVar()
        self.bet = tk.StringVar()
        self.dealercards = tk.StringVar()
        self.dealerpoints = tk.StringVar()
        self.yourcards = tk.StringVar()
        self.yourpoints = tk.StringVar()
        self.result = tk.StringVar()

        self.hit = ttk.Button(self, text="Hit", state="disabled", command = self.bothHit)
        self.stand = ttk.Button(self, text="Stand", state="disabled", command = self.stand)
        self.play = ttk.Button(self, text="Play", command=self.validateFunds)

        self.initCompontents()

        #load the wallet/ StartMoney/ decks/ hands

        self.deck = []
        self.player = []
        self.dealer = []
        self.startTime = ""
        
        
        self.startMoney = 0.0
        self.startMoney = ui.getStart()
        wallet = self.startMoney

        #Once the wallet is loaded, set it in the moneyF textbox.
        self.initWallet(wallet)
        
    
    def initCompontents(self):
        self.pack()

        #empty Lables for the purpose of expanding the width of the program and fields.
        ttk.Label(self, width=10).grid(column=1, row=2, sticky=tk.W)
        ttk.Label(self, width=10).grid(column=2, row=2, sticky=tk.W)
        ttk.Label(self, width=10).grid(column=3, row=2, sticky=tk.W)
        ttk.Label(self, width=10).grid(column=4, row=2, sticky=tk.W)

        #Creating the Labels
        ttk.Label(self, text="Money: ").grid(column=0, row=0, padx=3, pady=3, sticky=tk.W)
        ttk.Label(self, text="Bet: ").grid(column=0, row=1, padx=3, pady=3, sticky=tk.W)
        ttk.Label(self, text="DEALER").grid(column=0, row=2, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self, text="Cards: ").grid(column=0, row=3, padx=3, pady=3, sticky=tk.W)
        ttk.Label(self, text="Points: ").grid(column=0, row=4, padx=3, pady=3, sticky=tk.W)
        ttk.Label(self, text="YOU").grid(column=0, row=5, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self, text="Cards: ").grid(column=0, row=6, padx=3, pady=3, sticky=tk.W)
        ttk.Label(self, text="Points: ").grid(column=0, row=7, padx=3, pady=3, sticky=tk.W)
        ttk.Label(self, text="RESULT: ").grid(column=0, row=9, padx=3, pady=3, sticky=tk.W)

        #Create the Entry Fields
        ttk.Entry(self, textvariable=self.money, state='readonly').grid(column=1, row=0, columnspan=2, sticky=tk.EW)
        ttk.Entry(self, textvariable=self.bet).grid(column=1, row=1, columnspan=2, sticky=tk.EW)
        ttk.Entry(self, textvariable=self.dealercards, state='readonly').grid(column=1, row=3, columnspan=4, sticky=tk.EW)
        ttk.Entry(self, textvariable=self.dealerpoints, state='readonly').grid(column=1, row=4, columnspan=2, sticky=tk.EW)
        ttk.Entry(self, textvariable=self.yourcards, state='readonly').grid(column=1, row=6, columnspan=4, sticky=tk.EW)
        ttk.Entry(self, textvariable=self.yourpoints, state='readonly').grid(column=1, row=7, columnspan=2, sticky=tk.EW)
        ttk.Entry(self, textvariable=self.result, state='readonly').grid(column=1, row=9, columnspan=4, sticky=tk.EW)

        #Create the Buttons
        self.hit.grid(column=1, row=8, sticky=tk.EW)
        self.stand.grid(column=2, row=8, sticky=tk.EW)
        self.play.grid(column=1, row=10, sticky=tk.EW)
        ttk.Button(self, text="Exit", command=root.destroy).grid(column=2, row=10, sticky=tk.EW)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)


    def initWallet(self, wallet):
        self.money.set(wallet)

    def validateFunds(self):
        try: 
            if float(self.money.get()) <= 5:
                print()
                print("You didn't have enough money and had to buy more chips.")
                self.money.set(self.money.get + 100.00)
            else:
                pass

            if float(self.money.get()) > 5:
                self.getBet()
        except:
            traceback.print_exc(file=sys.stdout)


    def getBet(self):
        validBet = False
        if validBet == False:
            try:
                if float(self.bet.get()) <= float(self.money.get()) and float(self.bet.get()) >= 5 and float(self.bet.get()) <= 1000:
                    validbet = True
                    self.gameStart()
                else:
                    raise exception
            except:
                self.bet.set("Your bet cannot be below your total wallet amount, below 5, or higher than 1000.")


    def gameStart(self):
        #These below will reset all of the values when the game is restarted.
        self.dealercards.set("")
        self.dealerpoints.set("")
        self.yourcards.set("")
        self.yourpoints.set("")
        self.result.set("")
        self.deck = ui.getDeck()
        self.player = Hand()
        self.dealer = Hand()

        self.startTime = programtime.getStartTime()

        #The First Move
        ui.dealerHit(self.deck, self.dealer)
        ui.playerHit(self.deck, self.player)
        ui.playerHit(self.deck, self.player)

        #Setting it up to show the cards and point values.
        self.dealercards.set(self.dealer.cardList())
        self.dealerpoints.set(self.dealer.totalValue())
        self.yourcards.set(self.player.cardList())
        self.yourpoints.set(self.player.totalValue())

        #enabling hit and stand.
        #disabling the play button, which is re-enabled after stand is clicked. 
        self.hit.config(state="enabled")
        self.stand.config(state="enabled")
        self.play.config(state="disabled")
        

    def bothHit(self):
        ui.playerHit(self.deck, self.player)
        ui.dealerHit(self.deck, self.dealer)
        
        self.dealercards.set(self.dealer.cardList())
        self.dealerpoints.set(self.dealer.totalValue())
        self.yourcards.set(self.player.cardList())
        self.yourpoints.set(self.player.totalValue())


    def stand(self):
        if self.player.totalValue() > 21:
            difference = 99
        else:
            difference = 21 - self.player.totalValue()

        if self.dealer.totalValue() >= 21:
            difference2 = self.dealer.totalValue() - 21
        else:
            difference2 = 21 - self.dealer.totalValue()

        if difference > difference2:
            self.result.set("Sorry. You lose")
            loss = ui.playerLoss(float(self.money.get()), float(self.bet.get()))
            self.money.set(loss)
        elif difference < difference2:
            self.result.set("The dealer busted. You win!")
            win = ui.playerWin(float(self.money.get()), float(self.bet.get()))
            self.money.set(win)
        else:
            self.result.set("It was a tie...")
            
        stopTime = programtime.getEndTime()
        session = Session(self.startTime, self.startMoney, float(ui.getAddedMoney(self.startMoney, self.money.get())), stopTime, self.money.get())
        session.recordSession()
        self.hit.config(state="disabled")
        self.stand.config(state="disabled")
        self.play.config(state="enabled")
        

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Blackjack")
    BlackjackFrame(root)
    root.mainloop()
