#python3 -m Pyro4.naming

import random
try:
    from tkinter import *
except ImportError:
    from Tkinter import *
import Pyro4
from Pyro4 import threadutil
import Pyro4.util
import Pyro4.core


@Pyro4.expose
class dealer(object):
    names = []
    players = 0
    current_players = 0
    deck = {"1S":1,"2S":2,"3S":3,"4S":4,"5S":5,"6S":6,"7S":7,"8S":8,"9S":9,"10S":10,"JS":11,"QS":12,"KS":13,"1H":1,"2H":2,"3H":3,"4H":4,"5H":5,"6H":6,"7H":7,"8H":8,"9H":9,"10H":10,"JH":11,"QH":12,"KH":13,"1D":1,"2D":2,"3D":3,"4D":4,"5D":5,"6D":6,"7D":7,"8D":8,"9D":9,"10D":10,"JD":11,"QD":12,"KD":13,"1C":1,"2C":2,"3C":3,"4C":4,"5C":5,"6C":6,"7C":7,"8C":8,"9C":9,"10C":10,"JC":11,"QC":12,"KC":13}
    def __init__(self):
        pass
        
    def deal(self):
        
        random1 = random.choice(list(self.deck.keys())) #randomize card
        self.deck.pop(random1) #remove from deck
        print("===========================")
        print(self.deck)

        random2 = random.choice(list(self.deck.keys()))#randomize card
        self.deck.pop(random2) #remove from deck

        print("Card 1: "+random1)
        print("Card 2: "+random2)
        hand = [random1,random2]
        
        return hand


    def hit(self,currentHand):
        
        random1 = random.choice(list(self.deck.keys())) #randomize card
        self.deck.pop(random1) #remove from deck
        print("Card 1: "+random1)

        currentHand.append(random1)

        return currentHand

    def reshuffle(self):
        self.deck = {}
        self.deck = {"1S":1,"2S":2,"3S":3,"4S":4,"5S":5,"6S":6,"7S":7,"8S":8,"9S":9,"10S":10,"JS":11,"QS":12,"KS":13,"1H":1,"2H":2,"3H":3,"4H":4,"5H":5,"6H":6,"7H":7,"8H":8,"9H":9,"10H":10,"JH":11,"QH":12,"KH":13,"1D":1,"2D":2,"3D":3,"4D":4,"5D":5,"6D":6,"7D":7,"8D":8,"9D":9,"10D":10,"JD":11,"QD":12,"KD":13,"1C":1,"2C":2,"3C":3,"4C":4,"5C":5,"6C":6,"7C":7,"8C":8,"9C":9,"10C":10,"JC":11,"QC":12,"KC":13}

    def register(self,name):
        self.names.append(name)
        self.current_players = self.current_players + 1 

    def get_names(self):
        print(self.names)
        return self.names

    def get_players(self):
        print(self.players)
        return self.players
    
    def get_current_players(self):
        print(self.current_players)
        return self.current_players


def main():
    
    try:
        daemon = Pyro4.Daemon(host="127.0.0.1")
        ns = Pyro4.locateNS()
        uri = daemon.register(dealer())
        ns.register("it238.blackjack", uri)
        print("Black Jack Server is Ready.")
        daemon.requestLoop()
    except Pyro4.errors.NamingError:
        print("Can't find the Pyro Nameserver. Running without remote connections.")

if __name__ == "__main__":
    main()