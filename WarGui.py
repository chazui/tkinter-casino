import tkinter as tk
from war import WarGame
from PlayingCards import *
from ImageHandling import *

class WarGui:
    def __init__(self, window) -> None:
        self.window = window
        self.game = WarGame()
        self.current_display_index = 0
        self.card_labels:list[tk.Label] = []
        self.opp_labels:list[tk.Label] = []
        self.card_faces = []
        self.opp_faces = []
        self.bgcolor = self.window.bgcolor
    
    def make_war_frames(self):
        self.frm_main = tk.Frame(self.window, background=self.bgcolor)
        self.frm_main.pack(fill="both",expand=True)
        self.frm_opponent = tk.Frame(self.frm_main, borderwidth=1, relief=tk.GROOVE, background=self.bgcolor)
        self.frm_player = tk.Frame(self.frm_main, borderwidth=1, relief=tk.GROOVE, background=self.bgcolor)
        self.frm_display = tk.Frame(self.frm_main, borderwidth=1, relief=tk.GROOVE, background=self.bgcolor)
        self.deck_img = get_image("./assets/CardImages/CardBack2.gif")

        self.frm_main.columnconfigure(0, weight=1)
        self.frm_main.columnconfigure(1,weight=0)

        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)

        self.frm_opponent.grid(row=0, column=0, padx=20, pady=15, columnspan=2, sticky=tk.NSEW)
        self.frm_player.grid(row=1, column=0, padx=20, pady=15, columnspan=2, sticky=tk.NSEW)
        self.frm_display.grid(row=1, column=1, padx=20, pady=15, columnspan=2, sticky=tk.NSEW)

        self.lbl_opponent = tk.Label(master=self.frm_opponent, text=self.game.opp_display, background=self.bgcolor)
        self.lbl_player = tk.Label(master=self.frm_player, text=self.game.player_display, background=self.bgcolor)
        self.lbl_display = tk.Label(master=self.frm_display, text="Welcome to WAR!", background=self.bgcolor)
        btn_my_deck = tk.Button(master=self.frm_player, image=self.deck_img, command=self.next_play, background=self.bgcolor, relief="raised")
        btn_exit = tk.Button(master=self.frm_display, text="Exit Game", command=self.exit, background=self.bgcolor)
        self.lbl_opp_deck = tk.Label(master=self.frm_opponent, image=self.deck_img, background=self.bgcolor, relief="raised")

        self.lbl_opponent.pack(padx=5, pady=5)
        self.lbl_opp_deck.pack(side="left", padx=20, anchor="center")
        self.lbl_player.pack(padx=5, pady=5)
        btn_my_deck.pack(side="left", padx=20, anchor="center")
        btn_exit.pack()
        self.lbl_display.pack(padx=5, pady=5)
        self.card_list:list[tk.Label] = []
        self.dealer_list:list[tk.Label] = []

    def display_cards(self):
        debugger.msg(f'[display cards] Entering function. current_display_index={self.current_display_index}')
        if not self.game.isTie:
            debugger.msg('[display_cards] Starting clear_card_display')
            self.clear_card_display()
        mycards = self.game.get_mycards()
        oppcards = self.game.get_oppcards()
        while self.current_display_index < len(mycards):
            pic1 = get_cardface(mycards[self.current_display_index])
            self.card_faces.append(pic1)
            self.card_labels.append(
                tk.Label(self.frm_player, background=self.bgcolor, 
                         image=self.card_faces[self.current_display_index]))
            self.card_labels[self.current_display_index].pack(side="left", padx=20, anchor="center")
            pic2 = get_cardface(oppcards[self.current_display_index])
            self.opp_faces.append(pic2)
            self.opp_labels.append(
                tk.Label(self.frm_opponent,background=self.bgcolor, 
                         image=self.opp_faces[self.current_display_index]))
            self.opp_labels[self.current_display_index].pack(side="left", padx=20, anchor="center")
            self.current_display_index += 1

    def clear_card_display(self):
        if self.card_labels:
            for lbl in self.card_labels:
                lbl.destroy()
            self.card_faces.clear()
            self.card_labels.clear()
            self.game.mycards_to_display.clear()
        if self.opp_labels:
            for lbl in self.opp_labels:
                lbl.destroy()
            self.opp_faces.clear()
            self.opp_labels.clear()
            self.game.oppcards_to_display.clear()
            self.current_display_index = 0


    def next_play(self):
        self.display_cards()
        self.game.play()
        self.lbl_display.configure(text=self.game.display)
        self.lbl_player.configure(text=self.game.player_display)
        self.lbl_opponent.configure(text=self.game.opp_display)
        debugger.msg(f"[next_play] Scores: {self.game.current_score()}")

    def exit(self):
        self.frm_main.destroy()
        self.window.intro_display()