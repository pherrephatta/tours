# Test d'animation avec sprite dans Python avec tkinter
from tkinter import *
from PIL import Image, ImageTk

# # # Other
# https://pypi.org/project/arcade/

# # # Reference Sites
# http://effbot.org/tkinterbook
# http://people.cs.ksu.edu/~schmidt/200f07/Lectures/8.objectsF.html
# http://zetcode.com/tkinter/drawing/
# https://pythonprogramming.altervista.org/moving-an-image-with-tkinter-and-canvas/?doing_wp_cron=1567994168.4634540081024169921875
# https://www.tutorialspoint.com/python/python_gui_programming.htm
# https://tkdocs.com/tutorial/
# https://www.raywenderlich.com/3128-python-tutorial-how-to-generate-game-tiles-with-python-imaging-library

# # # Geometry Management
# pack() will organize in blocks
# grid() is table-like
# place() will use a specific location

class gameData():
    def __init__(self):
        # Window
        self.window = Tk()
        self.window.title("Animation de Sprites")
        # Frames
        # act like window surfaces
        self.frame = Frame(self.window)
        self.frame.grid()
        # Label
        # acts like text field
#        self.label = Label(self.frame, text="label!")
#        self.label.grid()
        # Text entry field
#        self.textentry = Entry(self.frame, width=20)
#        self.textentry.grid()
        # Buttons
#        self.button1 = Button(self.frame, text="Press me!")
#        self.button1.grid()
#        self.button2 = Button(self.frame, text="Don't press me!")
#        self.button2.grid()
        # Canvas
        self.canvas = Canvas(self.frame, width=100, height=100, bg="black")

        self.canvas.grid()
        # Bitmap
        self.spritesheet = Image.open("./assets/NES - Final Fantasy - Light Warriors.png")
        self.sprites = [(ImageTk.PhotoImage(self.spritesheet.crop((181,36,196,58))))]
        self.crtSprite = None

        self.update(0)

    def update(self, sprite):
        self.canvas.delete(self.crtSprite)
        self.crtSprite = self.sprites[sprite]
        self.canvas.create_image(0,0,image=self.crtSprite, anchor=NW)
        self.window.after(500, self.update, 0)

if __name__ == '__main__':
    gdata = gameData()
    gdata.window.mainloop()
    exit()
