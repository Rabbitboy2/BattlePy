from tkinter import *
import string
gui = Tk()
gui.title("Target Warfare")
mode = StringVar()
player = StringVar()
active = StringVar()
hitImg = PhotoImage(file="hitImg.png")
defaultImg = PhotoImage(file="default.png")
missImg = PhotoImage(file="missImg.png")
placeImg = PhotoImage(file = "place.png")
hitImg = hitImg.subsample(50)
missImg = missImg.subsample(70)
placeImg = placeImg.subsample(60)
player.set("p1")
mode.set("SetUP")

MasterGrid = {}
shipsP1 = []
shipsP2 = []
p2Hits = []
p1Hits = []
p2Miss = []
p1Miss = []
playerLeft = [15,15]

def getRef(num,size):
    mod = num%size 
    rowNum = num//size
    colNum = mod
    alphabet = list(string.ascii_uppercase)
    letter = alphabet[rowNum]
    ref = letter + str(colNum)
    print(ref)
    return(rowNum,colNum,ref)

def generateGrid(size):
    for x in range(size * size):
        print(x)
        rowVar,colVar,ref = getRef(x,size)
        print(ref) 
        MasterGrid[ref] = Button(gui, width=20,height=20,image=defaultImg,command=lambda refVar = ref:onClick(refVar))
        MasterGrid[ref].grid(row=rowVar, column=colVar)
        
    print(MasterGrid)
def clearGrid():
    for key in MasterGrid:
        btn = MasterGrid[key]
        btn.config(image=defaultImg)
def updateGrid():
    clearGrid()
    if mode.get() == "game" and player.get() == "p1":
        for x in p1Hits:
            cell = MasterGrid[x]
            cell.config(image=hitImg)
        for x in p1Miss:
            cell = MasterGrid[x]
            cell.config(image=missImg)
    elif mode.get() == "game" and player.get() == "p2":
        for x in p2Hits:
            cell = MasterGrid[x]
            cell.config(image=hitImg)
        for x in p2Miss:
            cell = MasterGrid[x]
            cell.config(image=missImg)
    elif mode.get() == "SetUP" and player.get() == "p1":
        for x in shipsP1:
            cell = MasterGrid[x]
            cell.config(image=placeImg)
    else:
        for x in shipsP2:
            cell = MasterGrid[x]
            cell.config(image=placeImg)
def onClick(listIndex):
    if active.get() == "F":
        return
    p1Left = playerLeft[0]
    p2Left = playerLeft[1]
    print(listIndex)
    print(player.get())
    if mode.get() == "SetUP":
        if player.get() == "p1":
            if p1Left != 0 and listIndex not in shipsP1:
                shipsP1.append(listIndex)
                print("Battleship Placed")
                p1Left = p1Left - 1
                playerLeft[0] = p1Left
                textStr = "P1:",p1Left,"Targets left to place"
                playerIndicator.config(text=textStr)
        else:
            if p2Left != 0 and listIndex not in shipsP2:
                shipsP2.append(listIndex)
                print("Battleship Placed")
                p2Left = p2Left - 1
                playerLeft[1] = p2Left
                textStr = "P2:",p2Left,"Targets left to place"
                playerIndicator.config(text=textStr)
    else:   
        if player.get() == "p1":
            if listIndex in p1Hits or listIndex in p1Miss:
                pass
            else:
                if listIndex in shipsP2:
                    print("Battleship Found")
                    p1Hits.append(listIndex)
                else:
                    p1Miss.append(listIndex)
                    textStr = "Player 2's Go... Press Next"
                    playerIndicator.config(text=textStr)
                    active.set("F")
                    clearGrid()
                    return
        else:
            if listIndex in p2Hits or listIndex in p2Miss:
                pass
            else:
                if listIndex in shipsP1:
                    print("Battleship Found")
                    p2Hits.append(listIndex)
                else:
                    p2Miss.append(listIndex)
                    textStr = "Player 1's Go... Press Next"
                    playerIndicator.config(text=textStr)
                    active.set("F")
                    clearGrid()
                    return
    updateGrid()
def NextFunc():
    active.set("T")
    p1Left = playerLeft[0]
    p2Left = playerLeft[1]
    clearGrid()
    if mode.get() == "SetUP" and player.get() == "p2":
        mode.set("game")
        playerIndicator.config(text="P1: Target P2's property")
        player.set("p1")
    elif mode.get() == "SetUP" and player.get() == "p1":
        textStr = "P2:",p2Left,"Targets left to place"
        playerIndicator.config(text=textStr)
        player.set("p2")
    elif mode.get() == "game" and player.get() == "p1":
        player.set("p2")  
        playerIndicator.config(text="P2: Target P1's property")
        updateGrid()
    elif mode.get() == "game" and player.get() == "p2":
        player.set("p1") 
        playerIndicator.config(text="P1: Target P2's property")
        updateGrid() 

gridSize = 7
generateGrid(gridSize)

playerIndicator = Label(gui,text="P1:0, P2:0")
playerIndicator.grid(column=0,columnspan=gridSize,row=gridSize+1,)
playerIndicator = Label(gui,text="P1: 15 Targets left to place")
playerIndicator.grid(column=0,columnspan=gridSize,row=gridSize+2,)
nextBtn = Button(gui,text="Next",command=NextFunc)
nextBtn.grid(column=0,columnspan=gridSize,row=gridSize + 3,rowspan=gridSize)
gui.mainloop()
