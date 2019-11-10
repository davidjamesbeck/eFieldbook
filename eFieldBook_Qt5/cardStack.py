##from PyQt5 import QtWidgets
from ELFB import cardStackVar, dataIndex, cardLoader

'''class for moving forward and back'''

def goToCard(fldbk,direction):
    ##move through cards on buttonclicks, called by buttons
    if direction == -1:
        targetID = cardStackVar.theQueue[cardStackVar.theCounter-1]
        cardStackVar.theCounter = cardStackVar.theCounter - 1
        fldbk.lFwdBtn.setEnabled(1)
        fldbk.tFwdBtn.setEnabled(1)
        fldbk.eFwdBtn.setEnabled(1)
        fldbk.dFwdBtn.setEnabled(1)
    else:
        targetID = cardStackVar.theQueue[cardStackVar.theCounter+1]
        cardStackVar.theCounter += 1
        fldbk.lRtnBtn.setEnabled(1)
        fldbk.tRtnBtn.setEnabled(1)
        fldbk.eRtnBtn.setEnabled(1)
        fldbk.dRtnBtn.setEnabled(1)
    if len(cardStackVar.theQueue) - 1 == cardStackVar.theCounter:
        fldbk.lFwdBtn.setEnabled(0)
        fldbk.tFwdBtn.setEnabled(0)
        fldbk.eFwdBtn.setEnabled(0)
        fldbk.dFwdBtn.setEnabled(0)
    if cardStackVar.theCounter == 0:
        fldbk.lRtnBtn.setEnabled(0)
        fldbk.tRtnBtn.setEnabled(0)
        fldbk.eRtnBtn.setEnabled(0)
        fldbk.dRtnBtn.setEnabled(0)                
    if targetID[0] == "L":
        navBar = fldbk.lLexNav
        targetCard = dataIndex.lexDict[targetID]
        cardLoader.loadLexCard(targetCard, navBtn=True)
        fldbk.tabWidget.setCurrentIndex(1)
    elif targetID[0] == "T":
        navBar = fldbk.tTextNav
        targetCard = dataIndex.textDict[targetID]
        cardLoader.loadTextCard(targetCard, navBtn=True)
        fldbk.tabWidget.setCurrentIndex(2)
    elif targetID[0] == "E":
        targetCard = dataIndex.exDict[targetID]
        if dataIndex.unsavedEdit == 1:
            pendingChange = 1
        else:
            pendingChange = 0
        cardLoader.loadExCard(targetCard, navBtn=True)
        dataIndex.unsavedEdit = 0
        if pendingChange == 1:
            dataIndex.unsavedEdit = 1
        fldbk.tabWidget.setCurrentIndex(3)
    elif targetID[0] == "D":
        navBar = fldbk.dDataNav
        targetCard = dataIndex.dataDict[targetID]
        cardLoader.loadDataCard(targetCard, navBtn=True)
        fldbk.tabWidget.setCurrentIndex(4)
    elif targetID[0] == "H":
        fldbk.tabWidget.setCurrentIndex(0)

    try:
        cardLoader.resetNavBars(navBar, targetID)
    except UnboundLocalError:
        fldbk.tabWidget.setCurrentIndex(0)                

def addToQueue(currentCard):
    '''add card to list, remove from top if more than 20, called by cardloaders'''
#    fldbk = dataIndex.fldbk
    if cardStackVar.theQueue[cardStackVar.theCounter] != currentCard:
        if len(cardStackVar.theQueue) - 1 == cardStackVar.theCounter:
            cardStackVar.theQueue.append(currentCard)
        else:
            cardStackVar.theQueue = cardStackVar.theQueue[0:cardStackVar.theCounter+1]
            cardStackVar.theQueue.append(currentCard)
        if len(cardStackVar.theQueue) <= 20:
            cardStackVar.theCounter += 1
        else:
            cardStackVar.theQueue.pop(0)
            cardStackVar.theCounter = 19
#        if cardStackVar.theCounter == 0:
#            fldbk.lRtnBtn.setEnabled(0)
#            fldbk.tRtnBtn.setEnabled(0)
#            fldbk.eRtnBtn.setEnabled(0)
#            fldbk.dRtnBtn.setEnabled(0)
#        else:
#            fldbk.lRtnBtn.setEnabled(1)
#            fldbk.tRtnBtn.setEnabled(1)
#            fldbk.eRtnBtn.setEnabled(1)
#            fldbk.dRtnBtn.setEnabled(1)                    
#        if cardStackVar.theCounter == len(cardStackVar.theQueue) - 1:
#            fldbk.lFwdBtn.setEnabled(0)
#            fldbk.tFwdBtn.setEnabled(0)
#            fldbk.eFwdBtn.setEnabled(0)
#            fldbk.dFwdBtn.setEnabled(0)
#        else:
#            fldbk.lFwdBtn.setEnabled(1)
#            fldbk.tFwdBtn.setEnabled(1)
#            fldbk.eFwdBtn.setEnabled(1)
#            fldbk.dFwdBtn.setEnabled(1)
