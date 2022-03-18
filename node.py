class Node:
    def __init__(self, id, dvalue, transitions = []):
        self. id = id
        self.dvalue = dvalue
        self.transitions = transitions
    
    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id
    
    def getValue(self):
        return self.dvalue

    def setValue(self, val):
        self.dvalue = val

    def getTransition(self):
        return self.transitions

    def setTransition(self, transitions):
        self.transitions.append(transitions)   
