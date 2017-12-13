import tkinter as tk
from tkinter import filedialog

class FileInstance:
    "a class that carries the file name, directory, parent/child info"
    def __init__(self, fileName, filePath,
                 ID, parents, children):
        self.fileName = fileName
        self.filePath = filePath
        self.ID = ID
        self.parents = parents
        self.children = children
    def displayAllInfo(self):
        # need to add in checks for missing children/parents
        # currently just using -99 for missing values
        print("File Name: " + str(fileName) +
              " | File Path: " + str(filePath) +
              " | Parents: " + str(parents) +
              " | Children: " + str(children))

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()
print(file_path)
