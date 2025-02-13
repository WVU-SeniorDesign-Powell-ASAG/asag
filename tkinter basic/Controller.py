#manages the interaction between the model and the view. It responds to user events, updates the model and triggers view updates


from tkinter import *
from tkinter import filedialog

class Controller:
    def __init__(self, view): #later when you implement database     def __init__(self,model, view):  
        #   self.model = model
          self.view = view

    def UploadFile(event=None):
        filename = filedialog.askopenfilename()
        print('Selected:', filename)





