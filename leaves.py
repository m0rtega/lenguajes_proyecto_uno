class Leaves:
    def __init__(self, id, parentId, value, importantId, children=[]):
        self.id = id
        self.parentId = parentId
        self.value = value
        self.children = children
        self.importantId = importantId
    
    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def getValue(self):
        return self.value

    def setValue(self, val):
        self.value = val
    
    def getParentId(self):
        return self.parentId

    def setParentId(self, parentId):
        self.parentId = parentId   

    def getChildren(self):
        return self.children

    def setChildren(self, children):
        self.children.append(children)   

    def getImportantId(self):
        return self.importantId

    def setImportantId(self, id):
        self.importantId = id

