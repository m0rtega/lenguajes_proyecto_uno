
id = 0
structures = []

class AutomataFD:
    
    def __init__(self):
        self.initialState = None
    
    def mov(self,statesMov, letterM,transM):
        moveA = []
        newArray = statesMov.copy()
        stacker = []
        for vMov in newArray:
            for bM in transM:
                if(bM[0] == vMov and bM[1] ==letterM):
                    moveA.append(bM[2])
        return moveA
        
    def lockE(self, lockStates,trans):
        lock = []
        newArray = lockStates.copy()
        visited = []
        for qE in newArray:
            for x in trans:
                if(x[0] == qE and x[1] =='ε' and (x[2] not in visited)):
                    visited.append(x[2])
                    newArray.append(x[2])
        res = [] 
        for i in newArray: 
            if i not in res: 
                res.append(i) 
        lock = res
        return lock

    def listToInt(self, list):
        listN = []
        listS = []
        for i in list:
            listN = listN + [int(i)]
        cs=sorted(listN)
        for i in cs:
            listS = listS + [str(i)]
        return listS

    def afn(self, start,trans,sim):

        elements = []
        newTransitions = []
        states = []
        startingValue = self.lockE(start,trans)
        startingValue = self.listToInt(startingValue)
        states.append(startingValue)
        elements.append(startingValue)

        for q in states:
            for c in sim:
                movea = self.mov(q,c,trans)
                movea = self.listToInt(movea)
                U = self.lockE(movea,trans)
                U = self.listToInt(U)
                if(U not in states and len(U) >= 1):
                    states.append(U)
                    elements.append(U)
                if(len(U) >= 1):
                    newTransitions.append( [q,c,U]  )
        return newTransitions, elements

        
    
    