import tkinter as tk
from PlayingCards import *
from PlayingCards import debugger as debugger

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Card Game!")
        self.geometry("1280x720")
        self.ui = None
        self.bgcolor = "#198534"
        self.configure(bg=self.bgcolor)
        self.launch = True
        self.intro_display()

    def intro_display(self):
        debugger.msg("[intro_display] Returning to intro frame")
        if self.launch:
            debugger.msg("[intro_display] Creating Intro Frame")
            self.frm_intro = tk.Frame(self, background=self.bgcolor)  
            self.frm_intro.pack(fill="both", expand=True)      
            self.intro_msg = tk.Label(self.frm_intro, text="Choose your card game!", font=("Arial",60), background=self.bgcolor)
            self.intro_msg.pack()
            self.btn_intro1 = tk.Button(self.frm_intro, text="Play BlackJack", font=("Arial",40), command=self.start_blackjack, background=self.bgcolor)
            self.btn_intro2 = tk.Button(self.frm_intro, text="Play War", font=("Arial",40), command=self.start_war, background=self.bgcolor)
            self.btn_intro1.pack()
            self.btn_intro2.pack()
            self.launch = False
        else:
            debugger.msg("[intro_display] Re-launching intro frame")
            self.frm_intro.pack(fill="both", expand=True)
        if self.ui:
            debugger.msg("[intro_display] Deleting old ui")
            del self.ui
            self.ui = None
        self.update_idletasks()
        debugger.msg("[intro_display] Update complete")

    def start_war(self):
        import WarGui
        self.frm_intro.pack_forget()
        self.ui = WarGui.WarGui(self)
        self.ui.make_war_frames()
        
    def start_blackjack(self):
        import BlackJackGUI
        self.frm_intro.pack_forget()
        self.ui = BlackJackGUI.BlackJackGui(self)
        self.ui.make_blackjack_frames()