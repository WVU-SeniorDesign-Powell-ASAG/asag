# creating the GUI elements and updating the display based on changes in the model


from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

# hugging face
from scipy.spatial import distance
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")
      

class View:
    def __init__(self, root):
        self.root = root
        self.root.title("CS 101 Automatic Short Answer Grader")
        self.root.attributes("-fullscreen", False)
        self.root.state("zoomed")
        self.root.configure(background="white")
        icon = PhotoImage(file="images/logo.png")
        root.iconphoto(True, icon)
        self.createWidgets()

    def createWidgets(self):
        # create scrollbar and canvas
        self.canvas = Canvas(self.root, background="white")
        self.scrollbar = Scrollbar(
            self.root, orient="vertical", command=self.canvas.yview
        )
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.frame = Frame(self.canvas, background="white")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.frame.bind("<Configure>", self.frameConfigure)

        # header info containing submission instructions
        font = "Helvetia, 10"
        bold_font = ("Helvetica", 10, "bold")
        headerText1 = """All CS101 Homeworks, Exams, and Participation Projects must be submitted through the submission tool below. Do not e-mail your files to the instructor."""
        headerText2 = """Be sure to save your work and close Microsoft Office before submitting your assignment. You are responsible for ensuring that you submit the correct file, for the correct assignment, on-time and ensuring that it is successfully received. Carefully read the status messages after your submission."""
        headerText3 = """If this is a late submission you must e-mail your section instructor to notify them of this late submission."""
        self.header1 = Label(
            self.frame,
            font=font,
            background="white",
            text=headerText1,
            wraplength=800,
            justify="left",
        )
        self.header1.grid(row=0, column=0, padx=200, pady=(50, 10), sticky="W")
        self.header2 = Label(
            self.frame,
            font=font,
            background="white",
            text=headerText2,
            wraplength=800,
            justify="left",
        )
        self.header2.grid(row=1, column=0, padx=200, pady=(0, 10), sticky="W")
        self.header3 = Label(
            self.frame, font=font, background="white", text=headerText3, justify="left"
        )
        self.header3.grid(row=2, column=0, padx=200, pady=(0, 10), sticky="W")

        # lines
        self.line = Label(
            self.frame,
            background="white",
            text="_____________________________________________________________________________________________________________________________________________________________",
        )
        self.line.grid(row=3, column=0)

        # student name
        self.name = Label(
            self.frame, font=font, background="white", text="Student Name:"
        )
        self.name.grid(row=4, column=0, padx=200, pady=(10, 0), sticky="W")
        # fake name for now???
        self.name = Label(
            self.frame, font=font, background="white", text="Bitmapped Powell"
        )
        self.name.grid(row=4, column=0, padx=450, pady=(10, 0), sticky="W")

        # line
        self.line = Label(
            self.frame,
            background="white",
            text="_____________________________________________________________________________________________________________________________________________________________",
        )
        self.line.grid(row=5, column=0)

        # student id
        self.name = Label(self.frame, font=font, background="white", text="Student ID:")
        self.name.grid(row=6, column=0, padx=200, pady=(10, 0), sticky="W")

        # student id fake text for now???
        self.name = Label(self.frame, font=font, background="white", text="123456789")
        self.name.grid(row=6, column=0, padx=450, pady=(10, 0), sticky="W")

        # line
        self.line = Label(
            self.frame,
            background="white",
            text="_____________________________________________________________________________________________________________________________________________________________",
        )
        self.line.grid(row=7, column=0)

        # Select Section dropdown
        self.sectionLabel = Label(
            self.frame, font=font, background="white", text="Select Section: "
        )
        self.sectionLabel.grid(row=8, column=0, padx=(200, 0), pady=(10, 0), sticky="W")

        self.sectionList = ["Section 1", "Section 2", "Section 3"]
        self.sectionVar = StringVar(self.frame)
        self.sectionVar.set(self.sectionList[0])
        self.sectionDropdown = OptionMenu(
            self.frame, self.sectionVar, *self.sectionList
        )
        self.sectionDropdown.grid(
            row=8, column=0, padx=(450, 0), pady=(10, 0), sticky="W"
        )
        self.sectionDropdown.config(width=20)

        # line
        self.line = Label(
            self.frame,
            background="white",
            text="_____________________________________________________________________________________________________________________________________________________________",
        )
        self.line.grid(row=9, column=0)

        # Select Assignment
        self.assignmentLabel = Label(
            self.frame, font=font, background="white", text="Select Assignment: "
        )
        self.assignmentLabel.grid(
            row=10, column=0, padx=(200, 0), pady=(10, 0), sticky="W"
        )

        self.assignmentList = ["Homework #6 Fortune 500 Companies", "Homework 3", "Hi"]
        self.assignmentVar = StringVar(self.frame)
        self.assignmentVar.set(self.assignmentList[0])
        self.assignmentDropdown = OptionMenu(
            self.frame, self.assignmentVar, *self.assignmentList
        )
        self.assignmentDropdown.grid(
            row=10, column=0, padx=(450, 0), pady=(10, 0), sticky="W"
        )
        self.assignmentDropdown.config(width=80)

        # line
        self.line = Label(
            self.frame,
            background="white",
            text="_____________________________________________________________________________________________________________________________________________________________",
        )
        self.line.grid(row=11, column=0)

        # Please upload your assigmnet files below text
        self.uploadText = Label(
            self.frame,
            font=font,
            background="white",
            text="Please upload your assignment below",
        )
        self.uploadText.grid(row=12, column=0, padx=(450, 0), pady=(10, 0), sticky="W")
        # line
        self.line = Label(
            self.frame,
            background="white",
            text="_____________________________________________________________________________________________________________________________________________________________",
        )
        self.line.grid(row=13, column=0)

        # Access
        self.uploadText = Label(
            self.frame,
            font=font,
            background="white",
            text="Microsoft Access ACCDB File",
        )
        self.uploadText.grid(row=14, column=0, padx=(450, 0), sticky="W")
        self.accessButton = Button(
            self.frame, text="Choose File", command=self.uploadFile
        )
        self.accessButton.grid(
            row=15, column=0, padx=(450, 0), pady=(10, 0), sticky="W"
        )
        self.accessButton.config(width=30)

        # line
        self.line = Label(
            self.frame,
            background="white",
            text="_____________________________________________________________________________________________________________________________________________________________",
        )
        self.line.grid(row=16, column=0)
        # Excel
        self.uploadText = Label(
            self.frame, font=font, background="white", text="Microsoft Excel XLSX File"
        )
        self.uploadText.grid(row=17, column=0, padx=(450, 0), sticky="W")
        self.accessButton = Button(
            self.frame, text="Choose File", command=self.uploadFile
        )
        self.accessButton.grid(
            row=18, column=0, padx=(450, 0), pady=(10, 0), sticky="W"
        )
        self.accessButton.config(width=30)
        # line
        self.line = Label(
            self.frame,
            background="white",
            text="_____________________________________________________________________________________________________________________________________________________________",
        )
        self.line.grid(row=19, column=0)
        # Word
        self.uploadText = Label(
            self.frame, font=font, background="white", text="Microsoft Word DOCX File"
        )
        self.uploadText.grid(row=20, column=0, padx=(450, 0), sticky="W")
        self.accessButton = Button(
            self.frame, text="Choose File", command=self.uploadFile
        )
        self.accessButton.grid(
            row=21, column=0, padx=(450, 0), pady=(10, 0), sticky="W"
        )
        self.accessButton.config(width=30)
        # line
        self.line = Label(
            self.frame,
            background="white",
            text="_____________________________________________________________________________________________________________________________________________________________",
        )
        self.line.grid(row=22, column=0)
        # Powerpoint
        self.uploadText = Label(
            self.frame,
            font=font,
            background="white",
            text="Microsoft PowerPoint PPTX File",
        )
        self.uploadText.grid(row=23, column=0, padx=(450, 0), sticky="W")
        self.accessButton = Button(
            self.frame, text="Choose File", command=self.uploadFile
        )
        self.accessButton.grid(
            row=24, column=0, padx=(450, 0), pady=(10, 0), sticky="W"
        )
        self.accessButton.config(width=30)
        # line
        self.line = Label(
            self.frame,
            background="white",
            text="_____________________________________________________________________________________________________________________________________________________________",
        )
        self.line.grid(row=25, column=0)

        # the files I am submitting text
        self.academicPolicy = Label(
            self.frame,
            font=font,
            background="white",
            text="The files I am submitting are in compliance with the CS101 Academic Integrity Policy",
        )
        self.academicPolicy.grid(
            row=26, column=0, padx=(500, 0), pady=(20, 0), sticky="W"
        )
        # homeworks and exams text
        bold_font = ("Helvetica", 10, "bold")
        self.hwText = Label(
            self.frame, font=bold_font, background="white", text="Homeworks and Exams:"
        )
        self.hwText.grid(row=27, column=0, padx=(500, 0), sticky="W")
        self.academicPolicy = Label(
            self.frame,
            font=font,
            justify="left",
            background="white",
            wraplength="500",
            text="The files are entirely my own work and were created by me from blank new files. I did not work with any other people, recieve any part of these files from others, or allow others access to any part of my files",
        )
        self.academicPolicy.grid(row=28, column=0, padx=(500, 0), sticky="W")

        # checkbox
        checkbutton = IntVar()
        self.checkbutton = Checkbutton(
            self.frame,
            text="Agree to CS101 Academic Integrity Policy",
            variable=checkbutton,
        )
        self.checkbutton.grid(row=29, column=0, padx=(500, 0), pady=(10, 0), sticky="W")

        # submit button, have to fill in entries and checkbox before going
        self.submitButton = Button(self.frame, text="Submit")
        self.submitButton.config(width=15)
        self.submitButton.grid(
            row=30, column=0, padx=(500, 0), pady=(10, 0), sticky="W"
        )

        # white space at bottom of page
        self.whitespace = Label(
            self.frame, font=bold_font, background="white", text="    "
        )
        self.whitespace.grid(row=31, column=0, padx=(500, 0), sticky="W")
        self.whitespace2 = Label(
            self.frame, font=bold_font, background="white", text="    "
        )
        self.whitespace2.grid(row=32, column=0, padx=(500, 0), sticky="W")
        self.whitespace3 = Label(
            self.frame, font=bold_font, background="white", text="    "
        )
        self.whitespace3.grid(row=33, column=0, padx=(500, 0), sticky="W")

        # functions for view

    #
    def frameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def uploadFile(self):
        filename = filedialog.askopenfilename()
        print("selected: ", filename)

    # hugging face
    approved_answers = [
        "The movie is awesome. It was a good thriller",
        "We are learning NLP throughg GeeksforGeeks",
        "The baby learned to walk in the 5th month itself",
    ]
    student_input = "I liked the movie."
    print("Test sentence:", student_input)
    test_vec = model.encode([student_input])[0]
    for sentence in approved_answers:
        similarity_score = 1 - distance.cosine(test_vec, model.encode([sentence])[0])
        print(f"\nFor {sentence}\nSimilarity Score = {similarity_score} ")
