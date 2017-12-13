import tkinter as tk
import re
import uuid
from tkinter import filedialog
from tkinter import messagebox

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
        print("File Name: " + str(self.fileName) +
              " | File Path: " + str(self.filePath) +
              " | Parents: " + str(self.parents) + 
              " | Children: " + str(self.children) +
              " | Siblings: " + str(self.siblings) )

def fileNameFinder(directory):
    locationOfLastSlash = 0
    for iterChars in range(len(directory)):
        if iterChars == "/":
            locationOfLastSlash = iterChars
    return directory[locationOfLastSlash:]

root = tk.Tk()
root.withdraw()

##file_path = filedialog.askopenfilename()
##print(file_path)

startBool = messagebox.askyesno("FileLink: Proof of Concept start page (Jason Liu Dec 2017)",
                                "Would you like to link files?")
if startBool:
    fileInstanceStagingArea = []
    print("Select File you would like to enter into the system")
    file_path = str(filedialog.askopenfilename())
    file_name = fileNameFinder(file_path)
    # generates a unique id based on the host ID and current Time
    # more information: https://docs.python.org/3.5/library/uuid.html
    file_uID = uuid.uuid1()
    
    parentLinkingBool = messagebox.askyesno("FileLink: Meet the Parents",
                                            "Are there any parent files to link?")
    if parentLinkingBool:
        parentCounter = 0
        while parentLinkingBool:
            parentCounter = parentCounter + 1
            print("Link parent file number " + str(parentCounter) + ", please")
            # currently assuming parent files are fresh
            parent_file_path = str(filedialog.askopenfilename())
            parent_file_name = fileNameFinder(parent_file_path)
            # ADD LATER: check to see if file already exists,
            # for now leave as is and assume it's new
            parent_uID = uuid.uuid1()
            establishedParent = FileInstance(parent_file_name, parent_file_path, parent_uID, -99, file_uID)
            fileInstanceStagingArea.append(establishedParent)
            # ADD LATER: link grandparent files if there are any
            file_parents.append(parent_uID)
            parentLinkingBool = messagebox.askyesno("FileLink: Meet the Parents",
                                                    "Are there any more parent files to link?")
    else:
        file_parents.append(-99)
        
    # loop to identify parents
