import thompson, AFD, tree
from graphviz import Digraph
import sys

# Inputs
regex = input("ingrese la expresion regular: ")
w = input("ingrese la cadena a evaluar: ")

def transformRegex(regex):
    #ε
    i = 0
    expr = ''
    par = []
    sub = ''
    resta = []
    while i <len(regex):
        if(regex[i] =='('):
            par.append(i)
        if regex[i] == '+':
            
            if(regex[i-1] == ')'):

                sub = regex[par.pop():i]
                
                expr = expr + '*' + sub
            else:
                expr = expr + '*' + regex[i-1]
        elif regex[i] == '?':
            if(regex[i-1] == ')'):
    
                sub = regex[par.pop():i]
                subl = len(sub)-1
                expr = expr[:-subl]
                expr = expr + sub
                expr = expr  +  '|' + 'ε)'
            else:
                letter = expr[-1]
                expr = expr[:-1]
                expr = expr + '(' + letter + '|' + 'ε)'
        else:
            expr = expr + regex[i]
        i+=1

    return expr


#Checks that the parenthesis have the same number of left and right ones
def verifyParenthesis(regex):
    right = 0
    left = 0 
    for i in regex:
        if(i == "("):
            right+=1
        if(i==")"):
            left+=1
    if(right == left):
        return True
    else:
        return False

# Adds a period everytime it is needed, this eases its lecture
def addPeriod(regex):
    i = 0
    expr = ''
    cont = 0 
    while i < len(regex):
        if (regex[i] == '|'):
            cont = 0
        elif(regex[i] == '('):
            if (cont == 1):
                expr = expr + '.'
                cont = 0;
        elif(regex[i] == ')' or regex[i] == '*'):
            pass
        else:
            cont = cont + 1
        if(cont == 2):
            expr = expr+'.'+regex[i]
            cont = 1
        else:
            expr = expr + regex[i]
        i += 1
    return expr

#Assigns the precedence every operation has in descending order
def getPrecedence(sym):
    if (sym == '*'):
        return 3
    if (sym == '.'):
        return 2
    if (sym == '|'):
        return 1
    return 0

# If the regex is valid, the program continues
if(verifyParenthesis(regex)):
    pass
else:
    sys.exit()

# We transform the regex
rAFD = regex
regex = transformRegex(regex)
regex = addPeriod(regex)
# We initialize our automatas
automata = thompson.Automata()
automataAFD = AFD.AutomataFD()

values = []
ops = []
i = 0 
nodes = []

while i < len(regex):
    if regex[i] == '(':
        ops.append(regex[i])
    elif regex[i].isalpha() or regex[i].isdigit():
        values.append(regex[i])
    elif regex[i] == ')':
        while len(ops) != 0 and ops[-1] != '(':
            op = ops.pop()
            if op != '*':
                val2 = values.pop()
                val1 = values.pop()
                temp = val1+op+val2
                nodes.append(temp)
                if(op == '|'):
                    automata.generateNodePipe(val1,val2,op)
                elif(op == '.'):
                    automata.generateNodeCat(val1,val2,op)
                values.append(temp)
        ops.pop()
    else:
        if(regex[i] != '*'):
            while (len(ops) != 0 and getPrecedence(ops[-1]) >= getPrecedence(regex[i])):
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                temp = val1+op+val2
                nodes.append(temp)
                if(op == '|'):
                    automata.generateNodePipe(val1,val2,op)
                elif(op == '.'):
                    automata.generateNodeCat(val1,val2,op)
                values.append(temp)
            ops.append(regex[i])
        else:
            
            val1 = values.pop()
            op = regex[i]
            temp = val1+op
            
            automata.generateNodeStar(val1,op)
            nodes.append(temp)
            values.append(temp)
    i+=1

while len(ops) != 0:
    val2 = values.pop()
    val1 = values.pop()
    op = ops.pop()
    temp = val1+op+val2
    nodes.append(temp)
    if(op == '|'):
        automata.generateNodePipe(val1,val2,op)
    elif(op == '.'):
        automata.generateNodeCat(val1,val2,op)
    else:
        print("Not an operator")
    values.append(temp)

# Here is where we graph our automatas
fTH = Digraph('finite_state_machine', filename='fsm.gv')
fTH.attr(rankdir='LR', size='8,5')
fTH.attr('node', shape='doublecircle')
fTH.node(str(automata.getNodes()[-1].getId()))

states = []
symbols = []
start = []
accept = []
transitions = []

start.append(str(automata.initialState))
accept.append(str(automata.finalState))

#Here we get the data
for i in automata.getNodes():
    states.append(i.getId())

    if(str(i.getValue()) != "ε" and str(i.getValue()) != ""):
        symbols.append(i.getValue())

    fTH.attr('node', shape='circle')
    large = len(i.getTransition())

    if(large == 0 ):
        pass
    elif (large > 1):
        for j in i.getTransition():  
            transitions.append(( str(i.getId()),str(i.getValue()), str(j)))
            fTH.edge(str(i.getId()), str(j), label= str(i.getValue()))
    else:
        transitions.append(( str(i.getId()),str(i.getValue()), str(i.getTransition()[0])))

        fTH.edge(str(i.getId()), str(i.getTransition()[0]), label=str(i.getValue()))

resT = [] 
for i in symbols: 
    if i not in resT: 
        resT.append(i) 
symbols = resT
# Lock method to simulate algorithms
def lockE(statesLock,trans):
        lock = []
        newArray = statesLock.copy()
        visited = []
        #
        for qE in newArray:
            for x in trans:
                if(x[0] == qE and x[1] =='ε' and (x[2] not in visited)):
                    #
                    visited.append(x[2])
                    newArray.append(x[2])
        res = [] 
        for i in newArray: 
            if i not in res: 
                res.append(i) 
        lock = res
        return lock

# Move method to simulate algorithms
def mov(statesMov, letterM,transM):
        moveA = []
        newArray = statesMov.copy()
        stacker = []
        for vMov in newArray:
            for bM in transM:
                if(bM[0] == vMov and bM[1] ==letterM):
                    #newArray.append(bM[2])
                    moveA.append(bM[2])
        return moveA

# Simulation using lock and move
def thompsonSimulation(ini,trans):
    s0 = lockE(ini,trans)
    for c in w:
        s0 = lockE(mov(s0, c,trans),trans)


fTH.view()

file = f'''
states = {states}
symbols = {symbols}
start = {start}
accept = {accept}
transitions = {transitions}
'''
thompsonSimulation(start,transitions)
with open("FILE.txt", "w", encoding="utf-8") as f:
    f.write(file)
f.close()

# We initialize the automata
automata, fValues = automataAFD.afn(start,transitions,symbols)

#We select our states and remove the repeats
key = []
acceptA = []
for i in fValues:
    for j in i:
        if(j == accept[0]):
            key.append(i)
resT = [] 
for i in key: 
    if i not in resT: 
        resT.append(i) 
key = resT

# Here we create the dictionary to assign to the states
newDictionary = {}
counter = 0
newValues = fValues.copy()

for i in newValues:
    newDictionary[tuple(i)] = counter
    counter +=1

for item in automata:
    item[0]= str(newDictionary.get(tuple(item[0])))
    item[2]= str(newDictionary.get(tuple(item[2])))

for item in key:
    acceptA.append(str(newDictionary.get(tuple(item))))

# here we graph our automata
fa = Digraph('finite_state_machine', filename='fsam.gv')
fa.attr(rankdir='LR', size='8,5')

for i in acceptA:
    fa.attr('node', shape='doublecircle')
    fa.node(i)

# We get the data
statesA = []
symbolsA = []
resT = [] 

for i in automata: 
    if i not in resT: 
        resT.append(i) 
automata = resT

for i in automata:
    statesA.append(i[0])
    statesA.append(i[2])
    fa.attr('node', shape='circle')
    fa.edge(str(i[0]), str(i[2]), label=str(i[1]))
resT = [] 

for i in statesA: 
    if i not in resT: 
        resT.append(i) 
statesA = resT
startA = [automata[0][0]]

# Subset simulation method
def setsSimulation(ini,trans):
    s = ini
    cont =0 
    for c in w:
        s = (mov(s, c,trans))
        
    for i in acceptA:
        if(i in s):
            cont+=1


file = f'''
states = {statesA}
symbols = {symbols}
start = {startA}
accept = {acceptA}
transitions = {automata}
'''
with open("FILE.txt", "a", encoding="utf-8") as f:
    f.write(file)
f.close()
setsSimulation(startA,automata)
fa.view()

AFDDclass = tree.Tree()
values = []
ops = []
i = 0 
nodes = []

rAFD = "("+rAFD+")#"
rAFD = transformRegex(rAFD)
rAFD = addPeriod(rAFD) 
regex = rAFD

while i < len(regex):
    if regex[i] == '(':
        ops.append(regex[i])
    elif regex[i].isalpha() or regex[i].isdigit() or regex[i] == '#':
        values.append(regex[i])
    elif regex[i] == ')':
        while len(ops) != 0 and ops[-1] != '(':
            op = ops.pop()
            if op != '*':
                val2 = values.pop()
                val1 = values.pop()
                temp = val1+op+val2
                nodes.append(temp)
                if(op == '|'):
                    AFDDclass.generateLeavesPipe(val1,val2,op)
                elif(op == '.'):
                    AFDDclass.generateNodeCat(val1,val2,op)
                values.append(temp)
        ops.pop()
    else:
        if(regex[i] != '*'):
            while (len(ops) != 0 and getPrecedence(ops[-1]) >= getPrecedence(regex[i])):
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                temp = val1+op+val2
                nodes.append(temp)
                if(op == '|'):
                    AFDDclass.generateLeavesPipe(val1,val2,op)
                    
                elif(op == '.'):
                    AFDDclass.generateNodeCat(val1,val2,op)
                    
                values.append(temp)
            ops.append(regex[i])
        else:
            
            val1 = values.pop()
            op = regex[i]
            temp = val1+op
            
            AFDDclass.generateNodeStar(val1,op)
            
            nodes.append(temp)
            values.append(temp)
    i+=1

while len(ops) != 0:
    val2 = values.pop()
    val1 = values.pop()
    op = ops.pop()
    temp = val1+op+val2
    nodes.append(temp)
    if(op == '|'):
        AFDDclass.generateLeavesPipe(val1,val2,op)
    elif(op == '.'):
        AFDDclass.generateNodeCat(val1,val2,op)
    else:
        print("Not a recognized symbol")
    values.append(temp)


# We get the tree
trees = AFDDclass.getNodes()
accept = []

# We get the accept state
for i in trees:
    if(i.getValue() =='#'):
        accept.append(i.getImportantId())

importantValues = AFDDclass.getImportantValues()
symbols = []

# Method to see if the value is nullable
def nullable(element):
    # We need to see if its a leaf, if it is, it cant have children
    if(len(element.getChildren()) > 0):

        if(element.getValue() == "|"):
            c1 = nullable(element.getChildren()[0])
            c2 = nullable(element.getChildren()[1])
            if(c1 or c2):
                return True
            else:
                return False
        elif(element.getValue() == "."):
            c1 = nullable(element.getChildren()[0])
            c2 = nullable(element.getChildren()[1])
            if(c1 and c2):
                return True
            else:
                return False
        else:
            return True
    else:
        if(element.getValue() != "ε"):
            return False
        else:
            return True

# We get the first position of the element
def firstPos(element):
    # We need to see if its a leaf, if it is, it cant have children
    if(len(element.getChildren()) > 0):
        if(element.getValue() == "|"):
            c1 = firstPos(element.getChildren()[0])
            c2 = firstPos(element.getChildren()[1])
            resp = (c1)+(c2)
            return resp
        elif(element.getValue() == "."):
            h1 = (element.getChildren()[0])
            if(nullable(h1)):
                c1 = firstPos(element.getChildren()[0])
                c2 = firstPos(element.getChildren()[1])
                resp = (c1)+(c2)
                return resp
            else:
                c1 = firstPos(element.getChildren()[0])
                return c1
        else:
            return firstPos(element.getChildren()[0])
    else:
        if(element.getValue() != "ε"):
            return [element.getImportantId()]
        else:
            return []

# We get the last position of the element
def lastPos(element):
    # We need to see if its a leaf, if it is, it cant have children
    if(len(element.getChildren()) > 0):
        if(element.getValue() == "|"):
            c1 = lastPos(element.getChildren()[0])
            c2 = lastPos(element.getChildren()[1])
            resp = (c1)+(c2)
            return resp
        elif(element.getValue() == "."):
            h2 = (element.getChildren()[1])
            if(nullable(h2)):
                c1 = lastPos(element.getChildren()[0])
                c2 = lastPos(element.getChildren()[1])
                resp = (c1)+(c2)
                return resp
            else:
                c2 = lastPos(element.getChildren()[1])
                return c2
        else:
            return lastPos(element.getChildren()[0])
    else:
        if(element.getValue() != "ε"):
            return [element.getImportantId()]
        else:
            return []


# We get the following position of the element
def followPos(element):
    # We need to see if its a leaf, if it is, it cant have children
    if(len(element.getChildren()) > 0):
        if(element.getValue() == "|"):
            c1 = lastPos(element.getChildren()[0])
            c2 = lastPos(element.getChildren()[1])
            resp = (c1)+(c2)
            return resp
        elif(element.getValue() == "."):
            h2 = (element.getChildren()[1])
            if(nullable(h2)):
                c1 = lastPos(element.getChildren()[0])
                c2 = lastPos(element.getChildren()[1])
                resp = (c1)+(c2)
                return resp
            else:
                c2 = lastPos(element.getChildren()[1])
                return c2
        else:
            return lastPos(element.getChildren()[0])
    else:
        if(element.getValue() != "ε"):
            return [element.getImportantId()]
        else:
            return []

# We get the nodes positions
positions = []
for i in trees:
    positions.append((i,firstPos(i),lastPos(i)))
followValues = []
followPosition = []
followTotal = []

# We assign the following position
for i in positions:
    if(i[0].getValue() == "."):
        hijo1 =  i[0].getChildren()[0]
        hijo2 =  i[0].getChildren()[1]
        for posicion in positions:
            if(posicion[0]==hijo1):
                followValues.append(posicion[2])
                followTotal.append(posicion[2])
            if(posicion[0]==hijo2):
                followPosition.append(posicion[1])
                followTotal.append(posicion[1])
    elif(i[0].getValue() == "*"):
        followValues.append(i[2])
        followPosition.append(i[1])
        followTotal.append(i[2])
        followTotal.append(i[1])

result = []
for i in followValues:
    for j in i:
        result.append([j])

for i in range(len(followValues)):
    for j in followValues[i]:
        for asd in followPosition[i]:
            result[j-1].append(asd)

for i in result:
    i.pop(0)
cont = 0

for i in (result):
    if(len(i)==0):
        cont+=1
    if (cont>1 and len(i)==0):
        result.remove(i)
rest = []

for elem in result: 
    a = list(set(elem))
    rest.append(a)
result = rest

for i in result:
    if(len(i) < 1):
        result.remove(i)

# We get the symbols of the tree
for i in trees:
    if(i.getValue() != "#" and i.getValue() != "ε" and len(i.getChildren()) < 1):
        symbols.append(i.getValue())
resT = [] 

for i in symbols: 
    if i not in resT: 
        resT.append(i) 
symbols = resT

for i in positions:
    if(i[0].getParentId() == ""):
        firstPosRoot = i[1]

# We create the states of the final automata
def Direct(firstPosRoot, symbols, importantValues):
    dStates = [firstPosRoot]
    numbers = []
    U = []
    newTransitions = []
    for i in dStates:
        for j in symbols:
            for k in importantValues:
                if(j == k[0].getValue() and (k[0].getImportantId() in i)):
                    numbers.append(k[0].getImportantId())

            for h in numbers:
                U += result[h-1]
            test = []

            for letter in U:
                if letter not in test:
                    test.append(letter)
            U = test            

            if (U not in dStates):
                dStates.append(U)
            if (len(U)>=1):
                newTransitions.append([i,j,U])
            U = []
            numbers.clear() 

    return newTransitions, dStates

    # We get the automata
newTransitions, dStates = Direct(firstPosRoot, symbols, importantValues)
key = []
acceptA = []
for i in dStates:
    for j in i:
        if(j == accept[0]):
            key.append(i)

# We create the dictionary to assign the new values to the automata states
newDictionary = {}
counter = 0
newValues = dStates.copy()
for i in newValues:
    newDictionary[tuple(i)] = counter
    counter +=1
for item in key:
    acceptA.append(str(newDictionary.get(tuple(item))))

for item in newTransitions:
    item[0]= str(newDictionary.get(tuple(item[0])))
    item[2]= str(newDictionary.get(tuple(item[2])))

# AFD Simulation
def afdSimulation(ini,trans):
    s = ini
    cont = 0
    for c in w:
        s = (mov(s, c,trans))
    for i in acceptA:
        if(i in s):
            cont+=1

# We graph the automata
fad = Digraph('finite_state_machine', filename='fsmasd.gv')
fad.attr(rankdir='LR', size='8,5')
for i in acceptA:
    fad.attr('node', shape='doublecircle')
    fad.node(i)
statesA = []
for i in newTransitions:
    statesA.append(i[0])
    statesA.append(i[2])
    fad.attr('node', shape='circle')
    fad.edge(i[0], i[2], label=i[1])
fad.view()
resT = [] 
for i in statesA: 
    if i not in resT: 
        resT.append(i) 
statesA = resT

file = f'''
states = {statesA}
symbols = {symbols}
start = {[newTransitions[0][0]]}
accept = {acceptA}
transitions = {newTransitions}
'''
afdSimulation([newTransitions[0][0]],newTransitions)
with open("FILE.txt", "a", encoding="utf-8") as f:
    f.write(file)
f.close()