import leaves

id = 0
idImp = 0
class Tree:
    def __init__(self):
        self.root = None
        self.finalNode = None
        self.nodes = []
        self.structures = []
        self.importantValues = []

    def getNodes(self):
        return self.nodes

    def getImportantValues(self):
        return self.importantValues

    def generateLeavesPipe(self, val1, val2, op):
        global id
        global idImp

        if(len(val1) == 1 and len(val2) == 1 and op =='|'):
            id+=1
            if(val1 != "ε"):
                idImp+=1
                leaf1 = leaves.Leaves(id,'',val1,idImp,[])
                self.importantValues.append((leaf1,idImp,id))
            else:
                leaf1 = leaves.Leaves(id,'',val1,'',[])
            self.nodes.append(leaf1)
            id+=1
            if(val2 != "ε"):
                idImp+=1
                leaf2 = leaves.Leaves(id,'',val2,idImp,[])
                self.importantValues.append((leaf2,idImp,id))
            else:
                leaf2 = leaves.Leaves(id,'',val2,'',[])

            self.nodes.append(leaf2)
            id+=1
            leaf3 = leaves.Leaves(id,'',op,'', [leaf1,leaf2] )
            self.nodes.append(leaf3)
            leaf1.setParentId(leaf3)
            leaf2.setParentId(leaf3)
            self.structures.append(leaf3.getId())
            self.finalNode = self.structures[-1]

        elif( (len(val1) == 1 and len(val2) > 1) and op =='|' ):
            print('The first value is a letter and the second one is a structure')

        elif(  (len(val1) > 1 and len(val2) == 1) and op =='|'):
            print('The first value is a structure and the second one is a letter')
    
        else:
            leafH2 = self.nodes[self.structures[-1]-1]
            leafH1 = self.nodes[self.structures[-2]-1]
            id+=1
            leaf1 = leaves.Leaves(id,'',op,'',[leafH1,leafH2])
            leafH2.setParentId(leaf1)
            leafH1.setParentId(leaf1)
            self.nodes.append(leaf1)

    def generateNodeStar(self,val1,op):
        global id
        global idImp

        if(len(val1) == 1 and op =='*'):
            id+=1
            if(val1 != "ε"):
                idImp+=1
                leaf1 = leaves.Leaves(id,'',val1,idImp,[])
                self.importantValues.append((leaf1,idImp,id))
            else:
                leaf1 = leaves.Leaves(id,'',val1,'',[])
            self.nodes.append(leaf1)
            id+=1
            leaf2 = leaves.Leaves(id,'',op,'',[])
            self.nodes.append(leaf2)
            leaf1.setParentId(leaf2)
            leaf2.setChildren(leaf1)
            self.structures.append(leaf2.getId())

            
        else:
            leafH = self.nodes[-1]  
            id+=1
            leaf1 = leaves.Leaves(id,'',op,'',[])
            self.nodes.append(leaf1)
            leafH.setParentId(leaf1)
            leaf1.setChildren(leafH)
            self.structures.pop()
            self.structures.append(leaf1.getId())
            self.estadoFinal = self.structures[-1]

    def generateNodeCat(self,val1,val2,op):
        global id
        global idImp
        if(len(val2)==1 and len(val1)>1):
            leafH1 = self.nodes[-1]
            id+=1
            if(val2 != "ε"):
                idImp+=1
                leafH2 = leaves.Leaves(id,'',val2,idImp,[])
                self.importantValues.append((leafH2,idImp,id))
            else:
                leafH2 = leaves.Leaves(id,'',val2,'',[])
            self.nodes.append(leafH2)
            id+=1
            leaf2 = leaves.Leaves(id,'',op,'',[])
            self.nodes.append(leaf2)
            leafH1.setParentId(leaf2)
            leafH2.setParentId(leaf2)
            children = []
            children.append(leafH1)
            children.append(leafH2)
            for i in children:
                leaf2.setChildren(i)
            self.structures.pop()
            self.structures.append(leaf2.getId())
        elif(len(val2)>1 and len(val1)==1):
            print("Concat node with structure")
        elif(len(val2)==1 and len(val1)==1):
            id+=1
            if(val1 != "ε"):
                idImp+=1
                leafH1 = leaves.Leaves(id,'',val1,idImp,[])
                self.importantValues.append((leafH1,idImp,id))
            else:
                leafH1 = leaves.Leaves(id,'',val1,'',[])
            self.nodes.append(leafH1)

            id+=1
            if(val2 != "ε"):
                idImp+=1
                leafH2 = leaves.Leaves(id,'',val2,idImp,[])
                self.importantValues.append((leafH2,idImp,id))
            else:
                leafH2 = leaves.Leaves(id,'',val2,'',[])
            self.nodes.append(leafH2)

            id+=1
            leaf2 = leaves.Leaves(id,'',op,'',[])
            self.nodes.append(leaf2)
            leafH1.setParentId(leaf2)
            leafH2.setParentId(leaf2)
            children = []
            children.append(leafH1)
            children.append(leafH2)
            for i in children:
                leaf2.setChildren(i)
            self.structures.append(leaf2.getId())
        else:
            leafH2 = self.nodes[self.structures[-1]-1]
            leafH1 = self.nodes[self.structures[-2]-1]
            id+=1
            leaf2 = leaves.Leaves(id,'',op,'',[])
            self.nodes.append(leaf2)
            leafH1.setParentId(leaf2)
            leafH2.setParentId(leaf2)
            children = []
            children.append(leafH1)
            children.append(leafH2)
            for i in children:
                leaf2.setChildren(i)
            self.structures.pop()
            self.structures.append(leaf2.getId())
            


    