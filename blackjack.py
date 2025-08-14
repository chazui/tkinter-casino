from PlayingCards import *

class BlackjackHand(Hand):
    def __init__(self, deck:Deck):
        super().__init__()
        self.drawm(deck,2)

    def reset(self, deck:Deck):
        self.cards = []
        self.drawm(deck,2)

    def score(self) -> int:
        isAce = 0
        score = 0
        for card in self.cards:
            if card.name == "A":
                isAce += 1
            else:
                score += int(card.blackjack_value)
        for _ in range(isAce):
            if score > 10: score += 1
            else: score += 11
        return score
    
    def isBust(self) -> bool:
        if self.score() > 21:
            return True
        return False
    
    def is21(self) -> bool:
        if self.score() == 21:
            return True
        return False
    
    def isBlackjack(self) -> bool:
        if self.is21() and len(self.cards) == 2:
            return True
        return False

class BlackJackDealer:
    def __init__(self,deck:Deck):
        super().__init__()
        self.deck = deck
        self.dealerHand = BlackjackHand(self.deck)
        self.playing = True
        self.current_score = self.dealerHand.score()
        
    def hit(self):
        if self.current_score < 17:
            self.dealerHand.draw(self.deck)
            self.current_score = self.dealerHand.score()
        else: 
            self.playing = False
    
    def reset(self):
        self.dealerHand.reset(self.deck)
        self.current_score = self.dealerHand.score()


class BlackJackGame:
    def __init__(self):
        self.deck = Deck()
        self.discard_pile = DiscardPile()
        self.myHand = BlackjackHand(self.deck)
        self.dealer = BlackJackDealer(self.deck)
        self.game_status = 0
        self.dealerFlip = False #Additional flag needed to update hole card in GUI
        self.display = "" #The GUI reads and displays this string
        self.playcount = 0 
        self.deck.shuffle()

    def start_game(self):
        debugger.msg(f"[start_game] Play count: {self.playcount}")
        if self.playcount > 0 and self.playcount % 5 == 0:
            self.deck.shuffle()
            debugger.msg(f"[start_game] Reshuffling deck")
            self.display = "Reshuffling deck..."
        self.myHand.reset(self.deck)
        self.dealer.reset()
        self.dealerFlip = False
        self.dealer.dealerHand.cards[0].isVisible = False
        self.game_status = 1
        if self.dealer.dealerHand.isBlackjack() or self.myHand.isBlackjack():
            self.end_game()
            return
        else:
            self.status_1() 

    def status_1(self):
        if self.myHand.score() < 21 and len(self.myHand.cards) < 5 and not self.dealer.dealerHand.isBlackjack():
            self.display = f"Your current score is {self.myHand.score()}.\nWould you like to draw another card?"
        else:
            self.end_game()

    def status_2(self):
        self.myHand.draw(self.deck)
        self.status_1()

    def end_game(self):
        self.playcount += 1
        self.game_status = 0
        self.dealer.dealerHand.cards[0].isVisible = True
        self.dealerFlip = True
        player_bust = self.myHand.isBust()

        debugger.msg(f"[end_game] dealer hand before hits: {self.dealer.dealerHand}")

        if player_bust:
            self.display = "Bust! You lose."
            return
        
        player_blackjack, dealer_blackjack = self.myHand.isBlackjack(), self.dealer.dealerHand.isBlackjack()
        
        if dealer_blackjack and player_blackjack:
            self.display = "Push! Both players Blackjack."
            return
        elif dealer_blackjack:
            self.display = "Player loses to dealer's Blackjack."
            return
        elif player_blackjack:
            self.display = "Blackjack! You win."
            return

        myScore = self.myHand.score() 
        while self.dealer.current_score < 17 and self.dealer.current_score < myScore:
            self.dealer.hit()

        dealer_bust = self.dealer.dealerHand.isBust()
        player_21, dealer_21 = self.myHand.is21(), self.dealer.dealerHand.is21()

        if dealer_bust:
            self.display = f"Dealer busts! You win with a score of {myScore}"
        elif dealer_21:
            if player_21:
                self.display = "Push! Both players score 21."
            else: 
                self.display = "Dealer scores 21! You lose."
        elif player_21:
            self.display = "21! You win!"
        elif myScore > self.dealer.current_score:
            self.display = f"You win! {myScore} to {self.dealer.current_score}"
        elif self.dealer.current_score > myScore:
            self.display = f"You lose-- Dealer wins {self.dealer.current_score} to {myScore}"
        else:
            assert(myScore == self.dealer.current_score)
            self.display = f"Push-- Players tie at {myScore}"

    def deal_action(self):
        match self.game_status:
            case 0:
                self.start_game()
            case 1:
                self.status_2()
      
    def stay_action(self):
        if self.game_status == 1:
            self.end_game()