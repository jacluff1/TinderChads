import numpy as np
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

    def __init__(self, **kwargs):
        self.finished = False
        if not os.path.isdir("user_data"): os.mkdir("user_data")
        self._set_options_and_handle_opening_sequence(**kwargs)
        self._run_batch()

    def _set_options_and_handle_opening_sequence(self, **kwargs):

        # set batch size
        self.batch_size = kwargs['batch_size'] if 'batch_size' in kwargs else 100

        # set directory that contains ladies' photos
        self.ladies = kwargs['ladies'] if 'ladies' in kwargs else "../ladies1"

        # find the total number of photos
        directory = np.array(os.listdir(self.ladies))
        jpg = np.array([ '.jpg' in x for x in directory ])
        self.images = directory[jpg]
        self.N = self.images.shape[0]

        # get the data filename, user id, and starting index
        directory = np.array(os.listdir())
        csv = np.array([ '.csv' in x for x in directory ])

        if np.any(csv):

            # get the filename
            self.filename = directory[csv][0]

            # get the id from the filename
            self.id = self.filename[ : self.filename.find('.csv') ]

            # load the file and extract the last index
            self.i = self._load_complete_csv().index[-1]

            # update batch_size if need be
            if self.i + self.batch_size > self.N:
                self.batch_size = self.N - self.i

            # set the DataFrame for the batch
            self.DF = pd.DataFrame(
                {'swipe':[2]*self.batch_size},
                index = np.arange(self.i+1, self.i+self.batch_size+1).astype(np.int32)
            )

        else:

            # make the id from timestamp
            self.id = datetime.now()

            # make the filename to save data
            self.filename = f"{self.id}.csv"

            # save the beginning index
            self.i = 0

            # save an empty DataFrame
            pd.DataFrame(columns=['id', 'swipe']).to_csv(self.filename, index=False)

            # set the DataFrame for the batch
            self.DF = pd.DataFrame(
                {'swipe':[2]*self.batch_size},
                index = np.arange(self.i, self.i+self.batch_size).astype(np.int32)
            )

    #===========================================================================
    # press buttons
    #===========================================================================

    def press_like(self):
        self.DF.loc[self.i,'swipe'] = 1
        self.i += 1
        self.counter += 1
        self._update_window()

    def press_dislike(self):
        self.DF.loc[self.i,'swipe'] = 0
        self.i += 1
        self.counter += 1
        self._update_window()

    def press_back(self):
        self.i -= 1
        if self.i == 0: self._destroy('back')
        self._update_window()

    def press_quit(self):
        self._destroy_all()

    def press_save(self):
        self._complete(check=False)

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

        if self.counter == 100:
            self._complete_batch()
            return
        elif self.i == self.N:
            self._complete()
            return
        elif self.i == 0:
            self._destroy('back')
        elif self.i == 1:
            self._create_back_button()
        self._load_image_and_counter()

    def _load_image_and_counter(self):

        # delete old image if present
        self._destroy('image')
        # load image
        im = Image.open(f"{self.ladies}/{self.i}.jpg")
        im = im.resize((600, 600), Image.ANTIALIAS) #The (250, 250) is (height, width)
        im = ImageTk.PhotoImage(im)
        self.image = tk.Label(self.window, image=im)
        self.image.place(x=100, y=80)

        # delete old text object if present
        self._destroy('text')
        # show text counter
        self.text = tk.Label(self.window,
            text = f"Image {self.i+1} / {self.N}",
            font = ('Helvetica', '30'),
            bg = window_background
        )
        self.text.place(x=450, y=30)

        # show updated window
        self.window.mainloop()

    #===========================================================================
    # create buttons
    #===========================================================================

    def _create_like_button(self):
        # destroy old object if present
        self._destroy('like')
        # create the like button and save it
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
        self._destroy('dislike')
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
        self._destroy('back')
        # create the back button, place it, and save it
        back = tk.Button(self.window,
            text = 'BACK',
            bg = button_background, # background
            fg = button_foreground, # foreground
            bd = 3, # border width
            width = 5, # button width
            height = 1, # button height
            font = font, # adjust the font and fontsize
            command = self.press_back # tell the button what to do when clicked
        )
        back.place(x=100, y=10)
        self.back = back

    def _create_quit_button(self):
        # destroy old object if present
        self._destroy('quit')
        # create the back button, place it, and save it
        quit = tk.Button(self.window,
            text = 'FINISHED',
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

    def _create_save_button(self):
        # destroy old object if present
        self._destroy('save')
        # create the save button, place it and save it
        save = tk.Button(self.window,
            text = 'SAVE',
            bg = button_background,
            fg = button_foreground,
            bd = 3,
            width = 5,
            height = 1,
            font = font,
            command = self.press_save
        )
        save.place(x=250, y=10)
        self.save = save

    #===========================================================================
    # hide buttons
    #===========================================================================

    def _destroy(self,attr):
        if hasattr(self,attr):
            getattr(self,attr).destroy()
            delattr(self,attr)

    def _destroy_all(self):
        for attr in ['like', 'dislike', 'back', 'save', 'image', 'text', 'quit', 'window']:
            self._destroy(attr)

    #===========================================================================
    # batch
    #===========================================================================

    def _run_batch(self):
        self.counter = 0
        self._create_window()
        self._create_like_button()
        self._create_dislike_button()
        self._create_back_button()
        self._create_save_button()
        self._update_window()

    #===========================================================================
    # handle csv
    #===========================================================================

    def _append_to_csv(self):
        # format the DF appropriatly
        self.DF['id'] = self.DF.index
        self.DF = self.DF[['id','swipe']]
        # append DF to csv
        self.DF.to_csv(self.filename, mode='a', header=False, index=False)

    def _load_complete_csv(self):

        # load data
        DF = pd.read_csv(self.filename, names=['id', 'swipe'])

        # sort by id
        DF.sort_values(by='id', inplace=True)

        # drop any duplicates, keeping the latest entry
        DF.drop_duplicates(keep='last', inplace=True)

        #output
        return DF

    def _add_complete_csv(self):
        self.DF = self._load_complete_csv()

    def _move_complete_csv_to_data(self):
        self.DF.to_csv(f"user_data/{self.filename}", index=False)

    #===========================================================================
    # complete
    #===========================================================================

    def _complete_batch(self):
        self._destroy_all()
        self._append_to_csv()

    def _complete(self, check=True):

        print("\ncompleted!")
        self._complete_batch()
        self._add_complete_csv()

        # group the swipes by {0: 'dislike', 1: 'like', 2: 'nan'}
        sizes = self.DF.groupby('swipe').size()

        if check:
            # check that the swipes are valid
            if all([ 0 in sizes , 1 in sizes ]):
                valid = [ (sizes[x]/self.N) > threshold for x in [0,1] ]
                if all(valid):
                    self._move_complete_csv_to_data()
            else:
                print("You have either not selected enough likes or not selected enough dislikes to be considered valid!")
        else:
            self._move_complete_csv_to_data()

        # delete csv from working directory
        os.remove(self.filename)


        # show thank you message
        self._create_window()
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

        # make sure program knows to quit if using a while loop
        self.finished = True

if __name__ == "__main__":
    gui = GUI()
    i,N = gui.i,gui.N
    while i < N:
        gui = GUI()
        if gui.finished: break
