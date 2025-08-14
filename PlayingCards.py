import copy

debug = False

class debugger:
    @staticmethod
    def msg(s:str):
        if debug:
            print(s)

class PlayingCard:
    def __init__(self, name, suit):
        self.validnames = {'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'}

        self.suitnames = {"Spades" : ("\u2660", "\u2664", "black"),"Clubs": ("\u2663", "\u2667", "black"),
                    "Hearts" : ("\u2665","\u2661", "red"),"Diamonds" : ("\u2666","\u2662", "red")} # Unicode characters for suits
        
        if name not in self.validnames:
            raise ValueError("Invalid card name")
        if suit not in self.suitnames:
            raise ValueError("Invalid suit name")
        
        self.name = name
        self.suit = suit
        self.filename = str(name) + '_' + suit[0].lower() + '.gif' #filename for .gif asset for GUI implementation
        self.card_display = name + suit

        # self.blackjack_value = 0
        self.isVisible = True # set to False later to have cards face-down
        self.invertColors = False # Depreciated. Must reconfig self.suitnames for Terminal
        self.suit_color = self.suitnames[suit][2]
        self.blackjack_value = self.getBlackJackValue()

        if not self.invertColors:   #Toggles between different unicode suit rcharacters. Set self.invertcolors to accomodate dark/light terminals
            self.suit = self.suitnames[suit][0]
        else:
            self.suit = self.suitnames[suit][1]

    def getBlackJackValue(self):
        if self.name.isalpha():
            if self.name == "A": return 1
            else: return 10
        else: return self.name

    def getAbsValue(self): 
        match self.name:
            case "J":
                return 11
            case "Q":
                return 12
            case "K":
                return 13
            case "A":
                return 14
            case _:
                return int(self.name)          
             
    def __str__(self) -> str:
        if self.isVisible: 
            self.card_display = self.name + self.suit
            return self.card_display
        else: return "???" # card face-down
        
class Deck:
    def __init__(self):
        self.cards = []
        self.topindex = 0
        Joker = PlayingCard("J","Spades") #card purely for iteration, used to build deck
        for suit in Joker.suitnames:
            for name in Joker.validnames:
                card = PlayingCard(name,suit)
                self.cards.append(copy.deepcopy(card))
        del Joker #no longer needed since deck is now built

    def isEmpty(self) -> bool:
        if not self.cards:
            return True
        else: return False

    def print(self):
        for i, _ in enumerate(self.cards, self.topindex):
            self.cards[i].print()

    def shuffle(self):
        import random
        random.shuffle(self.cards)
        self.topindex = 0

class DiscardPile:
    cards = []
    topindex = 0 # Exists only for compatability with Deck operations in Hand functions
    
    def isEmpty(self) -> bool:
        if not self.cards:
            return True
        else: return False

    def reset(self):
        self.cards = []

    def print(self):
        if self.isEmpty():
            print("Discard pile is empty.")
        else:
            self.cards[0].print()

class Hand:
    def __init__(self):
        self.cards:list[PlayingCard] = []

    def draw(self, deck: Deck | DiscardPile):
        if deck.isEmpty():
            if type(deck) == Deck: print("Deck is empty!")
            elif type(deck) == DiscardPile: print("Discard pile empty.")
        else:
            if type(deck) == Deck:
                self.cards.append(deck.cards[deck.topindex])
                deck.topindex += 1
            elif type(deck) == DiscardPile:
                self.cards.append(deck.cards[0])
                deck.cards.pop()

    def drawm(self, deck: Deck | DiscardPile, num_cards):
        for _ in range(num_cards):
            self.draw(deck)

    def discard(self, card:PlayingCard, pile:DiscardPile):
        pile.cards.insert(0, card)
        self.cards.remove(card)
    
    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def __str__(self) -> str:
        output = ''
        for card in self.cards:
            output = output + card.__str__() + ','
        return output