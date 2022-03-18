import node

id = 0
structures = []

class Automata:
    def __init__(self):
        self.initialState = None
        self.finalState = None
        self.nodes = []
    
    def getNodes(self):
        return self.nodes

    def generateNodeCat(self,val1,val2,op):
        global id
        global structures
        if(len(val2)==1 and len(val1)>1):
            id+=1
            nodeI1 = node.Node(id,'',[])
            self.nodes.append(nodeI1)
            nodeF1 = self.nodes[ structures[-1][1]-1 ]  
            nodeIP = self.nodes[ structures[-1][0]-1 ]
            nodeF1.setValue(val2)
            nodeF1.setTransition(nodeI1.getId())
            structures.pop()
            structures.append((nodeIP.getId(),nodeI1.getId()))
            self.initialState = structures[0][0]
            self.finalState = structures[-1][1]
        elif(len(val2)>1 and len(val1)==1):

            id+=1
            nodeI1 = node.Node(id,val1,[])
            self.nodes.append(nodeI1)
            nodeIP = self.nodes[ structures[-1][0]-1 ]
            nodeF = self.nodes[ structures[-1][1]-1 ]
            nodeI1.setTransition(nodeIP.getId())
            structures.pop()
            structures.append((nodeI1.getId(),nodeF.getId()))
            self.initialState = structures[0][0]
            self.finalState = structures[-1][1]


        elif(len(val2)==1 and len(val1)==1):
            id+=1
            nodeI1 = node.Node(id,val1,[id+1])
            self.nodes.append(nodeI1)
            # node 2
            id+=1
            nodeI = node.Node(id,val2,[id+1])
            self.nodes.append(nodeI)
            # node 3
            id+=1
            nodeF1 = node.Node(id,'',[])
            self.nodes.append(nodeF1)
            structures.append((nodeI1.getId(),nodeF1.getId()))
            self.initialState = structures[0][0]
            self.finalState = structures[-1][1]
        else:
            nodeU1 = self.nodes[ structures[-2][1] -1]
            nodeU2 = self.nodes[ structures[-1][0] -1]
            nodeU1.setValue('ε')
            nodeU1.setTransition(nodeU2.getId())
            nodeF = structures.pop()
            nodeI = structures.pop()
            structures.append((nodeI[0],nodeF[1]))
            self.initialState = structures[0][0]
            self.finalState = structures[-1][1]

    def generateNodePipe(self,val1,val2,op):
        global id
        global structures

        if(len(val1) == 1 and len(val2) == 1 and op =='|'):
            # node 1 
            id+=1
            nodeI1 = node.Node(id,val1,[id+1])
            self.nodes.append(nodeI1)
            # node 2
            id+=1
            nodeF1 = node.Node(id,'',[])
            self.nodes.append(nodeF1)
            # node 3
            id+=1
            nodeI2 = node.Node(id,val2,[id+1])
            self.nodes.append(nodeI2)
            # node 4
            id+=1
            nodeF2 = node.Node(id,'',[])
            self.nodes.append(nodeF2)

            # nodes operation
            id+=1
            nodeIP = node.Node(id,'ε',[nodeI1.getId(),nodeI2.getId()])
            self.nodes.append(nodeIP)
            id+=1
            nodeFP = node.Node(id,'',[])
            self.nodes.append(nodeFP)

            # updated nodes 
            nodeF1.setValue('ε')
            nodeF1.setTransition(nodeFP.getId())
            nodeF2.setValue('ε')
            nodeF2.setTransition(nodeFP.getId())
            structures.append((nodeIP.getId(),nodeFP.getId()))
            #print("LAS structures LUEGO DEL PIPE DE 1 Y 1",structures)
            self.initialState = structures[0][0]
            self.finalState = structures[-1][1]

        elif( (len(val1) == 1 and len(val2) > 1) and op =='|' ):
            # node 1 
            id+=1
            nodeI1 = node.Node(id,val1,[id+1])
            self.nodes.append(nodeI1)

            # node 2
            id+=1
            nodeF1 = node.Node(id,'',[])
            self.nodes.append(nodeF1)

            # nodes operation
            id+=1
            nodeIP = node.Node(id,'ε',[nodeI1.getId(), self.nodes[structures[-1][0]-1].getId() ])
            self.nodes.append(nodeIP)
            id+=1
            nodeFP = node.Node(id,'',[])
            self.nodes.append(nodeFP)

            # updated nodes 
            nodeF1.setValue('ε')
            nodeF1.setTransition(nodeFP.getId())
            nodeF2 = self.nodes[ structures[-1][1]-1 ] 
            nodeF2.setValue('ε')
            nodeF2.setTransition(nodeFP.getId())
            structures.pop()
            structures.append((nodeIP.getId(),nodeFP.getId()))

        elif(  (len(val1) > 1 and len(val2) == 1) and op =='|'):
            # node 1 
            id+=1
            nodeI1 = node.Node(id,val2,[id+1])
            self.nodes.append(nodeI1)
            # node 2
            id+=1
            nodeF1 = node.Node(id,'',[])
            self.nodes.append(nodeF1)

            # nodes operation
            id+=1
            nodeIP = node.Node(id,'ε',[nodeI1.getId(), self.nodes[structures[-1][0]-1].getId() ])
            self.nodes.append(nodeIP)
            id+=1
            nodeFP = node.Node(id,'',[])
            self.nodes.append(nodeFP)

            # updated nodes
            nodeF1.setValue('ε')
            nodeF1.setTransition(nodeFP.getId())
            nodeF2 = self.nodes[ structures[-1][1]-1 ] 
            nodeF2.setValue('ε')
            nodeF2.setTransition(nodeFP.getId())
            structures.pop()
            structures.append((nodeIP.getId(),nodeFP.getId()))

        else:
            # nodes operations
            id+=1
            nodeIP = node.Node(id,'ε',[structures[-2][0],structures[-1][0]])
            self.nodes.append(nodeIP)
            id+=1
            nodeFP = node.Node(id,'',[])
            self.nodes.append(nodeFP)

            # updated nodes 
            nodeF1 = self.nodes[ structures[-2][1]-1 ]  
            nodeF2 = self.nodes[ structures[-1][1]-1 ] 
            nodeF1.setValue('ε')
            nodeF1.setTransition(nodeFP.getId())
            nodeF2.setValue('ε')
            nodeF2.setTransition(nodeFP.getId())
            structures.pop()
            structures.pop()
            structures.append((nodeIP.getId(),nodeFP.getId()))
            self.initialState = structures[0][0]
            self.finalState = structures[-1][1]
            
            
            
            
