from PlayingCards import PlayingCard
import tkinter as tk

def get_image(path:str) -> tk.PhotoImage:
        image = None
        try:
            image = tk.PhotoImage(file=path)
        except tk.TclError:
              print("[ImageHandling.get_image()] INVALID IMAGE PATH")
              exit()
        return image
    
def get_cardface(card:PlayingCard):
        path = ''
        if card.isVisible:
            path = './assets/CardImages/' + card.filename
        else: 
            path = './assets/CardImages/CardBack2.gif'
        return get_image(path)