import pandas as pd
import tkinter as tk
from PIL import ImageTk, Image
from datetime import datetime
import os
import pdb

window_background = '#9EE5DB'
button_background = '#C4BDBD'
button_foreground = '#23A70C'
font = ('Helvetica', '30')
threshold = 0.05

class GUI:

    def __init__(self):

        # create user id
        self.id = datetime.now().strftime("%s")

        # save the total number of images
        self.N = len(os.listdir("ladies1"))

        # instantiate and save image index
        self.i = 0

        # instantiate and save empty DataFrame to hold swipes
        self.DF = pd.DataFrame({'swipe':[2]*self.N})

        # create window
        self._create_window()
        self._create_like_button()
        self._create_dislike_button()
        self._update_window()

    #===========================================================================
    # press buttons
    #===========================================================================

    def press_like(self):
        self.DF.iloc[self.i].swipe = 1
        assert self.DF.iloc[self.i].swipe == 1, "Noo!"
        self.i += 1
        self._update_window()

    def press_dislike(self):
        self.DF.iloc[self.i].swipe = 0
        assert self.DF.iloc[self.i].swipe == 0, "Noo!"
        self.i += 1
        self._update_window()

    def press_back(self):
        self.i -= 1
        self._update_window()

    def press_quit(self):
        self.quit.destroy()
        self.window.destroy()

    #===========================================================================
    # create update window
    #===========================================================================

    def _create_window(self):
        window = tk.Tk()
        window.title("Tinder Swiper")
        window.geometry("800x800")
        window.configure(background=window_background)
        self.window = window

    def _update_window(self):

        if self.i == 0:
            self._hide_back_button()
            self._load_image_and_counter()
        elif self.i == self.N:
        # elif self.i == self.N:
            self._complete()
        else:
            self._create_back_button()
            self._load_image_and_counter()

    def _load_image_and_counter(self):

        # delete old image if present
        if hasattr(self,'im'): self.im.destroy()
        # load image
        im = Image.open(f"ladies1/{self.i}.jpg")
        im = im.resize((600, 600), Image.ANTIALIAS) #The (250, 250) is (height, width)
        im = ImageTk.PhotoImage(im)
        self.im = tk.Label(self.window, image=im)
        self.im.place(x=100, y=80)

        # delete old text object if present
        if hasattr(self,'text'): self.text.destroy()
        # show text counter
        self.text = tk.Label(self.window,
            text = f"Image {self.i+1} / {self.N}",
            font = ('Helvetica', '30'),
            bg = '#9EE5DB'
        )
        self.text.place(x=450, y=30)

        # show updated window
        self.window.mainloop()

    #===========================================================================
    # create buttons
    #===========================================================================

    def _create_like_button(self):
        # destroy old object if present
        if hasattr(self,'dislike'): self.dislike.destroy()
        like = tk.Button(self.window,
            text = 'LIKE',
            bg = button_background, # background
            fg = button_foreground, # foreground
            bd = 3, # border width
            width = 10, # button width
            height = 2, # button height
            font = font, # adjust the font and fontsize
            command = self.press_like # tell the button what to do when clicked
        )
        like.place(x=450, y=690)
        self.like = like

    def _create_dislike_button(self):
        # destroy old object if present
        if hasattr(self,'dislike'): self.dislike.destroy()
        # create the dislike button, place it, and save it
        dislike = tk.Button(self.window,
            text = 'DISLIKE',
            bg = button_background, # background
            fg = button_foreground, # foreground
            bd = 3, # border width
            width = 10, # button width
            height = 2, # button height
            font = font, # adjust the font and fontsize
            command = self.press_dislike # tell the button what to do when clicked
        )
        dislike.place(x=100, y=690)
        self.dislike = dislike

    def _create_back_button(self):
        # destroy old object if present
        if hasattr(self,'back'): self.back.destroy()
        # create the back button, place it, and save it
        back = tk.Button(self.window,
            text = 'BACK',
            bg = button_background, # background
            fg = button_foreground, # foreground
            bd = 3, # border width
            width = 10, # button width
            height = 1, # button height
            font = font, # adjust the font and fontsize
            command = self.press_back # tell the button what to do when clicked
        )
        back.place(x=100, y=10)
        self.back = back

    def _create_quit_button(self):
        # destroy old object if present
        if hasattr(self,'quit'): self.quit.destroy()
        # create the back button, place it, and save it
        quit = tk.Button(self.window,
            text = 'QUIT',
            bg = button_background, # background
            fg = button_foreground, # foreground
            bd = 3, # border width
            width = 10, # button width
            height = 1, # button height
            font = font, # adjust the font and fontsize
            command = self.press_quit # tell the button what to do when clicked
        )
        quit.place(x=100, y=690)
        self.quit = quit

    #===========================================================================
    # hide buttons
    #===========================================================================

    def _hide_like_button(self):
        if hasattr(self,'like'): self.like.destroy()

    def _hide_dislike_button(self):
        if hasattr(self,'dislike'): self.dislike.destroy()

    def _hide_back_button(self):
        if hasattr(self,'back'): self.back.destroy()

    #===========================================================================
    # complete
    #===========================================================================

    def _complete(self):

        print("\ncompleted!")

        # group the swipes by {0: 'dislike', 1: 'like', 2: 'nan'}
        sizes = self.DF.groupby('swipe').size()

        # check that the swipes are valid
        if all([ 0 in sizes , 1 in sizes ]):
            valid = [ (sizes[x]/self.N) > threshold for x in [0,1] ]
            if all(valid):
                self.DF.to_csv(f"{self.ID}.csv")
        else:
            print("You have either not selected enough likes or not selected enough dislikes to be considered valid!")

        for ob in ['like', 'dislike', 'back', 'im', 'text']:
            getattr(self,ob).destroy()

        # show thank you message
        self.text = tk.Label(self.window,
            text = "Thank You! You have swiped your way to the finish line!",
            font = ('Helvetica', '50'),
            bg = window_background,
            wraplength = 600,
            justify= 'left',
        )
        self.text.place(x=100, y=200)

        self._create_quit_button()

        self.window.mainloop()
