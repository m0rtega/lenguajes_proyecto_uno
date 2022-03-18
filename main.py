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