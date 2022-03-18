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
