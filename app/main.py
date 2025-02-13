
from tkinter import * 
# import Controller
# import Model
import View

def main():
   root = Tk()
   view = View.View(root)
#    model= Model.Model()
#    controller = Controller.Controller(model, view)
   root.mainloop()

if __name__ == "__main__":
   main()