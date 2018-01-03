import tkinter as tk
import uuid
from tkinter import filedialog
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt

class FileInstance:
    "a class that carries the file name, directory, parent/child info"
    def __init__(self, fileName, filePath,
                 ID, parents, children):
        self.fileName = fileName
        self.filePath = filePath
        self.ID = str(ID)
        self.parents = parents
        self.children = children
    def displayAllInfo(self):
        # need to add in checks for missing children/parents
        # currently just using -99 for missing values
        print("File Name: " + str(self.fileName) +
              " | File Path: " + str(self.filePath) +
              " | uID: " + str(self.ID) +
              " | Parents: " + str(self.parents) + 
              " | Children: " + str(self.children) )

def fileNameFinder(directory):
    locationOfLastSlash = 0
    for iterChars in reversed(range(len(directory))):
        if directory[iterChars] == "/":
            locationOfLastSlash = iterChars
            break
    return directory[(locationOfLastSlash+1):]

#def nodeGenerator(graphStructure, nodeCount, filename, 
#                  filepath, ID, parents, children):
#    graphStructure.add_node(nodeCount,
#                            file_name = filename,
#                            file_path = filepath,
#                            file_uID = ID,
#                            file_parents = parents,
#                            file_children = children)
#    nodeCount = nodeCount + 1
#    return [graphStructure, nodeCount]
    
    

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
    file_parents = []
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
            establishedParent = FileInstance(parent_file_name, parent_file_path, parent_uID,
                                             -99, [file_uID])
            # establishedParent.displayAllInfo()
            fileInstanceStagingArea.append(establishedParent)
            # ADD LATER: link grandparent files if there are any
            file_parents.append(parent_uID)
            
            parentLinkingBool = messagebox.askyesno("FileLink: Meet the Parents",
                                                    "Are there additional parent files to link?")
    else:
        file_parents.append(-99)

    childLinkingBool = messagebox.askyesno("FileLink: Add Children Question",
                                            "Are there any child files to link?")
    file_children = []
    if childLinkingBool:
        childCounter = 0
        while childLinkingBool:
            childCounter = childCounter + 1
            print("Link child file number " + str(childCounter) + ", please")
            # currently assuming child files are fresh
            child_file_path = str(filedialog.askopenfilename())
            child_file_name = fileNameFinder(child_file_path)
            # ADD LATER: check to see if file already exists,
            # for now leave as is and assume it's new
            child_uID = uuid.uuid1()
            establishedChild = FileInstance(child_file_name, child_file_path, child_uID, 
                                            [file_uID], -99)
            fileInstanceStagingArea.append(establishedChild)
            # establishedChild.displayAllInfo()
            # ADD LATER: link grandparent files if there are any
            file_children.append(child_uID)
            childLinkingBool = messagebox.askyesno("FileLink: Add Children Question",
                                                    "Are there additional child files to link?")
    else:
        file_children.append(-99)

    # establish initial node with all given information: file name, file path, file uID, parents and children
    establishNode = FileInstance(file_name, file_path, file_uID, 
                                 file_parents, file_children)
    fileInstanceStagingArea.append(establishNode)
    # establishNode.displayAllInfo()
    
    outputGraph = nx.DiGraph()
    outputGraphNodeCount = 1
    uIDPointers = []

    for eachFileInstance in fileInstanceStagingArea:
        outputGraph.add_node(outputGraphNodeCount, 
                             file_name = eachFileInstance.fileName,
                             file_path = eachFileInstance.filePath,
                             file_uID = eachFileInstance.ID)
        uIDPointers.append([outputGraphNodeCount, eachFileInstance.ID])
        outputGraphNodeCount = outputGraphNodeCount + 1
        
    outputGraphNodePointer = 1
    for eachFileInstance in fileInstanceStagingArea:
        if (eachFileInstance.children == -99):
            print("no child files found for: " + str(eachFileInstance.fileName))
        else:
            # find which node Pointer refers to each child
            childrenToLink = eachFileInstance.children
            print("-- children to link: " + str(childrenToLink))
            for eachChild in childrenToLink:
                for eachUIDlisting in uIDPointers:
                    print("- - - eachUIDListing: " + str(eachUIDlisting) + " eachChild: " + str(eachChild))
                    if str(eachUIDlisting[1]) == str(eachChild):
                        print("-*-*-* Added edge!! " + str(outputGraphNodePointer) + " and " + str(eachUIDlisting[0]))
                        outputGraph.add_edge(outputGraphNodePointer, eachUIDlisting[0])
        outputGraphNodePointer = outputGraphNodePointer + 1
    
    # draW THE DAMN GRAPH
    nx.draw(outputGraph)
    
    
