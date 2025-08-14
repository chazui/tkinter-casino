from PlayingCards import *
from PlayingCards import debugger as debugger
# import copy

class WarDeck(Deck):
    def __init__(self, deck:Deck):
        self.whole_deck = deck
        self.whole_deck.shuffle()
        self.myHand = Hand()
        self.oppHand = Hand()
        self.wonCards = set()
        self.lostCards = set()

        self.myHand.drawm(self.whole_deck, 26) #Deck is split into 2 decks, represented as Hands
        self.oppHand.drawm(self.whole_deck, 26)

        self.max_index = 26

    def min_deck(self) -> int:
        return min(len(self.myHand.cards), len(self.oppHand.cards))

    def nextRound(self):
        if (self.myHand.cards and self.oppHand.cards):

            debugger.msg(f"[nextRound] myHand before operation: {[str(x) for x in self.myHand.cards]}")
            debugger.msg(f"[nextRound] wonCards before operation: {[str(x) for x in self.wonCards]}")
            debugger.msg(f"[nextRound] lostCards before operation: {[str(x) for x in self.lostCards]}")

            self.myHand.cards.extend(self.wonCards)
            for card in self.lostCards:
                debugger.msg(f"[nextRound] removing card '{str(card)}' from myHand...")
                self.myHand.cards.remove(card)

            debugger.msg(f"[nextRound] oppHand before operation: {[str(x) for x in self.oppHand.cards]}")

            self.oppHand.cards.extend(self.lostCards)
            for card in self.wonCards:
                debugger.msg(f"[nextRound] removing card '{str(card)}' from oppHand...")
                self.oppHand.cards.remove(card)

            debugger.msg(f"[nextRound] myHand after operation: {[str(x) for x in self.myHand.cards]}")
            debugger.msg(f"[nextRound] oppHand after operation: {[str(x) for x in self.oppHand.cards]}")

            self.wonCards.clear()
            self.lostCards.clear()

            self.myHand.shuffle()
            self.oppHand.shuffle()
            self.max_index = self.min_deck()

    

class WarGame:
    def __init__(self):
        self.whole_deck = Deck()
        self.deck = WarDeck(self.whole_deck)
        self.deck_pos = 0
        self.game_status = 0
        self.my_tie_cards = []
        self.opp_tie_cards = []
        self.mycards_to_display = []
        self.oppcards_to_display = []
        self.isTie = False
        self.display = "Let's play WAR!"
        self.player_display = "Click your deck to begin game!"
        self.opp_display = "Opponent Cards"
    
    def compare(self, myCard:PlayingCard, oppCard:PlayingCard):
        myScore = myCard.getAbsValue()
        oppScore = oppCard.getAbsValue()
        debugger.msg(f"[compare] isTie at start of function: {self.isTie}")

        assert myCard not in self.deck.lostCards
        assert oppCard not in self.deck.wonCards

        
        if myScore == oppScore:
            self.isTie = True
            self.display = ("Tie! Draw 3 and try again.")
            my_tiecards = []
            opp_tiecards = []
            i = 0
            max_index = self.deck.max_index
            while self.deck_pos < (max_index - 1):
                self.deck_pos += 1
                if i == 3: break
                my_tiecards.append(self.deck.myHand.cards[self.deck_pos]) 
                opp_tiecards.append(self.deck.oppHand.cards[self.deck_pos])
                i += 1

            self.my_tie_cards.extend(my_tiecards)
            self.opp_tie_cards.extend(opp_tiecards)

        elif myScore > oppScore:
            self.display = f"Win-- {myCard} > {oppCard}."
            woncards = list()
            if self.isTie:
                debugger.msg(f"[compare] Win condition after tie. Appending won cards")
                woncards.extend(self.opp_tie_cards)
                self.isTie = False
                self.my_tie_cards.clear()
                self.opp_tie_cards.clear()
            woncards.append(oppCard)
            self.deck.wonCards.update(woncards)
            self.deck_pos += 1
            debugger.msg(f"[compare] Won cards: {[str(x) for x in self.deck.wonCards]}") 

        else:
            self.display = f"Loss-- {myCard} < {oppCard}."
            lostcards = list()
            if self.isTie:
                lostcards.extend(self.my_tie_cards)
                debugger.msg(f"[compare] Loss condition after tie. Opponent appends lost cards.")
                self.isTie = False
                self.my_tie_cards.clear()
                self.opp_tie_cards.clear()
            lostcards.append(myCard)
            self.deck.lostCards.update(lostcards)
            self.deck_pos += 1
            debugger.msg(f"[compare] Lost cards: {[str(x) for x in self.deck.lostCards]}")

    def play(self):
        max_index = self.deck.max_index
        scores = self.current_score()
        self.player_display = f"Player Cards: {scores[0]}"
        self.opp_display = f"Opponent Cards: {scores[1]}"
        debugger.msg(f"[play] max_index: {max_index}, deck_pos: {self.deck_pos}")
        if self.game_continue():
            if self.deck_pos < max_index:
                self.compare(self.deck.myHand.cards[self.deck_pos], self.deck.oppHand.cards[self.deck_pos])
            else:
                self.deck.nextRound()
                self.display = f"A deck has reached its end at {max_index}!\nShuffling decks for the next round..."
                self.deck_pos = 0
                if self.isTie:
                    # self.deck_pos += len(self.my_tie_cards)
                    debugger.msg(f"[play] isTie check. deck pos = {self.deck_pos}")
                    debugger.msg(f"[play] ")            
            return True
        else:
            return False
        # print(self.display)
  
    def my_size(self):
        return len(self.deck.myHand.cards)
    
    def opp_size(self):
        return len(self.deck.oppHand.cards)
    
    def current_score(self):
        return (self.my_size() + len(self.deck.wonCards) - len(self.deck.lostCards)) , (self.opp_size() + len(self.deck.lostCards) - len(self.deck.wonCards))
    
    def game_continue(self):
        if self.my_size() == 0:
            self.player_display = "You lose! Better luck next time. Play Again?"
            return False
        if self.opp_size() == 0:
            self.player_display = "You win! Play Again?"
            return False
        return True
    
    def get_mycards(self):
        if self.deck_pos < self.deck.max_index:    
            self.mycards_to_display.extend(self.my_tie_cards)
            self.mycards_to_display.append(self.deck.myHand.cards[self.deck_pos])
            mycards = self.mycards_to_display
            debugger.msg(f"[get_mycards] my_cards: {[str(card) for card in mycards]}")
            return mycards
        return []

    def get_oppcards(self):
        if self.deck_pos < self.deck.max_index:
            self.oppcards_to_display.extend(self.opp_tie_cards)
            self.oppcards_to_display.append(self.deck.oppHand.cards[self.deck_pos])
            oppcards = list(self.oppcards_to_display)
            debugger.msg(f"[get_oppcards] opp_cards: {[str(card) for card in oppcards]}")
            return oppcards
        return []