from tkinter import Tk, Label, Entry, Button

def create_ui(submit_callback):
    root = Tk()
    root.title("Database Connection")
    Label(root, text="Database Path:").grid(row=0)
    entry = Entry(root)
    entry.grid(row=0, column=1)
    Button(root, text="Submit", command=submit_callback).grid(row=1, columnspan=2)
    root.mainloop()