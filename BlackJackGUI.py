import tkinter as tk
import blackjack
from PlayingCards import *
from ImageHandling import *

class BlackJackGui:
    def __init__(self, window) -> None:
        self.window = window
        self.game = blackjack.BlackJackGame()
        self.bgcolor = self.window.bgcolor

    def make_blackjack_frames(self):
        self.frm_main = tk.Frame(self.window, background=self.bgcolor, borderwidth=1, relief=tk.GROOVE)
        self.frm_main.pack(fill="both", expand=True)

        self.frm_deck = tk.Frame(self.frm_main, borderwidth=1, relief=tk.GROOVE, background=self.bgcolor)
        self.frm_dealer = tk.Frame(self.frm_main, borderwidth=1, relief=tk.GROOVE, background=self.bgcolor)
        self.frm_player = tk.Frame(self.frm_main, borderwidth=1, relief=tk.GROOVE, background=self.bgcolor)
        self.frm_control = tk.Frame(self.frm_main, borderwidth=1, relief=tk.GROOVE, background=self.bgcolor)

        self.card_labels:list[tk.Label] = []
        self.dealer_labels:list[tk.Label] = []
        self.card_faces = []
        self.dealer_faces = []
        self.current_display_index = 0
        self.current_dealer_index = 0

        self.frm_main.columnconfigure(0, weight=1)
        self.frm_main.columnconfigure(1, weight= 1)
        self.frm_main.columnconfigure(2, weight=0)
        self.frm_main.rowconfigure(0, weight=1)
        self.frm_main.rowconfigure(1, weight=1)

        self.frm_deck.grid(row=0, column=2, padx=20, pady=15, sticky=tk.NSEW)
        self.frm_dealer.grid(row=0, column=0, padx=20, pady=15, columnspan=2, sticky=tk.NSEW)
        self.frm_player.grid(row=1, column=0, padx=20, pady=15, columnspan=2, sticky=tk.NSEW)
        self.frm_control.grid(row=1, column=2, padx=20, pady=15, sticky=tk.NSEW)
        
        self.lbl_main_display = tk.Label(master=self.frm_control, text="Welcome to BlackJack!")

        lbl_deck = tk.Label(master=self.frm_deck, text="Deck Zone", background=self.bgcolor)
        lbl_deal = tk.Label(master=self.frm_dealer, text="Dealer Cards", background=self.bgcolor)
        lbl_player = tk.Label(master=self.frm_player, text="Player Cards", background=self.bgcolor)

        lbl_deck.pack(padx=5, pady=5)
        lbl_deal.pack(padx=5, pady=5)
        lbl_player.pack(padx=5, pady=5)
        self.lbl_main_display.pack(padx=5, pady=5)
        self.card_list:list[tk.Label] = []
        self.dealer_list:list[tk.Label] = []

    def hit_button(self):
        self.btn_stay.configure(text="Stay", command=self.staybutton)
        if self.game.game_status == 0:
            self.btn_deal.configure(text="Deal")
            self.clear_card_display()
        self.game.deal_action()
        self.display_cards()
        if self.game.game_status == 0:
            self.btn_deal.configure(text="Deal")
            self.btn_stay.configure(text="Exit", command=self.exit)
        else:
            self.btn_deal.configure(text="Hit")
            self.btn_stay.configure(text="Stay", command=self.staybutton)
        self.lbl_main_display.configure(text=self.game.display)

    def staybutton(self):
        if self.game.game_status == 1:
            self.game.stay_action()
            self.btn_deal.configure(text="Deal")
            self.btn_stay.configure(text="Exit", command=self.exit)
            self.lbl_main_display.configure(text=self.game.display)
            self.display_cards()

    def blackjack_display(self):
        self.card_back = get_image("./assets/CardImages/CardBack2.gif")
        card_back_deck = tk.Label(self.frm_deck, image=self.card_back, background=self.bgcolor)
        self.btn_deal = tk.Button(self.frm_control, text="Deal", command=self.hit_button, font=("Arial",60))
        self.btn_stay = tk.Button(self.frm_control, text="Stay", command=self.staybutton, font=("Arial",60))
        card_back_deck.pack()
        self.btn_deal.pack(side="left")
        self.btn_stay.pack(side="right")

    def display_cards(self):
        while self.current_display_index < len(self.game.myHand.cards):
            pic = get_cardface(self.game.myHand.cards[self.current_display_index])
            self.card_faces.append(pic)
            self.card_labels.append(tk.Label(self.frm_player, background=self.bgcolor, image=self.card_faces[self.current_display_index]))
            self.card_labels[self.current_display_index].pack(side="left", padx=20)
            self.current_display_index += 1
        while self.current_dealer_index < len(self.game.dealer.dealerHand.cards):
            pic = get_cardface(self.game.dealer.dealerHand.cards[self.current_dealer_index])
            self.dealer_faces.append(pic)
            self.dealer_labels.append(tk.Label(self.frm_dealer, background=self.bgcolor, image=self.dealer_faces[self.current_dealer_index]))
            self.dealer_labels[self.current_dealer_index].pack(side="left", padx=20)
            self.current_dealer_index += 1
        if self.game.dealerFlip:
            self.flipped_hole_card = get_cardface(self.game.dealer.dealerHand.cards[0])
            self.dealer_labels[0].configure(image=self.flipped_hole_card)

    def clear_card_display(self):
        if self.card_labels:
            for lbl in self.card_labels:
                lbl.destroy()
            self.current_display_index = 0
            self.card_faces.clear()
            self.card_labels.clear()
        if self.dealer_labels:
            for lbl in self.dealer_labels:
                lbl.destroy()
            self.current_dealer_index = 0
            self.dealer_faces.clear()
            self.dealer_labels.clear()
    
    def exit(self):
        del self.game
        self.frm_main.destroy()
        self.window.intro_display()