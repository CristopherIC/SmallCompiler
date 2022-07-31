RED = "\033[31m"
COLOR_OFF = '\033[0m'

import re
import sys
from myparser import Node, root, printChilds

variables={}

class Variable:
    def __init__(self,value,token):
        self.token = token
        self.value = value

def setVariables(r):
    if r.type == "dcl":
        if isDeclared(r,r.childs[1].type):
            sys.exit(RED + "La variable: " + r.childs[0].type + " " + r.childs[1].type + " ya está declarada en el scope." + COLOR_OFF)
        scopeNode = findScopeNode(r)
        if scopeNode in variables.keys():
            variables[scopeNode].append(Variable(r.childs[1].type,r.childs[0].type))
        else:
            variables[scopeNode]=[Variable(r.childs[1].type,r.childs[0].type)]
    if r.childs:
        for child in r.childs:
            setVariables(child)

#Revisa que una declaracion sea valida para el scope actual
def isDeclared(node, varName):
    if node in variables.keys() and varName in (o.value for o in variables[node]):
        return True
    if node.type == "if":
        currentNode = node
        while((currentNode.type == "if")):
            currentNode = currentNode.parent
            if currentNode == None:
                return False
        return isDeclared(currentNode, varName)
    if node.parent:
        return isDeclared(node.parent,varName)
    else:
        return False

#Revisa en que scope se encuentra el nodo que recibe
def findScopeNode(node):
    if(node.type in ["block","if"]):
        return node
    if node.parent:
        return findScopeNode(node.parent)
    return Node('Self')


def analyzer(r):
    checkChildren = True
    if r.type == "asg":
        correctType = ""
        if r.childs[0].type == "dcl":
            correctType = r.childs[0].childs[0].type
            varID = r.childs[0].childs[1].type
            checkID(r.childs[1], varID)
        elif (not isDeclared(r, r.childs[0].type)): 
            sys.exit(RED + "La variable " + r.childs[0].type + " no ha sido declarada aun" + COLOR_OFF)  
        else:
            correctType = getVarType(r,r.childs[0].type)
        if correctType == "int" or correctType == "float":
            treeNumTypeCheck(r.childs[1])
            if correctType == "float" and r.childs[1].parentType == "int":
                parseNode = Node('intToFloat', parentType = "float")
                r.childs[1].parent = parseNode
                parseNode.childs=[r.childs[1]]
                r.childs[1]=parseNode
            elif r.childs[1].parentType != correctType:
                sys.exit(RED + "Variables de tipo " + r.childs[1].parentType + " no pueden ser convertidas a " + correctType + COLOR_OFF)  
        #elif correctType == "boolean":
        checkChildren = False
        
    if r.childs and checkChildren:
        for child in r.childs:
            analyzer(child)
        
def checkID(node, id):
    if node.childs:
        for child in node.childs:
            checkID(child,id)
    elif node.type==id:
        sys.exit(RED + "No puedes declarar y asignar la variable en la misma linea" + COLOR_OFF)
        

def getVarType(node, varName):
    if node in variables.keys() and varName in (o.value for o in variables[node]):
        return [x for x in variables[node] if x.value == varName][0].token
    if node.type == "if":
        currentNode = node
        while((currentNode.type == "if") and currentNode.parent):
            currentNode = currentNode.parent
        return getVarType(currentNode, varName)
    if node.parent:
        return getVarType(node.parent, varName)
    else:
        return None

def treeNumTypeCheck(node):
    if node.childs:
        if not node.type in ["+","-","/","*","^"]:
            sys.exit(RED + "Asignación inválida" + COLOR_OFF)
        for child in node.childs:
            treeNumTypeCheck(child)
        if node.childs[0].parentType == node.childs[1].parentType:
            node.parenType = node.childs[0].parentType
        else:
            for i in range(len(node.childs)):
                if node.childs[i].parentType == "int":
                    parseNode = Node('intToFloat',parentType="float")
                    node.childs[i].parent = parseNode
                    print(i)
                    parseNode.childs[i] = [node.childs[i]]
                    node.childs[i] = parseNode
            node.parentType = "float"
    else:
        if(re.fullmatch(r'\d+', node.type)):
            node.parentType = "int"
        elif(re.fullmatch(r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))', node.type)):
            node.parentType = "float"
        else:
            if((node.type[0]=="-" and not isDeclared(node,node.type[1:])) or (node.type[0] != "-" and not isDeclared(node,node.type))):
                sys.exit(RED + "La variable " + node.type + " no ha sido declarada en el scope" + COLOR_OFF)  
            if(node.type[0]=="-"):
                varType = getVarType(node,node.type[1:])
            else:
                varType = getVarType(node,node.type)
            if varType == "boolean":
                sys.exit(RED + "No se pueden usar variables booleanas en operaciones numericas" + COLOR_OFF)
            node.parentType = varType

setVariables(root)
analyzer(root)
print("-----------")
printChilds(root)