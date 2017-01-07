import random
import sys
import server
import time
import Pyro4
from Pyro4 import threadutil
import Pyro4.util

try:
    from tkinter import *
except ImportError:
    from Tkinter import *

class GUI():
    def __init__(self,server):
        self.tk = Tk()
        self.server = server
        
        self.playerImages = ["pimg1","pimg2","pimg3","pimg4","pimg5","pimg6"]
        self.dealerImages = ["dimg1","dimg2","dimg3","dimg4","dimg5","dimg6"]
        # self.playerImages = []
        # self.dealerImages = []

        self.pbutton1 = Button(self.tk)
        self.pbutton2 = Button(self.tk)
        self.pbutton3 = Button(self.tk)
        self.pbutton4 = Button(self.tk)
        self.pbutton5 = Button(self.tk)
        self.pbutton6 = Button(self.tk)

        self.dbutton1 = Button(self.tk)
        self.dbutton2 = Button(self.tk)
        self.dbutton3 = Button(self.tk)
        self.dbutton4 = Button(self.tk)
        self.dbutton5 = Button(self.tk)
        self.dbutton6 = Button(self.tk)

        self.playerButtons = [self.pbutton1,self.pbutton2,self.pbutton3,self.pbutton4,self.pbutton5,self.pbutton6]
        self.dealerButtons = [self.dbutton1,self.dbutton2,self.dbutton3,self.dbutton4,self.dbutton5,self.dbutton6]
        # self.playerButtons = []
        # self.dealerButtons = []

        self.playerPts = 0
        self.dealerPts = 0
        self.player_total = 0
        self.dealer_total = 0
        self.dealerStand = False
        self.playerStand = False
        self.computerHand = []
        self.playerHand = []
        self.tk.wm_title("RMI Black Jack Game - Client")
        self.tk.geometry("500x500")
        self.tk.configure(background = 'dark green')
        self.tk.resizable(width=FALSE, height=FALSE)
        
        self.img1 = PhotoImage(file="cards/back.gif")
        self.button1 = Button(self.tk, image=self.img1)
        self.llabel = Label(self.tk, text="Black Jack!", bg="dark green", fg="white", font=40)
        self.dealermessage = Label(self.tk, text="", bg="dark green")
        self.playermessage = Label(self.tk, text="", bg="dark green")
        self.playermessage2 = Label(self.tk, text="", bg="dark green")
        self.result = Label(self.tk, text="", bg="dark green")
        self.dealerscore = Label(self.tk, text="", bg="dark green")
        self.playerscore = Label(self.tk, text="", bg="dark green")


        self.hitbutton = Button(self.tk, text="Hit", state="disabled", command=lambda: self.buttonhandler.button_clicked("hit"))
      
        self.standbutton = Button(self.tk, text="Stand", state="disabled", command=lambda: self.buttonhandler.button_clicked("stand"))
      
        self.dealbutton = Button(self.tk, text="Deal", state="disabled", command=lambda: self.buttonhandler.button_clicked("deal"))
      
        self.rlabel = Label(self.tk, text="Players:", bg="dark green", fg="white")
        self.listbox = Listbox(self.tk, width=15, height=25, font=(None, 8))
        self.blank_label = Label( self.tk, textvariable=" ---- ", bg="green")
        
        self.startbutton = Button(self.tk, text="Start Game", command=lambda: self.buttonhandler.button_clicked("start"))
        
        self.button1.place(x=150, y=150)
        self.llabel.place(x=145, y=250)
        self.hitbutton.place(x=50, y=460)
        self.standbutton.place(x=130, y=460)
        self.dealbutton.place(x=220, y=460)
        self.startbutton.place(x=300, y=460)

        self.rlabel.place(x=400, y=30)
        self.listbox.place(x=370, y=50)

        self.buttonhandler = self

    def defineCard(self, card):
        
        if card[1] == 'H':
            suit = "hearts"
        elif card[1] == 'C':
            suit = "clubs"
        elif card[1] == 'D':
            suit = "diamonds"
        else: 
            suit = "spades"

        if card[0] == 'K':
            rank = '13'
        elif card[0] == 'Q':
            rank = '12'    
        elif card[0] == 'J':
            rank = '11'
        else:
            rank = card[0]

        values = [rank, suit]
        return values

    def computeFaceUpCards(self, cards):
        total = 0
        count = 0
        # print(len(cards))

        while count < len(cards)-1:
            total = total + int(cards[count][0])
            count = count + 1

        return total

    def computeTotalCards(self, cards):
        total = 0
        count = 0
        # print(len(cards))

        while count < len(cards):
            total = total + int(cards[count][0])
            count = count + 1

        return total
    def updateDealer(self):
        self.dealermessage.destroy() 
        computerCardValues = []
        for card in self.computerHand:
            computerCardValues.append(self.defineCard(card))

        print(computerCardValues)
        dealer_message = "Total Cards: "
        dealer_up = self.computeTotalCards(computerCardValues)
        self.dealermessage = Label(self.tk, text=dealer_message+str(dealer_up), bg="dark green", fg="white")
        self.dealermessage.place(x=120, y=140)
        counter = 0
        #destroy cards
        while counter < len(computerCardValues):
            self.dealerButtons[counter].destroy()
            counter = counter + 1

        counter = 0
        x_axis = 30
        for numbers in computerCardValues:
            
            self.dealerImages[counter] = PhotoImage(file="cards/"+numbers[1]+"/"+str(numbers[0])+".gif")
            self.dealerButtons[counter] = Button(self.tk, image=self.dealerImages[counter])
            
            self.dealerButtons[counter].place(x=x_axis, y=30)
            x_axis = x_axis + 50    
            counter = counter + 1
    def checkWinner(self, dealerScore, playerScore):
        
        print("DEALER: ",dealerScore) 
        print("PLAYER: ",playerScore)
        self.dealbutton.destroy()
        self.result.destroy()
        self.dealerscore.destroy() 
        self.playerscore.destroy()


        if dealerScore == 21 and playerScore == 21:
            winner = "draw"
        elif dealerScore == 21:
            winner = "dealer"
        elif playerScore == 21:
            winner = "player"
        elif playerScore > 21:
            winner = "player-busted"
        elif dealerScore > 21:
            winner = "dealer-busted"    
        elif self.playerStand and self.dealerStand:
            if dealerScore == playerScore:
                winner = "draw"
            elif dealerScore > playerScore:
                winner = "dealer"
            else: 
                winner = "player"
        else:
            winner = "continue"


        if (winner == "player"):
            self.result = Label(self.tk, text="You won!!!", bg="dark green", fg="white")
            self.playerPts = self.playerPts + 1
            self.dealbutton = Button(self.tk, text="Deal", command=lambda: self.buttonhandler.button_clicked("deal"))
            self.dealbutton.place(x=220, y=460)
            self.updateDealer()

        elif (winner == "dealer"):
            self.result = Label(self.tk, text="You lost! \n Dealer Wins", bg="dark green", fg="white")
            self.dealerPts = self.dealerPts + 1
            self.dealbutton = Button(self.tk, text="Deal", command=lambda: self.buttonhandler.button_clicked("deal"))
            self.dealbutton.place(x=220, y=460)
            self.updateDealer()

        elif (winner == "dealer-busted"):
            self.result = Label(self.tk, text="You won!!! \n Dealer Busted", bg="dark green", fg="white")
            self.playerPts = self.playerPts + 1
            self.dealbutton = Button(self.tk, text="Deal", command=lambda: self.buttonhandler.button_clicked("deal"))
            self.dealbutton.place(x=220, y=460) 
            self.updateDealer()

        elif (winner == "player-busted"):
            self.result = Label(self.tk, text="You lost!!! \n Player Busted", bg="dark green", fg="white")
            self.dealerPts = self.dealerPts + 1
            self.dealbutton = Button(self.tk, text="Deal", command=lambda: self.buttonhandler.button_clicked("deal"))
            self.dealbutton.place(x=220, y=460) 
            self.updateDealer()

        elif (winner == "draw"):
            self.result = Label(self.tk, text="Ooops! The game is draw!", bg="dark green", fg="white")
            self.dealbutton = Button(self.tk, text="Deal", command=lambda: self.buttonhandler.button_clicked("deal"))
            self.dealbutton.place(x=220, y=460)
            self.updateDealer()

        else:
            self.result = Label(self.tk, text="Do you  want to hit or stand?", bg="dark green", fg="white") 
            self.dealbutton = Button(self.tk, text="Deal", state="disabled")
            self.dealbutton.place(x=220, y=460)

        

        self.dealerscore = Label(self.tk, text="Dealer Score: "+str(self.dealerPts), bg="dark green", fg="white")
        self.playerscore = Label(self.tk, text="Player Score: "+str(self.playerPts), bg="dark green", fg="white")
        self.result.place(x=120, y=210)
        self.dealerscore.place(x=20, y=190)
        self.playerscore.place(x=20, y=230)

    def stand(self, player):
        
        if player == "dealer":
            self.dealerStand = True
        else: 
            self.playerStand = True

    def dealerMove(self):

        if self.dealer_total >= 21 or self.player_total >= 21:
            print("continue")
            #disable hit and stand
            self.hitbutton.destroy()
            self.standbutton.destroy()

            self.hitbutton = Button(self.tk, text="Hit", state="disabled", command=lambda: self.buttonhandler.button_clicked("hit"))
            self.standbutton = Button(self.tk, text="Stand", state="disabled", command=lambda: self.buttonhandler.button_clicked("stand"))

            self.hitbutton.place(x=50, y=460)
            self.standbutton.place(x=130, y=460)

        else:
            if ( self.dealer_total > 15): 
                print("Stay")
                self.stand("dealer")
                self.checkWinner(self.dealer_total, self.player_total)
            if ( self.dealer_total <=15):
                self.dealerStand = False
                self.dealermessage.destroy() 
                computerCardValues = []
                self.computerHand = self.server.hit(self.computerHand)
                
                for card in self.computerHand:
                    computerCardValues.append(self.defineCard(card))

                print(computerCardValues)
                dealer_message = "Face Up Cards: "
                dealer_up = self.computeFaceUpCards(computerCardValues)
                self.dealermessage = Label(self.tk, text=dealer_message+str(dealer_up), bg="dark green", fg="white")
                
                counter = 0
                #destroy cards
                while counter < len(computerCardValues):
                    self.dealerButtons[counter].destroy()
                    counter = counter + 1

                counter = 0
                x_axis = 30
                for numbers in computerCardValues:
                    
                    if counter == len(computerCardValues) - 1:
                        self.dealerImages[counter] = PhotoImage(file="cards/back.gif")
                        self.dealerButtons[counter] = Button(self.tk, image=self.dealerImages[counter])
                    else:
                        self.dealerImages[counter] = PhotoImage(file="cards/"+numbers[1]+"/"+str(numbers[0])+".gif")
                        self.dealerButtons[counter] = Button(self.tk, image=self.dealerImages[counter])
                    
                    self.dealerButtons[counter].place(x=x_axis, y=30)
                    x_axis = x_axis + 50    
                    counter = counter + 1

                self.dealer_total = self.computeTotalCards(computerCardValues)
                self.checkWinner(self.dealer_total, self.player_total)

                self.dealermessage.place(x=120, y=140)


    def button_clicked(self, button):
        self.server.reshuffle()
        computerCardValues = []
        playerCardValues = []
        self.button1.destroy()
        self.llabel.destroy()
        self.startbutton.destroy()
        

        self.startbutton = Button(self.tk, text="Start Over", command=lambda: self.buttonhandler.button_clicked("start"))
        if button == "start":
            print("Start!!!")
            self.playerPts = 0
            self.dealerPts = 0
            
            self.computerHand = self.server.deal()

            self.playerHand = self.server.deal()

            for card in self.computerHand:
                computerCardValues.append(self.defineCard(card))
            
            print(computerCardValues)

            for card in self.playerHand:
                playerCardValues.append(self.defineCard(card))

            print(playerCardValues)

            # print(self.server.deal())
            
            dealer_message = "Face Up Cards: "
            player_message = "Face Up Cards: "
            player_message2 = "Total Cards: "
            dealer_up = 0
            player_up = 0
            
            self.dealbutton.destroy()
            self.hitbutton.destroy()
            self.standbutton.destroy()
            self.dealerscore.destroy()
            self.playerscore.destroy()
            self.dealermessage.destroy()
            self.playermessage.destroy()
            self.playermessage2.destroy()
            
            dealer_up = self.computeFaceUpCards(computerCardValues)
            player_up = self.computeFaceUpCards(playerCardValues)
            self.dealer_total = self.computeTotalCards(computerCardValues)
            self.player_total = self.computeTotalCards(playerCardValues)

            counter = 0
            x_axis = 30
            for numbers in computerCardValues:
                
                if counter == 1:
                    self.dealerImages[counter] = PhotoImage(file="cards/back.gif")
                    self.dealerButtons[counter] = Button(self.tk, image=self.dealerImages[counter])
                else:
                    self.dealerImages[counter] = PhotoImage(file="cards/"+numbers[1]+"/"+str(numbers[0])+".gif")
                    self.dealerButtons[counter] = Button(self.tk, image=self.dealerImages[counter])
                
                self.dealerButtons[counter].place(x=x_axis, y=30)
                x_axis = x_axis + 50    
                counter = counter + 1


            
            counter = 0 #reset counter
            x_axis = 30
            for numbers in playerCardValues:
                
                self.playerImages[counter] = PhotoImage(file="cards/"+numbers[1]+"/"+str(numbers[0])+".gif")
                self.playerButtons[counter] = Button(self.tk, image=self.playerImages[counter])
                self.playerButtons[counter].place(x=x_axis, y=270)
                x_axis = x_axis + 50
                counter = counter + 1
            
            self.dealerscore = Label(self.tk, text="Dealer Score: "+str(self.dealerPts), bg="dark green", fg="white")
            self.playerscore = Label(self.tk, text="Player Score: "+str(self.playerPts), bg="dark green", fg="white")

            self.dealermessage = Label(self.tk, text=dealer_message+str(dealer_up), bg="dark green", fg="white")
            self.playermessage = Label(self.tk, text=player_message+str(player_up), bg="dark green", fg="white")
            self.playermessage2 = Label(self.tk, text=player_message2+str(self.player_total), bg="dark green", fg="white")

            self.checkWinner(self.dealer_total, self.player_total)
            self.hitbutton = Button(self.tk, text="Hit", command=lambda: self.buttonhandler.button_clicked("hit"))
      
            self.standbutton = Button(self.tk, text="Stand", command=lambda: self.buttonhandler.button_clicked("stand"))

            self.dealerscore.place(x=20, y=190)
            self.playerscore.place(x=20, y=230)
            self.dealermessage.place(x=120, y=140)
            self.playermessage.place(x=120, y=380)
            self.playermessage2.place(x=120, y=400)
            self.hitbutton.place(x=50, y=460)
            self.standbutton.place(x=130, y=460)
            self.startbutton.place(x=300, y=460)

        elif button == "hit":
            self.playerStand = False
            self.playermessage.destroy()
            self.playermessage2.destroy()

            self.playerHand = self.server.hit(self.playerHand)
            
            for card in self.playerHand:
                playerCardValues.append(self.defineCard(card))

            print(playerCardValues)
            player_message = "Face Up Cards: "
            player_message2 = "Total Cards: "

            player_up = self.computeFaceUpCards(playerCardValues)
            self.player_total = self.computeTotalCards(playerCardValues)
            # print("TOTAL PLAYER: ", self.player_total )
            self.playermessage = Label(self.tk, text=player_message+str(player_up), bg="dark green", fg="white")
            self.playermessage2 = Label(self.tk, text=player_message2+str(self.player_total), bg="dark green", fg="white")

            counter = 0
            #destroy cards
            while counter < len(playerCardValues):
                self.playerButtons[counter].destroy()
                counter = counter + 1


            counter = 0 
            x_axis = 30
            for numbers in playerCardValues:
                self.playerImages[counter] = PhotoImage(file="cards/"+numbers[1]+"/"+str(numbers[0])+".gif")
                self.playerButtons[counter] = Button(self.tk, image=self.playerImages[counter])
                self.playerButtons[counter].place(x=x_axis, y=270)
                x_axis = x_axis + 50
                counter = counter + 1


            self.checkWinner(self.dealer_total, self.player_total)
            
            self.playermessage.place(x=120, y=380)
            self.playermessage2.place(x=120, y=400)
            self.startbutton.place(x=300, y=460)

            self.dealerMove()

        elif button == "stand":
            self.stand("player")


            self.checkWinner(self.dealer_total, self.player_total)
            self.startbutton.place(x=300, y=460)
            self.dealerMove()

        elif button == "deal":
            self.dealerStand = False
            self.playerStand = False

            for card in self.computerHand:
                computerCardValues.append(self.defineCard(card))

            for card in self.playerHand:
                playerCardValues.append(self.defineCard(card))

            counter = 0
            #destroy cards
            while counter < len(playerCardValues):
                self.playerButtons[counter].destroy()
                counter = counter + 1

            counter = 0
            #destroy cards
            while counter < len(computerCardValues):
                self.dealerButtons[counter].destroy()
                counter = counter + 1

            # counter = 0
            # x_axis = 30
            # for numbers in computerCardValues:
                  
            #     self.dealerButtons[counter] = Button(self.tk, bg="dark green")
                
            #     self.dealerButtons[counter].place(x=x_axis, y=30)
            #     x_axis = x_axis + 50    
            #     counter = counter + 1

            # counter = 0 #reset counter
            # x_axis = 30
            # for numbers in playerCardValues:
                
            #     self.playerButtons[counter] = Button(self.tk, bg="dark green")
            #     self.playerButtons[counter].place(x=x_axis, y=270)
            #     x_axis = x_axis + 50
            #     counter = counter + 1

            computerCardValues = []
            playerCardValues = []
            self.computerHand = []
            self.playerHand = []
            self.computerHand = self.server.deal()
            self.playerHand = self.server.deal()
            self.dealer_total = 0
            self.player_total = 0

            for card in self.computerHand:
                computerCardValues.append(self.defineCard(card))
            
            print(computerCardValues)

            for card in self.playerHand:
                playerCardValues.append(self.defineCard(card))

            print(playerCardValues)

            # print(self.server.deal())
            
            dealer_message = "Face Up Cards: "
            player_message = "Face Up Cards: "
            player_message2 = "Total Cards: "
            dealer_up = 0
            player_up = 0
            
            self.dealbutton.destroy()
            self.hitbutton.destroy()
            self.standbutton.destroy()
            self.dealerscore.destroy()
            self.playerscore.destroy()
            self.dealermessage.destroy()
            self.playermessage.destroy()
            self.playermessage2.destroy()
            
            dealer_up = self.computeFaceUpCards(computerCardValues)
            player_up = self.computeFaceUpCards(playerCardValues)
            self.dealer_total = self.computeTotalCards(computerCardValues)
            self.player_total = self.computeTotalCards(playerCardValues)

            counter = 0
            x_axis = 30
            for numbers in computerCardValues:
                
                if counter == 1:
                    self.dealerImages[counter] = PhotoImage(file="cards/back.gif")
                    self.dealerButtons[counter] = Button(self.tk, image=self.dealerImages[counter])
                else:
                    self.dealerImages[counter] = PhotoImage(file="cards/"+numbers[1]+"/"+str(numbers[0])+".gif")
                    self.dealerButtons[counter] = Button(self.tk, image=self.dealerImages[counter])
                
                self.dealerButtons[counter].place(x=x_axis, y=30)
                x_axis = x_axis + 50    
                counter = counter + 1
            
            
            counter = 0 #reset counter
            x_axis = 30
            for numbers in playerCardValues:
                
                self.playerImages[counter] = PhotoImage(file="cards/"+numbers[1]+"/"+str(numbers[0])+".gif")
                self.playerButtons[counter] = Button(self.tk, image=self.playerImages[counter])
                self.playerButtons[counter].place(x=x_axis, y=270)
                x_axis = x_axis + 50
                counter = counter + 1
            
            self.dealerscore = Label(self.tk, text="Dealer Score: "+str(self.dealerPts), bg="dark green", fg="white")
            self.playerscore = Label(self.tk, text="Player Score: "+str(self.playerPts), bg="dark green", fg="white")

            self.dealermessage = Label(self.tk, text=dealer_message+str(dealer_up), bg="dark green", fg="white")
            self.playermessage = Label(self.tk, text=player_message+str(player_up), bg="dark green", fg="white")
            self.playermessage2 = Label(self.tk, text=player_message2+str(self.player_total), bg="dark green", fg="white")

            self.checkWinner(self.dealer_total, self.player_total)
            self.hitbutton = Button(self.tk, text="Hit", command=lambda: self.buttonhandler.button_clicked("hit"))
      
            self.standbutton = Button(self.tk, text="Stand", command=lambda: self.buttonhandler.button_clicked("stand"))

            self.dealerscore.place(x=20, y=190)
            self.playerscore.place(x=20, y=230)
            self.dealermessage.place(x=120, y=140)
            self.playermessage.place(x=120, y=380)
            self.playermessage2.place(x=120, y=400)
            self.hitbutton.place(x=50, y=460)
            self.standbutton.place(x=130, y=460)
            self.startbutton.place(x=300, y=460)



   


def main():
    player_name = input("Type your name?")
    
    server = Pyro4.Proxy("PYRONAME:it238.blackjack")
    server.register(player_name)
    # server.get_names()
    
    # print(server.get_players())
    # while(server.get_players() != server.get_current_players()):
    #     print("Waiting for other players...")
    #     time.sleep(10)

    print()
    print("====================")
    print("GAME STARTED!!!")
    gui = GUI(server)
    
    names = server.get_names()
    for name in names:

        colorint = random.randint(0, 0xFFFFFF)
        color = '#%06x' % colorint
        inversecolor = 'black'
        
        gui.listbox.insert(END, name)
        gui.listbox.itemconfig(END, bg=color, fg=inversecolor)

    gui.tk.mainloop()

if __name__ == "__main__":
    main()
